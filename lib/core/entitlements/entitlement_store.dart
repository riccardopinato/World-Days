import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import 'entitlement_models.dart';

abstract interface class EntitlementStore {
  Future<EntitlementSnapshot> load();

  Future<void> save(EntitlementSnapshot snapshot);

  Future<PendingPurchaseCompletion?> loadPendingCompletion();

  Future<void> savePendingCompletion(PendingPurchaseCompletion pending);

  Future<void> clearPendingCompletion({
    String? transactionId,
  });
}

class SharedPreferencesEntitlementStore implements EntitlementStore {
  const SharedPreferencesEntitlementStore();

  static const _key = 'world_days_entitlement_v1';
  static const _pendingCompletionKey =
      'world_days_pending_purchase_completion_v1';

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

  @override
  Future<PendingPurchaseCompletion?> loadPendingCompletion() async {
    final preferences = await SharedPreferences.getInstance();
    final raw = preferences.getString(_pendingCompletionKey);
    if (raw == null || raw.isEmpty) return null;

    try {
      final decoded = Map<String, dynamic>.from(jsonDecode(raw) as Map);
      return PendingPurchaseCompletion.fromJson(decoded);
    } catch (_) {
      await preferences.remove(_pendingCompletionKey);
      return null;
    }
  }

  @override
  Future<void> savePendingCompletion(
    PendingPurchaseCompletion pending,
  ) async {
    final preferences = await SharedPreferences.getInstance();
    final ok = await preferences.setString(
      _pendingCompletionKey,
      jsonEncode(pending.toJson()),
    );
    if (!ok) throw StateError('pending_purchase_completion_write_failed');
  }

  @override
  Future<void> clearPendingCompletion({
    String? transactionId,
  }) async {
    final preferences = await SharedPreferences.getInstance();
    if (transactionId != null) {
      final current = await loadPendingCompletion();
      if (current != null && current.transactionId != transactionId) {
        return;
      }
    }
    final ok = await preferences.remove(_pendingCompletionKey);
    if (!ok && preferences.containsKey(_pendingCompletionKey)) {
      throw StateError('pending_purchase_completion_clear_failed');
    }
  }
}
