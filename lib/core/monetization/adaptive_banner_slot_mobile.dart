import 'package:flutter/material.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

import 'admob_ids.dart';
import 'monetization_controller.dart';

class AdaptiveBannerSlot extends StatefulWidget {
  const AdaptiveBannerSlot({
    super.key,
    required this.controller,
  });

  final MonetizationController controller;

  @override
  State<AdaptiveBannerSlot> createState() => _AdaptiveBannerSlotState();
}

class _AdaptiveBannerSlotState extends State<AdaptiveBannerSlot> {
  BannerAd? _banner;
  AdSize? _size;
  int? _lastWidth;
  bool _loading = false;

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
      _disposeBanner();
    }
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _maybeLoad();
  }

  void _onMonetizationChanged() {
    if (!mounted) return;
    if (!widget.controller.canRequestAds) {
      _disposeBanner();
      setState(() {});
      return;
    }
    _maybeLoad();
  }

  Future<void> _maybeLoad() async {
    if (!mounted ||
        !widget.controller.canRequestAds ||
        _loading) {
      return;
    }

    final width = MediaQuery.sizeOf(context).width.floor();
    if (width <= 0 || (_banner != null && _lastWidth == width)) return;

    final adUnitId = AdMobIds.banner();
    if (adUnitId == null) return;

    _loading = true;
    _lastWidth = width;
    await _banner?.dispose();
    _banner = null;
    _size = null;

    final size =
        await AdSize.getLargeAnchoredAdaptiveBannerAdSize(width);
    if (!mounted || size == null) {
      _loading = false;
      return;
    }

    late final BannerAd banner;
    banner = BannerAd(
      adUnitId: adUnitId,
      size: size,
      request: const AdRequest(),
      listener: BannerAdListener(
        onAdLoaded: (ad) {
          if (!mounted) {
            ad.dispose();
            return;
          }
          setState(() {
            _banner = banner;
            _size = size;
            _loading = false;
          });
        },
        onAdFailedToLoad: (ad, error) {
          debugPrint(
            'World Days banner load failed: '
            '${error.code} ${error.domain} ${error.message}',
          );
          ad.dispose();
          if (mounted) {
            setState(() {
              _banner = null;
              _size = null;
              _loading = false;
            });
          }
        },
      ),
    );
    banner.load();
  }

  Future<void> _disposeBanner() async {
    await _banner?.dispose();
    _banner = null;
    _size = null;
    _loading = false;
    _lastWidth = null;
  }

  @override
  void dispose() {
    widget.controller.removeListener(_onMonetizationChanged);
    _banner?.dispose();
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
