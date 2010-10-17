#!/usr/bin/python
import sys
sys.path += ['.']

# Import Pygame modules
import pygame
from pygame.locals import *

# Import important stuff
from globals import *
from scenehandler import *
from renderer import *
from mixer import *

from scene_preload import *
from scene_mainmenu import *

sceneHandler = None
renderer = None
mixer = None
enableSound = True
listener = None
fullScreen = False

def init():
    global sceneHandler
    global renderer
    global fullScreen
    global enableSound

    # Initialize renderer
    renderer = Renderer()
    renderer.init('Pyzzlix', 320, 240, fullScreen)
    mixer = Mixer()
    mixer.init(enableSound)
    
    # Initialize and populate scene stack
    sceneHandler = SceneHandler()

    sceneHandler.pushScene(Scene_Preload())    
    #sceneHandler.pushScene(Scene_MainMenu())    

def cleanup():
    global renderer
    
    # Clean up stuff
    mixer.cleanup()
    renderer.cleanup()
    

def main():
    print "Running Pyzzlix!"
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
            #print "FPS:", str(fpscounter)
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
                    elif event.type == KEYDOWN and event.key == K_F1:
                        ptime = pygame.time.get_ticks() * 0.001
                        renderer.toggleFullScreen()
                        pausedTime += (pygame.time.get_ticks() * 0.001) - ptime
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
        mainClock.tick(60) #sleeping

    #Game Over
    cleanup()


#this calls the 'main' function when this script is executed
if __name__ == '__main__': 
    if "--no-sound" in sys.argv:
        enableSound = False

    main()
