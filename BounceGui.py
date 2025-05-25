import g2d
from BounceGame import BounceGameDragon

class BounceGui:
    def __init__(self):
        self._game = BounceGameDragon()
        g2d.init_canvas(self._game.arena().size())
        self._bubble = g2d.load_image("bubble-bobble.png")
        self._mappa = g2d.load_image("bubble-bobble-maps.png")
        g2d.main_loop(self.tick)

    def handle_keyboard(self):
        drag = self._game.dragon()
        drag2 = self._game.dragon2()
        
        if g2d.key_pressed("ArrowUp"):
            drag.go_jump()
        if g2d.key_pressed("ArrowRight"):
            drag.go_right(True)
        elif g2d.key_released("ArrowRight"):
            drag.go_right(False)
        if g2d.key_pressed("ArrowLeft"):
            drag.go_left(True)
        elif g2d.key_released("ArrowLeft"):
            drag.go_left(False)
        if g2d.key_pressed("Spacebar"):
            drag.shoot()


        if g2d.key_pressed("w"):
            drag2.go_jump()
        if g2d.key_pressed("d"):
            drag2.go_right(True)
        elif g2d.key_released("d"):
            drag2.go_right(False)
        if g2d.key_pressed("a"):
            drag2.go_left(True)
        elif g2d.key_released("a"):
            drag2.go_left(False)
        if g2d.key_pressed("c"):
            drag2.shoot() 

    def tick(self):
        self.handle_keyboard()
        arena = self._game.arena()
        game = self._game
        ScoreGreen = game.game_score_dragon()
        ScoreBlue = game.game_score_dragon2()
        g2d.clear_canvas()
        g2d.draw_image_clip(self._mappa, game.returnMap(), (0,0,512,424))
        arena.move_all()
        xcount = 0
        for a in str(ScoreGreen):
            num = int(a)
            g2d.draw_image_clip(self._bubble, (148+(num*9),1607,8,9), (128+(16*xcount),50,16,18))
            xcount += 1
        xcount = 0
        for a in str(ScoreBlue):
            num = int(a)
            g2d.draw_image_clip(self._bubble, (148+(num*9),1619,8,9), (384+(16*xcount),50,16,18))
            xcount += 1
        
        for a in arena.actors():
            if a.symbol() != (0, 0, 0, 0):
                g2d.draw_image_clip(self._bubble, a.symbol(), a.position())
            
        if game.game_Lose():
            g2d.alert("Game over")
            g2d.close_canvas()
            
        if game.game_Win():
            g2d.alert("Game won")
            g2d.close_canvas()

def main():
    gui = BounceGui()

main()
