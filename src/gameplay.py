import pygame
def start_bgm(volume=0.2):
    global bgm
    global init_start_bgm
    if init_start_bgm == 0:
        # if sys.platform == "emscripten":
        #   place_sound = pygame.mixer.Sound("./source/sound/selectBlock.ogg")
        # else:
        #   place_sound = pygame.mixer.Sound("./source/sound/selectBlock.wav") # or .WAV,.mp3,.MP3
        bgm = pygame.mixer.Sound('./src/resources/game_song.ogg')
        bgm.set_volume(volume)
        bgm.play(-1)
        init_start_bgm = 1