enum ContentPackState {
  bundled,
  checking,
  updateAvailable,
  downloading,
  verifying,
  ready,
  failed,
}

final class ContentPackManifest {
  const ContentPackManifest({
    required this.schemaVersion,
    required this.packId,
    required this.version,
    required this.kind,
    required this.sizeBytes,
    required this.sha256,
    required this.payloadUrl,
    required this.generatedAt,
  });

  final int schemaVersion;
  final String packId;
  final String version;
  final String kind;
  final int sizeBytes;
  final String sha256;
  final String payloadUrl;
  final String generatedAt;

  factory ContentPackManifest.fromJson(Map<String, dynamic> json) {
    final manifest = ContentPackManifest(
      schemaVersion: (json['schemaVersion'] as num?)?.toInt() ?? 0,
      packId: json['packId']?.toString() ?? '',
      version: json['version']?.toString() ?? '',
      kind: json['kind']?.toString() ?? '',
      sizeBytes: (json['sizeBytes'] as num?)?.toInt() ?? 0,
      sha256: json['sha256']?.toString().toLowerCase() ?? '',
      payloadUrl: json['payloadUrl']?.toString() ?? '',
      generatedAt: json['generatedAt']?.toString() ?? '',
    );
    manifest.validate();
    return manifest;
  }

  void validate() {
    if (schemaVersion != 1) {
      throw const FormatException('unsupported_content_manifest_schema');
    }
    if (packId != 'world-days-catalog') {
      throw const FormatException('unexpected_content_pack_id');
    }

    final uri = Uri.tryParse(payloadUrl);
    final safeVersion = RegExp(r'^[A-Za-z0-9._-]+
  }

  Map<String, dynamic> toJson() => {
        'schemaVersion': schemaVersion,
        'packId': packId,
        'version': version,
        'kind': kind,
        'sizeBytes': sizeBytes,
        'sha256': sha256,
        'payloadUrl': payloadUrl,
        'generatedAt': generatedAt,
      };
}

final class StoredContentPack {
  const StoredContentPack({
    required this.manifest,
    required this.bytes,
  });

  final ContentPackManifest manifest;
  final List<int> bytes;
}

final class ContentPackPointer {
  const ContentPackPointer({
    required this.activeVersion,
    this.previousVersion,
  });

  final String activeVersion;
  final String? previousVersion;

  factory ContentPackPointer.fromJson(Map<String, dynamic> json) =>
      ContentPackPointer(
        activeVersion: json['activeVersion']?.toString() ?? '',
        previousVersion: json['previousVersion']?.toString(),
      );

  Map<String, dynamic> toJson() => {
        'activeVersion': activeVersion,
        'previousVersion': previousVersion,
      };
}

final class ContentPackStatus {
  const ContentPackStatus({
    required this.state,
    this.activeVersion,
    this.remoteVersion,
    this.lastError,
  });

  final ContentPackState state;
  final String? activeVersion;
  final String? remoteVersion;
  final String? lastError;
}
).hasMatch(version);
    final safeSha = RegExp(r'^[0-9a-f]{64}
  }

  Map<String, dynamic> toJson() => {
        'schemaVersion': schemaVersion,
        'packId': packId,
        'version': version,
        'kind': kind,
        'sizeBytes': sizeBytes,
        'sha256': sha256,
        'payloadUrl': payloadUrl,
        'generatedAt': generatedAt,
      };
}

final class StoredContentPack {
  const StoredContentPack({
    required this.manifest,
    required this.bytes,
  });

  final ContentPackManifest manifest;
  final List<int> bytes;
}

final class ContentPackPointer {
  const ContentPackPointer({
    required this.activeVersion,
    this.previousVersion,
  });

  final String activeVersion;
  final String? previousVersion;

  factory ContentPackPointer.fromJson(Map<String, dynamic> json) =>
      ContentPackPointer(
        activeVersion: json['activeVersion']?.toString() ?? '',
        previousVersion: json['previousVersion']?.toString(),
      );

