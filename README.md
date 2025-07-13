# Warnterra

Warnterra is a top-down action RPG built with [pygame-ce](https://github.com/pygame-community/pygame-ce).  
You control a hero, collect and swap weapons, fight animated enemies, use skills, and interact with a dynamic world.

---

## Features

- Multiple weapons with skill bars and swapping (Tab, with cooldown)
- Animated enemies, projectiles, area effects, and items
- Item pickups with special effects (press **R** to collect)
- Floating/bobbing item effects
- Preloaded assets for fast performance
- Tiled map support (with pytmx)
- Modular codebase (entities, projectiles, items, UI, etc.)

---

## Controls

- **WASD / Arrow keys**: Move
- **Mouse**: Aim/attack
- **Tab**: Swap weapon (5s cooldown)
- **R**: Pick up item when near
- **F1-F4**: Debug/cheat keys
- **ESC**: Pause

---

## Requirements

- Python 3.8+
- pygame-ce
- pytmx

Install dependencies:
```sh
pip install pygame-ce pytmx
```

---

## How to Run

1. Clone or download this repository.
2. Place all assets (images, audio, maps) in the correct folders as referenced in the code.
3. Run the game:
    ```sh
    python code/main.py
    ```

---

## Folder Structure

```
code/
  main.py
  entity.py
  player.py
  enemies.py
  projectiles.py
  items.py
  ...
images/
  enemies/
  projectiles/
  items/
  UI/
  ...
audio/
  ...
data/
  maps/
  tilesets/
  ...
```

---

## Asset Preloading

All images and sounds are preloaded at startup for performance.  
If you add new weapons, enemies, or items, place their images in the appropriate folders.

---

## Customization

- Add new weapons by subclassing `Weap` and adding to `Weapon_Dict`.
- Add new enemies by subclassing `Enemy` and adding to `enemy_classes`.
- Add new items by subclassing `Item` or `Weapon_Item`.

---

## Credits

- [pygame-ce](https://github.com/pygame-community/pygame-ce)
- [pytmx](https://github.com/bitcraft/pytmx)
- All asset authors (see images/audio folders for attributions)

---

Enjoy playing and modding Warnterra!
