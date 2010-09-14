#!/usr/bin/python

import sys

# Import Pygame modules
import os, pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


# Import important stuff
from globals import *
from scenehandler import *
from renderer import *
from scene_maingame import *
from font import *



background = 0
sceneHandler = 0
screen = 0
fullscreen = False

def init():
    global background
    global sceneHandler
    global screen
    
    # Initialize screen and window
    screen = setDisplay(fullscreen)
    pygame.display.set_caption('Pyzzlix')
    pygame.mouse.set_visible(0)

    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 100))
    
    # Initialize renderer
    renderer = Renderer()
    renderer.setScreen(screen)
    
    # Initialize and populate scene stack
    sceneHandler = SceneHandler()
    mainscene = Scene_MainGame()
    sceneHandler.pushScene(mainscene)

    font_normal = Font("font_normal.bmp", 8, 8);


def setDisplay(fullscreen):
    if (fullscreen == True):
        screen = pygame.display.set_mode((320, 240), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
    else:
        screen = pygame.display.set_mode((320, 240))
    return screen

def render():
    # Display The Background
    screen.blit(background, (0, 0))
    sceneHandler.renderScenes()
    pygame.display.flip()
    
def update(time):
    sceneHandler.update(time)

def main():
    global fullscreen

    #Initialize Everything
    pygame.init()
    
    # Initialize custom stuff
    init()
            
    # Initialize main clockg
    mainClock = pygame.time.Clock()
    time = pygame.time.get_ticks() * 0.001
    lastfpsupdate = time
    fpscounter = 0
    
    #Main Loop
    while 1:
        mainClock.tick(30)
        lasttime = time
        time = pygame.time.get_ticks() * 0.001
        
        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_F1:
                fullscreen = not fullscreen
                setDisplay(fullscreen)
            elif event.type == KEYDOWN:
                sceneHandler.handleKeyInput(event.key, KEYDOWN)
            elif event.type == KEYUP:
                sceneHandler.handleKeyInput(event.key, KEYUP)

        # Update everything
        update(time - lasttime)
        
        # Draw everything on screen
        render()
        
        fpscounter += 1
        if (time - lastfpsupdate >= 1.0):
            print "FPS:", str(fpscounter)
            fpscounter = 0
            lastfpsupdate = time
    
        sys.stdout.flush()

    #Game Over

#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()