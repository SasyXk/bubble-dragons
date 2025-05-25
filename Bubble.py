import g2d
from random import randint , choice
from actor import Actor, Arena

class FireBall(Actor):
    def __init__(self, arena, pos,a,color):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._wimage, self._himage = 1198, 1050
        self._dx = 7 * a #"a", decides the direction (1,-1)
        self._dy = -1
        self._color = color
        self._arena = arena
        self._bordmappa = 31
        self._bordmappaylow = 7

        #image
        self._image = 0
        self._count = 0
        self._goUp = 0
        self._goDown = 0
        arena.add(self)
        
    def directionImage(self):
        
        # FireBall launch
        if(self._image == 0): 
            if(self._dx > 0):
                if(self._count < 3):
                    self._wimage, self._himage = 1270, 1050
                elif(3<=self._count < 6):
                    self._wimage, self._himage = 1252, 1050
                elif(6 <= self._count):
                    self._wimage, self._himage = 1234, 1050
                self._count += 1
                
            elif(self._dx < 0):
                if(self._count < 5):
                    self._wimage, self._himage = 6, 1050
                elif(5 <=self._count < 10):
                    self._wimage, self._himage = 23, 1050
                elif(10 <= self._count):
                    self._wimage, self._himage = 41, 1050
                self._count += 1

        # FireBall Floating in the air
        elif(self._image == 1): 
            if(self._count < 20):
                self._wimage, self._himage = 6, 1072
            elif( 20 <=self._count < 39):
                self._wimage, self._himage = 25, 1072
            else:
                self._count = -1
            self._count += 1

        # FireBall explosion
        if(self._image == 2): 
            if(self._count < 5):
                self._wimage, self._himage = 590, 1050
            elif( 5 <=self._count < 10):
                self._wimage, self._himage = 614, 1050
            elif( 10 <=self._count < 15):
                self._wimage, self._himage = 590, 1050
            elif( 15 <=self._count < 20):
                self._wimage, self._himage = 614, 1050
            else:
                self._arena.remove(self)
            self._count += 1
            
    def move(self):
        self.directionImage()
        arena_w, arena_h = self._arena.size()

         # Distance traveled horizontally
        if(self._goUp < 20):
            self._x += self._dx
            if self._x < self._bordmappa:
                self._x = self._bordmappa
                self._goUp = 100
            elif self._x > arena_w - self._w - self._bordmappa:
                self._x  = arena_w - self._w - self._bordmappa
                self._goUp = 100
            self._goUp += 1

        # Ascent/descent
        else: 
            if(self._image != 2):
                self._image = 1
                self._y += self._dy
                if self._y < self._bordmappa:
                    self._y = self._bordmappa
                    self._dy = -self._dy
                    self._goDown = 1
                if(self._goDown == 30):
                    self._goDown = 0
                    self._dy = -self._dy
                elif(self._goDown >= 1):
                    self._goDown += 1
    # Dragon Blast
    def collide(self, other):
        if isinstance(other, Dragon) and self._image == 1: 
            self._image = 2
            self._count = 0
            scr = 10
            other.Score(scr)
            Points(self._arena,(self._x,self._y),scr,other.ReturnColor())
            
        # platform collision
        if isinstance(other, Platform) and self._image == 0: 
            x1, y1, w1, h1 = self.position()
            x2, y2, w2, h2 = other.position() 
            border1,border2 = x2, x2+w2

            # If it is inside the platform it explodes,
            # otherwise it changes state and rises upwards 
            if(border1 < x1  < border2 - w1): 
                self._goUp = 100
                self._image = 2
            else:
                self._goUp = 100
                self._image = 1

    def CollideEnemy(self):
        self._arena.remove(self)

    def returnImage(self):
        return self._image
    
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):

        # GreenBubble
        if (self._color == 1): # BlueBubble
            if self._image == 0:
                if(self._wimage > 500):
                    self._wimage -= 215
                elif self._wimage < 500:
                    self._wimage += 215
            elif self._image == 1:
                if(self._wimage > 500):
                    self._wimage -= 54
                elif self._wimage < 500:
                    self._wimage += 54
            
        w = self._wimage, self._himage, self._w, self._h
        if (self._color == 1):
            if self._image == 0:
                if(self._wimage > 500):
                    self._wimage += 215
                elif self._wimage < 500:
                    self._wimage -= 215
            elif self._image == 1:
                if(self._wimage > 500):
                    self._wimage += 54
                elif self._wimage < 500:
                    self._wimage -= 54
        return w

