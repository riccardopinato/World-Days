import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/data/catalog_repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('bundled catalog loads with stable identities', () async {
    final snapshot = await const CatalogRepository().load();
    expect(snapshot.records.length, greaterThanOrEqualTo(260));
    expect(snapshot.byId.length, snapshot.records.length);
    expect(snapshot.byId['world-habitat-day']?.title, 'World Habitat Day');
    expect(snapshot.occurrences2026.length, greaterThanOrEqualTo(260));
  });
}
