import 'dart:typed_data';

import 'content_pack_models.dart';

abstract interface class ContentPackTransport {
  bool get supported;

  Future<String> getText(Uri uri);

  Future<List<int>> getBytes(
    Uri uri, {
    required int maxBytes,
  });

  Future<void> close();
}

Future<List<int>> collectBoundedContentBytes(
  Stream<List<int>> stream, {
  required int maxBytes,
}) async {
  if (maxBytes <= 0) {
    throw const FormatException('content_payload_invalid_max_bytes');
  }

  final buffer = BytesBuilder(copy: false);
  var received = 0;
  await for (final chunk in stream) {
    received += chunk.length;
    if (received > maxBytes) {
      throw const FormatException('content_payload_exceeds_byte_cap');
    }
    buffer.add(chunk);
  }
  return buffer.takeBytes();
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
