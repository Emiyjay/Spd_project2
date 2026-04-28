[app]
title = SPD Hub Manager
package.name = spdhub
package.domain = org.spd.hub
version = 1.0

source.dir = .
source.include_exts = py,csv

requirements = python3,kivy,openssl

orientation = portrait

android.api = 31
android.minapi = 21
android.ndk = 25b

android.archs = arm64-v8a
android.permissions = INTERNET

source.exclude_dirs = tests, bin, venv, .git, __pycache__
source.exclude_exts = spec, pyc, log

[buildozer]
log_level = 2
warn_on_root = 1

p4a.branch = master
