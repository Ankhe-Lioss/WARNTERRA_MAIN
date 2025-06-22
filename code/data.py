entity_stats = {
#   "enemy_name" : (hp, atk, def, spd, hp_multiplier, atk_multiplier, def_multiplier, atk_range, keep_range)
    "Player" : (500 , 125, 15, 400, 75 , 25  , 2.5, 0   , 0  ),
    "Poro"   : (250 , 50 , 10, 450, 75 , 25  , 3  , 20  , 10 ),
    "Meele"  : (500 , 45 , 10, 300, 65 , 30  , 1.5, 50  , 10 ),
    "Karthus": (250 , 75 , 10, 200, 25 , 75  , 1  , 650 , 400),
    "Chogath": (700 , 40 , 15, 200, 150, 20  , 2  , 200 , 100),
    "Veigar" : (8000, 80 , 20, 250, 400, 40  , 5  , 1000, 550),
    "Lulu"   : (300 , 20 ,  5, 250, 60 , 10  , 0.5, 750 , 600),
    "Nocturne":(450 , 60 , 20,   0, 50 , 30  , 2  , 1000, 900)
}

skill_stats = {
#   "Skill" : (cooldown, warmup, cast_time)
#player
    "Gauntlet_primary" : (1000, 0, 0),
    "Gauntlet_secondary" : (2000, 0, 100),
    "Gauntlet_q_skill" : (4800, 0, 200),
    "Gauntlet_e_skill" : (19250, 10000, 750),
    
    "Bow_primary" : (1000, 1000, 0),
    "Bow_primary_enhanced": (450, 500, 150),
    "Bow_secondary": (6500, 5000, 3500),
    "Bow_q_skill": (3800, 1000, 200),
    "Bow_e_skill": (16000, 5000, 300),
#enemy
    "Poro_stomp" : (1500, 0, 1000),
    "Chogath_stomp" : (2500, 1000, 750),
    "Karthus_primary" : (1000, 1000, 500),
    "Lulu_primary" : (4000, 1000, 1000),
    "Lulu_buff" : (9000, 3000, 1000),
# Veigar
    "Veigar_primary" : (1800, 0, 200),
    "Veigar_secondary" : (3800, 3000, 200),
    
    "Veigar_ult" : (29500, 0, 500),
    "Veigar_aoe" : (0, 0, 500),
    "Veigar_cage" : (10000, 0, 5000)
}

player_projectiles = {
#   "proj" : (atk_scale_multification, speed)
    "Gauntlet_primary" : (1, 1000),
    "Gauntlet_q_skill" : (3, 1000),
    "Gauntlet_e_skill" : (2, 700),
    
    "Bow_primary" : (1, 1000),
    "Bow_primary_enhanced": (0.5, 800),
    "Bow_q_skill": (0.5, 700),
    "Bow_e_skill": (0, 600)
}

enemy_projectiles = {
#   "proj" : (atk_scale_multification, speed)
    "Karthus_Primary" : (0.5, 750),
    "Lulu_Primary" : (0.5, 600),
# Veigar
    "Veigar_Primary" : (1, 750),
    "Veigar_Secondary" : (0.75, 500),
    "Veigar_Ult" : (0, 700)
}

Aoe_stat={
#   aoe skill=[scale_atk,frame_number,life_time]
    'Poro_Stomp':(0.5, 3, 1000),
    'Chogath_Rupture':(2, 5, 1000),
    'Veigar_Darkmatter':(2, 9, 1000)
}