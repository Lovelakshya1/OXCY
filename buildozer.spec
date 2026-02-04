[app]
title = OXCY
package.name = oxcy
package.domain = org.oxcy.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,flet,yt-dlp,requests,ffmpeg-python

# Android specific
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a

# This packs FFmpeg into the APK!
android.add_jars = assets/ffmpeg-android-arm64.jar
