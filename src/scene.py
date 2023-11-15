import copy
import pygame,sys
from pygame.locals import *
from pygame.surface import Surface
from src.ui import *
from src.gameplay import *

# 표시 괸리자
# 사용하고 싶은 컴포넌트는 add 클래스로 추가함
# ex) display_manager.add(Button,button_img, button_img_hovered, button_shadow)
# load 클래스로 추가한 컴포넌트를 불러옴
# ex) display_manager.load(Button,'b1',text='시작',fontcolor=(227,123,64),fontsize=40,gamedisplay=self.gamePad)
# 자동으로 필요한 속성 값 요구하기 때문에 문제 없이 사용 가능
class display_manager:
  def __setitem__(self, key, value):
      setattr(self, key, value)

  def __getitem__(self, key):
      return getattr(self, key)
  
  def __init__(self):
    self.test = 1
    self.images = {}
    self.types = {}
    self.mode = 0
    self.button = None

  def add(self,instance,*arg):
    self.types[instance.__name__] = instance(*arg)

  def load(self,instance,name,**data):
    error_key = ''
    # try:
    temp = copy.deepcopy(self.types[instance.__name__])
    methods = [method.split('_') for method in dir(temp) if method.startswith('__') is False]
    settable_methods = [method[1] for method in methods if (len(method) > 1) and method[0] == 'settable']

    for key,value in data.items():
      error_key = key
      if key in settable_methods:
        temp['settable_' + key](value)
    self.images[name] = temp
    # except:
    #   print(instance.__name__ + ' has no '+error_key+' methods')
    #   print(settable_methods)

  def draw(self,name,x,y):
    self.images[name].draw(x,y)


  def get(self,name):
    return self.images[name]

  def clear(self,clear_type = 'all', args:list = []):
    names = [arg.__name__ for arg in args]
    print(names, self.images.values())
    if clear_type == 'all':
      self.images.clear()
    elif clear_type == 'except':
      for key,value in self.images.items():
        if type(value).__name__ in names:
          self.images.pop(key)
    elif clear_type == 'only':
      for name in names:
        if self.images.get(name) is not None:
          self.images.pop(name)




