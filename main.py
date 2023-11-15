# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.7.17 (default, Jun  6 2023, 20:10:09) 
# [GCC 11.3.0]
# Embedded file name: animal_Pyramid.py

import pygame, sys, random, os.path, asyncio
# mod = sys.modules[__name__]
from time import sleep
from pygame.locals import *
from src.resources import *
from src.ui import *
from src.gameplay import *
from src.scene import *

Black = (0, 0, 0)
White = (255, 255, 255)
padWidth = 600
padHeight = 800



class horse:

    def __init__(self, horse_num, img, x, y, pad):
        self.horse_num = horse_num
        self.img = img
        self.x = x
        self.y = y
        self.pad = pad
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        self.pad.blit(self.img, (self.x, self.y))



class horse_menu:

    def __init__(self, x, y, img, img_hovered, pad):
        self.x = x
        self.y = y
        self.img = img
        self.img_hovered = img_hovered
        self.pad = pad
        self.alpha = self.img.convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
        self.is_blind = False

    def draw(self):
        if self.is_hovering():
            self.pad.blit(self.img_hovered, (self.x, self.y))
        else:
            if self.is_blind == True:
                self.pad.blit(self.img_hovered, (self.x, self.y))
            else:
                self.pad.blit(self.img, (self.x, self.y))

    def sound(self):
        self.sound.play(0, 2, 1)

    def is_hovering(self):
        mouse = pygame.mouse.get_pos()
        if self.x< mouse[0] < self.x + 32:
            if self.y< mouse[1] < self.y + 32:
                return 1
        return 0


def init_infor_player_data():
    global player_infor
    init_list = [
     0]
    player_infor = []
    for i in range(0, 3):
        player_infor.append(init_list * 12)


def init_player_infor():
    loop_count_player = 7
    for horsetype in range(1, 6):
        while loop_count_player:
            x = random.randint(0, 2)
            y = random.randint(0, 11)
            if player_infor[x][y] == 0:
                player_infor[x][y] = horsetype
                loop_count_player -= 1

        loop_count_player = 7

    for i in range(0, 3):
        for j in range(0, 12):
            if player_infor[i][j] == 0:
                player_infor[i][j] = 6

    for i in range(0, 3):
        player_infor[i].sort()


def can_put_update():
    global can_put
    global click_horse
    click_horse = 1
    can_put = []
    print('block_type =  %d' % block_type)
    for i in range(0, 8):
        for j in range(0, i + 1):
            if i == 7:
                if data_list[i][j] == 0:
                    can_put.append((i, j))
            if block_type != 5:
                if data_list[i + 1][j + 1] is player_infor[player_turn][player_select_horse_num] or data_list[i + 1][j] is player_infor[player_turn][player_select_horse_num]:
                    if data_list[i + 1][j + 1] != 6:
                        if data_list[i + 1][j] != 6:
                            if data_list[i + 1][j + 1] != 0 and data_list[i + 1][j] != 0:
                                can_put.append((i, j))
                            else:
                                if data_list[i + 1][j + 1] != 0:
                                    if data_list[i + 1][j] != 0:
                                        can_put.append((i, j))

    show_highlight()


def show_highlight():
    fLb_pos_x = 0
    fLb_pos_y = 0
    highlight_img = pygame.image.load(highlight[0])
    draw_object(background, 0, 0)
    draw_horse_on_borad()
    for y in range(1, 9):
        fLb_pos_x = fb_pos_x - 20 * (y - 1)
        fLb_pos_y = fb_pos_y + 40 * (y - 1)
        for x in range(0, y):
            for i, j in can_put:
                clickab_point_x = fLb_pos_x + x * 40
                clickab_point_y = fLb_pos_y
                if i == y - 1:
                    if j == x:
                        highlight_img = pygame.image.load(highlight[count_highlight])
                        draw_object(highlight_img, clickab_point_x, clickab_point_y)