class Enemy(Actor):
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._wimage, self._himage = 6, 246
        self._speed = 2
        self._gravity = 0.4
        self._dx, self._dy = -self._speed, 0
        self._arena = arena
        self._salta = 1
        self._bordmappa = 31
        self._bordmappaylow = 7
    
        # Image
        self._image = 2
        self._count = 0
        self._timer = 0
        self._goDown = 0
        
        arena.add(self)
        
    def directionImage(self):
        # Left
        if(self._image == 2): 
            if(self._count < 7):
                self._wimage, self._himage = 6, 245
            elif(7<=self._count < 14):
                self._wimage, self._himage = 24, 245
            elif(14<=self._count < 21):
                self._wimage, self._himage = 43, 245
            elif(21<=self._count < 28):
                self._wimage, self._himage = 62, 245
            elif(self._count == 28):
                self._count = -1
            self._count += 1

        # Right
        if(self._image == 1): 
            if(self._count < 7):
                self._wimage, self._himage = 1269, 245
            elif(7<=self._count < 14):
                self._wimage, self._himage = 1251, 245
            elif(14<=self._count < 21):
                self._wimage, self._himage = 1232, 245
            elif(21<=self._count < 28):
                self._wimage, self._himage = 1212, 245
            elif(self._count == 28):
                self._count = -1
            self._count += 1

        # Death by fireBall
        if(self._image == 3): 
            if(self._count < 15):
                self._wimage, self._himage = 304, 245
            elif(15<=self._count < 30):
                self._wimage, self._himage = 322, 245
            elif(30 <= self._count < 45):
                self._wimage, self._himage = 340, 245
            elif(45 <= self._count < 60):
                self._wimage, self._himage = 322, 245
            elif(self._count == 60):
                self._count = -1
            self._count += 1

        # bubble burst
        if(self._image == 4): 
            if(self._count < 5):
                self._wimage, self._himage = 590, 1050
            elif( 5 <=self._count < 10):
                self._wimage, self._himage = 614, 1050
            elif( 10 <=self._count < 15):
                self._wimage, self._himage = 590, 1050
            elif( 15 <=self._count < 20):
                self._wimage, self._himage = 614, 1050
            else:
                self._arena.remove(self)
            self._count += 1

    # Decides the movement
    def randomd(self): 
        r = randint(0,4)
        if(r == 0):#sinistra
            self._image = 2
            self._dx = -self._speed
        elif(r == 1):#destra
            self._image = 1
            self._dx = self._speed
        elif(r >= 2): #salto
            if(self._salta == 0):
                self._dy = -4 * self._speed
                self._salta = 1
        
    def timer(self): #per accedere alla funzione randomd() ogni 70 frame
        if(self._timer == 0):
            self.randomd()
        if(self._timer == 70):
            self.randomd()
        self._timer += 1
        if(self._timer == 139):
            self._timer = 0
        
    def move(self):
        if(self._image == 3): #se Enemy è nella bolla
            if(self._goDown == 0):#Se la bolla ha finito la discesa
                self._dy = -1.5 #torna su
                self._timer = 0
            self._dx = 0
            self._gravity = 0
        elif(self._image == 4): #se la bolla è stata presa
            self._dx = 0
            self._dy = 0
            self._gravity = 0
        else:
            self.timer() #Enemy si muove
        
        self.directionImage()
        self._salta = 1
        arena_w, arena_h = self._arena.size()
        self._y += self._dy
        if self._y < self._bordmappa:
            self._y = self._bordmappa
            if(self._image == 3): #se Enemy è una bolla, toccando il bordo superiore dell mappa torna giù per un tot: "35" Frame:
                self._dy = -self._dy 
                self._goDown = 1
        if(self._image == 3):
            if(self._goDown == 75):
                self._goDown = 0
            elif(self._goDown >= 1):
                    self._goDown += 1
                    
        elif self._y > arena_h - self._h - self._bordmappa + self._bordmappaylow: 
            self._y = arena_h - self._h - self._bordmappa + self._bordmappaylow
            self._dy = 1
            self._salta = 0
            
        self._dy += self._gravity

        self._x += self._dx
        if self._x < self._bordmappa:
            self._x = self._bordmappa
            self._dx = self._speed
            self._image = 1
            self._timer = 1 
        elif self._x > arena_w - self._w - self._bordmappa:
            self._x = arena_w - self._w - self._bordmappa
            self._dx = -self._speed
            self._image = 2
            self._timer = 1
            
    def collide(self, other):
        if isinstance(other, Platform):
            x1, y1, w1, h1 = self.position()
            x2, y2, w2, h2 = other.position()
            prv_x,pvr_y = x1 - self._dx, y1 - self._dy

            if prv_x + w1 <= x2:
                self._x = x2 - w1
            elif prv_x >= x2 + w2:
                self._x = x2 + w2
            elif pvr_y + h1 <= y2:
                self._y,self._dy = y2 - h2, 3
                self._salta = 0
                
        if isinstance(other, Platform) and self._image == 3:
            self._goDown = 0
            
        if isinstance(other, FireBall):
            imag = other.returnImage()
            if(imag == 0 and self._image < 3): #Se la FireBall non è una bolla e se Enemy non è una bolla
                other.CollideEnemy()#La bolla viene tolta dall'arena
                self._image = 3 #Enemy diventa una Bolla
            
        if isinstance(other, Dragon):
            if(self._image == 3) and other.ReturnDead() != 1: #Se Enemy è una bolla, e Dragon è vivo
                self._image = 4
                self._count = 0
                scr = 350
                other.Score(scr) #aumento punteggio Dragon
                Points(self._arena,(self._x,self._y),scr,other.ReturnColor())

    def returnImage(self):
        return self._image
    
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return self._wimage, self._himage, self._w, self._h
    
