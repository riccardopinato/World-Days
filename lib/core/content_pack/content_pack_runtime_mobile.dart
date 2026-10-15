import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';

import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';

import 'content_pack_io.dart';
import 'content_pack_manager.dart';
import 'content_pack_models.dart';

ContentPackManager createContentPackManager({
  required ContentPayloadValidator validator,
}) =>
    ContentPackManager(
      transport: _HttpContentPackTransport(),
      storage: _FileContentPackStorage(),
      validator: validator,
    );

class _HttpContentPackTransport implements ContentPackTransport {
  final http.Client _client = http.Client();

  @override
  bool get supported => true;

  @override
  Future<String> getText(Uri uri) async {
    final response =
        await _client.get(uri).timeout(const Duration(seconds: 15));
    if (response.statusCode != HttpStatus.ok) {
      throw HttpException(
        'content_manifest_http_${response.statusCode}',
        uri: uri,
      );
    }
    return response.body;
  }

  @override
  Future<List<int>> getBytes(
    Uri uri, {
    required int maxBytes,
  }) async {
    if (maxBytes <= 0) {
      throw const FormatException('content_payload_invalid_max_bytes');
    }

    final request = http.Request('GET', uri);
    final response = await _client
        .send(request)
        .timeout(const Duration(seconds: 15));

    if (response.statusCode != HttpStatus.ok) {
      throw HttpException(
        'content_payload_http_${response.statusCode}',
        uri: uri,
      );
    }

    final declaredLength = response.contentLength;
    if (declaredLength != null && declaredLength > maxBytes) {
      throw const FormatException('content_payload_exceeds_byte_cap');
    }

    final buffer = BytesBuilder(copy: false);
    var received = 0;
    await for (final chunk
        in response.stream.timeout(const Duration(seconds: 30))) {
      received += chunk.length;
      if (received > maxBytes) {
        throw const FormatException('content_payload_exceeds_byte_cap');
      }
      buffer.add(chunk);
    }
    return buffer.takeBytes();
  }

  @override
  Future<void> close() async => _client.close();
}

class _FileContentPackStorage implements ContentPackStorage {
  Directory? _directory;

  @override
  bool get supported => true;

  Future<Directory> _root() async {
    final existing = _directory;
    if (existing != null) return existing;
    final base = await getApplicationSupportDirectory();
    final value = Directory(
      '${base.path}${Platform.pathSeparator}world_days_content_pack',
    );
    if (!await value.exists()) await value.create(recursive: true);
    _directory = value;
    return value;
  }

  Future<File> _pointerFile() async =>
      File('${(await _root()).path}${Platform.pathSeparator}pointer.json');

  Future<File> _pointerBackupFile() async => File(
        '${(await _root()).path}${Platform.pathSeparator}pointer.backup.json',
      );

  Future<File> _manifestFile(String version) async => File(
        '${(await _root()).path}${Platform.pathSeparator}'
        'manifest_${_safeVersion(version)}.json',
      );

  Future<File> _payloadFile(String version) async => File(
        '${(await _root()).path}${Platform.pathSeparator}'
        'pack_${_safeVersion(version)}.json',
      );

  @override
  Future<StoredContentPack?> readActive() async {
    final pointer = await _readPointer();
    if (pointer == null || pointer.activeVersion.isEmpty) return null;
    return _readVersion(pointer.activeVersion);
  }

  @override
  Future<StoredContentPack?> readPrevious() async {
    final pointer = await _readPointer();
    final version = pointer?.previousVersion;
    if (version == null || version.isEmpty) return null;
    return _readVersion(version);
  }

  Future<StoredContentPack?> _readVersion(String version) async {
    final manifestFile = await _manifestFile(version);
    final payloadFile = await _payloadFile(version);
    if (!await manifestFile.exists() || !await payloadFile.exists()) {
      return null;
    }

    final decoded = jsonDecode(await manifestFile.readAsString());
    if (decoded is! Map) return null;
    final manifest = ContentPackManifest.fromJson(
      Map<String, dynamic>.from(decoded),
    );
    final bytes = await payloadFile.readAsBytes();
    return StoredContentPack(manifest: manifest, bytes: bytes);
  }

