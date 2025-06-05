class Skill:
    def __init__(self, cooldown, weap):
        self.weap = weap
        self.ready = True
        self.pre = 0
        self.cooldown = cooldown

class Shoot(Skill):
    pass