def test_pos(x, y, z, data_form):
    global is_OK
    is_OK = 0
    if len(data_list[x - 1]) < y:
        print('다시 입력하시오.')
    else:
        for i, j in can_put:
            if x == i:
                if y == j:
                    is_OK = 1
                    break

    if z != 6:
        if is_OK == 1 and x != 7:
            if data_list[x + 1][y + 1] == z or data_list[x + 1][y] == z:
                if data_form == 0:
                    data_list[x][y] = z
                return 1
            if data_form == 1:
                return 0
            print('선택하신 위치에 그 블럭을 놓을 수 없습니다.')
            is_OK = 0
        else:
            if is_OK == 1:
                if x == 7:
                    if data_form == 0:
                        data_list[x][y] = z
                    return 1
            if data_form == 1:
                return 0
            print('놓을 수 있는 블럭 중에 입력하신 좌표가 일치하지 않습니다._1')
            is_OK = 0
    else:
        if z == 6:
            if x == 7:
                if data_form == 0:
                    data_list[x][y] = z
                return 1
            if x != 7:
                if data_list[x + 1][y + 1] != 0:
                    if data_list[x + 1][y] != 0:
                        if data_form == 0:
                            data_list[x][y] = z
                        return 1
                if data_form == 1:
                    return 0
                print('놓을 수 있는 블럭 중에 입력하신 좌표가 일치하지 않습니다._2')
                is_OK = 0


def neverchange():
  global init_start_bgm
  init_start_bgm = 0


def initGame():
    global background
    global background_num
    global block_type
    global can_put
    global clock
    global count_highlight
    global data_list
    global gamePad
    global game_over
    global highlight
    global horseNUM
    global horse_bar_background
    global horse_img_1
    global horse_img_h
    global horse_num
    global horse_num_h
    global is_inited
    global no_blind
    global no_horse_count
    global onGame
    global p1_score
    global p2_score
    global p3_score
    global place_sound
    global player_1_imgs
    global player_turn
    global player_turn_img
    global setting_data
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.time.set_timer(USEREVENT + 1, 1000)
    if sys.platform == "emscripten":
      place_sound = pygame.mixer.Sound("./src/resources/sound/selectBlock.ogg")
    else:
      place_sound = pygame.mixer.Sound("./src/resources/sound/selectBlock.wav") # or .WAV,.mp3,.MP3
    background_num = ['./src/resources/logo/WhileBreak.png', './src/resources/board1.png', './src/resources/board1.png']
    horse_num = ['./src/resources/horse/block 1.png','./src/resources/horse/block 2.png','./src/resources/horse/block 3.png','./src/resources/horse/block 4.png',
      './src/resources/horse/block 5.png','./src/resources/horse/block 6.png']
    horse_num_h = ['./src/resources/horse/block 1_h.png','./src/resources/horse/block 2_h.png','./src/resources/horse/block 3_h.png','./src/resources/horse/block 4_h.png',
      './src/resources/horse/block 5_h.png','./src/resources/horse/block 6_h.png']
    highlight = ['./src/resources/effect/highlight0.png', './src/resources/effect/highlight1.png', './src/resources/effect/highlight2.png']
    player_turn_img = [
      './src/resources/player/player_1.png', './src/resources/player/player_2.png', './src/resources/player/player_3.png']
    player_1_imgs = ['./src/resources/effect/time1.png','./src/resources/effect/time2.png','./src/resources/effect/time3.png',
      './src/resources/effect/time4.png','./src/resources/effect/time5.png']

    horse_img_h = pygame.image.load(horse_num_h[0])
    # horse_bar_background = pygame.image.load('./src/resources/background/horsebar.png').convert()

    horse_img_1 = pygame.image.load(horse_num[0])
    background = pygame.image.load(background_num[0])
    no_blind = set()
    data_list = []
    a = [0]
    can_put = []
    for i in range(1, 9):
        data_list.append(a * i)


    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('Animal Pyramid')
    horseNUM = 0
    clock = pygame.time.Clock()
    init_infor_player_data()
    init_player_infor()
    player_turn = 0
    is_inited = 0
    count_highlight = 0
    block_type = 0
    no_horse_count = 0
    horse_menu_display(player_turn)
    icon_img = pygame.image.load('./src/resources/icon/icon.png')
    pygame.display.set_icon(icon_img)
    game_over = False
    onGame = True

    if not os.path.isfile('./setting_data/setting.txt'):
        print("setting data not found")
        setting_data = [
         50, 50]
    else:
        f = open('./setting_data/setting.txt', 'r')
        data = f.read()
        data = data.split()
        print("setting data:",data)
        setting_data = data
        f.close()
        
    place_sound.set_volume(int(setting_data[0]) * 0.01)

    p1_score = 0
    p2_score = 0
    p3_score = 0





