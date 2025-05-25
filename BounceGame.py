from Bubble import *
from random import randint

class BounceGameDragon:
    def __init__(self):
        self._arena = Arena((512, 424))
        arena = self._arena
        self._imageWmap, self._imageHmap = 512,424
        self._drag = Dragon(arena,(50,420),0) #50,420
        self._drag2 = Dragon(arena,(450,420),1) #450,420
        self._level = 1
        self.level()
        
    def removeItems(self):
        for a in self._arena.actors():
            if not isinstance(a, Dragon):
                self._arena.remove(a)
            
                          
    def level(self):
        arena = self._arena
        if(self._level == 1):
            self._Wmap, self._Hmap = 0,0
            pltf1 = [(Platform(arena, (32, 320),(32,16))),(Platform(arena, (112, 320),(288,16))),
                     (Platform(arena, (448, 320),(32,16))),(Platform(arena, (32, 240),(32,16))),
                     (Platform(arena, (112, 240),(288,16))),(Platform(arena, (448, 240),(32,16))),
                     (Platform(arena, (32, 160),(32,16))),(Platform(arena, (112, 160),(288,16))),
                     (Platform(arena, (448, 160),(32,16)))]
            orange = [(Orange(arena,(150,306))),(Orange(arena,(250,306))),(Orange(arena,(350,306))),
                      (Orange(arena,(460,306))),(Orange(arena,(50,306))),(Orange(arena,(350,226))),
                      (Orange(arena,(450,226))),(Orange(arena,(200,226))),(Orange(arena,(170,226))),
                      (Orange(arena,(35,146))),(Orange(arena,(450,146))),(Orange(arena,(189,146)))]
            for i in range(0,4):
                r = randint(0+31,512-31)
                Enemy(arena,(r,80)) #r,80

            
        elif(self._level == 2):
            self.removeItems()
            self._drag.spown()
            self._drag2.spown()
            self._Wmap, self._Hmap = 512,0

            pltf2 = [(Platform(arena, (207, 80),(97,16))),(Platform(arena, (272, 160),(80,16))),
                     (Platform(arena, (160, 160),(80,16))),(Platform(arena, (112, 240),(288,16))),
                     (Platform(arena, (64, 320),(112,16))),(Platform(arena, (208, 320),(112,16))),
                     (Platform(arena, (336, 320),(112,16)))]
            orange = [(Orange(arena,(258,66))),(Orange(arena,(300,146))),(Orange(arena,(198,146))),
                      (Orange(arena,(130,226))),(Orange(arena,(220,226))),(Orange(arena,(290,226))),
                      (Orange(arena,(350,226))),(Orange(arena,(89,306))),(Orange(arena,(230,306))),
                      (Orange(arena,(360,306)))]
            for i in range(0,4):
                r = randint(0+31,512-31)
                Enemy(self._arena,(r,80)) #r,80
        elif(self._level == 3):
            self.removeItems()
            self._drag.spown()
            self._drag2.spown()
            self._Wmap, self._Hmap = 0,3816
            
            
    def returnMap(self):
        return  self._Wmap, self._Hmap , self._imageWmap, self._imageHmap
    
    def arena(self) -> Arena:
        return self._arena

    def dragon(self) -> Dragon:
        return self._drag
    
    def dragon2(self) -> Dragon:
        return self._drag2

    def game_Lose(self) -> bool:
        for a in self._arena.actors():
            if isinstance(a, Dragon):
                return False
        return True
        
    def game_Win(self)-> bool:
        for a in self._arena.actors():
            if isinstance(a, Enemy):
                return False
        if (self._level < 3):
            self._level += 1
            self.level()
            return False
        if (self._level == 3):
            return True
    
    def game_score_dragon(self) -> str:
        return str(self._drag.Score(0))

    def game_score_dragon2(self):
        return str(self._drag2.Score(0))
        