class Dragon(Actor):
    def __init__(self, arena, pos,color):
        self._x, self._y = pos
        self._w, self._h = 15, 16
        self._dragonColor = color
        self._wimage, self._himage = 1270, 16
        self._speed = 2.5
        self._gravity = 0.4
        self._dx, self._dy = 0, 0
        self._arena = arena
        self._salta = 0
        self._bordmappa = 31
        self._bordmappaylow = 7
        
        #shoot
        self._shoot = 0
        
        #lives
        self._lives = 3
        self._dead = 0
        #Animazione morte
        self._rotation = 0 
        self._rotemp = 0
        self._immortalCount = 0 #Count per il Respown
        self._GravityDown = False #Non fa partire l'animazione della morte fino a quando
                                  #non collide con la Platform o con il bordomappa
        #Points
        self._points = 0
        #image
        if self._dragonColor == 0: #immagine partenza Verde
            self._image = 3
        else:
            self._image = 4 #/Blu
        self._imagej = 0
        self._count = 1
        self._imagesh = 0
        
        arena.add(self)
        
    def directionImage(self):
        if(self._imagej == 0):# movimento
            
            if(self._image == 1): #destra
                if(self._count < 7):#animazione movimento
                    self._wimage, self._himage =  1268, 16
                elif(7<=self._count < 14):
                    self._wimage, self._himage =  1205, 16
                elif(14<=self._count < 21):
                    self._wimage, self._himage =  1247, 16 
                elif(21<=self._count < 28):
                    self._wimage, self._himage =  1226, 16 
                elif(self._count == 28):
                    self._count = -1
                self._count += 1
    
            elif(self._image == 2): #sinistra
                if(self._count < 7):#animazione movimento
                    self._wimage, self._himage =  27, 16
                elif(7<=self._count < 14):
                    self._wimage, self._himage =  70, 16 
                elif(14<=self._count < 21):
                    self._wimage, self._himage =6, 16
                elif(21<=self._count < 28):
                    self._wimage, self._himage =  48, 16
                elif(self._count == 28):
                    self._count = -1
                self._count += 1
                
            elif(self._image == 3):
                self._wimage, self._himage = 1268, 16
            elif(self._image == 4):
                self._wimage, self._himage = 6, 16
                
        elif(self._imagej == 3): # salto
            if(self._image == 4 or self._image == 2): # movimento in salto sinistra
                if(self._dy < 0):
                    self._wimage, self._himage = 236, 36
                elif(self._dy > 0):
                    self._wimage, self._himage = 194, 36
            elif(self._image == 3 or self._image == 1): # movimento in salto destra
                if(self._dy < 0):
                    self._wimage, self._himage = 1037, 36
                elif(self._dy > 0):
                    self._wimage, self._himage = 1079, 36
                    
        #salto terminato        
        elif(self._image == 3 or self._image == 1):
            self._wimage, self._himage = 1268, 16
        elif(self._image == 4 or self._image == 2):
            self._wimage, self._himage = 6, 16

        if(self._imagesh == 4):#animazione Shoot
            self.imageShoot()
            
    def imageShoot(self): #Controllo animazione Shoot
        if(self._image == 4 or self._image == 2): #destra
            if(self._count1 < 3):
                self._wimage, self._himage =  150, 16
            elif(3<=self._count1 < 6):
                self._wimage, self._himage =  171, 16
            elif(6<=self._count1 < 9):
                self._wimage, self._himage =  150, 16 
            elif(self._count1 == 9):
                self._imagsh = 0
                    
        if(self._image == 3 or self._image == 1): #sinistra
            if(self._count1 < 3):
                self._wimage, self._himage =  1124, 16
            elif(3<=self._count1 < 6):
                self._wimage, self._himage =  1103, 16
            elif(6<=self._count1 < 9):
                self._wimage, self._himage =  1124, 16 
            elif(self._count1 == 9):
                self._imagesh = 0
        self._count1 += 1
       
    def dead(self): #Controllo animazione morte
        if self._GravityDown: #Se Dragon sta collidendo con Platform o con il bordomappa
            if(self._rotemp <=3):#Rotazione
                self._dy = 0
                if(self._rotation < 2):
                    self._wimage, self._himage = 103, 68
                elif( 2 <=self._rotation < 4):
                    self._wimage, self._himage = 124, 68
                elif( 4 <=self._rotation < 6):
                     self._wimage, self._himage = 145, 68
                elif( 6 <=self._rotation < 8):
                    self._wimage, self._himage = 166, 68
                else:
                    self._rotation = -1
                    self._rotemp += 1
                self._rotation += 1
            elif(self._rotemp <= 8):#Stelline
                if(self._rotation == 0 and self._rotemp == 4):
                    self._w, self._h = 15, 26
                    self._y -= 10 
                if(self._rotation < 2):
                    self._wimage, self._himage = 188, 58
                elif( 2 <=self._rotation < 4):
                    self._wimage, self._himage = 212, 58
                elif( 4 <=self._rotation < 6):
                     self._wimage, self._himage = 233, 58
                elif( 6 <=self._rotation < 8):
                    self._wimage, self._himage = 254, 58
                else:
                    if(self._rotemp == 8): #fine animazione con azzeramento contatori
                        self._w, self._h = 15, 16
                        self.spown()
                        self.Finish()
                        self._dead = 2  # respown immortal
                        self._rotemp = -1
                        self._shoot = 1 
                        self._GravityDown = False
                    self._rotation = -1
                    self._rotemp += 1
                self._rotation += 1
        else:#Continua a cadere
            self._wimage, self._himage = 103, 68
            self._y += 4
            arena_w, arena_h = self._arena.size()
            if self._y >= arena_h - self._h - self._bordmappa + self._bordmappaylow: #se va troppo in basso
                self._y = arena_h - self._h - self._bordmappa + self._bordmappaylow
                self._GravityDown = True
    
    def move(self):
        if(self._dead == 0 or self._dead == 2): #Se Dragon è vivo
            arena_w, arena_h = self._arena.size()
            if(self._shoot >= 1): #Controllo se Dragon ha sparato
                self.shootsleep()
            self._salta = 1
            self._y += self._dy
            if self._y < self._bordmappa:
                self._y = self._bordmappa
                self._dy = 2
            elif self._y > arena_h - self._h - self._bordmappa + self._bordmappaylow: 
                self._y = arena_h - self._h - self._bordmappa + self._bordmappaylow
                self._salta = 0
                self._imagej = 0

            self._dy += self._gravity

            self._x += self._dx
            if self._x < self._bordmappa:
                self._x = self._bordmappa
            elif self._x > arena_w - self._w - self._bordmappa:
                self._x = arena_w - self._w - self._bordmappa

            if(self._dead == 2): #Se Dragon è appena respownato, self._dead = 2
                self._immortalCount += 1
                if(self._immortalCount % 4 == 0): #per ricaricare l'immagine ogni 4 frame
                    self.directionImage()
                else:
                    self._wimage, self._himage = 2000, 0 #Immagine inesistente, per non far apparire nulla
                    
                if(self._immortalCount == 120): #Tempo di immortalità terminato
                    self._dead = 0
                    self._immortalCount = 0

            else: #se Dragon è vivo e, non è appena respownato, load image standard  
                self.directionImage()
            
        elif(self._dead == 1):#se morto
            self._shoot = 1 #non può sparare
            self.dead() #animazione morte 
                
