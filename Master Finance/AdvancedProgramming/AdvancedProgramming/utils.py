import sys
from pathlib import Path
import pygame
from pygame.image import load

# Initialize the game screen with the specified size and title
def InitGame(screensize, title):
    '''
    Initialize the game screen with the specified size and title.

    Args:
        screensize (tuple): Size of the game screen.
        title (str): Title of the game window.

    Returns:
        pygame.Surface: The game screen surface.
    '''
    pygame.init()
    screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)
    pygame.display.set_caption(title)
    return screen

# Quit the game and optionally quit pygame
def QuitGame(use_pygame=True):
    '''
    Quit the game and optionally quit pygame.

    Args:
        use_pygame (bool, optional): Whether to quit pygame. Defaults to True.
    '''
    if use_pygame:
        pygame.quit()
    sys.exit()

# Load a sprite image with the specified filename and return it as a pygame Surface object
def LoadSprite(name, with_alpha=True):
    '''
    Load a sprite image with the specified filename and return it as a pygame Surface object.

    Args:
        name (str): Name of the sprite image file.
        with_alpha (bool, optional): Whether to include alpha channel. Defaults to True.

    Returns:
        pygame.Surface: The loaded sprite image surface.
    '''
    filename = Path(__file__).parent / Path("assets/sprites/" + name + ".png")
    sprite = load(filename.resolve())
    if with_alpha:
        return sprite.convert_alpha()
    return sprite.convert()

# Split the text into lines that fit within the specified rectangle using the specified font
def TextScroller(text: str, text_rect, font) -> list:
    '''
    Split the text into lines that fit within the specified rectangle using the specified font.

    Args:
        text (str): The text to split into lines.
        text_rect (pygame.Rect): The rectangle to fit the lines within.
        font (pygame.font.Font): The font to use for rendering the text.

    Returns:
        list: The list of lines that fit within the rectangle.
    '''
    # Split the text into individual lines
    lines = text.split('\n')
    # Split each line into individual words
    words = [line.split() for line in lines]
    # Create a list to hold the final lines
    final_lines = []
    # Loop through each line in the text
    for line in words:
        line_length = 0
        line_words = []
        # Loop through each word in the line
        for word in line:
            # Calculate the length of the current word, plus a space
            word_length = font.size(word + ' ')[0]
            # If adding the current word would exceed the maximum line width,
            # append the current line to the final lines list and start a new line
            if line_length + word_length > text_rect.width:
                final_lines.append(' '.join(line_words))
                line_length = 0
                line_words = []
            # Add the current word to the current line
            line_words.append(word)
            line_length += word_length
        # Append the final line to the final lines list
        final_lines.append(' '.join(line_words))
    # Return the list of final lines
    return final_lines

