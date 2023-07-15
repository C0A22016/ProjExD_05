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
        self.rect.center = (random.randint(self.rect.width//2, WIDTH-self.rect.width//2), 0)
        self.vy = +6
        self.bound = random.randint(self.rect.height//2, 90)
        self.state = "down"
        self.interval = random.randint(100, 300)
        
    def update(self):
        if self.rect.centery > self.bound:
            self.vy = 0
            self.state = "stop"
        self.rect.centery += self.vy


class Bullet(pg.sprite.Sprite):
    """
    敵の弾に関するクラス
    """
    imgs = [pg.transform.rotozoom(pg.image.load("ex05/fig/ロケット.png"), 180, 0.08),
            pg.transform.rotozoom(pg.image.load("ex05/fig/雷.png"), 0, 0.04)]
    speed_lst = [2, 8]
    damage_lst = [1, 2]

    def __init__(self, emy: Enemy):
        """
        弾の種類を決定
        引数1 emy：弾を放つする敵機
        """
        super().__init__()
        num = random.randint(0,1)  # 乱数で弾の種類を決定
        self.image = __class__.imgs[num]  # numを元に画像を決定
        self.rect = self.image.get_rect() 
        self.rect.centerx = emy.rect.centerx
        self.rect.centery = emy.rect.centery+emy.rect.height/2
        self.speed = __class__.speed_lst[num]  # numを元に弾の速度を決定
        self.damage = __class__.damage_lst[num]  # numを元に与えるダメージを決定
        

    def update(self):
        """
        弾をspeedの値に基づきy軸方向に移動させる
        """
        self.rect.move_ip(0, self.speed)
        if self.rect.centery + self.rect.height >= HEIGHT + self.rect.height * 2:
            self.kill()


def main():
    pg.display.set_caption("ブロック崩し改")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #黒い背景を作成
    bg_img = pg.transform.rotozoom(pg.Surface((WIDTH, HEIGHT)), 0, 1.0)
    pg.draw.rect(bg_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    blocks = pg.sprite.Group()
    enemys = pg.sprite.Group()  # 敵のグループ作成
    bullets = pg.sprite.Group()  # 敵の弾のグループ作成
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

        if tmr%200 == 0 and len(enemys) < 10:  # 一定のフレーム毎に1回，敵機を出現させる
            enemys.add(Enemy())
            
        for emy in enemys:
            if emy.state == "stop" and tmr%emy.interval == 0:
                # 敵機が停止状態に入ったら，intervalに応じて弾を発射
                bullets.add(Bullet(emy))
        screen.blit(bg_img, [0, 0])
        
        # ブロックの更新と描画
        blocks.update(screen)
        enemys.update()
        enemys.draw(screen)
        bullets.update()
        bullets.draw(screen)
        
        # 画面の更新
        pg.display.flip()
        tmr += 1
        clock.tick(50)
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()