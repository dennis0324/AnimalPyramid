import pygame
from pygame.surface import Surface
##########################################
#
# 알아두기: Image, Button, Silde의 'settable_*' 메소드는 scence에서 자동으로 호출됨
# 'settable_' 이 prefix로 붙은 메소드는 자동으로 호출됨 
#
##########################################

# TOOD: draw 함수 추상화

def draw_object(gamePad,obj, x, y):
    if obj == None:
        return
    gamePad.blit(obj, (x, y))

class Player:

    def __init__(self, playernum, score):
        self.playernum = playernum
        self.score = score

    def draw(self, win):
        (pygame.draw, rect)

# Image 클래스 
class Image:
    def __setitem__(self, key, value):
      setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)
    
    def __init__(self):
      self.pad = None
      self.img = None

    def settable_image(self,img):
      self.img = pygame.image.load(img)

    def settable_gamedisplay(self,gamedisplay):
      self.pad = gamedisplay
    
    def draw(self, x, y):
      self.pad.blit(self.img, (x, y))

    def get_pad(self):
      return self.pad

class Button:
    def __setitem__(self, key, value):
      setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)
    
    def __init__(self, img, hover_img, shadow):
        self.text = None
        self.font_color = None
        self.font_size = None
        self.img = img
        self.hover_img = hover_img
        self.shadow = shadow
        self.pad = None

    def settable_gamedisplay(self,gamedisplay):
      self.img = pygame.image.load(self.img)
      self.rect = self.img.get_rect()
      self.hover_img = pygame.image.load(self.hover_img)
      self.shadow = pygame.image.load(self.shadow)
      self.pad = gamedisplay

    def settable_fontcolor(self,font_color):
      self.font_color = font_color
      self.text2surface()
    
    def settable_fontsize(self,font_size):
      self.font_size = font_size
      self.text2surface()

    def settable_text(self, text):
      self.text = text
      self.text2surface()

    # fontcolor, fontsize, text가 모두 설정되어야만 text2surface가 실행됨 
    # 순서와 상관없이 실행되도록 하기 위해 text2surface를 따로 빼놓음
    def text2surface(self):
      if self.text and self.font_color and self.font_size:
        font = pygame.font.Font('./src/resources/font/PFStardust.ttf', self.font_size)
        self.screen_text = font.render(self.text, True, self.font_color)
        hovered_color = (self.font_color[0] - 30, self.font_color[1] - 30, self.font_color[2] - 30)
        self.screen_text_hovered = font.render(self.text, True, hovered_color)
        self.text_width, self.text_hight = font.size(self.text)
        self.center = ((160 - self.text_width) / 2, (80 - self.text_hight) / 2)
       
    
    def draw(self,x, y):
        self.rect.topleft = (x, y)
        if self.is_hovering(x,y):
            self.pad.blit(self.shadow, (x + 10, y + 10))
            self.pad.blit(self.hover_img, (x, y))
            self.pad.blit(self.screen_text_hovered, (x + self.center[0], y + self.center[1] + 5))
        else:
            self.pad.blit(self.shadow, (x + 10, y + 10))
            self.pad.blit(self.img, (x, y))
            self.pad.blit(self.screen_text, (x + self.center[0], y + self.center[1] + 5))

    def is_hovering(self,x,y):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
          return 1
        return 0
    def get_pad(self):
      return self.pad


class crown:

    def __init__(self, x, y, pad):
        self.x = x
        self.y = y
        self.pad = pad
        self.crown_img = pygame.image.load('./source/player/crown.png')

    def draw(self):
        self.pad.blit(self.crown_img, (self.x, self.y))

