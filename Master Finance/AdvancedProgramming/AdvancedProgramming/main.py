import os
from typing import Tuple
import pygame
import utils

from scenes import *


class Config:
    '''
    Game configuration settings.
    '''
    width: int = 960  # Width of the game screen
    height: int = 540  # Height of the game screen
    rootdir: str = os.path.split(os.path.abspath(__file__))[0]  # Directory path of the current script file
    SCREENSIZE: Tuple[int, int] = (width, height)  # Screen size as a tuple of width and height
    FPS: int = 30  # Frames per second for the game
    COMPUT_STEPS: int = 360  # Number of steps for game computations
    TITLE: str = 'Game'  # Title of the game


class SceneManager:
    '''
    Manages scene transitions in the game.
    '''

    def __init__(self, screen: pygame.Surface):
        '''
        Initialize the SceneManager with the initial scene.

        Args:
            screen (pygame.Surface): The screen surface to render the scenes on.
        '''
        self.go_to(TitleScene(screen))  # Transition to the TitleScene

    def go_to(self, scene):
        '''
        Transition to a new scene or a stored scene.

        Args:
            scene: The scene to transition to.
        '''
        if scene and scene.save_state:
            self.stored_scene = scene
        self.scene = scene # Set Current scene to the new scene
        self.scene.manager = self # Set the manager of the new scene

    def store_scene(self, scene):
        '''
        Store a scene for later use.

        Args:
            scene: The scene to store.
        '''
        self.stored_scene = scene  # Store the provided scene

    def get_stored_scene(self):
        '''
        Retrieve the stored scene.

        Returns:
            Scene: The stored scene.
        '''
        return self.stored_scene  # Return the stored scene

    def restart_game(self,screen):
        '''
        Restarts the game and deletes the stored Scene

        Args:
            screen (pygame.Surface): The screen surface to render the scenes on.
        '''
        self.stored_scene = None
        self.go_to(InvestmentScene(screen))
class Game:
    '''
    Main game class.
    '''

    def __init__(self):
        '''
        Initialize the game.
        '''
        self.config: Config = Config()  # Initialize game configuration
        self.screen: pygame.Surface = utils.InitGame(
            self.config.SCREENSIZE, self.config.TITLE
        )  # Initialize the screen

    def run(self):
        '''
        Start the game loop.
        '''
        timer: pygame.time.Clock = pygame.time.Clock()  # Create a clock object for managing the frame rate
        running: bool = True  # Flag to control the game loop
        self.manager: SceneManager = SceneManager(self.screen)  # Create a SceneManager object
        last_ticks: int = 0  # Time in milliseconds of the last frame update

        while running:
            cur_ticks: int = pygame.time.get_ticks()  # Get the current time in milliseconds
            nb_ticks: int = cur_ticks - last_ticks  # Calculate the time elapsed since the last frame update

            if nb_ticks > 1000 // self.config.FPS:
                self.scene()  # Execute the current scene's logic
                last_ticks = pygame.time.get_ticks()  # Update the last frame update time

            timer.tick(self.config.COMPUT_STEPS)  # Limit the frame rate

    def scene(self):
        '''
        Execute the current scene's event handling, update, and rendering functions.
        '''
        self.manager.scene.handle_events(pygame.event.get(), self.screen)  # Handle events for the current scene
        self.manager.scene.update(self.screen)  # Update the current scene
        self.manager.scene.render(self.screen)  # Render the current scene
        pygame.display.flip()
