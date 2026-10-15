import 'dart:convert';

import 'package:crypto/crypto.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/core/content_pack/content_pack_io.dart';
import 'package:world_days/core/content_pack/content_pack_manager.dart';
import 'package:world_days/core/content_pack/content_pack_models.dart';

class _FakeTransport implements ContentPackTransport {
  _FakeTransport({
    required this.manifestText,
    required this.payloadBytes,
    this.failManifest = false,
    this.failPayload = false,
  });

  String manifestText;
  List<int> payloadBytes;
  bool failManifest;
  bool failPayload;

  @override
  bool get supported => true;

  @override
  Future<String> getText(Uri uri) async {
    if (failManifest) throw StateError('manifest_network_down');
    return manifestText;
  }

  @override
  Future<List<int>> getBytes(Uri uri) async {
    if (failPayload) throw StateError('payload_network_down');
    return payloadBytes;
  }

  @override
  Future<void> close() async {}
}

class _MemoryStorage implements ContentPackStorage {
  StoredContentPack? active;
  StoredContentPack? previous;
  int activationCount = 0;
  int rollbackCount = 0;

  @override
  bool get supported => true;

  @override
  Future<StoredContentPack?> readActive() async => active;

  @override
  Future<StoredContentPack?> readPrevious() async => previous;

  @override
  Future<void> activate(
    ContentPackManifest manifest,
    List<int> bytes,
  ) async {
    previous = active;
    active = StoredContentPack(
      manifest: manifest,
      bytes: List<int>.from(bytes),
    );
    activationCount++;
  }

  @override
  Future<bool> rollback() async {
    final fallback = previous;
    if (fallback == null) return false;
    final current = active;
    active = fallback;
    previous = current;
    rollbackCount++;
    return true;
  }

  @override
  Future<void> close() async {}
}

Map<String, dynamic> _payload(String version) => {
      'schemaVersion': 1,
      'packId': 'world-days-catalog',
      'version': version,
      'marker': 'valid',
    };

List<int> _payloadBytes(String version) =>
    utf8.encode(jsonEncode(_payload(version)));

ContentPackManifest _manifest(
  String version,
  List<int> bytes, {
  String? hashOverride,
}) =>
    ContentPackManifest(
      schemaVersion: 1,
      packId: 'world-days-catalog',
      version: version,
      kind: 'catalog',
      sizeBytes: bytes.length,
      sha256: hashOverride ?? sha256.convert(bytes).toString(),
      payloadUrl:
          'https://riccardopinato.github.io/World-Days/content/pack-$version.json',
      generatedAt: '2026-10-15',
    );

String _manifestJson(ContentPackManifest manifest) =>
    jsonEncode(manifest.toJson());

void _validator(Map<String, dynamic> payload) {
  if (payload['schemaVersion'] != 1 ||
      payload['packId'] != 'world-days-catalog' ||
      payload['marker'] != 'valid') {
    throw const FormatException('invalid_test_payload');
  }
}

