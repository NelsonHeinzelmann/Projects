import os
from typing import Tuple, List
import numpy as np
from utils import *
import random
import unittest

WHITE: Tuple[int, int, int] = (255, 255, 255)  # RGB value for white color
FONT_NAME: str = 'Corbel'  # Font name for the game

class TitleScene(object):
    '''
    Title scene class for the game.
    '''

    def __init__(self, screen: pygame.Surface):
        '''
        Initialize the TitleScene.

        Args:
            screen (pygame.Surface): The screen surface to render the scene on.
        '''
        super(TitleScene, self).__init__()  # Call the constructor of the object class
        self.save_state: bool = False  # Flag to indicate save state

        # Initialize the font and background image
        self.sfont: pygame.font.Font = pygame.font.SysFont(FONT_NAME, 35)  # Set the font for the scene
        self.background: pygame.Surface = LoadSprite('Background', False)  # Load the background image

        # Load and play the background music
        self.rootdir: str = os.path.split(os.path.abspath(__file__))[0]  # Directory path of the current script file
        music_path: str = self.rootdir + "//assets//sounds//background.mp3"  # Path to the background music file
        pygame.mixer.music.load(music_path)  # Load the background music
        pygame.mixer.music.set_volume(0.3)  # Set the volume of the background music
        pygame.mixer.music.play(-1)  # Play the background music in a loop

    def render(self, screen: pygame.Surface):
        '''
        Render the scene.

        Args:
            screen (pygame.Surface): The screen surface to render the scene on.
        '''
        self.width: int = screen.get_width()  # Get the width of the screen
        self.height: int = screen.get_height()  # Get the height of the screen
        screen.blit(self.background, (0, 0))  # Draw the background image on the screen
        text: pygame.Surface = self.sfont.render('> press space to start <', True, WHITE)  # Render the text
        text_rect: pygame.Rect = text.get_rect(center=(self.width/2, self.height/2))  # Get the rect for centering the text
        screen.blit(text, text_rect)  # Draw the text on the screen

    def update(self, screen: pygame.Surface):
        '''
        Update the scene.

        Args:
            screen (pygame.Surface): The screen surface of the scene.
        '''
        pass  # No updates required for the title scene

    def handle_events(self, event: pygame.event.Event, screen: pygame.Surface):
        '''
        Handle events for the scene.

        Args:
            event (pygame.event.Event): The event to handle.
            screen (pygame.Surface): The screen surface of the scene.
        '''
        for e in event:
            if e.type == pygame.QUIT:
                QuitGame()  # Quit the game if the quit event is triggered
            if e.type == pygame.VIDEORESIZE:
                pass  # Placeholder for handling video resize event
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.manager.go_to(MainMenuScene(screen))  # Transition to the main menu scene

class MainMenuScene:
    '''
    Main menu scene class for the game.
    '''

    def __init__(self, screen: pygame.Surface):
        '''
        Initialize the MainMenuScene.

        Args:
            screen (pygame.Surface): The screen surface to render the scene on.
        '''
        self.save_state: bool = False  # Flag to indicate save state
        self.sfont: pygame.font.Font = pygame.font.SysFont(FONT_NAME, 35)  # Set the font for the scene
        self.button_colors: List[Tuple[int, int, int]] = [(25, 25, 25) for _ in range(3)]  # Colors for the buttons
        self.background: pygame.Surface = LoadSprite('Background', False)  # Load the background image
        self.rootdir: str = os.path.split(os.path.abspath(__file__))[0]  # Directory path of the current script file
        self.hover_sound: pygame.mixer.Sound = pygame.mixer.Sound(self.rootdir + "//assets//sounds//mouse_hover.mp3")  # Load the hover sound effect
        self.menu_items: List[str] = ['Play', 'Options', 'Exit']  # Menu item names
        self.width: int = screen.get_width()  # Get the width of the screen
        self.height: int = screen.get_height()  # Get the height of the screen
        self.menu_rects: List[pygame.Rect] = [pygame.Rect(self.width/2 - 70, self.height/2 + i*50 - 70, 140, 40) for i in range(len(self.menu_items))]  # Rectangles for the menu items
        self.options_button: pygame.Rect = pygame.Rect(self.width/2 - 70, self.height/2+10, 140, 40)  # Rectangle for the options button

    def render(self, screen: pygame.Surface):
        '''
        Render the scene.

        Args:
            screen (pygame.Surface): The screen surface to render the scene on.
        '''
        screen.blit(self.background, (0, 0))  # Draw the background image on the screen

        for i, rect in enumerate(self.menu_rects):
            pygame.draw.rect(screen, self.button_colors[i], rect)  # Draw the buttons
            pygame.draw.rect(screen, WHITE, rect, 2)  # Draw white border around the buttons
            text: pygame.Surface = self.sfont.render(self.menu_items[i], True, WHITE)  # Render the text for the menu items
            text_rect: pygame.Rect = text.get_rect(center=rect.center)  # Get the rect for centering the text
            screen.blit(text, text_rect)  # Draw the text on the screen

    def update(self, screen: pygame.Surface):
        '''
        Update the scene.

        Args:
            screen (pygame.Surface): The screen surface of the scene.
        '''
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()

        for i, rect in enumerate(self.menu_rects):
            if rect.collidepoint(mouse_pos):
                if self.button_colors[i] != (50, 50, 50):
                    self.button_colors[i] = (50, 50, 50)
                    self.hover_sound.play()
            else:
                self.button_colors[i] = (25, 25, 25)

    def handle_events(self, events: List[pygame.event.Event], screen: pygame.Surface):
        '''
        Handle events for the scene.

        Args:
            events (List[pygame.event.Event]): The events to handle.
            screen (pygame.Surface): The screen surface of the scene.
        '''
        mouse_pos: Tuple[int, int] = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                QuitGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(self.menu_rects):
                    if rect.collidepoint(mouse_pos):
                        if self.menu_items[i] == 'Play':
                            self.manager.go_to(ScenarioGeneration(screen))  # Transition to the scenario generation scene
                        elif self.menu_items[i] == 'Options':
                            self.manager.go_to(OptionsScene(screen, return_scene=self))  # Transition to the options scene
                        elif self.menu_items[i] == 'Exit':
                            QuitGame()  # Quit the game