#<g2d.key_pressed>       
    def go_left(self,go: bool):
        if go:
            self._image = 2
            self._dx = -self._speed
            self._wimage, self._himage = 6, 16
        elif self._dx < 0:
           self._dx = 0
           self._image = 4
           self._wimage, self._himage = 6, 16

    def go_right(self,go: bool):
        if go:
              self._image = 1
              self._dx = self._speed
              self._wimage, self._himage = 1268, 16   
        elif self._dx > 0:
            self._dx = 0
            self._image = 3
            self._wimage, self._himage = 1268, 16
            
    def go_jump(self):
        if (self._salta == 0):
            self._imagej = 3
            self._dy = -3.2 * self._speed
            self._salta = 1

    def shoot(self): #shoot
        if self._shoot == 0: 
            self._count1 = 0
            self._imagesh = 4 # animazione Dragon Spara
            self._shoot = 1
            if(self._image == 3 or self._image == 1):
                a = 1
            else:
                a = -1
            FireBall(self._arena,(self._x,self._y),a,self._dragonColor) #"a" è una variabile di controllo per la direzione della FireBall
#<\g2d.key_pressed>
            
    def collide(self, other):
        if isinstance(other, Platform):
            x1, y1, w1, h1 = self.position()
            x2, y2, w2, h2 = other.position()
            prv_x,pvr_y = x1 - self._dx, y1 - self._dy

            if prv_x + w1 <= x2:
                self._x = x2 - w1
            elif prv_x >= x2 + w2:
                self._x = x2 + w2
            elif pvr_y + h1 <= y2:
                self._y,self._dy = y2 - h2, 3
                self._salta = 0
                self._imagej = 0

            borders = [(x1+w1 - x2, -1, 0), (x2+w2 - x1, 1, 0),
                       (y1+h1 - y2, 0, -1)]
            move = min(borders)
            if(self._dead == 1 and move[2] != 0):
                self._y -= 1
                self._GravityDown = True #Quando è morto, mentre scende verso il basso, urtando la piattaforma smette di scendere.


        if isinstance(other, Enemy) and other.returnImage() < 3 and self._dead == 0: #se collide con Enemy, se Enemy è vivo, se Dragon è vivo.
            self._dead = 1 #morto
            self._lives -= 1

    def shootsleep(self): #Controllo Attesa prima di poter sparare di nuovo "per evitare spam" 
        self._shoot += 1
        if self._shoot == 10:
            self._shoot = 0
            
    def spown(self):
        if self._dragonColor == 0:
            self._x, self._y = 50,384 #respown angolo a Sinistra
            self._wimage, self._himage = 1270, 16
        else:
            self._x, self._y = 450,384 #respown angolo a Destra
            self._wimage, self._himage = 4, 16
            
    def Score(self,x):
        self._points += x
        return self._points

    def Finish(self): #Vite terminate
        if(self._lives == 0):
            self._arena.remove(self)

    def lives(self):
        return self._lives
            
    def ReturnDead(self): #Return stato del Dragon: Vivo, Respown Immortal, Morto
        return self._dead
    
    def ReturnColor(self):
        return self._dragonColor

    def position(self):
        return self._x, self._y, self._w, self._h
    
    def symbol(self):
        #Dragon Verde
        if(self._dragonColor == 1): #Dragon Blue
            if(self._wimage < 500):
                self._wimage += 323
            else:
                self._wimage -= 323
        w = self._wimage, self._himage, self._w, self._h
        if self._dragonColor == 1:
            if(self._wimage < 323*2):
                self._wimage -=323
            else:
                self._wimage +=323
        return w