  Future<ContentPackPointer?> _readPointer() async {
    final primary = await _pointerFile();
    final backup = await _pointerBackupFile();

    for (final file in [primary, backup]) {
      if (!await file.exists()) continue;
      try {
        final decoded = jsonDecode(await file.readAsString());
        if (decoded is! Map) continue;
        final pointer = ContentPackPointer.fromJson(
          Map<String, dynamic>.from(decoded),
        );
        if (pointer.activeVersion.isNotEmpty) return pointer;
      } catch (_) {
        // Try the crash-safe backup pointer before giving up.
      }
    }
    return null;
  }

  @override
  Future<void> activate(
    ContentPackManifest manifest,
    List<int> bytes,
  ) async {
    final current = await _readPointer();
    final manifestFile = await _manifestFile(manifest.version);
    final payloadFile = await _payloadFile(manifest.version);
    final manifestTemp = File('${manifestFile.path}.tmp');
    final payloadTemp = File('${payloadFile.path}.tmp');

    await _deleteIfExists(manifestTemp);
    await _deleteIfExists(payloadTemp);

    await payloadTemp.writeAsBytes(bytes, flush: true);
    await manifestTemp.writeAsString(
      jsonEncode(manifest.toJson()),
      flush: true,
    );

    await _replaceFile(payloadTemp, payloadFile);
    await _replaceFile(manifestTemp, manifestFile);

    final previous = current?.activeVersion == manifest.version
        ? current?.previousVersion
        : current?.activeVersion;

    await _writePointer(
      ContentPackPointer(
        activeVersion: manifest.version,
        previousVersion: previous,
      ),
    );

    await _purgeUnused(
      keepVersions: {
        manifest.version,
        ?previous,
      },
    );
  }

  @override
  Future<bool> rollback() async {
    final pointer = await _readPointer();
    final previous = pointer?.previousVersion;
    if (pointer == null || previous == null || previous.isEmpty) return false;
    if (await _readVersion(previous) == null) return false;

    await _writePointer(
      ContentPackPointer(
        activeVersion: previous,
        previousVersion: pointer.activeVersion,
      ),
    );
    return true;
  }

  Future<void> _writePointer(ContentPackPointer pointer) async {
    final target = await _pointerFile();
    final backup = await _pointerBackupFile();
    final temp = File('${target.path}.next');

    await _deleteIfExists(temp);
    await temp.writeAsString(jsonEncode(pointer.toJson()), flush: true);

    if (await target.exists()) {
      await _deleteIfExists(backup);
      await target.copy(backup.path);
    }

    await _replaceFile(temp, target);
  }

  Future<void> _purgeUnused({
    required Set<String> keepVersions,
  }) async {
    final root = await _root();
    await for (final entity in root.list()) {
      if (entity is! File) continue;
      final name = entity.uri.pathSegments.last;
      final match =
          RegExp(r'^(?:manifest|pack)_(.+)\.json$').firstMatch(name);
      if (match == null) continue;
      final version = match.group(1);
      if (version != null && !keepVersions.contains(version)) {
        await _deleteIfExists(entity);
      }
    }
  }

  Future<void> _replaceFile(File source, File target) async {
    if (await target.exists()) await target.delete();
    await source.rename(target.path);
  }

  Future<void> _deleteIfExists(File file) async {
    if (await file.exists()) await file.delete();
  }

  String _safeVersion(String value) {
    if (!RegExp(r'^[A-Za-z0-9._-]+$').hasMatch(value)) {
      throw const FormatException('invalid_content_pack_version');
    }
    return value;
  }

  @override
  Future<void> close() async {}
}
