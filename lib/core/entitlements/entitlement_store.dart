import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import 'entitlement_models.dart';

abstract interface class EntitlementStore {
  Future<EntitlementSnapshot> load();

  Future<void> save(EntitlementSnapshot snapshot);
}

class SharedPreferencesEntitlementStore implements EntitlementStore {
  const SharedPreferencesEntitlementStore();

  static const _key = 'world_days_entitlement_v1';

  @override
  Future<EntitlementSnapshot> load() async {
    final preferences = await SharedPreferences.getInstance();
    final raw = preferences.getString(_key);
    if (raw == null || raw.isEmpty) return const EntitlementSnapshot.free();

    try {
      final decoded = Map<String, dynamic>.from(jsonDecode(raw) as Map);
      return EntitlementSnapshot.fromJson(decoded).asOfflineCache();
    } catch (_) {
      return const EntitlementSnapshot.free();
    }
  }

  @override
  Future<void> save(EntitlementSnapshot snapshot) async {
    final preferences = await SharedPreferences.getInstance();
    final ok = await preferences.setString(
      _key,
      jsonEncode(snapshot.toJson()),
    );
    if (!ok) throw StateError('entitlement_write_failed');
  }
}