  Map<String, dynamic> toJson() => {
        'activeVersion': activeVersion,
        'previousVersion': previousVersion,
      };
}

final class ContentPackStatus {
  const ContentPackStatus({
    required this.state,
    this.activeVersion,
    this.remoteVersion,
    this.lastError,
  });

  final ContentPackState state;
  final String? activeVersion;
  final String? remoteVersion;
  final String? lastError;
}
).hasMatch(sha256);
    const maxPackBytes = 5 * 1024 * 1024;
    const allowedHost = 'riccardopinato.github.io';
    const allowedPathPrefix = '/World-Days/content/';

    final safePayloadUri = uri != null &&
        uri.scheme == 'https' &&
        uri.host == allowedHost &&
        uri.port == 443 &&
        uri.userInfo.isEmpty &&
        uri.query.isEmpty &&
        uri.fragment.isEmpty &&
        uri.path.startsWith(allowedPathPrefix) &&
        uri.pathSegments.isNotEmpty &&
        RegExp(r'^world-days-content-[A-Za-z0-9._-]+\.json
  }

  Map<String, dynamic> toJson() => {
        'schemaVersion': schemaVersion,
        'packId': packId,
        'version': version,
        'kind': kind,
        'sizeBytes': sizeBytes,
        'sha256': sha256,
        'payloadUrl': payloadUrl,
        'generatedAt': generatedAt,
      };
}

final class StoredContentPack {
  const StoredContentPack({
    required this.manifest,
    required this.bytes,
  });

  final ContentPackManifest manifest;
  final List<int> bytes;
}

final class ContentPackPointer {
  const ContentPackPointer({
    required this.activeVersion,
    this.previousVersion,
  });

  final String activeVersion;
  final String? previousVersion;

  factory ContentPackPointer.fromJson(Map<String, dynamic> json) =>
      ContentPackPointer(
        activeVersion: json['activeVersion']?.toString() ?? '',
        previousVersion: json['previousVersion']?.toString(),
      );

  Map<String, dynamic> toJson() => {
        'activeVersion': activeVersion,
        'previousVersion': previousVersion,
      };
}

final class ContentPackStatus {
  const ContentPackStatus({
    required this.state,
    this.activeVersion,
    this.remoteVersion,
    this.lastError,
  });

  final ContentPackState state;
  final String? activeVersion;
  final String? remoteVersion;
  final String? lastError;
}
)
            .hasMatch(uri.pathSegments.last);

    if (!safeVersion ||
        kind != 'catalog' ||
        sizeBytes <= 0 ||
        sizeBytes > maxPackBytes ||
        !safeSha ||
        !safePayloadUri) {
      throw const FormatException('invalid_content_manifest');
    }
  }

  Map<String, dynamic> toJson() => {
        'schemaVersion': schemaVersion,
        'packId': packId,
        'version': version,
        'kind': kind,
        'sizeBytes': sizeBytes,
        'sha256': sha256,
        'payloadUrl': payloadUrl,
        'generatedAt': generatedAt,
      };
}

final class StoredContentPack {
  const StoredContentPack({
    required this.manifest,
    required this.bytes,
  });

  final ContentPackManifest manifest;
  final List<int> bytes;
}

final class ContentPackPointer {
  const ContentPackPointer({
    required this.activeVersion,
    this.previousVersion,
  });

  final String activeVersion;
  final String? previousVersion;

  factory ContentPackPointer.fromJson(Map<String, dynamic> json) =>
      ContentPackPointer(
        activeVersion: json['activeVersion']?.toString() ?? '',
        previousVersion: json['previousVersion']?.toString(),
      );

  Map<String, dynamic> toJson() => {
        'activeVersion': activeVersion,
        'previousVersion': previousVersion,
      };
}

final class ContentPackStatus {
  const ContentPackStatus({
    required this.state,
    this.activeVersion,
    this.remoteVersion,
    this.lastError,
  });

  final ContentPackState state;
  final String? activeVersion;
  final String? remoteVersion;
  final String? lastError;
}
