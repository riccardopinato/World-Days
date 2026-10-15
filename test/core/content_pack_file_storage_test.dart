import 'dart:io';

import 'package:crypto/crypto.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:world_days/core/content_pack/content_pack_models.dart';
import 'package:world_days/core/content_pack/file_content_pack_storage.dart';

ContentPackManifest _manifest(String version, List<int> bytes) =>
    ContentPackManifest(
      schemaVersion: 1,
      packId: 'world-days-catalog',
      version: version,
      kind: 'catalog',
      sizeBytes: bytes.length,
      sha256: sha256.convert(bytes).toString(),
      payloadUrl:
          'https://riccardopinato.github.io/World-Days/content/world-days-content-$version.json',
      generatedAt: '2026-10-15',
    );

void main() {
  test('file storage atomically tracks active and previous versions', () async {
    final root = await Directory.systemTemp.createTemp('world_days_pack_test_');
    addTearDown(() => root.delete(recursive: true));

    final storage = FileContentPackStorage(
      rootProvider: () async => root,
    );

    final v1 = [1, 2, 3];
    final v2 = [4, 5, 6, 7];

    await storage.activate(_manifest('1', v1), v1);
    expect((await storage.readActive())?.manifest.version, '1');
    expect(await storage.readPrevious(), isNull);

    await storage.activate(_manifest('2', v2), v2);

    final active = await storage.readActive();
    final previous = await storage.readPrevious();
    expect(active?.manifest.version, '2');
    expect(active?.bytes, v2);
    expect(previous?.manifest.version, '1');
    expect(previous?.bytes, v1);

    final entities = await root.list().toList();
    final files = entities.whereType<File>();
    final names = files.map((file) => file.uri.pathSegments.last).toSet();
    expect(names, contains('pointer.json'));
    expect(names, contains('pointer.backup.json'));
    expect(names, contains('manifest_1.json'));
    expect(names, contains('pack_1.json'));
    expect(names, contains('manifest_2.json'));
    expect(names, contains('pack_2.json'));
  });

  test('rollback swaps back to the last known good version', () async {
    final root = await Directory.systemTemp.createTemp('world_days_pack_test_');
    addTearDown(() => root.delete(recursive: true));

    final storage = FileContentPackStorage(
      rootProvider: () async => root,
    );
    final v1 = [10, 11];
    final v2 = [20, 21];

    await storage.activate(_manifest('1', v1), v1);
    await storage.activate(_manifest('2', v2), v2);

    expect(await storage.rollback(), isTrue);
    expect((await storage.readActive())?.manifest.version, '1');
    expect((await storage.readPrevious())?.manifest.version, '2');
  });

  test('corrupt primary pointer falls back to crash-safe backup', () async {
    final root = await Directory.systemTemp.createTemp('world_days_pack_test_');
    addTearDown(() => root.delete(recursive: true));

    final storage = FileContentPackStorage(
      rootProvider: () async => root,
    );
    final v1 = [1];
    final v2 = [2];

    await storage.activate(_manifest('1', v1), v1);
    await storage.activate(_manifest('2', v2), v2);

    await File('${root.path}${Platform.pathSeparator}pointer.json')
        .writeAsString('{broken');

    final recovered = await storage.readActive();
    expect(recovered?.manifest.version, '1');
    expect(recovered?.bytes, v1);
  });
}
