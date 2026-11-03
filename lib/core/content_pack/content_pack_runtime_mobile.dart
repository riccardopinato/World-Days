import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import 'content_pack_io.dart';
import 'content_pack_manager.dart';
import 'file_content_pack_storage.dart';

ContentPackManager createContentPackManager({
  required ContentPayloadValidator validator,
}) =>
    ContentPackManager(
      transport: HttpContentPackTransport(),
      storage: FileContentPackStorage(),
      validator: validator,
    );

class HttpContentPackTransport implements ContentPackTransport {
  HttpContentPackTransport({http.Client? client})
      : _client = client ?? http.Client();

  final http.Client _client;
  static const int maxManifestBytes = 64 * 1024;

  @override
  bool get supported => true;

  @override
  Future<String> getText(Uri uri) async {
    // Reject redirects rather than following an unpinned content origin.
    final request = http.Request('GET', uri)..followRedirects = false;
    final response = await _client.send(request)
        .timeout(const Duration(seconds: 15));
    if (response.statusCode != HttpStatus.ok) {
      throw HttpException(
        'content_manifest_http_${response.statusCode}',
        uri: uri,
      );
    }
    final bytes = await collectBoundedContentBytes(
      response.stream.timeout(const Duration(seconds: 30)),
      maxBytes: maxManifestBytes,
    );
    return utf8.decode(bytes);
  }

  @override
  Future<List<int>> getBytes(
    Uri uri, {
    required int maxBytes,
  }) async {
    if (maxBytes <= 0) {
      throw const FormatException('content_payload_invalid_max_bytes');
    }

    final request = http.Request('GET', uri)..followRedirects = false;
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

    return collectBoundedContentBytes(
      response.stream.timeout(const Duration(seconds: 30)),
      maxBytes: maxBytes,
    );
  }

  @override
  Future<void> close() async => _client.close();
}
