# Android signing identity — World Days

Status: **USER-ACTION GATE / NOT YET PRODUCTION VERIFIED**

## Stable product identity

- Application ID: `com.riccardopinato.world_days`
- Stable release alias: `world-days-release`
- Expected certificate SHA-256:
  `B4:6C:A3:08:1B:6B:51:2F:F9:4F:31:0B:0C:CE:27:14:B4:43:E4:65:A2:1F:48:47:C4:01:62:72:DF:80:BD:D3`

The private keystore and passwords are intentionally not committed.

## Why one final reinstall is required

The first distributed internal APK and the Step 9 APK were produced by ephemeral CI/debug signing identities. Their signer certificate SHA-256 values differ:

- first internal APK: `881BBCBCB68D7298A2DC1FC139C0351B3101C0470B5E031049269C9B92BFFAC1`
- Step 9 internal APK: `86A5AD68122D12643A270A6C85713ED47DA7DFAFDF3B2D324D948BAF976526FD`

Android will not accept an APK signed by the new permanent identity as an in-place update over an APK signed by either old identity. The transition to the first permanently signed APK therefore requires one uninstall/reinstall.

After that transition, every direct APK signed with the permanent identity and a higher versionCode can update the installed app in place without clearing application data.

## Required GitHub Actions secrets

Add these repository secrets before running **Signed Android QA**:

- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_KEYSTORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

The workflow reconstructs the keystore only at runtime, verifies the resulting APK certificate against the expected fingerprint, hashes the artifacts, and never uploads the keystore.

## Evidence gate

Production signing is **not verified** until a real Signed Android QA workflow run passes certificate verification. After the first stable APK is installed, perform an N → N+1 in-place update test using the same workflow identity.
