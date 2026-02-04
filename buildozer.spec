[app]
title = OXCY
package.name = oxcy
package.domain = org.operator
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# PATHS TO YOUR ASSETS
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/icon.png

# UPDATED REQUIREMENTS FOR API AND LOGIC
requirements = python3,flet,yt-dlp,google-api-python-client,requests,certifi,urllib3

orientation = portrait
android.archs = arm64-v8a
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# Android API levels
android.api = 33
android.minapi = 21
android.sdk = 33
