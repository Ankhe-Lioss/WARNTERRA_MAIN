[app]
title = Warnterra
package.name = warnterra
package.domain = org.yourdomain
source.dir = .
source.include_exts = py,png,jpg,jpeg,ogg,wav,tmx,zip,txt
source.include_patterns = Code/*,audio/*,Images/*,data/*
source.main = Code/main.py

version = 0.1

# ✅ Python modules needed
requirements = python3, pygame-ce, pytmx

orientation = landscape

# Uncomment and provide files if needed
# presplash.filename = Images/UI/presplash.png
# icon.filename = Images/UI/icon.png

# ✅ Required permissions for storage
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# ✅ Use common 32-bit & 64-bit ARM architectures
android.arch = armeabi-v7a, arm64-v8a
android.minapi = 21
android.ndk_api = 21

fullscreen = 1
android.hide_statusbar = 1

# ✅ SDL2 entrypoint is required for pygame-ce
android.entrypoint = org.libsdl.app.SDLActivity

# Logging level: 2 = info
log_level = 2

# Clean packaging (remove test or cache folders)
exclude_patterns = tests/*,__pycache__/*

# ✅ Required for pygame-ce
android.bootstrap = pygame

# If using zipped assets or fonts/data, use:
# android.add_assets = data/,Images/,audio/

# You can add a theme (optional)
# android.theme = '@android:style/Theme.NoTitleBar'

# Optional: environment variables
# environment = 

# Optional: logcat filters
# android.logcat_filters = *:S python:D

# Optional: if you have .so libraries
# android.add_libs_armeabi =

# Optional: keep app in portrait or allow both
# orientation = sensorLandscape

# End of file
