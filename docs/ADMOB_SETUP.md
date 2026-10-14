# AdMob / UMP production setup — World Days

Status: **CLIENT IMPLEMENTED / PRODUCTION CONFIG USER-ACTION GATE**

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

## AdMob console / UMP server-side gate

The APK integration alone is not enough for production monetization.

Before distributing the production build:
1. create/register World Days in AdMob;
2. create the Android banner ad unit;
3. configure and publish the European regulations/UMP message for World Days;
4. provide a real public privacy-policy URL;
5. configure the required languages and consent choices;
6. verify Privacy Options/revocation on a physical device when UMP requires the entry point;
7. configure/verify app-ads.txt when required for the release channel.

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

Production monetization remains **NOT CERTIFIED** until the exact signed production artifact is tested on-device with the real AdMob configuration.