def make_setting_file():
    if not os.path.isfile('./setting_data/setting.txt'):
        f = open('./setting_data/setting.txt', 'w')
        f.close()
    else:
        f = open('./setting_data/setting.txt', 'w')
        f.write('%d %d' % (int(setting_data[0]), int(setting_data[1])))
        f.close()


hb_pos_x = 64
hb_pos_y = 734

def blind_horse_menu():
    print('가지고 있는 말 블라인 확인중...')
    yes_blind = set()
    player_horse = set(player_infor[player_turn])
    yes_blind = player_horse.difference(no_blind)
    for i in yes_blind:
        if i == 6:
            yes_blind.remove(6)
            break

    for i in range(0, len(player_infor[player_turn])):
        for j in list(yes_blind):
            if player_infor[player_turn][i] == j:
                globals()['bm_{}'.format(i)].is_blind = True


def horse_menu_display(player_tnum):
    global hb_pos_x
    global hb_pos_y
    global horse_img
    global horse_img_h
    global is_inited
    before_count = 0
    if is_inited == 1:
        for x in range(0, before_count):
            del globals()['bm_{}'.format(x)]

    i = 0
    for x in player_infor[player_tnum]:
        if x == 1:
            horse_img = pygame.image.load(horse_num[0])
            horse_img_h = pygame.image.load(horse_num_h[0])
        else:
            if x == 2:
                horse_img = pygame.image.load(horse_num[1])
                horse_img_h = pygame.image.load(horse_num_h[1])
            else:
                if x == 3:
                    horse_img = pygame.image.load(horse_num[2])
                    horse_img_h = pygame.image.load(horse_num_h[2])
                else:
                    if x == 4:
                        horse_img = pygame.image.load(horse_num[3])
                        horse_img_h = pygame.image.load(horse_num_h[3])
                    else:
                        if x == 5:
                            horse_img = pygame.image.load(horse_num[4])
                            horse_img_h = pygame.image.load(horse_num_h[4])
                        else:
                            if x == 6:
                                horse_img = pygame.image.load(horse_num[5])
                                horse_img_h = pygame.image.load(horse_num_h[5])
        globals()['bm_{}'.format(i)] = horse_menu(hb_pos_x + i * 40, hb_pos_y, horse_img, horse_img_h, gamePad)
        i += 1
        is_inited = 1


def logo():
    draw_object(gamePad,background, 0, 0)
    pygame.display.update()
    pygame.time.delay(1000)


