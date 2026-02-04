[app]
title = OXCY
package.name = oxcy
package.domain = org.oxcy.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# Critical: 'openssl' and 'libffi' are added to prevent compilation errors
requirements = python3,flet,requests,urllib3,openssl,libffi

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/icon.png

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
