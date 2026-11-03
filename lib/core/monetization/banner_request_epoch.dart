/// Invalidates in-flight asynchronous banner loads when eligibility changes.
final class BannerRequestEpoch {
  int _value = 0;

  int begin() => ++_value;
  void invalidate() => _value++;
  bool isCurrent(int value) => value == _value;
}
