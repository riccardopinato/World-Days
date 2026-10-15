# AdMob / UMP production setup — World Days

Status: **ANDROID BANNER + UMP PRODUCTION PHYSICALLY VERIFIED — 2026-10-15**

World Days now has two deliberately separate advertising lanes.

## QA / manual testing

The normal development APK uses:
- Google sample AdMob App IDs;
- Google sample adaptive banner IDs;
- UMP client integration;
- no production ad traffic.

This is the only lane to use for ordinary manual testing.

## Production Android lane

Workflow:
- **Production Android Release**
- trigger: manual `workflow_dispatch`;
- output: signed ARM64 APK + AAB + signer/hash evidence.

Required GitHub Actions repository secrets:
- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_KEYSTORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`
- `ADMOB_ANDROID_APP_ID`
- `ADMOB_ANDROID_BANNER_ID`

The workflow fails closed when:
- a required value is missing;
- an AdMob ID is malformed;
- a Google sample/test ID is used in the production lane;
- the resulting APK signer differs from the permanent World Days certificate.

## Public privacy policy

Canonical production URL:

`https://riccardopinato.github.io/World-Days/privacy.html`

The page is part of the GitHub Pages artifact generated from `web/privacy.html`.
Keep the policy aligned with the production app whenever data practices, SDKs or backend behavior change.

## AdMob console / UMP server-side gate

The APK integration alone is not enough for production monetization.

Completed on 2026-10-15:
1. World Days registered in AdMob;
2. production Android banner ad unit configured;
3. European regulations/UMP message published for World Days;
4. canonical Privacy Policy URL configured;
5. clean-state consent form verified on a physical Android device;
6. deny-consent flow verified;
7. Privacy Choices/revocation entry point verified;
8. production banner serving verified.

Remaining pre-store item: configure/verify app-ads.txt when the final release channel and developer website identity are fixed.

## Banner placement

The free banner is a **large anchored adaptive banner at the top of the application shell**.

It has a dedicated layout slot:
- no overlay on content;
- no overlap with the bottom navigation;
- no ad request on Web Preview;
- no request until UMP says ads may be requested.

## Release truth

- QA banner visible with Google test traffic != production monetization verified.
- Production APK signed correctly != UMP console configured.
- Ad request eligible != ad loaded.
- Ad loaded != physical impression verified.

The Android banner + UMP block is physically verified on the exact production lane. Full monetization is still incomplete until the lifetime Remove Ads entitlement and its no-request behavior pass sandbox and physical QA.
