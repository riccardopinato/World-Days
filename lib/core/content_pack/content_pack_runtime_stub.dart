import 'content_pack_io.dart';
import 'content_pack_manager.dart';

ContentPackManager createContentPackManager({
  required ContentPayloadValidator validator,
}) =>
    ContentPackManager(
      transport: const _UnsupportedTransport(),
      storage: const _UnsupportedStorage(),
      validator: validator,
    );

class _UnsupportedTransport implements ContentPackTransport {
  const _UnsupportedTransport();

  @override
  bool get supported => false;

  @override
  Future<List<int>> getBytes(Uri uri) =>
      Future.error(UnsupportedError('content_pack_transport_unsupported'));

  @override
  Future<String> getText(Uri uri) =>
      Future.error(UnsupportedError('content_pack_transport_unsupported'));

  @override
  Future<void> close() async {}
}

class _UnsupportedStorage implements ContentPackStorage {
  const _UnsupportedStorage();

  @override
  bool get supported => false;

  @override
  Future<void> activate(manifest, bytes) =>
      Future.error(UnsupportedError('content_pack_storage_unsupported'));

  @override
  Future<void> close() async {}

  @override
  Future<StoredContentPack?> readActive() async => null;

  @override
  Future<StoredContentPack?> readPrevious() async => null;

  @override
  Future<bool> rollback() async => false;
}
