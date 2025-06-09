entity_stats = {
#   "enemy_name" : (hp, atk, def, spd, hp_multiplier, atk_multiplier, def_multiplier)
    "Player" : (500, 100, 10, 500, 50, 20, 5),
    "Poro"   : (300, 50 , 10, 250, 75, 10, 2)
}

weapon_skills = {
#   "weap" : (MOUSE_L, MOUSE_R, Q, E)
    "Gauntlet" : ("Gautlet_Primary", "Gautlet_Secondary", "Gauntlet_Q", "Gauntlet_E")
}

skill_stats = {
#   "Skill" : (cooldown, warmup, cast_time)
    "Gauntlet_primary" : (1000, 0, 0),
    "Gauntlet_secondary" : (2000, 0, 100),
    "Gauntlet_q_skill" : (5000, 0, 200),
    "Gauntlet_e_skill" : (15000, 10000, 750)
}

player_projectiles = {
#   "proj" : (atk_scale_multification, speed)
    "Gauntlet_primary" : (1, 1000),
    "Gauntlet_q_skill" : (3, 1000),
    "Gauntlet_e_skill" : (5, 750)
}