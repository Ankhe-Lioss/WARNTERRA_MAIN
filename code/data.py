entity_stats = {
#   "enemy_name" : (hp, atk, def, spd, hp_multiplier, atk_multiplier, def_multiplier, atk_range, keep_range)
    "Player" : (500 , 125, 15, 400, 75 , 25  , 2.5, 0   , 0  ),
    "Poro"   : (250 , 50 , 10, 450, 75 , 25  , 3  , 20  , 10 ),
    "Meele"  : (500 , 45 , 10, 300, 65 , 30  , 1.5, 50  , 10 ),
    "Karthus": (250 , 75 , 10, 200, 25 , 75  , 1  , 650 , 400),
    "Chogath": (700 , 40 , 15, 200, 150, 20  , 2  , 200 , 100),
    "Veigar" : (12600,80 , 25, 250, 792, 80  , 5  , 1000, 550),
    "Lulu"   : (300 , 20 ,  5, 250, 60 , 10  , 0.5, 750 , 600),
    "Nocturne":(400 , 80 , 20,   0, 40 , 30  , 2  , 5000, 900),
    "Maokai" : (800 , 30 , 20, 100, 95 , 11  , 3  , 200 , 100),
    "Soraka" : (14000,100, 25, 300, 777, 45  , 4.5, 1000, 625)
} 

skill_stats = {
#   "Skill" : (cooldown, warmup, cast_time)
#player
    "Gauntlet_primary" : (1000, 0, 0),
    "Gauntlet_secondary" : (4900, 0, 100),
    "Gauntlet_q_skill" : (4500, 0, 0),
    "Gauntlet_e_skill" : (11250, 10000, 750),
    
    "Bow_primary" : (1000, 500, 0),
    "Bow_primary_enhanced": (450, 500, 150),
    "Bow_secondary": (6500, 5000, 3500),
    "Bow_q_skill": (3800, 1000, 200),
    "Bow_e_skill": (12000, 6000, 300),
    
    "Bazooka_primary" : (1000, 500, 0),
    "Bazooka_primary_enhanced" : (1000, 500, 0),
    "Bazooka_secondary" : (10000, 2000, 5000),
    "Bazooka_q_skill" : (3500, 1000, 0),
    "Bazooka_e_skill" : (12000, 4000, 0),
    
    "Calibrum_primary" : (1000, 0, 0),
    "Infernum_primary" : (1000, 0, 0),
    "Calibrum_skill" : (6000, 0, 500),
    "Infernum_skill" : (8300, 0, 200),
    "Lunar_swap" : (1000, 500, 500),
    "Lunar_ult" : (19500, 5000, 500),
    
#enemy
    "Poro_stomp" : (1500, 0, 1000),
    "Chogath_stomp" : (2500, 1000, 750),
    "Karthus_primary" : (1000, 1000, 500),
    "Lulu_primary" : (4000, 1000, 1000),
    "Lulu_buff" : (9000, 3000, 1000),
    "Nocturne_sprint" : (3000, 2000, 500),
    "Maokai_primary" : (4000, 0, 1000),
# Veigar
    "Veigar_primary" : (1800, 0, 200),
    "Veigar_secondary" : (3800, 3000, 200),
    
    "Veigar_ult" : (29500, 0, 500),
    "Veigar_aoe" : (0, 0, 500),
    "Veigar_cage" : (10000, 0, 5000),
# Soraka
    "Soraka_heal" : (2000, 1000, 1000),
    "Soraka_primary" : (500, 0, 1000),
    "Soraka_cc" : (5000, 3000, 1000),
    "Soraka_ult" : (5000, 2000, 1000),
# Other
    "Summon_healing_buff" : (20000, 0, 0),
    "Summon_speed_buff" : (20000, 0, 0),
    "Summon_attack_buff" : (20000, 0, 0)
}

player_projectiles = {
#   "proj" : (atk_scale_multification, speed)
    "Gauntlet_primary" : (1.5, 1200),
    "Gauntlet_q_skill" : (2.5, 1000),
    "Gauntlet_e_skill" : (2.5, 700),
    
    "Bow_primary" : (1.2, 1000),
    "Bow_primary_enhanced": (0.75, 800),
    "Bow_q_skill": (0.65, 700),
    "Bow_e_skill": (1, 600),
    
    "Bazooka_primary" : (1.2, 900),
    "Bazooka_primary_enhanced" : (0, 850),
    "Bazooka_q_skill" : (0, 800),
    "Bazooka_e_skill" : (0, 600),
    
    "Calibrum_primary" : (1.2, 1200),
    "Infernum_primary" : (0.6, 900),
    "Calibrum_skill" : (3, 700),
    "Infernum_skill" : (0.5, 1500),
    "Infernum_ray" : (0.25, 800),
    "Lunar_ult" : (0, 700)
}

enemy_projectiles = {
#   "proj" : (atk_scale_multification, speed)
    "Karthus_Primary" : (0.5, 750),
    "Lulu_Primary" : (0.5, 600),
    "Maokai_Primary" : (1, 800),
# Veigar
    "Veigar_Primary" : (0.6, 750),
    "Veigar_Secondary" : (0.5, 500),
    "Veigar_Ult" : (0, 700),
# Other
    "Healing_Buff" : (0, 0),
    "Speed_Buff" : (0, 0),
    "Attack_Buff" : (0, 0)
}

aoe_stat={
#   aoe skill=[scale_atk, frame_number, life_time]
    'Poro_Stomp':(0.5, 3, 1000),
    'Chogath_Rupture':(2, 5, 1000),
    'Veigar_Darkmatter':(1, 9, 200),
    'Soraka_star': (0.5, 4, 400),
# Player

    'Bow_explosion' : (1, 8, 500),
    'Bazooka_pe' : (0.8, 4, 200),
    'Bazooka_q' : (1.5, 4, 200),
    'Bazooka_e' : (1, 4, 200),
    'Calibrum_ult' : (3, 12, 600),
    'Infernum_ult' : (1.5, 12, 600),

# Environment
    'Barrel_Explode' : (1, 4, 500)
}

apply_scale = {
    'Bazooka_e' : 0.66, # Burning dps scale
    'Barrel_Explode' : (0.1, 0.01), # Normal, boss, scale by max hp 
    'Calibrum_mark' : 0.3          # Bonus dmg when break the mark
}