import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル(横, 縦)
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    # 横方向判定
    if rct.left < 0 or WIDTH < rct.right:  # 画面外なら
        yoko = False
    # 縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom:  # 画面外なら
        tate = False
    return (yoko, tate)

def gameover():
    """
    Game Overを表示する関数
    こうかとんと爆弾が衝突したときに呼び出される
    """
    # 文字の設定
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    #こうかとんの画像
    make_img = pg.image.load("fig/8.png")
    make_img = pg.transform.rotozoom(make_img, 0, 1.0)
    right_make_rct = make_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
    left_make_rct = make_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))
    
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)  # 半透明にする
    overlay.fill((0, 0, 0))  # 黒で塗りつぶす

    screen = pg.display.get_surface()
    screen.blit(overlay, (0, 0))
    screen.blit(text, text_rect)
    screen.blit(make_img, right_make_rct)
    screen.blit(make_img, left_make_rct)
    pg.display.update()



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
 
    # こうかとん初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))  # 黒を透明にする
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        # こうかとんRectと爆弾Rectの衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover()
            time.sleep(5)  # 5秒待つ
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 左右方向
                sum_mv[1] += mv[1]  # 上下方向
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # 画面外なら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bb_rct.move_ip(vx, vy)  # 爆弾移動 
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 左右が画面外なら
            vx *= -1
        if not tate:  # 
            vy *= -1
    
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()