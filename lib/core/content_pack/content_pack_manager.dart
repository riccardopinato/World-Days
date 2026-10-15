import 'dart:convert';

import 'package:crypto/crypto.dart';
import 'package:flutter/foundation.dart';

import 'content_pack_io.dart';
import 'content_pack_models.dart';

typedef ContentPayloadValidator = void Function(Map<String, dynamic> payload);

class ContentPackManager extends ChangeNotifier {
  ContentPackManager(
    this._transport,
    this._storage,
    this._validator, {
    Uri? manifestUri,
  }) : manifestUri = manifestUri ??
            Uri.parse(
              'https://riccardopinato.github.io/World-Days/content/manifest.json',
            );

  final ContentPackTransport _transport;
  final ContentPackStorage _storage;
  final ContentPayloadValidator _validator;
  final Uri manifestUri;

  ContentPackState _state = ContentPackState.bundled;
  ContentPackManifest? _activeManifest;
  ContentPackManifest? _remoteManifest;
  Map<String, dynamic>? _activePayload;
  String? _lastError;
  String? _bundledVersion;

  bool get supported => _transport.supported && _storage.supported;
  ContentPackState get state => _state;
  ContentPackManifest? get activeManifest => _activeManifest;
  ContentPackManifest? get remoteManifest => _remoteManifest;
  Map<String, dynamic>? get activePayload => _activePayload;
  String? get lastError => _lastError;
  String? get bundledVersion => _bundledVersion;

  void setBundledVersion(String version) {
    final normalized = version.trim();
    if (normalized.isEmpty || _bundledVersion == normalized) return;
    _bundledVersion = normalized;
    notifyListeners();
  }

  ContentPackStatus get status => ContentPackStatus(
        state: _state,
        activeVersion: _activeManifest?.version ?? _bundledVersion,
        remoteVersion: _remoteManifest?.version,
        lastError: _lastError,
      );

  Future<void> initialize() async {
    if (!supported) {
      _state = ContentPackState.bundled;
      return;
    }

    try {
      final active = await _storage.readActive();
      if (active == null) {
        _state = ContentPackState.bundled;
        return;
      }
      await _acceptStored(active);
      _state = ContentPackState.ready;
    } catch (error) {
      final recovered = await _recoverPrevious();
      if (!recovered) {
        _activeManifest = null;
        _activePayload = null;
        _state = ContentPackState.bundled;
        _lastError = 'active_pack_invalid:$error';
      }
    }
    notifyListeners();
  }

  Future<bool> checkForUpdate() async {
    if (!supported) return false;
    _state = ContentPackState.checking;
    _lastError = null;
    notifyListeners();

    try {
      final raw = await _transport.getText(manifestUri);
      final decoded = jsonDecode(raw);
      if (decoded is! Map) {
        throw const FormatException('manifest_not_object');
      }
      final manifest = ContentPackManifest.fromJson(
        Map<String, dynamic>.from(decoded),
      );
      _remoteManifest = manifest;

      final currentVersion = _activeManifest?.version ?? _bundledVersion;
      if (currentVersion == manifest.version) {
        _state = ContentPackState.ready;
        notifyListeners();
        return false;
      }
      _state = ContentPackState.updateAvailable;
      notifyListeners();
      return true;
    } catch (error) {
      _state =
          _activeManifest == null ? ContentPackState.bundled : ContentPackState.ready;
      _lastError = 'manifest_check:$error';
      notifyListeners();
      return false;
    }
  }

  Future<bool> installAvailableUpdate() async {
    final manifest = _remoteManifest;
    if (!supported || manifest == null) return false;

    _state = ContentPackState.downloading;
    _lastError = null;
    notifyListeners();

    try {
      final bytes = await _transport.getBytes(Uri.parse(manifest.payloadUrl));
      _state = ContentPackState.verifying;
      notifyListeners();

      final payload = _verifyAndDecode(manifest, bytes);
      await _storage.activate(manifest, bytes);

      _activeManifest = manifest;
      _activePayload = payload;
      _state = ContentPackState.ready;
      _lastError = null;
      notifyListeners();
      return true;
    } catch (error) {
      _state =
          _activeManifest == null ? ContentPackState.bundled : ContentPackState.ready;
      _lastError = 'pack_install:$error';
      notifyListeners();
      return false;
    }
  }

  Future<bool> rollback() async {
    if (!supported) return false;
    try {
      final changed = await _storage.rollback();
      if (!changed) return false;
      final active = await _storage.readActive();
      if (active == null) {
        _activeManifest = null;
        _activePayload = null;
        _state = ContentPackState.bundled;
      } else {
        await _acceptStored(active);
        _state = ContentPackState.ready;
      }
      _lastError = null;
      notifyListeners();
      return true;
    } catch (error) {
      _lastError = 'pack_rollback:$error';
      notifyListeners();
      return false;
    }
  }

  Future<void> _acceptStored(StoredContentPack stored) async {
    _activePayload = _verifyAndDecode(stored.manifest, stored.bytes);
    _activeManifest = stored.manifest;
  }

  Future<bool> _recoverPrevious() async {
    try {
      final previous = await _storage.readPrevious();
      if (previous == null) return false;
      _verifyAndDecode(previous.manifest, previous.bytes);
      final rolledBack = await _storage.rollback();
      if (!rolledBack) return false;
      final active = await _storage.readActive();
      if (active == null) return false;
      await _acceptStored(active);
      _state = ContentPackState.ready;
      _lastError = 'rolled_back_invalid_active_pack';
      return true;
    } catch (_) {
      return false;
    }
  }

  Map<String, dynamic> _verifyAndDecode(
    ContentPackManifest manifest,
    List<int> bytes,
  ) {
    if (bytes.length != manifest.sizeBytes) {
      throw const FormatException('content_pack_size_mismatch');
    }
    final actual = sha256.convert(bytes).toString().toLowerCase();
    if (actual != manifest.sha256) {
      throw const FormatException('content_pack_checksum_mismatch');
    }

    final decoded = jsonDecode(utf8.decode(bytes));
    if (decoded is! Map) {
      throw const FormatException('content_pack_not_object');
    }
    final payload = Map<String, dynamic>.from(decoded);
    _validator(payload);
    return payload;
  }

  @override
  void dispose() {
    _transport.close();
    _storage.close();
    super.dispose();
  }
}
