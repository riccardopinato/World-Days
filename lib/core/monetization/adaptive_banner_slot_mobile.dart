import 'dart:async';

import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

import 'admob_ids.dart';
import 'banner_request_epoch.dart';
import 'monetization_controller.dart';

class AdaptiveBannerSlot extends StatefulWidget {
  const AdaptiveBannerSlot({super.key, required this.controller});

  final MonetizationController controller;

  @override
  State<AdaptiveBannerSlot> createState() => _AdaptiveBannerSlotState();
}

class _AdaptiveBannerSlotState extends State<AdaptiveBannerSlot> {
  BannerAd? _banner;
  AdSize? _size;
  int? _lastWidth;
  bool _loading = false;
  final BannerRequestEpoch _epoch = BannerRequestEpoch();

  @override
  void initState() {
    super.initState();
    widget.controller.addListener(_onMonetizationChanged);
  }

  @override
  void didUpdateWidget(covariant AdaptiveBannerSlot oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.controller != widget.controller) {
      oldWidget.controller.removeListener(_onMonetizationChanged);
      widget.controller.addListener(_onMonetizationChanged);
      unawaited(_disposeBanner());
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) unawaited(_maybeLoad());
      });
    }
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    unawaited(_maybeLoad());
  }

  void _onMonetizationChanged() {
    if (!mounted) return;
    if (!widget.controller.canRequestAds) {
      // Invalidate synchronously: in-flight adaptive size requests and
      // callbacks cannot load or display an ad after consent is revoked.
      unawaited(_disposeBanner());
      setState(() {});
      return;
    }
    unawaited(_maybeLoad());
  }

  bool _eligible(int generation, int width) =>
      mounted &&
      _epoch.isCurrent(generation) &&
      widget.controller.canRequestAds &&
      MediaQuery.sizeOf(context).width.floor() == width;

  void _finishPending(int generation) {
    if (!_epoch.isCurrent(generation)) return;
    _loading = false;
    _lastWidth = null;
  }

  void _retryAfterWidthChange(int generation, int width) {
    if (!_epoch.isCurrent(generation) || !mounted) return;
    _finishPending(generation);
    if (widget.controller.canRequestAds &&
        MediaQuery.sizeOf(context).width.floor() != width) {
      unawaited(_maybeLoad());
    }
  }

  Future<void> _maybeLoad() async {
    if (!mounted || !widget.controller.canRequestAds || _loading) return;

    final width = MediaQuery.sizeOf(context).width.floor();
    if (width <= 0 || (_banner != null && _lastWidth == width)) return;

    final adUnitId = AdMobIds.banner();
    if (adUnitId == null) return;

    final generation = _epoch.begin();
    _loading = true;
    _lastWidth = width;
    final previous = _banner;
    _banner = null;
    _size = null;
    await previous?.dispose();

    if (!_eligible(generation, width)) {
      _retryAfterWidthChange(generation, width);
      return;
    }

    AdSize? size;
    try {
      size = await AdSize.getLargeAnchoredAdaptiveBannerAdSize(width);
    } catch (error) {
      debugPrint('World Days adaptive banner size failed: $error');
      _finishPending(generation);
      return;
    }
    if (!_eligible(generation, width)) {
      _retryAfterWidthChange(generation, width);
      return;
    }
    if (size == null) {
      _finishPending(generation);
      return;
    }

    late final BannerAd banner;
    banner = BannerAd(
      adUnitId: adUnitId,
      size: size,
      request: const AdRequest(),
      listener: BannerAdListener(
        onAdLoaded: (ad) {
          if (!_eligible(generation, width)) {
            unawaited(ad.dispose());
            _retryAfterWidthChange(generation, width);
            return;
          }
          setState(() {
            _banner = banner;
            _size = size;
            _loading = false;
          });
        },
        onAdFailedToLoad: (ad, error) {
          unawaited(ad.dispose());
          if (!_epoch.isCurrent(generation)) return;
          debugPrint(
            'World Days banner load failed: '
            '${error.code} ${error.domain} ${error.message}',
          );
          _finishPending(generation);
          if (mounted) setState(() {
            _banner = null;
            _size = null;
          });
        },
      ),
    );

    // Critical: re-check eligibility after all awaits and immediately
    // before issuing the provider ad request.
    if (!_eligible(generation, width)) {
      unawaited(banner.dispose());
      _retryAfterWidthChange(generation, width);
      return;
    }
    try {
      await banner.load();
    } catch (error) {
      unawaited(banner.dispose());
      if (_epoch.isCurrent(generation)) {
        debugPrint('World Days banner request failed: $error');
        _finishPending(generation);
      }
    }
  }

  Future<void> _disposeBanner() async {
    _epoch.invalidate();
    final old = _banner;
    _banner = null;
    _size = null;
    _loading = false;
    _lastWidth = null;
    await old?.dispose();
  }

  @override
  void dispose() {
    _epoch.invalidate();
    widget.controller.removeListener(_onMonetizationChanged);
    final old = _banner;
    _banner = null;
    unawaited(old?.dispose() ?? Future<void>.value());
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final ad = _banner;
    final size = _size;
    if (!widget.controller.canRequestAds || ad == null || size == null) {
      return const SizedBox.shrink();
    }
    return Material(
      color: Theme.of(context).colorScheme.surface,
      child: SafeArea(
        bottom: false,
        child: SizedBox(
          width: double.infinity,
          height: size.height.toDouble(),
          child: Center(
            child: SizedBox(
              width: size.width.toDouble(),
              height: size.height.toDouble(),
              child: AdWidget(ad: ad),
            ),
          ),
        ),
      ),
    );
  }
}