class ScenarioGeneration(object):
    '''
    Scenario generation scene class for the game.
    '''

    def __init__(self, screen: pygame.Surface):
        '''
        Initialize the ScenarioGeneration scene.

        Args:
            screen (pygame.Surface): The screen surface to render the scene on.
        '''
        super(ScenarioGeneration, self).__init__()  # Call the constructor of the object class
        self.save_state: bool = False  # Flag to indicate save state
        self.sfont: pygame.font.Font = pygame.font.SysFont(FONT_NAME, 17)  # Set the font for the scene
        self.invest_button_color: Tuple[int, int, int] = (25, 25, 25)  # Color for the invest button
        self.background: pygame.Surface = LoadSprite('Background', False)  # Load the background image
        self.rootdir: str = os.path.split(os.path.abspath(__file__))[0]  # Directory path of the current script file
        self.page_turn: pygame.mixer.Sound = pygame.mixer.Sound(self.rootdir + "//assets//sounds//page_turn.mp3")  # Load the page turn sound effect
        self.page_turn.play()  # Play the page turn sound effect
        pygame.mixer.music.load(self.rootdir + "//assets//sounds//music.mp3")  # Load the music
        pygame.mixer.music.play(-1)  # Play the music in a loop
        self.hover_sound: pygame.mixer.Sound = pygame.mixer.Sound(self.rootdir + "//assets//sounds//mouse_hover.mp3")  # Load the hover sound effect

        # Initialize the object state
        self.done: bool = False  # Flag to indicate if the scenario generation is done
        self.scenario: str = Path(self.rootdir + "//assets//texts//scenario1.txt").read_text()  # Load the scenario text
        self.width: int = screen.get_width()  # Get the width of the screen
        self.height: int = screen.get_height()  # Get the height of the screen
        self.text_rect: pygame.Rect = pygame.Rect(self.width*1/5, self.height*1/5, self.width*3/5, self.height*3/5)  # Rectangle for the text area
        self.button_rect: pygame.Rect = pygame.Rect(self.width*4/5, self.height*4/5, self.width*1/5, self.height*1/5)  # Rectangle for the button area
        self.lines: TextScroller = TextScroller(self.scenario, self.text_rect, self.sfont)  # Text scroller object
        self.line_index: int = 0  # Current line index
        self.char_index: int = 0  # Current character index
        self.draw_rect: bool = False  # Flag to indicate if the rectangle should be drawn

    def render(self, screen: pygame.Surface):
        '''
        Render the scene.

        Args:
            screen (pygame.Surface): The screen surface to render the scene on.
        '''
        screen.blit(self.background, (0, 0))  # Draw the background image on the screen
        self.width: int = screen.get_width()  # Get the width of the screen
        self.height: int = screen.get_height()  # Get the height of the screen

        # Render the text lines
        for i in range(self.line_index):
            if self.done == True:
                current_text: pygame.Surface = self.sfont.render(self.lines[i], True, WHITE)
            elif i+1 == self.line_index:
                # Render partially typed line
                current_text: pygame.Surface = self.sfont.render(self.lines[i][:self.char_index], True, WHITE)
            else:
                # Render full line
                current_text: pygame.Surface = self.sfont.render(self.lines[i], True, WHITE)
            text_height: int = current_text.get_height()
            screen.blit(current_text, (self.width*1/5, self.height*1/5 + (text_height+2)*i))
            
            if i == self.line_index - 1:
                self.draw_rect: bool = True  # Set the flag to draw a rectangle at the end of text rendering

        # Render the button
        pygame.draw.rect(self.background, self.invest_button_color, [self.width-150, self.height-50, 140, 40])
        text: pygame.Surface = self.sfont.render('Invest now!', True, WHITE)
        text_rect: pygame.Rect = text.get_rect(center=(self.width-80, self.height-30))
        screen.blit(text, text_rect)
    
    def update(self, screen: pygame.Surface):
        '''
        Update the scene.

        Args:
            screen (pygame.Surface): The screen surface of the scene.
        '''
        if not self.done:
            self.char_index += 5  # Increment the char_index by 5 for the typing effect
            if self.char_index >= len(self.lines[self.line_index]):
                self.char_index = 0  # Reset the char_index to 0
                self.line_index += 1  # Move to the next line
                if self.line_index >= len(self.lines):
                    self.done: bool = True  # Set the scene as done if all lines have been rendered
                    return  # Return to avoid further updates

        try:
            self.width  # Try to access the width attribute
        except AttributeError:
            return  # If the width attribute is not found, return to avoid further updates

        self.mouse: Tuple[int, int] = pygame.mouse.get_pos()  # Get the current mouse position as a tuple of (x, y) coordinates

        if self.width-150 <= self.mouse[0] <= self.width - 10 and self.height-50 <= self.mouse[1] <= self.height - 10:
            # Check if the mouse position is within the invest button area
            if self.invest_button_color == (50, 50, 50):
                return  # If the button color is already set, return to avoid further updates
            else:
                self.invest_button_color = (50, 50, 50)  # Set the button color to indicate hover effect
                self.hover_sound.play()  # Play the hover sound effect
        else:
            self.invest_button_color = (25, 25, 25)  # Reset the button color to its default value

    def handle_events(self, event: pygame.event.Event, screen: pygame.Surface):
        '''
        Handle events for the scene.

        Args:
            event (pygame.event.Event): The event to handle.
            screen (pygame.Surface): The screen surface of the scene.
        '''
        for e in event:
            if e.type == pygame.QUIT:
                QuitGame()  # Quit the game if the quit event is triggered
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.mixer.music.load(self.rootdir + "//assets//sounds//background.mp3")
                    pygame.mixer.play(-1)
                    self.manager.go_to(MainMenuScene(screen))  # Transition to the main menu scene
                if e.key == pygame.K_SPACE:
                    self.manager.go_to(InvestmentScene(screen))  # Transition to the investment scene
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(e.pos):
                    self.page_turn.play()
                    self.manager.go_to(InvestmentScene(screen))  # Transition to the investment scene

