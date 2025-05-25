import unittest
from Bubble import *

class FireBallTest(unittest.TestCase):

    def test_corner(self):
        a = Arena((512, 424))
        b = FireBall(a, (512-31-16, 180),1,0)  # dx = 7, dy = -1
        bordo = 31
        h_w = 16
        b.move()  #Trova il bordo, e cambia Stato 
        b.move()  #La FireBall sale verso l'alto
        self.assertTrue(b.position() == (512-bordo-h_w, 180-1, h_w, h_w))

    def test_move(self):
        a = Arena((512, 424))
        test_values = ( (40, 180, 47, 180),
                        (40, 215, 47, 215),
                        (40, 340, 47, 340),
                        (295, 80, 302, 80),
                        (295, 80, 302, 80))
        for param in test_values:
            x0, y0, x1, y1 = param
            b = FireBall(a, (x0, y0),1,0)
            b.move()
            self.assertTrue(b.position() == (x1, y1, 16, 16))

    def test_collide_Dragon(self):
        a = Arena((512, 424))
        d = Dragon(a, (230, 384),0)
        f = FireBall(a, (512-31-16, 180),1,0) #FireBall all'angolo
        f.move() #Trova il bordo, e cambia Stato
        f.move() #La FireBall sale verso l'alto
        f.collide(d)
        self.assertTrue(f.returnImage() == 2) #FireBall scoppia

    def test_collide_Platform1(self):#Collisione mentre si trova all'interno della piattaforma
        a = Arena((512, 424))
        f = FireBall(a, (40,250),1,0)
        p = Platform(a, (32, 240),(32,16))
        f.collide(p)  
        self.assertTrue(f.returnImage() == 2) #FireBall scoppia

    def test_collide_Platform2(self):#Collisione mentre si all'esterno della piattaforma
        a = Arena((512, 424))
        f = FireBall(a, (180,250),1,0)
        p = Platform(a, (200, 240),(32,16))
        f.collide(p)
        self.assertTrue(f.returnImage() == 1) #FireBall diventa Bolla

class DragonTest(unittest.TestCase):

    def test_right(self):
        a = Arena((512, 424))
        d = Dragon(a, (230, 384),0)
        d.go_right(True)
        d.move()
        d.move()
        d.go_right(False)
        self.assertTrue(d.position() == (235.0, 384, 15, 16))

    def test_collide_Enemy(self):
        a = Arena((512, 424))
        n = Enemy(a, (0, 0))
        d = Dragon(a, (230, 384),0)
        d.collide(n)
        d.collide(n)  # no effect
        self.assertTrue(d.lives() == 2)
    
    def test_collide_Platform(self):
        a = Arena((512, 424))
        p = Platform(a, (32, 240),(32,16))
        d = Dragon(a, (40, 210),0)
        for i in range(10): #Collide la Platform dall'alto e rimane sopra.
            d.move()
            d.collide(p)
        self.assertTrue(d.position() == (40, 240-16, 15, 16))

    def test_shoot(self):
        a = Arena((512, 424))
        d = Dragon(a, (230, 384),0)
        x = 0
        for i in range(10): #Spara per 10 volte
            d.shoot()
        for hh in a.actors(): #Ma per "def shootsleep" in Dragon, non si creano più FireBall
            if isinstance(hh,FireBall):
                x += 1
        self.assertTrue(x == 1)#Una sola FireBall

    def test_jump(self):
        a = Arena((512, 424))
        d = Dragon(a, (230, 384),0)
        d.go_jump() #Salta la prima volta
        test_values = (376.0, 368.4, #Valori di y durante il salto
                       361.2, 354.4,
                       348.0, 342.0,
                       336.4, 331.2,
                       326.4, 322.0)
        for i in range(10):
            d.go_jump() #no effect, sta già saltando
            d.move()
            y = test_values[i]
            self.assertTrue(d.position() == (230, y, 15, 16))

    def test_dead_notMove(self):
        a = Arena((512, 424))
        n = Enemy(a, (0, 0))
        d = Dragon(a, (230, 384),0) #Dragon sul bordo inferiore della mappa
        d.collide(n) #collide con Enemy
        d.go_right(True) # dx aumenta
        for i in range(10):
            d.move #resta fermo perchè è presente l'animazione della morte
        self.assertTrue(d.position() == (230, 384, 15, 16))#posizione di partenza

class EnemyTest(unittest.TestCase):

    def test_collide_FireBall_1(self):
        a = Arena((512, 424))
        n = Enemy(a, (200, 384))
        f = FireBall(a, (200,200),1,0)
        n.collide(f) #Collide con Fireball, Enemy entra nella bolla, e sale verso l'alto
        for i in range(20):
            n.move() #y -= 1.5
            self.assertTrue(n.position() == (200, 384.0-((i+1)*1.5), 16, 16))

    def test_collide_FireBall_2(self):
        a = Arena((512, 424))
        n = Enemy(a, (200, 384))
        f = FireBall(a, (512-31-16, 180),1,0) #FireBall sul corner -> Diventa una Bolla
        f.move()
        f.move()
        n.collide(f) #Collide con Fireball, ma è una bolla
        n.move()
        n.move()
        self.assertTrue(n.position() != (200, 384-(2), 16, 16)) #diverso dal caso di test_collide_FireBall_1

if __name__ == '__main__':
    unittest.main()