def setting():
    vol_sld1 = 0
    start_img = pygame.image.load('./src/resources/open_and_setting/title.png')
    start_setting = pygame.image.load('./src/resources/open_and_setting/setting.png')
    setting_title = pygame.image.load('./src/resources/open_and_setting/background_setting_title.png')
    setting_sound = pygame.image.load('./src/resources/open_and_setting/background_sound.png')
    setting_music = pygame.image.load('./src/resources/open_and_setting/background_music.png')
    setting_effect = pygame.image.load('./src/resources/open_and_setting/background_effect.png')
    button_img = pygame.image.load('./src/resources/button.png')
    button_img_hovered = pygame.image.load('./src/resources/button_1.png')
    button_shadow = pygame.image.load('./src/resources/buttonshadow.png')
    button_apply = button(button_img, button_img_hovered, button_shadow, 80, 600, gamePad, '적용', (227,
                                                                                                  123,
                                                                                                  64), 40)
    button_exit = button(button_img, button_img_hovered, button_shadow, 360, 600, gamePad, '나가기', (227,
                                                                                                   123,
                                                                                                   64), 40)
    print(setting_data)
    sld1 = silde(vol_sld1, 40, 250, 365, 10, gamePad, int(setting_data[0]))
    sld2 = silde(vol_sld1, 40, 250, 440, 10, gamePad, int(setting_data[1]))
    button_apply.is_blind = False
    print('onGame = %d' % onGame)
    draw_object(start_setting, 0, 0)
    draw_object(setting_title, 0, 0)
    draw_object(setting_sound, 0, 0)
    draw_object(setting_music, 0, 0)
    draw_object(setting_effect, 0, 0)
    sildes = [sld1, sld2]
    in_setting = True
    while in_setting:
        button_apply.draw()
        for s in sildes:
            s.draw()

        if onGame == False:
            button_exit.draw()
        else:
            for event in pygame.event.get():
                if event.type in [pygame.QUIT]:
                    in_opening = False
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        if button_apply.rect.collidepoint((mouse[0], mouse[1])):
                            in_setting = False
                            print('setting Apply')
                            make_setting_file()
                            if onGame != False:
                                opening()
                            else:
                                print('draw horaw on board')
                                draw_object(background, 0, 0)
                                draw_horse_on_borad()
                                horse_menu_display(player_turn)
                        if button_exit.rect.collidepoint((mouse[0], mouse[1])):
                            make_setting_file()
                            initGame()
                            opening()
                    mouse = pygame.mouse.get_pos()
                    if event.type == MOUSEBUTTONDOWN:
                        for s in sildes:
                            if s.button_rect.collidepoint(mouse):
                                s.is_hit = True

                    if event.type == MOUSEBUTTONUP:
                        for s in sildes:
                            if sld2.is_hit == True:
                                bgm.set_volume(s.number * 0.01)
                                setting_data[1] = int(s.number)
                            else:
                                if sld1.is_hit == True:
                                    place_sound.set_volume(s.number * 0.01)
                                    setting_data[0] = int(s.number)
                                s.is_hit = False

                if event.type == USEREVENT + 1:
                    vol_sld1 += 1

            for s in sildes:
                if s.is_hit == True:
                    s.move()

            pygame.display.update()


fb_pos_x = 285
fb_pos_y = 278

def draw_horse_on_borad():
    for i in range(0, horseNUM):
        globals()['block_{}'.format(i)].draw()


def horse_rel2ab():
    global before_Count
    global clickab_point_x
    global clickab_point_y
    global fLb_pos_x
    global fLb_pos_y
    global no_horse_count
    global p1_score
    global p2_score
    global p3_score
    before_Count = 0
    for y in range(1, 9):
        fLb_pos_x = fb_pos_x - 20 * (y - 1)
        fLb_pos_y = fb_pos_y + 40 * (y - 1)
        for x in range(0, y):
            if fLb_pos_x + x * 40<= mouse[0] <= fLb_pos_x + x * 40 + 32:
                pass
            if fLb_pos_y<= mouse[1] <= fLb_pos_y + 32:
                clickab_point_x = fLb_pos_x + x * 40
                clickab_point_y = fLb_pos_y
                print('절대좌표_ (%d, %d)' % (y, x))
                if test_pos(y - 1, x, player_infor[player_turn][player_select_horse_num], 0):
                    click_horse = 0
                    if player_turn == 0:
                        p1_score += 10
                    else:
                        if player_turn == 1:
                            p2_score += 10
                        else:
                            if player_turn == 2:
                                p3_score += 10
                    place_sound.play(0, 1000, 1000)
                    horse_img_1 = pygame.image.load(horse_num[player_infor[player_turn][player_select_horse_num] - 1])
                    globals()['block_{}'.format(horseNUM)] = horse(player_select_horse_num, horse_img_1, clickab_point_x, clickab_point_y, gamePad)
                    before_Count = len(player_infor[player_turn])
                    no_horse_count = 0
                    globals()['block_{}'.format(horseNUM)].draw()
                    pygame.display.update()
                    turn2next_player(0)