class Orange(Actor): #Frutto
    def __init__(self, arena, pos):
        self._x, self._y = pos
        self._w, self._h = 14, 14
        self._wimage, self._himage = choice(((282, 802),(353,802),(317,802),
                                             (335,802),(264,802),(47,802))) #Diversi Frutti
        self._arena = arena
        arena.add(self)
    
    def move(self):
        pass

    def collide(self, other):
        if isinstance(other, Dragon):
            x = choice((20,30,40,50)) #Scelta casuale dello score
            Points(self._arena,(self._x,self._y),x,other.ReturnColor())
            other.Score(x)
            self._arena.remove(self)
        
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return self._wimage, self._himage, 14, 14

class Platform(Actor):
    def __init__(self, arena, pos , dim):
        self._x, self._y = pos
        self._w, self._h = dim
        self._arena = arena
        arena.add(self)
    
    def move(self):
        pass

    def collide(self, other):
        pass
        
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 0, 0, 0, 0
 
class Points(Actor): #Animazione Punteggio dopo Uccisione/Frutto
    def __init__(self, arena, pos,score,color):
        self._arena = arena
        self._x, self._y = pos
        self._wimage, self._himage = 0,0
        self._w, self._h = 10, 8
        self._dy = -1
        self._dx = choice((0.5,-0.5))
        if(10<=score <= 50):
            self._w, self._h = 16, 8
            self._wimage, self._himage = 7+((score/10 - 1)*16), 1315
        elif(score==350):
            self._w, self._h = 16, 8
            self._wimage, self._himage = 255, 1315
        if(color == 1):
            self._himage = 1352
        self._count = 0
        arena.add(self)
        
    def move(self):
        self._x += self._dx
        self._y += self._dy
        if(self._count == 30):
            self._arena.remove(self)
        self._count += 1
        
    def collide(self, other):
        pass
        
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return self._wimage, self._himage, self._w, self._h
