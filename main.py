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
renderer = 0
screen = 0
fullscreen = False

def init():
    global background
    global sceneHandler
    global screen
    global renderer
    
    # Initialize renderer
    renderer = Renderer()
    renderer.init('Pyzzlix', 320, 240)
    
    # Initialize and populate scene stack
    sceneHandler = SceneHandler()
    mainscene = Scene_MainGame()
    sceneHandler.pushScene(mainscene)

    
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
            else:
                sceneHandler.handleEvent(event)

        # Update everything
        update(time - lasttime)
        
        # Draw everything on screen
        renderer.render()
        
        fpscounter += 1
        if (time - lastfpsupdate >= 1.0):
            print "FPS:", str(fpscounter)
            fpscounter = 0
            lastfpsupdate = time
    
        sys.stdout.flush()

    #Game Over

#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