def turn2next_player(no_horse2Put):
    global before_Count
    global game_over
    global horseNUM
    global player_turn
    before_Count = len(player_infor[player_turn])
    if not no_horse2Put:
        if len(player_infor[0]) == 0 or len(player_infor[1]) == 0 or len(player_infor[2]) == 0:
            game_over = True
        player_infor[player_turn].remove(player_infor[player_turn][player_select_horse_num])
        horseNUM += 1
    player_turn += 1
    if player_turn >= 3:
        player_turn = 0
    draw_horse_on_borad()
    if not test_turn():
        show_player_turn()
        horse_menu_display(player_turn)
    if test_turn():
        turn2next_player(1)
    pygame.display.update()


def test_turn():
    global game_over
    global no_blind
    global no_horse_count
    no_blind = set()
    if not game_over:
        print()
        print('==================================================')
        print('player %d의 차례' % (player_turn + 1))
        print('%d %d %d' % (p1_score, p2_score, p3_score))
        print('==================================================')
        for i in range(0, 8):
            print(data_list[i])

        print('==================================================')
        for i in range(0, 3):
            print(player_infor[i])

        print('test_turn - 실행중... player %d' % player_turn)
        count_put = 0
        no_put_count = 0
        have_horse_list = set()
        have_horse_list = set(player_infor[player_turn])
        print('가지고 있는 말의 종류: {}'.format(have_horse_list))
        for horsetype in list(have_horse_list):
            for i in range(0, 8):
                for j in range(0, i + 1):
                    if data_list[i][j] == 0:
                        if i == 7:
                            if data_list[i][j] == 0:
                                no_put_count = 1
                                no_blind.add(horsetype)
                    if horsetype != 6:
                        if data_list[i + 1][j + 1] is horsetype or data_list[i + 1][j] is horsetype:
                            if data_list[i + 1][j + 1] != 0:
                                if data_list[i + 1][j] != 0:
                                    if data_list[i + 1][j + 1] != 6 and data_list[i + 1][j] != 6:
                                        no_put_count = 1
                                        no_blind.add(horsetype)
                                    else:
                                        if data_list[i + 1][j + 1] != 0:
                                            if data_list[i + 1][j] != 0:
                                                no_put_count = 1
                                                no_blind.add(horsetype)

        print('no_horse_count = %d' % no_horse_count)
        if no_put_count == 0:
            print('그 플레이어는 놓을 수 있는 블럭이 없습니다.')
            no_horse_count += 1
            if no_horse_count > 5:
                print('게임 종료')
                game_over = True
            return 1
        blind_horse_menu()


def show_player_turn():
    global PT_img
    PT_img = pygame.image.load(player_turn_img[player_turn])
    player_effect = pygame.image.load('./source/effect/time1.png')
    for i in range(0, 5):
        score_1.draw()
        score_2.draw()
        score_3.draw()
        crown_1.draw()
        player_effect = pygame.image.load(player_1_imgs[i])
        draw_object(PT_img, 0, 100)
        draw_object(player_effect, 0, 100)
        pygame.display.update()
        pygame.time.delay(70)
        draw_object(background, 0, 0)

    pygame.display.update()
    draw_object(background, 0, 0)
    draw_object(horse_bar_background, hb_pos_x - 4, hb_pos_y - 4)
    pygame.display.update()


def text_show_timer():
    pass


def show_rank():
    score_1.text2 = '{}'.format(p1_score)
    score_2.text2 = '{}'.format(p2_score)
    score_3.text2 = '{}'.format(p3_score)
    score_1.draw()
    score_2.draw()
    score_3.draw()
    pos_p1 = (20, 5)
    pos_p2 = (225, 5)
    pos_p3 = (430, 5)
    scores = [
     p1_score, p2_score, p3_score]
    Winner = [0]
    for i in range(0, 3):
        if Winner[0] != i:
            if scores[Winner[0]] == scores[i]:
                Winner.append(i)
            if scores[Winner[0]] < scores[i]:
                Winner = [
                 i]

    for i in Winner:
        if i == 0:
            crown_1.x = pos_p1[0]
            crown_1.y = pos_p1[1]
            crown_1.draw()
        elif i == 1:
            crown_1.x = pos_p2[0]
            crown_1.y = pos_p2[1]
            crown_1.draw()
        if i == 2:
            crown_1.x = pos_p3[0]
            crown_1.y = pos_p3[1]
            crown_1.draw()