void main() {
  test('remote version equal to bundled catalog is not reinstalled', () async {
    final bytes = _payloadBytes('1');
    final manifest = _manifest('1', bytes);
    final manager = ContentPackManager(
      transport: _FakeTransport(
        manifestText: _manifestJson(manifest),
        payloadBytes: bytes,
      ),
      storage: _MemoryStorage(),
      validator: _validator,
    );

    await manager.initialize();
    manager.setBundledVersion('1');

    expect(await manager.checkForUpdate(), isFalse);
    expect(manager.state, ContentPackState.ready);
    expect(manager.status.activeVersion, '1');
  });

  test('manifest requires bounded HTTPS payload metadata', () {
    expect(
      () => ContentPackManifest.fromJson({
        'schemaVersion': 1,
        'packId': 'world-days-catalog',
        'version': '2',
        'kind': 'catalog',
        'sizeBytes': 10,
        'sha256': List.filled(64, 'a').join(),
        'payloadUrl': 'http://example.test/pack.json',
        'generatedAt': '2026-10-15',
      }),
      throwsFormatException,
    );

    expect(
      () => ContentPackManifest.fromJson({
        'schemaVersion': 1,
        'packId': 'world-days-catalog',
        'version': '../unsafe',
        'kind': 'catalog',
        'sizeBytes': 10,
        'sha256': List.filled(64, 'a').join(),
        'payloadUrl': 'https://example.test/pack.json',
        'generatedAt': '2026-10-15',
      }),
      throwsFormatException,
    );
  });

  test('fresh verified update becomes active only after validation', () async {
    final bytes = _payloadBytes('2');
    final manifest = _manifest('2', bytes);
    final transport = _FakeTransport(
      manifestText: _manifestJson(manifest),
      payloadBytes: bytes,
    );
    final storage = _MemoryStorage();
    final manager = ContentPackManager(
      transport: transport,
      storage: storage,
      validator: _validator,
    );

    await manager.initialize();
    expect(manager.state, ContentPackState.bundled);

    expect(await manager.checkForUpdate(), isTrue);
    expect(manager.state, ContentPackState.updateAvailable);

    expect(await manager.installAvailableUpdate(), isTrue);
    expect(manager.state, ContentPackState.ready);
    expect(manager.activeManifest?.version, '2');
    expect(manager.activePayload?['marker'], 'valid');
    expect(storage.activationCount, 1);
  });

  test('checksum mismatch never activates corrupt bytes', () async {
    final oldBytes = _payloadBytes('1');
    final oldManifest = _manifest('1', oldBytes);
    final newBytes = _payloadBytes('2');
    final brokenManifest = _manifest(
      '2',
      newBytes,
      hashOverride: List.filled(64, '0').join(),
    );
    final storage = _MemoryStorage()
      ..active = StoredContentPack(
        manifest: oldManifest,
        bytes: oldBytes,
      );
    final manager = ContentPackManager(
      transport: _FakeTransport(
        manifestText: _manifestJson(brokenManifest),
        payloadBytes: newBytes,
      ),
      storage: storage,
      validator: _validator,
    );

    await manager.initialize();
    expect(manager.activeManifest?.version, '1');

    expect(await manager.checkForUpdate(), isTrue);
    expect(await manager.installAvailableUpdate(), isFalse);

    expect(manager.activeManifest?.version, '1');
    expect(storage.active?.manifest.version, '1');
    expect(storage.activationCount, 0);
    expect(manager.lastError, contains('checksum'));
  });

  test('manifest network failure preserves the current active pack', () async {
    final bytes = _payloadBytes('1');
    final manifest = _manifest('1', bytes);
    final storage = _MemoryStorage()
      ..active = StoredContentPack(manifest: manifest, bytes: bytes);
    final transport = _FakeTransport(
      manifestText: _manifestJson(manifest),
      payloadBytes: bytes,
      failManifest: true,
    );
    final manager = ContentPackManager(
      transport: transport,
      storage: storage,
      validator: _validator,
    );

    await manager.initialize();
    expect(manager.state, ContentPackState.ready);

    expect(await manager.checkForUpdate(), isFalse);
    expect(manager.state, ContentPackState.ready);
    expect(manager.activeManifest?.version, '1');
    expect(manager.lastError, contains('manifest_check'));
  });

  test('payload network failure keeps old active pack untouched', () async {
    final oldBytes = _payloadBytes('1');
    final oldManifest = _manifest('1', oldBytes);
    final newBytes = _payloadBytes('2');
    final newManifest = _manifest('2', newBytes);
    final storage = _MemoryStorage()
      ..active = StoredContentPack(
        manifest: oldManifest,
        bytes: oldBytes,
      );
    final manager = ContentPackManager(
      transport: _FakeTransport(
        manifestText: _manifestJson(newManifest),
        payloadBytes: newBytes,
        failPayload: true,
      ),
      storage: storage,
      validator: _validator,
    );

    await manager.initialize();
    expect(await manager.checkForUpdate(), isTrue);
    expect(await manager.installAvailableUpdate(), isFalse);

    expect(manager.activeManifest?.version, '1');
    expect(storage.active?.manifest.version, '1');
    expect(storage.activationCount, 0);
  });

  test('invalid active pack rolls back to previous verified pack', () async {
    final previousBytes = _payloadBytes('1');
    final previousManifest = _manifest('1', previousBytes);

    final corruptBytes = _payloadBytes('2');
    final corruptManifest = _manifest(
      '2',
      corruptBytes,
      hashOverride: List.filled(64, 'f').join(),
    );

    final storage = _MemoryStorage()
      ..active = StoredContentPack(
        manifest: corruptManifest,
        bytes: corruptBytes,
      )
      ..previous = StoredContentPack(
        manifest: previousManifest,
        bytes: previousBytes,
      );

    final manager = ContentPackManager(
      transport: _FakeTransport(
        manifestText: _manifestJson(previousManifest),
        payloadBytes: previousBytes,
      ),
      storage: storage,
      validator: _validator,
    );

    await manager.initialize();

    expect(manager.state, ContentPackState.ready);
    expect(manager.activeManifest?.version, '1');
    expect(storage.rollbackCount, 1);
    expect(manager.lastError, 'rolled_back_invalid_active_pack');
  });

  test('no stored pack plus network failure remains bundled', () async {
    final bytes = _payloadBytes('1');
    final manifest = _manifest('1', bytes);
    final manager = ContentPackManager(
      transport: _FakeTransport(
        manifestText: _manifestJson(manifest),
        payloadBytes: bytes,
        failManifest: true,
      ),
      storage: _MemoryStorage(),
      validator: _validator,
    );

    await manager.initialize();
    expect(manager.state, ContentPackState.bundled);

    expect(await manager.checkForUpdate(), isFalse);
    expect(manager.state, ContentPackState.bundled);
    expect(manager.activeManifest, isNull);
  });
}
