[app]
title = Warnterra
package.name = warnterra
package.domain = org.yourdomain
source.dir = .
source.include_exts = py,png,jpg,jpeg,ogg,wav,tmx,zip,txt
source.include_patterns = Code/*,audio/*,Images/*,data/*

# If your main file is in Code/main.py, set this:
source.main = Code/main.py

# Versioning
version = 0.1

# Requirements (external Python modules)
requirements = python3, pygame-ce, pytmx

# Orientation
orientation = landscape

# Presplash and Icon (optional)
# presplash.filename = Images/UI/presplash.png
# icon.filename = Images/UI/icon.png

# Permissions (add if you need file or internet access)
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android specific
android.arch = armeabi-v7a, arm64-v8a
android.minapi = 21
android.ndk_api = 21

# (Optional) Fullscreen
fullscreen = 1

# (Optional) Hide status bar
android.hide_statusbar = 1

# (Optional) If you want to use SDL2 (recommended for pygame-ce)
android.entrypoint = org.libsdl.app.SDLActivity

# (Optional) If you want to keep logs
log_level = 2

# (Optional) Exclude test files
exclude_patterns = tests/*,__pycache__/*

# (Optional) Add extra Java .jar files (if needed)
# android.add_jars =

# (Optional) Add extra .so files (if needed)
# android.add_libs_armeabi =

# (Optional) Add extra assets (if needed)
# android.add_assets =

# (Optional) Set the app theme
# android.theme = '@android:style/Theme.NoTitleBar'

# (Optional) Set the entry point if not main.py
# entrypoint = Code/main.py

# (Optional) Set the logcat filters
# android.logcat_filters = *:S python:D

# (Optional) Set the bootstrap (pygame for pygame-ce)
android.bootstrap = pygame

# (Optional) Add environment variables
# environment =

# (Optional) Add extra requirements (comma separated)
# requirements = python3, pygame-ce, pytmx

# (Optional) Add any other settings you need

# End of file