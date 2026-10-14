import 'dart:async';

import 'package:flutter/material.dart';

import 'app/app_controller.dart';
import 'app/world_days_app.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final controller = AppController();
  await controller.initialize();
  runApp(WorldDaysApp(controller: controller));
  unawaited(controller.initializeMonetization());
}