class Pyramid:
  # 표시 모드
  mod = 0
  init = False

  # 각 플레이어 점수
  p1_score = 0
  p2_score = 0
  p3_score = 0

  # 소리 설정
  setting_data = []

  def __init__(self,gamePad,setting_data):
    button_img = './src/resources/button.png'
    button_img_hovered = './src/resources/button_1.png'
    button_shadow = './src/resources/buttonshadow.png'
    self.display_manager = display_manager()
    self.display_manager.add(Button,button_img, button_img_hovered, button_shadow)
    self.display_manager.add(Image)
    # self.display_manager.add(Silde)
    self.gamePad = gamePad
    self.setting_data = setting_data
    pass

  def show(self, event):
    if self.mod == 0:
      if not self.init:
        self.init_intro()
      self.show_intro(event)
    elif self.mod == 1:
      self.show_ingame(event)
    elif self.mod == 2:
      self.show_score(event)
    elif self.mod == 3:
      if not self.init:
        self.init_setting()
      self.show_setting(event)

  def init_intro(self):
    self.init = True
    self.display_manager.clear()
    self.display_manager.load(Image,'start_img', image='./src/resources/open_and_setting/title.png',gamedisplay=self.gamePad)
    self.display_manager.load(Image,'start_title', image='./src/resources/open_and_setting/title_1.png',gamedisplay=self.gamePad)

    self.display_manager.load(Button,'b1',text='시작',fontcolor=(227,123,64),fontsize=40,gamedisplay=self.gamePad)
    self.display_manager.load(Button,'b2',text='나가기',fontcolor=(227,123,64),fontsize=40,gamedisplay=self.gamePad)
    self.display_manager.load(Button,'b3',text='설정',fontcolor=(227,123,64),fontsize=40,gamedisplay=self.gamePad)

  def show_intro(self,events):
    # start_bgm(int(self.setting_data[1]) * 0.01)
    self.display_manager.draw('start_img', 0, 0)
    self.display_manager.draw('start_title', 0, 0)


    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
          mouse = pygame.mouse.get_pos()
          if self.display_manager.get('b1').rect.collidepoint((mouse[0], mouse[1])):
            print('1 press')
            in_opening = False
            # asyncio.run(runGame())
          if self.display_manager.get('b2').rect.collidepoint((mouse[0], mouse[1])):
            print('2 press')
            sys.exit()
          if self.display_manager.get('b3').rect.collidepoint((mouse[0], mouse[1])):
            print('3 press')
            self.mod = 3
            self.init = False

    self.display_manager.draw('b1',30,600)
    self.display_manager.draw('b2',220,600)
    self.display_manager.draw('b3',410,600)


            
  def show_ingame():
    pass

  def init_setting(self):
    self.init = True
    self.display_manager.clear()
    vol_sld1 = 0
    self.display_manager.load(Image,'start_img', image='./src/resources/open_and_setting/title.png',gamedisplay=self.gamePad)
    self.display_manager.load(Image,'start_setting', image='./src/resources/open_and_setting/setting.png',gamedisplay=self.gamePad)
    self.display_manager.load(Image,'start_title', image='./src/resources/open_and_setting/title_1.png',gamedisplay=self.gamePad)
    self.display_manager.load(Image,'setting_title', image='./src/resources/open_and_setting/background_setting_title.png',gamedisplay=self.gamePad)
    self.display_manager.load(Image,'setting_sound', image='./src/resources/open_and_setting/background_sound.png',gamedisplay=self.gamePad)
    self.display_manager.load(Image,'setting_music', image='./src/resources/open_and_setting/background_music.png',gamedisplay=self.gamePad)
    self.display_manager.load(Image,'setting_effect', image='./src/resources/open_and_setting/background_effect.png',gamedisplay=self.gamePad)


    self.display_manager.load(Button,'button_apply',text='적용',fontcolor=(227,123,64),fontsize=40,gamedisplay=self.gamePad)
    self.display_manager.load(Button,'button_exit',text='나가기',fontcolor=(227,123,64),fontsize=40,gamedisplay=self.gamePad)

    # sld1 = silde(vol_sld1, 40, 250, 365, 10, self.gamePad, int(self.setting_data[0]))
    # sld2 = silde(vol_sld1, 40, 250, 440, 10, self.gamePad, int(self.setting_data[1]))
    # button_apply.is_blind = False
    # self.display_manager.draw('start_title', 0, 0)
    # sildes = [sld1, sld2]
  def show_setting(self,events):
    self.display_manager.draw('start_img', 0, 0)
    self.display_manager.draw('start_setting', 0, 0)
    self.display_manager.draw('setting_title', 0, 0)
    self.display_manager.draw('setting_sound', 0, 0)
    self.display_manager.draw('setting_music', 0, 0)
    self.display_manager.draw('setting_effect', 0, 0)
    self.display_manager.draw('button_apply', 80, 600)

    mouse = pygame.mouse.get_pos()
    for event in events:
      if self.mod == 2:
        self.display_manager.draw('button_exit', 360, 600)
      else:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if self.display_manager.get('button_apply').rect.collidepoint((mouse[0], mouse[1])):
                in_setting = False
                print('setting Apply')
                # make_setting_file()
                if self.mod != 2:
                    self.mod = 0
                    self.init = False
                else:
                    print('draw horaw on board')
                    # draw_object(background, 0, 0)
                    # draw_horse_on_borad()
                    # horse_menu_display(player_turn)
            if self.display_manager.get('button_exit').rect.collidepoint((mouse[0], mouse[1])):
                self.mod = 0
                self.init = False
                # make_setting_file()
                # initGame()
                # opening()
        # if event.type == MOUSEBUTTONDOWN:
        #     for s in sildes:
        #         if s.button_rect.collidepoint(mouse):
        #             s.is_hit = True

        # if event.type == MOUSEBUTTONUP:
        #     for s in sildes:
        #         if sld2.is_hit == True:
        #             bgm.set_volume(s.number * 0.01)
        #             setting_data[1] = int(s.number)
        #         else:
        #             if sld1.is_hit == True:
        #                 place_sound.set_volume(s.number * 0.01)
        #                 setting_data[0] = int(s.number)
        #             s.is_hit = False

            if event.type == USEREVENT + 1:
                vol_sld1 += 1

  def show_score():
    pass