#!/usr/bin/python

import sys

# Import Pygame modules
import os, pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


# Import important stuff
import globals
from globals import *

import scenestack
from scenestack import *

import scene_maingame
from scene_maingame import *

def init():
    global screen
    global background
    global sceneStack
    
    # Initialize screen
    screen = pygame.display.set_mode((320, 240))
    pygame.display.set_caption('Pyzzlix')
    pygame.mouse.set_visible(0)

    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 100))
    
    # Initialize and populate scene stack
    sceneStack = SceneStack()
    mainscene = Scene_MainGame()
    sceneStack.registerScene(mainscene)
    sceneStack.pushScene(mainscene)

def render():
    # Display The Background
    screen.blit(background, (0, 0))
    sceneStack.renderScenes(screen)
    pygame.display.flip()
    
def update(time):
    sceneStack.update(time)

def main():
    #Initialize Everything
    pygame.init()
    
    # Initialize custom stuff
    init()
            
    # Initialize main clockg
    mainClock = pygame.time.Clock()
    
    #Main Loop
    while 1:
        mainClock.tick(5)
        time = pygame.time.get_ticks() * 0.001

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN:
                sceneStack.handleKeyInput(event.key, KEYDOWN)
            elif event.type == KEYUP:
                sceneStack.handleKeyInput(event.key, KEYUP)

        # Update everything
        update(time)
        
        # Draw everything on screen
        render()

        sys.stdout.flush()

    #Game Over

#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()