class InvestmentScene(object):
    '''
    Class representing an investment scene.
    '''

    class LineGraph:
        '''
        Class representing a line graph.
        '''

        def __init__(self, size: tuple, color: tuple, thickness: int, padding: int):
            '''
            Initialize the LineGraph object.

            Args:
                size (tuple): Size of the graph in pixels (width, height).
                color (tuple): Color of the graph line as RGB values (R, G, B).
                thickness (int): Thickness of the graph line in pixels.
                padding (int): Padding around the graph in pixels.
            '''

            self.size = size  # Size of the graph
            self.color = color  # Color of the graph line
            self.thickness = thickness  # Thickness of the graph line
            self.padding = padding  # Padding around the graph
            self.gfont = pygame.font.SysFont(FONT_NAME, 13)  # Font for graph labels
            self.points = []  # List to store the normalized data points
            self.min_value = None  # Minimum value in the data
            self.max_value = None  # Maximum value in the data

        def normalize_data(self, data: list) -> list:
            '''
            Normalize the data for graph rendering.

            Args:
                data (list): Data points to normalize.

            Returns:
                list: Normalized data points.
            '''

            # Find the minimum and maximum values in the data list
            self.min_value = min(data)
            self.max_value = max(data)

            range_value = self.max_value - self.min_value  # Calculate the range of values

            normalized_data = []  # List to store normalized data points

            if len(data) == 1:
                # If there's only one point, center it on the x-axis
                normalized_data.append((0.5, 0.5))
            else:
                usable_width = self.size[0] - 2 * self.padding  # Calculate the width of the usable x-axis
                spacing = usable_width / (len(data) - 1)  # Calculate the spacing between each point

                for i, value in enumerate(data):
                    x = self.padding + i * spacing  # Calculate the x coordinate of the point

                    y = (value - self.min_value) / range_value  # Normalize the y value to a range between 0 and 1

                    y = (1 - y) * self.size[1] - self.padding  # Calculate the y coordinate of the point

                    x = max(self.padding, min(x, self.size[0] - self.padding))  # Clip the x coordinate to graph boundaries
                    y = max(self.padding, min(y, self.size[1] - self.padding))  # Clip the y coordinate to graph boundaries

                    normalized_data.append((x, y))  # Append the normalized point (x, y)

            return normalized_data

        def render(self, surface: pygame.Surface, data: list, pos: tuple, y_label: str = None, percentage: bool = False,
           x_label: str = 'Quarter') -> None:
            '''
            Render the graph on the specified surface.

            Args:
                surface (pygame.Surface): The surface to render the graph on.
                data (list): The data points to render.
                pos (tuple): The position of the graph on the surface.
                y_label (str, optional): The label for the y-axis. Defaults to None.
                percentage (bool, optional): Whether to show y-axis values as percentages. Defaults to False.
                x_label (str, optional): The label for the x-axis. Defaults to 'Quarter'.
            '''

            # Normalize the data points by calculating their coordinates based on the graph size and padding
            self.points = self.normalize_data(data)

            # Create a new surface to draw the graph on
            graph_surface = pygame.Surface(self.size).convert_alpha()
            graph_surface.fill([0, 0, 0, 0])

            # Draw the x and y axis lines on the graph surface
            pygame.draw.line(graph_surface, WHITE, (self.padding, self.size[1] - self.padding),
                            (self.size[0] - self.padding, self.size[1] - self.padding))
            pygame.draw.line(graph_surface, WHITE, (self.padding, self.size[1] - self.padding),
                            (self.padding, self.padding))

            # Draw the data points as a line connecting each point on the graph surface
            for i in range(len(self.points) - 1):
                pygame.draw.line(graph_surface, self.color, self.points[i], self.points[i + 1], self.thickness)

            if x_label:
                # Calculate the spacing between each tick mark along the x-axis
                tick_spacing = (self.size[0] - 2 * self.padding) / (len(data) - 1)

                # Loop through the data and draw tick marks and labels for each point along the x-axis
                for i, value in enumerate(data):
                    x = self.padding + i * tick_spacing  # Calculate the x position of the tick mark
                    pygame.draw.line(graph_surface, WHITE, (x, self.size[1] - self.padding),
                                    (x, self.size[1] - self.padding + 5), 1)  # Draw the tick mark
                    label_surface = self.gfont.render(str(i), True, WHITE)  # Draw the label
                    label_pos = (x - label_surface.get_width() // 2, self.size[1] - self.padding + self.gfont.get_linesize() / 2)
                    graph_surface.blit(label_surface, label_pos)

                x_label_surface = self.gfont.render(x_label, True, WHITE)  # Draw the x-axis label
                x_label_pos = (self.size[0] - self.padding - x_label_surface.get_width() / 2,
                            self.size[1] - self.padding + self.gfont.get_linesize() * 1.1)
                graph_surface.blit(x_label_surface, x_label_pos)

            if y_label:
                y_label_surface = self.gfont.render(str(y_label), True, WHITE)  # Draw the y-axis label
                y_label_pos = (self.padding - y_label_surface.get_width() / 2, self.padding - self.gfont.get_linesize() * 1.1)
                graph_surface.blit(y_label_surface, y_label_pos)

                max_value = max(data)
                tick_spacing = max_value / 5

                # Loop through the tick marks and draw them along with corresponding labels along the y-axis
                for i in range(6):
                    value = tick_spacing * i
                    y = self.size[1] - self.padding - i * (self.size[1] - 2 * self.padding) / 5

                    if percentage:
                        label_text = f"{value * 100:.2f}%"  # Format the label as a percentage
                    else:
                        if max_value > 1000000:
                            label_text = f"{value:.2e}"  # Format the label using scientific notation
                        else:
                            label_text = f"{value:.2f}"  # Format the label as a decimal

                    label_surface = self.gfont.render(label_text, True, WHITE)
                    label_pos = (self.padding - label_surface.get_width() - self.gfont.get_linesize(),
                                y - label_surface.get_height() // 2)

                    pygame.draw.line(graph_surface, WHITE, (self.padding, y), (self.padding - 5, y), 1)  # Draw the tick mark
                    graph_surface.blit(label_surface, label_pos)

            surface.blit(graph_surface, pos)  # Blit the graph surface onto the main surface

    def __init__(self, screen):
        '''
        Initialize the InvestmentScene object.
        '''
        super(InvestmentScene, self).__init__()  # Constructor of the object class

        # Set attributes with their initial values

        self.save_state: bool = True
        
        self.width: int = screen.get_width()  # Get the width of the screen
        self.height: int = screen.get_height()  # Get the height of the screen
        self.port_to_win: int = 505000
        self.WAIT_TIME: int = 200000  # 20 seconds in milliseconds
        self.MAX_PERIODS: int = 18
        self.current_period: int = 1
        self.sfont = pygame.font.SysFont(FONT_NAME, 17)
        self.background = LoadSprite('Background', False)
        self.plot_color: tuple = (0, 0, 255)
        self.plot_thickness: int = 2
        self.plot_padding: int = 70
        self.plot_size: tuple = (self.width/2, self.height/2)
        self.time_step: float = 0.01
        self.max_time_steps: int = 300
        self.money: float = 500000
        self.stock_share: float = 0
        self.bond_share: float = 0
        self.stock_price_history: list = []
        self.bond_price_history: list = []
        self.inflation_price_history: list = []
        self.fed_rate_history: list = []
        self.time_history: list = []
        self.game_states: list = []
        self.starting_stock_share: float = 0
        self.starting_bond_share: float = 0
        self.starting_money: float = 500000

        # Set attributes related to financial parameters

        self.inflation_mean: float = 0.02
        self.inflation_sigma: float = 0.002
        self.inflation_ar_coef: float = 0.9
        self.inflation_ma_coef: float = 0.5

        self.fed_rate_mean: float = 0.02
        self.fed_rate_sigma: float = 0.002
        self.fed_rate_ar_coef: float = 0.6
        self.fed_rate_ma_coef: float = 0.2

        self.stock_mean: float = 100
        self.stock_sigma: float = 0.1
        self.stock_ar_coef: float = 0.8
        self.stock_ma_coef: float = 0.1
        self.stock_inflation_coef: float = 1.5
        self.stock_fed_rate_coef: float = -2

        self.bond_mean: float = 200
        self.bond_sigma: float = 0.1
        self.bond_ar_coef: float = 0.5
        self.bond_ma_coef: float = 0.2
        self.bond_inflation_coef: float = -2.5
        self.bond_fed_rate_coef: float = -2.5

        # Create graph objects

        self.inflation_graph = self.LineGraph(self.plot_size, self.plot_color, self.plot_thickness, self.plot_padding)
        self.fed_rate_graph = self.LineGraph(self.plot_size, self.plot_color, self.plot_thickness, self.plot_padding)
        self.stock_price_graph = self.LineGraph(self.plot_size, self.plot_color, self.plot_thickness, self.plot_padding)
        self.bond_price_graph = self.LineGraph(self.plot_size, self.plot_color, self.plot_thickness, self.plot_padding)

        pygame.time.set_timer(pygame.USEREVENT + 1, self.WAIT_TIME)
        self.generate_initial_data()

        # Create a Portfolio object

        self.portfolio = Portfolio(self.starting_money, self.stock_price_history, self.bond_price_history)

    def generate_initial_data(self) -> None:
        '''
        Generate initial data for the investment scene.
        '''

        # Generate initial data using log-normal distribution

        # Append an initial random value within the range [0.02, 0.05] to the inflation price history
        self.inflation_price_history.append(random.uniform(0.02, 0.05))

        # Append an initial random value within the range [0, 0.1] to the federal reserve rate history
        self.fed_rate_history.append(random.uniform(0, 0.1))

        # Generate an initial stock price value using a log-normal distribution
        # The mean and standard deviation of the log-normal distribution are calculated based on the stock_mean and stock_sigma variables
        self.stock_price_history.append(
            np.random.lognormal(np.log(self.stock_mean ** 2 / np.sqrt(self.stock_sigma ** 2 + self.stock_mean ** 2)),
                                np.sqrt(np.log(self.stock_sigma ** 2 / self.stock_mean ** 2 + 1))))

        # Generate an initial bond price value using a log-normal distribution
        # The mean and standard deviation of the log-normal distribution are calculated based on the bond_mean and bond_sigma variables
        self.bond_price_history.append(
            np.random.lognormal(np.log(self.bond_mean ** 2 / np.sqrt(self.bond_sigma ** 2 + self.bond_mean ** 2)),
                                np.sqrt(np.log(self.bond_sigma ** 2 / self.bond_mean ** 2 + 1))))

        # Append a time value of 0 to the time history
        self.time_history.append(0)

        # Generate additional data points by calling the generate_next_data method
        # This populates the price histories further based on the initial data
        for _ in range(12):
            self.generate_next_data()

    def generate_next_data(self) -> None:
        '''
        Generate next data using ARMA(1,1).
        '''

        # Generate next data using ARMA(1,1) for each variable

        # --- Inflation ---
        # Calculate the mean value for the next inflation data point using the ARMA(1,1) coefficients and the current inflation history
        mean = self.inflation_ar_coef * self.inflation_price_history[-1] + (1 - self.inflation_ar_coef) * self.inflation_mean
        inflation_change = self.inflation_price_history[-1] - self.inflation_mean
        fed_rate_change = self.fed_rate_history[-1] - self.fed_rate_mean

        # Calculate the error term by considering the impact of the federal reserve rate and inflation on stock prices
        error = -0.01 * self.fed_rate_history[-1] + np.random.uniform(-0.1, 0.1) - self.stock_fed_rate_coef * fed_rate_change - self.stock_inflation_coef * inflation_change

        # Calculate the moving average term for inflation by multiplying the error term by the inflation moving average coefficient
        ma_term = self.inflation_ma_coef * error

        # Append the next inflation data point to the inflation price history by applying the moving average term, mean, and error
        self.inflation_price_history.append(self.inflation_price_history[-1] * ma_term + mean + error)


        # --- Federal Reserve Rate ---
        # Calculate the mean value for the next federal reserve rate data point using the ARMA(1,1) coefficients, the mean value, and the change in inflation
        mean = self.fed_rate_ar_coef * self.fed_rate_history[-1] + (1 - self.fed_rate_ar_coef) * self.fed_rate_mean + max(-0.025, min(0.025, 0.25 * inflation_change))  # Limit Fed rate variation to 2.5% per year

        # Generate a random uniform error term
        error = np.random.uniform(-0.1, 0.1)

        # Calculate the moving average term for the federal reserve rate by multiplying the error term by the federal reserve rate moving average coefficient
        ma_term = self.fed_rate_ma_coef * error

        # Append the next federal reserve rate data point to the history, ensuring it stays within the range of 0 to 0.1
        self.fed_rate_history.append(max(0, min(self.fed_rate_history[-1] * ma_term + mean + error, 0.1)))


        # --- Stock Prices ---
        # Calculate the mean value for the next stock price data point using the ARMA(1,1) coefficients, the mean value, the change in inflation, and the change in the federal reserve rate
        mean = self.stock_ar_coef * self.stock_price_history[-1] + (1 - self.stock_ar_coef) * self.stock_mean + self.stock_inflation_coef * inflation_change + self.stock_fed_rate_coef * fed_rate_change

        # Generate a random normal error term for stock prices
        error = np.random.normal(0, self.stock_sigma)

        # Calculate the moving average term for stock prices by multiplying the error term by the stock moving average coefficient
        ma_term = self.stock_ma_coef * error

        # Append the next stock price data point to the history by applying the moving average term, mean, and error
        self.stock_price_history.append(self.stock_price_history[-1] * ma_term + mean + error)


        # --- Bond Prices ---
        # Calculate the mean value for the next bond price data point using the ARMA(1,1) coefficients, the mean value, the change in inflation, and the change in the federal reserve rate
        mean = self.bond_ar_coef * self.bond_price_history[-1] + (1 - self.bond_ar_coef) * self.bond_mean + self.bond_inflation_coef * inflation_change + self.bond_fed_rate_coef * fed_rate_change

        # Generate a random normal error term for bond prices
        error = np.random.normal(0, self.bond_sigma)

        # Calculate the moving average term for bond prices by multiplying the error term by the bond moving average coefficient
        ma_term = self.bond_ma_coef * error

        # Append the next bond price data point to the history by applying the moving average term, mean, and error
        self.bond_price_history.append(self.bond_price_history[-1] * ma_term + mean + error)

    def render(self, screen: pygame.Surface) -> None:
        '''
        Render the investment scene on the screen.

        Args:
            screen (pygame.Surface): The surface of the screen to render the scene on.
        '''

        # Draw background
        screen.blit(self.background, (0, 0))
        self.width: int = screen.get_width()  # Get the width of the screen
        self.height: int = screen.get_height()  # Get the height of the screen

        # Calculate portfolio, stock, and bond values
        portfolio_value = self.portfolio.value()
        stock_value = self.portfolio.stock_value()
        bond_value = self.portfolio.bond_value()

        # Draw line graphs for inflation, fed rate, stock price, and bond price
        self.inflation_graph.render(screen, self.inflation_price_history, (self.plot_padding/2, 0 - self.plot_padding/2), 'Inflation', True)
        self.fed_rate_graph.render(screen, self.fed_rate_history, (self.width/2 - self.plot_padding/2, 0 - self.plot_padding/2), 'Fed Rate', True)
        self.stock_price_graph.render(screen, self.stock_price_history, (self.plot_padding/2, self.height/2 - self.plot_padding*1.5), 'Stock price')
        self.bond_price_graph.render(screen, self.bond_price_history, (self.width/2 - self.plot_padding/2, self.height/2 - self.plot_padding*1.5), 'Bond price')

        # Draw additional information about the investment scene
        linewidth = 25
        screen.blit(self.sfont.render("Quarter: {}".format(self.current_period), True, WHITE), (self.plot_padding, self.height - self.plot_padding*2))
        screen.blit(self.sfont.render("Portfolio Value: ${:.3f}".format(portfolio_value), True, WHITE), (self.width/3, self.height - self.plot_padding*2))
        screen.blit(self.sfont.render("Cash: ${:.3f}".format(self.portfolio.money), True, WHITE), (self.plot_padding, self.height - self.plot_padding*2 + linewidth))
        screen.blit(self.sfont.render("Stocks: {:.3f}".format(stock_value), True, WHITE), (self.width/3, self.height - self.plot_padding*2 + linewidth))
        screen.blit(self.sfont.render("Bonds: {:.3f}".format(bond_value), True, WHITE), (self.width*2/3, self.height - self.plot_padding*2 + linewidth))
        stock_weight, bond_weight, cash_weight = self.portfolio.weights()
        screen.blit(self.sfont.render("Cash weight: {:.2f}%".format(cash_weight * 100), True, WHITE), (self.plot_padding, self.height - self.plot_padding*2 + linewidth*2))
        screen.blit(self.sfont.render("Stock weight: {:.2f}%".format(stock_weight * 100), True, WHITE), (self.width/3, self.height - self.plot_padding*2 + linewidth*2))
        screen.blit(self.sfont.render("Bond weight: {:.2f}%".format(bond_weight * 100), True, WHITE),(self.width*2/3, self.height - self.plot_padding*2 + linewidth*2))

        # Update the screen to display the rendered investment scene
        pygame.display.update()

    def update(self, screen: pygame.Surface) -> None:
        '''
        Update the investment scene.
        '''
        pass

    def handle_events(self, event: pygame.event.Event, screen: pygame.Surface) -> None:
        '''
        Handle the events for the investment scene.

        Args:
            event (pygame.event.Event): Event to handle.
            screen (pygame.Surface): Surface of the screen.
        '''
        # Check for events
        for e in event:
            if e.type == pygame.QUIT:
                QuitGame()  # User clicked the close button, quit the game
            elif e.type == pygame.USEREVENT + 1:  # Timer event
                if self.current_period < self.MAX_PERIODS:
                    self.current_period += 1
                    self.generate_next_data()  # Generate next set of data
                else:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop the timer event

            elif e.type == pygame.KEYDOWN:
                total_value = self.portfolio.value()  # Get total value of the portfolio
                change_amount = total_value * 0.1  # Calculate change amount as 10% of total value

                if e.key == pygame.K_s:
                    self.portfolio.buy_stock(change_amount)  # Buy stocks with the change amount
                elif e.key == pygame.K_b:
                    self.portfolio.buy_bond(change_amount)  # Buy bonds with the change amount
                elif e.key == pygame.K_c:
                    self.portfolio.increase_cash(change_amount)  # Increase cash with the change amount

            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                if self.current_period < self.MAX_PERIODS:
                    self.current_period += 1
                    self.generate_next_data()  # Generate next set of data
                else:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Stop the timer event

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.manager.go_to(PauseMenuScene(screen))  # Switch to the PauseMenuScene

            if self.current_period == self.MAX_PERIODS:
                final_port = self.portfolio.value()  # Get final portfolio value
                if final_port >= self.port_to_win:
                    self.manager.go_to(EndScene(screen, True, final_port))  # Switch to EndScene with win status and final portfolio value
                else:
                    self.manager.go_to(EndScene(screen, False, final_port))  # Switch to EndScene with lose status and final portfolio value

class EndScene:
    def __init__(self, screen, won, final_portfolio_value):
        '''
        Initialize the EndScene object.

        Args:
            screen (pygame.Surface): The screen surface to render the end scene on.
            won (bool): Indicates whether the player won or lost the game.
            final_portfolio_value (float): The final value of the player's portfolio.
        '''
        self.save_state = False  # Flag to indicate if the game state should be saved
        self.sfont = pygame.font.SysFont(FONT_NAME, 17)  # Font for rendering text
        self.background = LoadSprite('Background', False)  # Background image
        self.rootdir = os.path.split(os.path.abspath(__file__))[0]  # Root directory of the game
        self.width = screen.get_width()  # Width of the screen
        self.height = screen.get_height()  # Height of the screen
        self.final_portfolio_value = final_portfolio_value  # The final value of the player's portfolio

        # Set the appropriate message and background music based on whether the player won or lost
        if won:
            pygame.mixer.music.load(self.rootdir + "//assets//sounds//background.mp3")
            self.message = f"You WON! Final portfolio value: ${final_portfolio_value:.2f}"
        else:
            pygame.mixer.music.load(self.rootdir + "//assets//sounds//background.mp3")
            self.message = f"You LOST! Final portfolio value: ${final_portfolio_value:.2f}"

        pygame.mixer.music.play(-1)  # Play the background music indefinitely

    def render(self, screen):
        '''
        Render the end scene on the screen.

        Args:
            screen (pygame.Surface): The screen surface to render the end scene on.
        '''
        screen.blit(self.background, (0, 0))  # Draw the background image
        # Oscillating text size for a 'pulsating' effect
        size = (pygame.time.get_ticks() % 1000) / 100 + 17
        font = pygame.font.SysFont(FONT_NAME, int(size))
        text = font.render(self.message, True, WHITE)  # Render the end scene message
        text_rect = text.get_rect(center=(self.width / 2, self.height / 2))
        screen.blit(text, text_rect)  # Draw the text on the screen at the center

    def handle_events(self, event, screen):
        '''
        Handle the events for the end scene.

        Args:
            event (pygame.event.Event): The event to handle.
            screen (pygame.Surface): The screen surface.
        '''
        for e in event:
            if e.type == pygame.QUIT:
                QuitGame()  # Quit the game if the window is closed

    def update(self, screen):
        '''
        Update the end scene.

        Args:
            screen (pygame.Surface): The screen surface.
        '''
        pass  # No updates needed for the end scene

class PauseMenuScene:
    def __init__(self, screen):
        '''
        Initialize the PauseMenuScene object.

        Args:
            screen (pygame.Surface): The screen surface to render the pause menu scene on.
        '''
        self.save_state = False  # Flag to indicate if the game state should be saved
        self.rootdir = os.path.split(os.path.abspath(__file__))[0]  # Root directory of the game
        self.menu_items = ['Resume', 'Options', 'Restart', 'Quit Game']  # Menu items
        self.sfont = pygame.font.SysFont(FONT_NAME, 28)  # Font for rendering menu text
        self.background = LoadSprite('Background', False)  # Background image
        self.width = screen.get_width()  # Width of the screen
        self.height = screen.get_height()  # Height of the screen
        self.menu_colors = [(25, 25, 25) for _ in self.menu_items]  # Initial color for menu items
        self.hover_sound = pygame.mixer.Sound(self.rootdir + "//assets//sounds//mouse_hover.mp3")  # Sound effect for menu item hover

        self.menu_rects = [pygame.Rect(self.width/2 - 70, self.height/2 + i*50 - 70, 140, 40) for i in range(len(self.menu_items))]  # Rectangles for menu items

    def render(self, screen):
        '''
        Render the pause menu scene on the screen.

        Args:
            screen (pygame.Surface): The screen surface to render the pause menu scene on.
        '''
        screen.blit(self.background, (0, 0))  # Draw the background image
        for i, rect in enumerate(self.menu_rects):
            pygame.draw.rect(screen, self.menu_colors[i], rect)  # Draw the menu item rectangle
            pygame.draw.rect(screen, WHITE, rect, 2)  # Draw the outline of the menu item rectangle
            text = self.sfont.render(self.menu_items[i], True, WHITE)  # Render the menu item text
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)  # Draw the menu item text on the screen

    def handle_events(self, events, screen):
        '''
        Handle the events for the pause menu scene.

        Args:
            events (list): The list of events to handle.
            screen (pygame.Surface): The screen surface.
        '''
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                QuitGame()  # Quit the game if the window is closed
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(self.menu_rects):
                    if rect.collidepoint(mouse_pos):
                        if self.menu_items[i] == 'Resume':
                            self.manager.go_to(self.manager.get_stored_scene())  # Go back to the previous scene
                        elif self.menu_items[i] == 'Options':
                            self.manager.go_to(OptionsScene(screen, return_scene=self))  # Go to the options scene
                        elif self.menu_items[i] == 'Restart':
                            self.manager.restart_game(screen)  # Restart the game
                        elif self.menu_items[i] == 'Quit Game':
                            QuitGame()  # Quit the game

    def update(self, screen):
        '''
        Update the pause menu scene.

        Args:
            screen (pygame.Surface): The screen surface.
        '''
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.menu_rects):
            if rect.collidepoint(mouse_pos):
                if self.menu_colors[i] != (50, 50, 50):
                    self.menu_colors[i] = (50, 50, 50)  # Change the color of the menu item when hovered
                    self.hover_sound.play()  # Play the hover sound effect
            else:
                self.menu_colors[i] = (25, 25, 25)  # Reset the color of the menu item if not hovered

