import 'package:flutter/widgets.dart';

import 'monetization_controller.dart';

class AdaptiveBannerSlot extends StatelessWidget {
  const AdaptiveBannerSlot({
    super.key,
    required this.controller,
  });

  final MonetizationController controller;

  @override
  Widget build(BuildContext context) => const SizedBox.shrink();
}
