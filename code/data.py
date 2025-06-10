entity_stats = {
#   "enemy_name" : (hp, atk, def, spd, hp_multiplier, atk_multiplier, def_multiplier, atk_range)
    "Player" : (500, 100, 10, 400, 50 , 20  , 5  , 0  ),
    "Poro"   : (300, 50 , 10, 350, 75 , 10  , 2  , 100),
    "Meele"  : (500, 45 , 10, 300, 65 , 12.5, 2.5, 50 ),
    "Karthus": (400, 75 , 10, 300, 25 , 25  , 2  , 500),
    "Chogath": (950, 20 , 20, 200, 150, 10  , 5  , 200)
}

skill_stats = {
#   "Skill" : (cooldown, warmup, cast_time)
#player
    "Gauntlet_primary" : (1000, 0, 0),
    "Gauntlet_secondary" : (2000, 0, 100),
    "Gauntlet_q_skill" : (5000, 0, 200),
    "Gauntlet_e_skill" : (15000, 10000, 750),
#enemy
    "Poro_stomp" : (1000, 0, 750),
    "Chogath_stomp" : (2500, 1000, 750),
    "Karthus_primary" : (500, 1000, 200)
}

player_projectiles = {
#   "proj" : (atk_scale_multification, speed)
    "Gauntlet_primary" : (1, 1000),
    "Gauntlet_q_skill" : (3, 1000),
    "Gauntlet_e_skill" : (3, 700)
}

enemy_projectiles = {
#   "proj" : (atk_scale_multification, speed)
    "Karthus_Primary" : (0.2, 750),
}