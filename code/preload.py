from setting import *


def preload_all_image(game):
    #game asset
    game.cursor_image = pygame.image.load(os.path.join('images', 'UI', 'cursor.png')).convert_alpha()
    game.check_in_image=pygame.image.load(os.path.join('images','enviroment','check_in','0.png'))
    game.icon = pygame.image.load(os.path.join('images', 'UI', 'icon.png')).convert_alpha()
    game.skill_bar = pygame.image.load(os.path.join('images', 'UI', 'skill_bar', 'skill_bar.png')).convert_alpha()

    #enemies
    enemy_frames = {}
    enemies_folder=os.path.join('images','enemies')
    for enemy_name in os.listdir(enemies_folder):
        enemy_path = os.path.join(enemies_folder, enemy_name)
        if not os.path.isdir(enemy_path):
            continue
        enemy_frames[enemy_name] = {}
        for dirpath, dirnames, filenames in os.walk(enemy_path):
            state = os.path.basename(dirpath)
            frame_files = [f for f in sorted(filenames) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not frame_files:
                continue
            enemy_frames[enemy_name][state] = []
            for filename in frame_files:
                full_path = os.path.join(dirpath, filename)
                surf = pygame.image.load(full_path).convert_alpha()
                enemy_frames[enemy_name][state].append(surf)
    game.enemy_frames=enemy_frames

    #projectiles
    base_path = os.path.join('images', 'projectiles')
    projectile_frames={}
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if not os.path.isdir(folder_path):
            continue
        projectile_frames[folder] = {}
        for subfolder in os.listdir(folder_path):
            subfolder_path = os.path.join(folder_path, subfolder)
            if not os.path.isdir(subfolder_path):
                continue
            frames = []
            for i in range(4):  # Assuming 4 frames per projectile
                img_path = os.path.join(subfolder_path, f'{i}.png')
                if os.path.exists(img_path):
                    surf = pygame.image.load(img_path).convert_alpha()
                    frames.append(surf)
            if frames:
                projectile_frames[folder][subfolder] = frames
    game.projectile_frames=projectile_frames
    spawn_frames = []
    spawn_folder = os.path.join('images', 'enviroment', 'enemy_spawn_animation')
    for i in range(15):  # Assuming 15 frames as in your spawn.py
        img_path = os.path.join(spawn_folder, f'{i}.png')
        if os.path.exists(img_path):
            surf = pygame.image.load(img_path).convert_alpha()
            spawn_frames.append(surf)
    game.spawn_frames = spawn_frames

    #status
    status_frames = {}
    status_folder = os.path.join('images', 'status')
    if os.path.exists(status_folder):
        for status_name in os.listdir(status_folder):
            status_path = os.path.join(status_folder, status_name)
            if not os.path.isdir(status_path):
                continue
            frames = []
            for i in range(5):  # Assuming 5 frames per status
                img_path = os.path.join(status_path, f'{i}.png')
                if os.path.exists(img_path):
                    surf = pygame.image.load(img_path).convert_alpha()
                    frames.append(surf)
            if frames:
                status_frames[status_name] = frames
    game.status_frames = status_frames

    # Preload status icons
    status_icons = {}
    icons_folder = os.path.join('images', 'icons', 'status')
    if os.path.exists(icons_folder):
        # Buff types
        buff_folder = os.path.join(icons_folder, 'Buff')
        if os.path.exists(buff_folder):
            for icon_file in os.listdir(buff_folder):
                if icon_file.lower().endswith('.png'):
                    icon_path = os.path.join(buff_folder, icon_file)
                    icon_name = os.path.splitext(icon_file)[0]
                    surf = pygame.image.load(icon_path).convert_alpha()
                    status_icons[icon_name] = pygame.transform.scale(surf, (24, 24))
        # Other status icons
        for icon_file in os.listdir(icons_folder):
            icon_path = os.path.join(icons_folder, icon_file)
            if icon_file.lower().endswith('.png') and os.path.isfile(icon_path):
                icon_name = os.path.splitext(icon_file)[0]
                surf = pygame.image.load(icon_path).convert_alpha()
                status_icons[icon_name] = pygame.transform.scale(surf, (24, 24))
    game.status_icons = status_icons

    #hp bar
    game.bar_bg = pygame.image.load(os.path.join('images', 'UI', 'health_bar', '0.png')).convert_alpha()
    game.bar_empty = pygame.image.load(os.path.join('images', 'UI', 'health_bar', '3.png')).convert_alpha()
    game.bar_full = pygame.image.load(os.path.join('images', 'UI', 'health_bar', '5.png')).convert_alpha()

    #AOE
    aoe_frames = {}
    aoe_folder = os.path.join('images', 'aoe')
    if os.path.exists(aoe_folder):
        for aoe_name in os.listdir(aoe_folder):
            aoe_path = os.path.join(aoe_folder, aoe_name)
            if not os.path.isdir(aoe_path):
                continue
            frames = []
            for i in range(30):  # Adjust max frame count as needed
                img_path = os.path.join(aoe_path, f'{i}.png')
                if os.path.exists(img_path):
                    surf = pygame.image.load(img_path).convert_alpha()
                    frames.append(surf)
            if frames:
                aoe_frames[aoe_name] = frames
    game.aoe_frames = aoe_frames

    # AOE warning
    aoe_warning_frames = {}
    warning_folder = os.path.join('images', 'enviroment')
    if os.path.exists(warning_folder):
        for warning_name in ['Spawn_rupture', 'Spawn_darkmatter', 'Spawn_Soraka_star', 'Spawn_Soraka_cc']:
            warning_path = os.path.join(warning_folder, warning_name)
            if not os.path.isdir(warning_path):
                continue
            frames = []
            for i in range(20):  # Adjust max frame count as needed
                img_path = os.path.join(warning_path, f'{i}.png')
                if os.path.exists(img_path):
                    surf = pygame.image.load(img_path).convert_alpha()
                    frames.append(surf)
            if frames:
                aoe_warning_frames[warning_name] = frames
    game.aoe_warning_frames = aoe_warning_frames