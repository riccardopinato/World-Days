import 'content_pack_models.dart';

abstract interface class ContentPackTransport {
  bool get supported;

  Future<String> getText(Uri uri);

  Future<List<int>> getBytes(Uri uri);

  Future<void> close();
}

abstract interface class ContentPackStorage {
  bool get supported;

  Future<StoredContentPack?> readActive();

  Future<StoredContentPack?> readPrevious();

  Future<void> activate(
    ContentPackManifest manifest,
    List<int> bytes,
  );

  Future<bool> rollback();

  Future<void> close();
}