class OptionsScene:
    def __init__(self, screen, return_scene=None):
        '''
        Initialize the OptionsScene object.

        Args:
            screen (pygame.Surface): The screen surface to render the options scene on.
            return_scene (object, optional): The scene to return to when the "Return" button is clicked. Defaults to None.
        '''
        self.save_state = False  # Flag to indicate if the game state should be saved
        self.sfont = pygame.font.SysFont(FONT_NAME, 20)  # Font for rendering text
        self.background = LoadSprite('Background', False)  # Background image
        self.width = screen.get_width()  # Width of the screen
        self.height = screen.get_height()  # Height of the screen
        self.return_scene = return_scene  # Scene to return to
        self.return_button = pygame.Rect(self.width/2 - 70, self.height - 50, 140, 40)  # Rectangle for the "Return" button

    def render(self, screen):
        '''
        Render the options scene on the screen.

        Args:
            screen (pygame.Surface): The screen surface to render the options scene on.
        '''
        screen.blit(self.background, (0, 0))  # Draw the background image
        controls = ["s: Increase Stock weight by 10% of portfolio",
                    "b: Increase Bond weight by 10% of portfolio",
                    "c: Increase Cash weight by 10% of portfolio",
                    "Enter: Update period",
                    "Esc: Pause game"]

        for i, control in enumerate(controls):
            text = self.sfont.render(control, True, WHITE)  # Render the control text
            screen.blit(text, (self.width / 4, self.height / 4 + i * 25))  # Draw the control text on the screen
        pygame.draw.rect(screen, (25, 25, 25), self.return_button)  # Draw the "Return" button rectangle
        pygame.draw.rect(screen, WHITE, self.return_button, 2)  # Draw the outline of the "Return" button rectangle
        text = self.sfont.render("Return", True, WHITE)  # Render the "Return" button text
        text_rect = text.get_rect(center=self.return_button.center)
        screen.blit(text, text_rect)  # Draw the "Return" button text on the screen

    def handle_events(self, events, screen):
        '''
        Handle the events for the options scene.

        Args:
            events (list): The list of events to handle.
            screen (pygame.Surface): The screen surface.
        '''
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                QuitGame()  # Quit the game if the window is closed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.return_button.collidepoint(mouse_pos):
                    if self.return_scene:
                        self.manager.go_to(self.return_scene)  # Go back to the return scene

    def update(self, screen):
        '''
        Update the options scene.

        Args:
            screen (pygame.Surface): The screen surface.
        '''
        pass