class Silde:

    def __init__(self, txt, text_size, x, y, round_size, pad, button_data_value, first_setting=50):
        self.screen = pad
        self.background = pygame.image.load('./src/resources/open_and_setting/setting.png')
        self.txt = '{}'.format(txt)
        self.text_size = text_size
        self.x = x
        self.y = y
        self.first_setting = first_setting
        self.round_size = round_size
        self.silder_img = pygame.image.load('./src/resources/open_and_setting/silder.png')
        self.silder_shadow = pygame.image.load('./src/resources/open_and_setting/silder_shadow.png')
        self.silder_point = pygame.image.load('./src/resources/open_and_setting/silder_shadow.png')
        self.text = pygame.font.Font('./src/resources/font/PFStardust.ttf', self.text_size)
        self.is_hit = False
        self.render_txt = self.text.render(self.txt, 1, (0, 0, 0))
        self.text_width, self.text_height = self.text.size(self.txt)
        self.txt_rect = self.render_txt.get_rect(center=(self.text_width / 2, self.text_height / 2))
        self.cover = pygame.Surface((int(self.text_width + 220 + 50), int(self.text_height)), pygame.SRCALPHA, 32)
        self.cover.blit(self.background, (-self.x, -self.y))
        self.bar = pygame.Surface([220, 16], pygame.SRCALPHA, 32)
        self.bar = self.bar.convert_alpha()
        self.bar.blit(self.silder_img, (0, 0))
        self.bar_rect = self.bar.get_rect(center=(110, 8))
        self.surf = pygame.Surface((int(self.text_width + 220 + 50), int(self.text_height)), pygame.SRCALPHA, 32)
        self.surf = self.surf.convert_alpha()
        self.text_width, self.text_height = self.text.size(self.txt)
        self.number = button_data_value
        self.button2pos = self.x + self.text_width + 50 + 198 - (100 - self.number) / 100 * 190
        
        self.button_surf = pygame.Surface([12, 12], pygame.SRCALPHA, 32)
        self.button_surf = self.button_surf.convert_alpha()
        self.button_pos = [self.button2pos, self.y + self.text_height / 2 + 2]
        pygame.draw.circle(self.button_surf, [255, 255, 255], [6, 6], 6, 0)

    def draw(self):
        self.render_txt = self.text.render('{}'.format(self.number), 1, (0, 0, 0))
        self.surf.blit(self.cover, (0, 0))
        self.surf.blit(self.render_txt, self.txt_rect)
        self.surf.blit(self.bar, (self.bar_rect[0] + 75, self.text_height / 2))
        self.button_rect = self.button_surf.get_rect(topleft=(self.button_pos[0], self.button_pos[1]))
        self.screen.blit(self.surf, (self.x, self.y))
        self.screen.blit(self.button_surf, self.button_pos)

    def update(self, number):
        pass

    def move(self):
        mouse = pygame.mouse.get_pos()
        if self.x + self.text_width + 60 <= mouse[0] - 6:
            if mouse[0] + 6 <= self.x + self.text_width + 50 + 214:
                self.number = int((190 - (self.x + self.text_width + 50 + 214 - mouse[0] - 7)) / 190 * 100)
                self.button_pos[0] = mouse[0] - 6


class score:

    def __init__(self, x, y, pad, text1, text2, text_size):
        self.x = x
        self.y = y
        self.pad = pad
        self.text1 = text1
        self.text2 = text2
        self.text_size = text_size
        self.cover = pygame.Surface([150, 70], pygame.SRCALPHA, 32)
        self.cover = self.cover.convert_alpha()
        self.img_background = pygame.image.load('./src/resources/player/player_score.png')
        self.cover.blit(self.img_background, [0, 0])
        self.surf = pygame.Surface([150, 70], pygame.SRCALPHA, 32)
        self.surf = self.surf.convert_alpha()
        self.surf.blit(self.img_background, [0, 0])
        self.text_name = pygame.font.Font('./src/resources/font/PFStardust.ttf', self.text_size)
        self.name_width, self.name_height = self.text_name.size(text1)
        self.text_score = pygame.font.Font('./src/resources/font/PFStardust.ttf', self.text_size)
        self.score_width, self.score_height = self.text_score.size(text2)

    def draw(self):
        self.name_render = self.text_name.render(self.text1, 1, (0, 0, 0))
        self.name_rect = self.name_render.get_rect(center=(self.name_width / 2, self.name_height / 2))
        self.score_render = self.text_score.render(self.text2, 1, (0, 0, 0))
        self.score_rect = self.score_render.get_rect(center=(self.score_width / 2, self.score_height / 2))
        self.surf.blit(self.cover, [0, 0])
        self.surf.blit(self.name_render, [10, 10])
        self.surf.blit(self.score_render, [10, 20 + self.score_height])
        self.pad.blit(self.surf, [self.x, self.y])