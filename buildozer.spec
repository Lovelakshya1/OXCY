[app]
title = OXCY
package.name = oxcy
package.domain = org.oxcy.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# ADDED: yt-dlp, ffmpeg-python, and sqlite3 (critical for phones)
requirements = python3,flet,requests,urllib3,openssl,libffi,yt-dlp,ffmpeg-python,sqlite3

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/icon.png

# ADDED: WAKE_LOCK to keep music playing when screen is off
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,WAKE_LOCK
