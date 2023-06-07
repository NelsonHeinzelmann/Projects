import random
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


class DataProcessing:
    '''Data Processing class for generating and preprocessing game data.

    This class generates data by simulating games and preprocesses the
    generated data to be used for model training.

    Attributes:
        scene (object): An instance of the game scene.
        n_periods (int): Maximum number of periods in the game.
        scaler_X (MinMaxScaler): Scaler used to normalize input data.
    '''

    def __init__(self, scene,rolling_window):
        '''Initialize the data processing class with the given scene and rolling window.'''
        self.scene = scene
        self.n_periods = self.scene.MAX_PERIODS
        self.scaler_X = MinMaxScaler()
        self.rolling_window = rolling_window

    def generate_data(self, num_games=20000):
        '''Generate data by simulating a number of games (Monte Carlo simulation).

        Args:
            num_games (int): The number of games to simulate.

        Returns:
            list: A list of game data, each element representing a game.
        '''
        data_list = []

        for i in range(num_games):
            self.scene.reset_game()
            game_data = []
            print(f'Game {i + 1}/{num_games}', end='\r')

            for _ in range(self.n_periods):
                decision = random.choice(['buy_stock', 'buy_bond', 'increase_cash'])
                total_value = self.scene.get_portfolio_value()
                np.array(self.scene.get_portfolio_weights()).reshape(1, -1)
                change = random.uniform(0.1, 0.4)
                change_amount = total_value * change

                self.scene.handle_events(decision, change_amount)
                self.scene.handle_events("end_turn", 0)

            game_states = self.scene.get_state()

            if isinstance(game_states, list):
                game_data.extend(game_states)
            elif isinstance(game_states, dict):
                game_data.append(game_states)
            else:
                raise ValueError('Unexpected type for game_states')

            data_list.append(game_data)

        return data_list

    def get_train_test_split(self, test_size=0.2, random_state=42):
        '''Generate train and test splits from the game data.

        Args:
            test_size (float): Proportion of the dataset to include in the test split.
            random_state (int): Random seed for train-test split.

        Returns:
            tuple: Numpy arrays for X_train, X_test, y_train, y_test.
        '''
        print('Generating data')
        games_data = self.generate_data()
        print('Done generating data')
        print('Generating training examples')

        X = []
        y = []

        nb_games = len(games_data)
        for i, game_data in enumerate(games_data):
            game_data_df = pd.DataFrame(game_data)
            print(f'Game {i + 1}/{nb_games}', end='\r')
            for j in range(self.rolling_window, len(game_data_df)):
                X.append(game_data_df.iloc[j - self.rolling_window:j][['Stock_Price', 'Bond_Price', 'Fed_Rate', 'Inflation']].values)
                y.append(game_data_df.iloc[j][['Stock_Price','Bond_Price']].values)

        X = np.array(X)
        y = np.array(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        # We fit first to make sure there is no difference in the scaling
        X_train = self.scaler_X.fit_transform(X_train.reshape(X_train.shape[0], -1)).reshape(X_train.shape)
        X_test = self.scaler_X.transform(X_test.reshape(X_test.shape[0], -1)).reshape(X_test.shape)


        return X_train, X_test, y_train, y_test
