// Host-side Flutter integration driver: writes engine FrameTiming reportData
// to build/integration_response_data.json on the connected test workstation.
import 'package:integration_test/integration_test_driver.dart';

Future<void> main() => integrationDriver();
