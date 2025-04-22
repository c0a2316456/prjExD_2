import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650

DELTA = {
    pg.K_UP : (0 , -5),
    pg.K_DOWN : (0 , +5),
    pg.K_LEFT : (-5 , 0),
    pg.K_RIGHT : (+5 , 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:

    #引値：こうかとんrectまたは爆弾rect
    #戻り値：判定結果タプル(縦、横)
    #画面内ならTrue、画面外ならFalse

    besi, vert= True, True

    if rct.left < 0 or WIDTH < rct.right:
        besi = False

    if rct.top < 0 or HEIGHT < rct.bottom:
        vert = False

    return besi, vert   




def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    kt_sad_img = pg.image.load("fig/8.png")
    kt_sad_img = pg.transform.rotozoom(kt_sad_img, 0, 0.9)


    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))

    speed = 1
    max_speed = 10
    timer = 300

    c_img = pg.Surface((20, 20))
    pg.draw.circle(c_img, (255, 0, 0), (10, 10), 10)
    c_rct = c_img.get_rect()
    c_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    c_img.set_colorkey((0, 0, 0))

    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            screen.fill((0,0,0))

            fonto = pg.font.Font(None, 60)
            txt = fonto.render("GAME OVER", True, (255, 255, 255))
            screen.blit(txt, [WIDTH // 2 - 120 , HEIGHT // 2 ])

            le_sad_rect = kt_sad_img.get_rect()
            le_sad_rect.center = 20, HEIGHT//2

            ri_sad_rect = kt_sad_img.get_rect()
            ri_sad_rect.center = 50, HEIGHT//2
            
            bb_rct.center = WIDTH // 2, HEIGHT // 2

            pg.display.update()
            time.sleep(5)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key , mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        #if key_lst[pg.K_UP]:
        #   sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])


        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        
        besi, vert = check_bound(bb_rct)
        if not besi:
            vx *= -1
        if not vert:
            vy *= -1


        screen.blit(bb_img, bb_rct)
        # screen.blit(bb_img, bb_rct)
        screen.blit(c_img, c_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

        if tmr % timer == 0 and speed < max_speed:
            speed += 1
            vx = 5 * speed if vx > 0 else -5 * speed
            vy = 5 * speed if vy > 0 else -5 * speed

        dx = kk_rct.centerx - c_rct.centerx
        dy = kk_rct.centery - c_rct.centery
        distance = max((dx**2 + dy**2) ** 0.5, 1) 
        speed = 3

        c_rct.move_ip(speed * dx / distance, speed * dy / distance)

        if kk_rct.colliderect(bb_rct) or kk_rct.colliderect(c_rct):
            screen.fill((0,0,0))

            fonto = pg.font.Font(None, 60)
            txt = fonto.render("GAME OVER", True, (255, 255, 255))
            screen.blit(txt, [WIDTH // 2 - 120 , HEIGHT // 2 ])

            le_sad_rect = kt_sad_img.get_rect()
            le_sad_rect.center = 20, HEIGHT//2

            ri_sad_rect = kt_sad_img.get_rect()
            ri_sad_rect.center = 50, HEIGHT//2
            
            bb_rct.center = WIDTH // 2, HEIGHT // 2

            pg.display.update()
            time.sleep(5)
            return

        





if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()