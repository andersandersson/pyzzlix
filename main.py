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
    renderer.init('Pyzzlix', 320, 240, fullscreen)
    
    # Initialize and populate scene stack
    sceneHandler = SceneHandler()
    mainscene = Scene_MainGame()
    sceneHandler.pushScene(mainscene)

def main():
    global fullscreen

    #Initialize Everything
    pygame.init()
    
    # Initialize custom stuff
    init()
            
    # Initialize main clockg
    mainClock = pygame.time.Clock()
    time = pygame.time.get_ticks() * 0.001
    pausedTime = 0
    nextupdatetime = time
    lastrendertime = time
    lastfpsupdate = time
    fpscounter = 0
    
    LOGICS_PER_SEC = 20.0
    logicLength = 1.0 / LOGICS_PER_SEC
    
    #Main Loop
    while 1:        
        time = pygame.time.get_ticks() * 0.001 - pausedTime
        
        if (time - lastfpsupdate >= 1.0):
            print "FPS:", str(fpscounter)
            fpscounter = 0
            lastfpsupdate = time
        
        # Logic loop
        if (time > nextupdatetime):
            while (time > nextupdatetime):
                nextupdatetime += logicLength
                
                # Update scene timers
                sceneHandler.updateTimers(logicLength)
                
                # Handle Input Events
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return
                    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        return
                    elif event.type == KEYDOWN and event.key == K_F1:
                        fullscreen = not fullscreen
                        ptime = pygame.time.get_ticks() * 0.001
                        renderer.toggleFullScreen()
                        pausedTime += (pygame.time.get_ticks() * 0.001) - ptime
                        renderer.render(0)
                    else:
                        sceneHandler.handleEvent(event)

                # Do all ticks
                sceneHandler.doSceneTicks()
                
                # Draw everything on screen, use the same timestamp as logic step
                renderer.render(0)
                lastrendertime = time
                fpscounter += 1
        else:
            renderer.render(time - lastrendertime)
            lastrendertime = time
            fpscounter += 1
            
        sys.stdout.flush()
        #mainClock.tick(100) #sleeping

    #Game Over

#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