class Portfolio:
    '''
    Portfolio class representing a collection of stocks, bonds, and money.
    '''
    def __init__(self, money, stock_price_history, bond_price_history, stock_share=0, bond_share=0):
        '''
        Initialize the Portfolio class.

        Args:
            money (float): Amount of money in the portfolio.
            stock_price_history (list): List of historical stock prices.
            bond_price_history (list): List of historical bond prices.
            stock_share (float, optional): Number of shares of stocks. Defaults to 0.
            bond_share (float, optional): Number of shares of bonds. Defaults to 0.

        Raises:
            ValueError: If the price history for stocks or bonds is empty.
        '''
        self.money = money
        self.stock_share = stock_share
        self.bond_share = bond_share
        self._stock_price_history = stock_price_history
        self._bond_price_history = bond_price_history

        if not self._stock_price_history or not self._bond_price_history:
            raise ValueError('Price history for stocks and bonds should not be empty')

    def value(self):
        '''
        Calculate and return the total value of the portfolio.

        Returns:
            float: Total value of the portfolio.
        '''
        return self.money + self.stock_value() + self.bond_value()

    def weights(self):
        '''
        Calculate and return the weights of the stocks, bonds, and cash in the portfolio.

        Returns:
            tuple: Tuple containing the weights of stocks, bonds, and cash.
        '''
        total_value = self.value()
        weights = [
            (value / total_value if total_value != 0 else 0)
            for value in [self.stock_value(), self.bond_value(), self.money]
        ]
        return tuple(weights)

    def stock_value(self):
        '''
        Calculate and return the value of the stocks in the portfolio.

        Returns:
            float: Value of the stocks in the portfolio.
        '''
        return self.stock_share * self._stock_price_history[-1]

    def bond_value(self):
        '''
        Calculate and return the value of the bonds in the portfolio.

        Returns:
            float: Value of the bonds in the portfolio.
        '''
        return self.bond_share * self._bond_price_history[-1]

    def buy_stock(self, amount):
        '''
        Buy stocks with the given amount of money.

        Args:
            amount (float): Amount of money to spend on buying stocks.
        '''
        stock_price = self._stock_price_history[-1]
        shares_to_buy = amount / stock_price
        if self.money >= amount:
            self.money -= amount
            self.stock_share += shares_to_buy
        else:
            amount_required = amount - self.money
            self.sell_bond(amount_required)  # sell enough bonds to afford the stock
            if self.money >= amount:  # check if you now have enough money
                self.money -= amount
                self.stock_share += shares_to_buy
            else:
                print('Not enough money or bonds to buy stocks.')

    def buy_bond(self, amount):
        '''
        Buy bonds with the given amount of money.

        Args:
            amount (float): Amount of money to spend on buying bonds.
        '''
        bond_price = self._bond_price_history[-1]
        shares_to_buy = amount / bond_price
        if self.money >= amount:
            self.money -= amount
            self.bond_share += shares_to_buy
        else:
            amount_required = amount - self.money
            self.sell_stock(amount_required)  # sell enough stocks to afford the bond
            if self.money >= amount:  # check if you now have enough money
                self.money -= amount
                self.bond_share += shares_to_buy
            else:
                print('Not enough money or stocks to buy bonds.')

    def sell_stock(self, amount):
        '''
        Sell stocks for the given amount of money.

        Args:
            amount (float): Amount of money to receive from selling stocks.
        '''
        stock_price = self._stock_price_history[-1]
        shares_to_sell = amount / stock_price
        if self.stock_share >= shares_to_sell:
            self.stock_share -= shares_to_sell
            self.money += amount
        else:
            print('Not enough stocks to sell.')

    def sell_bond(self, amount):
        '''
        Sell bonds for the given amount of money.

        Args:
            amount (float): Amount of money to receive from selling bonds.
        '''
        bond_price = self._bond_price_history[-1]
        shares_to_sell = amount / bond_price
        if self.bond_share >= shares_to_sell:
            self.bond_share -= shares_to_sell
            self.money += amount
        else:
            print('Not enough bonds to sell.')

    def increase_cash(self, change_amount):
        '''
        Increase the amount of cash in the portfolio by selling stocks and bonds.

        Args:
            change_amount (float): Amount of cash to increase by.
        '''
        if self.stock_value() >= change_amount / 2 and self.bond_value() >= change_amount / 2:
            self.sell_stock(change_amount / 2)
            self.sell_bond(change_amount / 2)
        elif self.stock_value() < change_amount / 2 <= self.bond_value():
            if self.bond_value() >= change_amount - self.stock_value():
                change = change_amount - self.stock_value()
                self.sell_stock(self.stock_value())
                self.sell_bond(change)
            else:
                self.sell_stock(self.stock_value())
                self.sell_bond(self.bond_value())
        elif self.bond_value() < change_amount / 2 <= self.stock_value():
            if self.stock_value() >= change_amount - self.bond_value():
                change = change_amount - self.bond_value()
                self.sell_bond(self.bond_value())
                self.sell_stock(change)
            else:
                self.sell_stock(self.stock_value())
                self.sell_bond(self.bond_value())
        else:
            self.sell_bond(self.bond_value())
            self.sell_stock(self.stock_value())
