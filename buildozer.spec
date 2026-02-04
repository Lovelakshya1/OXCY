[app]
title = OXCY
package.name = oxcy
package.domain = org.oxcy.music
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,flet,yt-dlp,requests

# Android UI Settings
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.api = 33

# Icon & Splash (Ensure these files exist in your 'assets' folder)
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/icon.png

# Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
