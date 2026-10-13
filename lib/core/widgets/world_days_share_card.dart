import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:share_plus/share_plus.dart';

import '../../domain/observance.dart';
import '../../l10n/app_localizations.dart';
import '../visual/observance_visuals.dart';

class WorldDaysShareCard extends StatelessWidget {
  const WorldDaysShareCard({
    super.key,
    required this.observance,
    required this.badgeText,
  });

  final Observance observance;
  final String badgeText;

  @override
  Widget build(BuildContext context) {
    final style = ObservanceVisuals.resolve(observance);

    return MediaQuery(
      data: MediaQuery.of(context).copyWith(
        textScaler: TextScaler.noScaling,
      ),
      child: AspectRatio(
        aspectRatio: 4 / 5,
        child: ObservanceArtwork(
        style: style,
        borderRadius: BorderRadius.circular(34),
        foreground: Padding(
          padding: const EdgeInsets.all(28),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 11,
                      vertical: 7,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: .18),
                      borderRadius: BorderRadius.circular(999),
                      border: Border.all(
                        color: Colors.white.withValues(alpha: .22),
                      ),
                    ),
                    child: Text(
                      badgeText,
                      style: Theme.of(context).textTheme.labelMedium?.copyWith(
                            color: Colors.white,
                            fontWeight: FontWeight.w800,
                          ),
                    ),
                  ),
                  const Spacer(),
                  const Icon(
                    Icons.public_rounded,
                    color: Colors.white,
                    size: 30,
                  ),
                ],
              ),
              const Spacer(),
              Icon(style.icon, color: Colors.white, size: 46),
              const SizedBox(height: 16),
              Text(
                observance.title,
                maxLines: 5,
                overflow: TextOverflow.ellipsis,
                style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.w900,
                      height: .98,
                    ),
              ),
              const SizedBox(height: 14),
              Text(
                observance.authority.name,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      color: Colors.white.withValues(alpha: .86),
                      fontWeight: FontWeight.w600,
                    ),
              ),
              const SizedBox(height: 28),
              Row(
                children: [
                  Expanded(
                    child: Text(
                      'WORLD DAYS',
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.labelLarge?.copyWith(
                            color: Colors.white,
                            fontWeight: FontWeight.w900,
                            letterSpacing: 1.4,
                          ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Text(
                    'discover daily',
                    maxLines: 1,
                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                          color: Colors.white.withValues(alpha: .72),
                        ),
                  ),
                ],
              ),
            ],
          ),
          ),
        ),
      ),
    );
  }
}

Future<void> showWorldDaysShareCard({
  required BuildContext context,
  required Observance observance,
  required String badgeText,
}) {
  return showModalBottomSheet<void>(
    context: context,
    useSafeArea: true,
    isScrollControlled: true,
    showDragHandle: true,
    builder: (context) => _ShareCardSheet(
      observance: observance,
      badgeText: badgeText,
    ),
  );
}

class _ShareCardSheet extends StatefulWidget {
  const _ShareCardSheet({
    required this.observance,
    required this.badgeText,
  });

  final Observance observance;
  final String badgeText;

  @override
  State<_ShareCardSheet> createState() => _ShareCardSheetState();
}

class _ShareCardSheetState extends State<_ShareCardSheet> {
  final _boundaryKey = GlobalKey();
  bool _sharing = false;

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);

    return SingleChildScrollView(
      padding: EdgeInsets.fromLTRB(
        20,
        4,
        20,
        20 + MediaQuery.viewPaddingOf(context).bottom,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            l10n.shareCard,
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.w900,
                ),
          ),
          const SizedBox(height: 6),
          Text(
            l10n.shareCardDescription,
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: 18),
          Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 360),
              child: RepaintBoundary(
                key: _boundaryKey,
                child: Material(
                  type: MaterialType.transparency,
                  child: WorldDaysShareCard(
                    observance: widget.observance,
                    badgeText: widget.badgeText,
                  ),
                ),
              ),
            ),
          ),
          const SizedBox(height: 20),
          Builder(
            builder: (buttonContext) => FilledButton.icon(
              onPressed: _sharing ? null : () => _share(buttonContext),
              icon: _sharing
                  ? const SizedBox.square(
                      dimension: 20,
                      child: CircularProgressIndicator(strokeWidth: 2.4),
                    )
                  : const Icon(Icons.ios_share_rounded),
              label: Text(l10n.shareThisDay),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _share(BuildContext buttonContext) async {
    final l10n = AppLocalizations.of(context);
    setState(() => _sharing = true);

    try {
      final box = buttonContext.findRenderObject() as RenderBox?;
      final origin = box != null && box.hasSize
          ? box.localToGlobal(Offset.zero) & box.size
          : const Rect.fromLTWH(1, 1, 1, 1);

      await WidgetsBinding.instance.endOfFrame;
      final boundary = _boundaryKey.currentContext?.findRenderObject()
          as RenderRepaintBoundary?;
      if (boundary == null) {
        throw StateError('Share card boundary unavailable');
      }

      final image = await boundary.toImage(pixelRatio: 3);
      final data = await image.toByteData(format: ui.ImageByteFormat.png);
      if (data == null) {
        throw StateError('Share card PNG encoding failed');
      }

      final bytes = data.buffer.asUint8List(
        data.offsetInBytes,
        data.lengthInBytes,
      );
      await SharePlus.instance.share(
        ShareParams(
          files: [
            XFile.fromData(
              bytes,
              mimeType: 'image/png',
            ),
          ],
          fileNameOverrides: [
            'world-days-${widget.observance.id}.png',
          ],
          sharePositionOrigin: origin,
        ),
      );
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(l10n.shareFailed)),
        );
      }
    } finally {
      if (mounted) setState(() => _sharing = false);
    }
  }
}