async def runGame():
    global background
    global block_type
    global crown_1
    global horse_img
    global mouse
    global onGame
    global player_select_horse_num
    global score_1
    global score_2
    global score_3
    score_1 = score(20, 30, gamePad, 'player1', '0', 20)
    score_2 = score(225, 30, gamePad, 'player2', '0', 20)
    score_3 = score(430, 30, gamePad, 'player3', '0', 20)
    crown_1 = crown(20, 5, gamePad)
    show_rank()
    gameOver_img = pygame.image.load('./source/Game_over.png')
    click_horse = 1
    player_select_horse_num = 0
    onGame = False
    background = pygame.image.load(background_num[1])
    draw_object(background, 0, 0)
    pygame.display.update()
    show_player_turn()
    while not onGame:
        show_rank()
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    print('horse_img: %d %d' % (player_turn, player_select_horse_num))
                    try:
                        horse_img = pygame.image.load(horse_num[player_infor[player_turn][player_select_horse_num] - 1])
                    except IndexError:
                        print('오류 발생: %d' % player_select_horse_num)

                    print('mouse pos_{}'.format(mouse))
                    print('click_horse = %d' % click_horse)
                    if event.button == 1:
                        if click_horse == 1:
                            horse_rel2ab()
                    if event.button == 1:
                        for x in range(0, 12):
                            if globals()['bm_{}'.format(x)].rect.collidepoint((mouse[0], mouse[1])):
                                if globals()['bm_{}'.format(x)].is_blind != True:
                                    click_horse = 1
                                    player_select_horse_num = x
                                    block_type = player_infor[player_turn][player_select_horse_num] - 1
                                    can_put_update()
                                    print('선택하신 블럭= %d ' % (player_infor[player_turn][player_select_horse_num] - 1))
                                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print('ESC pressed')
                        setting()
                if event.type == USEREVENT + 1:
                    text_show_timer()
            if game_over == True:
                draw_object(gameOver_img, 0, 300)
                top = [0]
                scores = [
                 p1_score, p2_score, p3_score]
                Winner = [0]
                for i in range(0, 3):
                    if Winner[0] != i:
                        if scores[Winner[0]] == scores[i]:
                            Winner.append(i)
                        if scores[Winner[0]] < scores[i]:
                            Winner = [
                             i]

                Winner_text = 'Player '
                for i in Winner:
                    Winner_text += '%d ' % (i + 1)

                Winner_text += 'WIN!'
                print(Winner_text)
                font = pygame.font.Font('./source/font/PFStardust.ttf', 50)
                font_width, font_heith = font.size(Winner_text)
                screen_text = font.render(Winner_text, True, (255, 255, 255))
                gamePad.blit(screen_text, (300 - font_width / 2, 500))
                pygame.display.update()
                pygame.time.delay(4000)
                initGame()
                opening()

        draw_horse_on_borad()
        for i in range(0, len(player_infor[player_turn])):
            globals()['bm_{}'.format(i)].draw()

        pygame.display.update()
        await asyncio.sleep(0)
    pygame.quit()
global COUNT_DOWN
neverchange()
initGame()
logo()

pyramid = Pyramid(gamePad,setting_data)
async def main():
    clock = pygame.time.Clock()

    in_opening = True
    SNAKE_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SNAKE_UPDATE, 200) 
    # while True:

    while in_opening:
        events = pygame.event.get()
        for event in events:
            if event.type in [pygame.QUIT]:
                in_opening = False
                pygame.quit()
                sys.exit()

        pyramid.show(events)
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())