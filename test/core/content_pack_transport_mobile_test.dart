import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:world_days/core/content_pack/content_pack_runtime_mobile.dart';

void main() {
  final uri = Uri.parse('https://riccardopinato.github.io/World-Days/content/manifest.json');

  test('manifest response under cap is decoded normally', () async {
    final client = MockClient((_) async => http.Response('{"ok":true}', 200));
    final transport = HttpContentPackTransport(client: client);
    expect(jsonDecode(await transport.getText(uri)), {'ok': true});
    await transport.close();
  });

  test('unbounded manifest response is rejected before materialization', () async {
    final client = MockClient((_) async => http.Response(
      List<String>.filled(HttpContentPackTransport.maxManifestBytes + 1, 'x').join(), 200,
    ));
    final transport = HttpContentPackTransport(client: client);
    await expectLater(transport.getText(uri), throwsFormatException);
    await transport.close();
  });

  test('HTTP redirects are not accepted for manifest or payload', () async {
    final client = MockClient((_) async => http.Response('', 302, headers: {
      'location': 'https://untrusted.example/data',
    }));
    final transport = HttpContentPackTransport(client: client);
    await expectLater(transport.getText(uri), throwsA(isA<HttpException>()));
    await expectLater(
      transport.getBytes(uri, maxBytes: 1024),
      throwsA(isA<HttpException>()),
    );
    await transport.close();
  });
}
