from typing import Any
import pygame as pg
import sys
import random

from pygame.sprite import AbstractGroup
WIDTH, HEIGHT = 1600, 900
class Block(pg.sprite.Sprite):
    """
    ブロックに関するクラス
    """
    def __init__(self,width:int,height:int,x:int,y:int):
        super().__init__()
        self.img = pg.Surface((width, height))
        self.img.fill((255, 255, 255))  # 白色で塗りつぶす
        self.rect = self.img.get_rect()
        self.rect.center = x,y
    def update(self,screen: pg.Surface):
        screen.blit(self.img,self.rect)


class Enemy(pg.sprite.Sprite):
    """
    敵に関するクラスです。 
    """
    def __init__(self):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("ex05/fig/UFO.png"), 0, 0.1)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(self.rect.width, WIDTH-self.rect.width), 0)
        self.vy = +6
        self.bound = random.randint(self.rect.height, 90)
        self.state = "down"
        self.interval = random.randint(50, 300)
        
    def update(self):
        """
        敵機を速度ベクトルself.vyに基づき移動（降下）させる
        ランダムに決めた停止位置_boundまで降下したら，_stateを停止状態に変更する
        引数 screen：画面Surface
        """
        if self.rect.centery > self.bound:
            self.vy = 0
            self.state = "stop"
        self.rect.centery += self.vy


def main():
    pg.display.set_caption("ブロック崩し改")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    blocks = pg.sprite.Group()
    enemys = pg.sprite.Group()
    tmr = 0
    clock = pg.time.Clock()
    
    # 初期ブロックの追加
    for i in range(1,10):
        for j in range(1,10):
            blocks.add(Block(100, 25,200+(110*i),100+(30*j)))
    
    while True:
        key_lst = pg.key.get_pressed()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0

        if tmr%300 == 0:  # 200フレームに1回，敵機を出現させる
            enemys.add(Enemy())
        
        # ブロックの更新と描画
        blocks.update(screen)
        enemys.update()
        enemys.draw(screen)
        
        # 画面の更新
        pg.display.flip()
        tmr += 1
        clock.tick(50)
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()