class TestPortfolio(unittest.TestCase):
    def setUp(self):
        '''
        Set up the test environment for the Portfolio class.
        '''
        self.stock_price_history = [10, 20, 30]
        self.bond_price_history = [100, 200, 300]
        self.money = 1000
        self.stock_share = 10
        self.bond_share = 5
        self.portfolio = Portfolio(self.money, self.stock_price_history, self.bond_price_history,
                                   self.stock_share, self.bond_share)

    def test_portfolio_value(self):
        '''
        Test the calculation of the portfolio value.
        '''
        self.assertEqual(self.portfolio.value(), 1000 + 30 * 10 + 300 * 5)

    def test_portfolio_weights(self):
        '''
        Test the calculation of portfolio weights.
        '''
        weights = self.portfolio.weights()
        self.assertEqual(weights[0], (30 * 10) / (1000 + 30 * 10 + 300 * 5))
        self.assertEqual(weights[1], (300 * 5) / (1000 + 30 * 10 + 300 * 5))
        self.assertEqual(weights[2], 1000 / (1000 + 30 * 10 + 300 * 5))

    def test_portfolio_stock_value(self):
        '''
        Test the calculation of the stock value in the portfolio.
        '''
        self.assertEqual(self.portfolio.stock_value(), 30 * 10)

    def test_portfolio_bond_value(self):
        '''
        Test the calculation of the bond value in the portfolio.
        '''
        self.assertEqual(self.portfolio.bond_value(), 300 * 5)

    def test_portfolio_buy_sell(self):
        '''
        Test the buy and sell operations in the portfolio.
        '''
        # buy stocks
        self.portfolio.buy_stock(300)
        self.assertEqual(self.portfolio.stock_share, 10 + 300 / 30)

        # sell stocks
        self.portfolio.sell_stock(200)
        self.assertEqual(self.portfolio.stock_share, 10 + 300 / 30 - 200 / 30)

        # buy bonds
        self.portfolio.buy_bond(900)
        self.assertEqual(self.portfolio.bond_share, 5 + 900 / 300)

        # sell bonds
        self.portfolio.sell_bond(600)
        self.assertEqual(self.portfolio.bond_share, 5 + 900 / 300 - 600 / 300)

    def test_portfolio_increase_cash(self):
        '''
        Test the increase_cash method in the portfolio.
        '''
        self.portfolio.increase_cash(500)
        self.assertEqual(self.portfolio.money, 1000 + 500)

    def test_portfolio_buy_sell_failure(self):
        '''
        Test the buy and sell operations when they should fail.
        '''
        # attempt to buy more stocks than affordable
        self.portfolio.buy_stock(10000)
        self.assertEqual(self.portfolio.stock_share, 10)  # no change in shares

        # attempt to sell more stocks than owned
        self.portfolio.sell_stock(10000)
        self.assertEqual(self.portfolio.stock_share, 10)  # no change in shares

        # attempt to buy more bonds than affordable
        self.portfolio.buy_bond(100000)
        self.assertEqual(self.portfolio.bond_share, 5)  # no change in bonds

        # attempt to sell more bonds than owned
        self.portfolio.sell_bond(10000)
        self.assertEqual(self.portfolio.bond_share, 5)

if __name__ == '__main__':
    unittest.main()
