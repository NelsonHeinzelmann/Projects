import numpy as np
import random

class InvestmentScene(object):
    def __init__(self):
        super(InvestmentScene, self).__init__() # Constructor of object class
        self.WAIT_TIME = 200000  # 20 seconds in milliseconds
        self.MAX_PERIODS = 18
        self.current_period = 0
        self.time_step = 0.01
        self.max_time_steps = 300
        self.money = 500000
        self.stock_share = 0
        self.bond_share = 0
        self.stock_price_history = []
        self.bond_price_history = []
        self.inflation_price_history = []
        self.fed_rate_history = []
        self.time_history = []
        self.game_states = []
        self.starting_stock_share = 0
        self.starting_bond_share = 0
        self.starting_money = 500000

        self.inflation_mean = 0.02
        self.inflation_sigma = 0.002
        self.inflation_ar_coef = 0.9
        self.inflation_ma_coef = 0.5

        self.fed_rate_mean = 0.02
        self.fed_rate_sigma = 0.002
        self.fed_rate_ar_coef = 0.6
        self.fed_rate_ma_coef = 0.2

        self.stock_mean = 100
        self.stock_sigma = 0.1
        self.stock_ar_coef = 0.8
        self.stock_ma_coef = 0.1
        self.stock_inflation_coef = 1.5
        self.stock_fed_rate_coef = -2

        self.bond_mean = 200
        self.bond_sigma = 0.1
        self.bond_ar_coef = 0.5
        self.bond_ma_coef = 0.2
        self.bond_inflation_coef = -2.5
        self.bond_fed_rate_coef = -2.5

        self.generate_initial_data()


    def generate_initial_data(self):
        # Generate initial data using log-normal distribution
        self.inflation_price_history.append(random.uniform(0.02, 0.05))
        self.fed_rate_history.append(random.uniform(0, 0.1))
        self.stock_price_history.append(
            np.random.lognormal(np.log(self.stock_mean ** 2 / np.sqrt(self.stock_sigma ** 2 + self.stock_mean ** 2)),
                                np.sqrt(np.log(self.stock_sigma ** 2 / self.stock_mean ** 2 + 1))))
        self.bond_price_history.append(
            np.random.lognormal(np.log(self.bond_mean ** 2 / np.sqrt(self.bond_sigma ** 2 + self.bond_mean ** 2)),
                                np.sqrt(np.log(self.bond_sigma ** 2 / self.bond_mean ** 2 + 1))))
        self.time_history.append(0)
        self.update_game_state()

        for _ in range(11):
            self.handle_events('end_turn', 0)
    def generate_next_data(self):
        # Generate next data using ARMA(1,1)
        # Inflation
        mean = self.inflation_ar_coef * self.inflation_price_history[-1] + (
                1 - self.inflation_ar_coef) * self.inflation_mean
        inflation_change = self.inflation_price_history[-1] - self.inflation_mean
        fed_rate_change = self.fed_rate_history[-1] - self.fed_rate_mean
        stock_price_change = self.stock_price_history[-1] - self.stock_mean
        bond_price_change = self.bond_price_history[-1] - self.bond_mean
        error = -0.01 * self.fed_rate_history[-1] + np.random.uniform(-0.1,
                                                                      0.1) - self.stock_fed_rate_coef * fed_rate_change - self.stock_inflation_coef * inflation_change  # Impact of Fed rate and Inflation on stock prices
        ma_term = self.inflation_ma_coef * error
        self.inflation_price_history.append(self.inflation_price_history[-1] * ma_term + mean + error)

        # Federal Reserve Rate
        mean = self.fed_rate_ar_coef * self.fed_rate_history[-1] + (
                1 - self.fed_rate_ar_coef) * self.fed_rate_mean + max(-0.025, min(0.025,
                                                                                  0.25 * inflation_change))  # Limit Fed rate variation to 2.5% per year
        error = np.random.uniform(-0.1, 0.1)
        ma_term = self.fed_rate_ma_coef * error
        self.fed_rate_history.append(max(0, min(self.fed_rate_history[-1] * ma_term + mean + error, 0.1)))

        # Stock Prices
        mean = self.stock_ar_coef * self.stock_price_history[-1] + (1 - self.stock_ar_coef) * self.stock_mean + \
               self.stock_inflation_coef * inflation_change + \
               self.stock_fed_rate_coef * fed_rate_change

        error = np.random.normal(0, self.stock_sigma)
        ma_term = self.stock_ma_coef * error
        self.stock_price_history.append(self.stock_price_history[-1] * ma_term + mean + error)

        # Bond Prices
        mean = self.bond_ar_coef * self.bond_price_history[-1] + (1 - self.bond_ar_coef) * self.bond_mean + \
               self.bond_inflation_coef * inflation_change + \
               self.bond_fed_rate_coef * fed_rate_change

        error = np.random.normal(0, self.bond_sigma)
        ma_term = self.bond_ma_coef * error
        self.bond_price_history.append(self.bond_price_history[-1] * ma_term + mean + error)
        # self.update_game_state()

    def render(self, screen):
        pass
    def update(self, screen):
        pass

    def handle_events(self, action, change_amount):
        if action == 'buy_stock':
            self.buy_stock(change_amount)
            #print("Buy stock")
        elif action == 'sell_stock':
            self.sell_stock(change_amount)
            #print("Sell stock")
        elif action == 'buy_bond':
            self.buy_bond(change_amount)
            #print("Buy bond")
        elif action == 'sell_bond':
            self.sell_bond(change_amount)
            #print("Sell bond")
        elif action == 'increase_cash':
            self.increase_cash(change_amount)
            #print("Increase cash")
        elif action == 'decrease_cash':
            self.decrease_cash(change_amount)
            #print("Decrease cash")
        elif action == 'end_turn':
            if self.current_period < self.MAX_PERIODS + 12:
                self.current_period += 1
                self.generate_next_data()
                self.update_game_state()

    def portfolio_value(self):
        stock_value = self.stock_share * self.stock_price_history[-1]
        bond_value = self.bond_share * self.bond_price_history[-1]
        return self.money + stock_value + bond_value

    def portfolio_weights(self):
        total_value = self.portfolio_value()
        stock_weight = self.stock_share * self.stock_price_history[-1] / total_value
        bond_weight = self.bond_share * self.bond_price_history[-1] / total_value
        cash_weight = self.money / total_value
        return stock_weight, bond_weight, cash_weight

    def get_portfolio_weights(self):
        # Returns the current portfolio weights
        return self.portfolio_weights()

    def get_state(self):
        return self.game_states

    def get_last_state(self):
        return self.game_states[-1]


    def get_portfolio_value(self):
        stock_value = self.stock_share * self.stock_price_history[-1]
        bond_value = self.bond_share * self.bond_price_history[-1]
        portfolio_value = self.money + stock_value + bond_value
        return portfolio_value

    def reset_game(self):
        self.inflation_price_history = []
        self.fed_rate_history = []
        self.stock_price_history = []
        self.bond_price_history = []
        self.time_history = []
        self.game_states = []
        self.current_period = 0
        self.money = self.starting_money
        self.stock_share = self.starting_stock_share
        self.bond_share = self.starting_bond_share
        self.generate_initial_data()

    def get_stock_price(self):
        return self.stock_price_history[-1]

    def get_bond_price(self):
        return self.bond_price_history[-1]

    def update_game_state(self):
        # Calculate portfolio values and weights
        # self.current_period += 1

        stock_value = self.stock_share * self.stock_price_history[-1]
        bond_value = self.bond_share * self.bond_price_history[-1]
        portfolio_value = self.money + stock_value + bond_value
        stock_weight, bond_weight, cash_weight = self.portfolio_weights()
        # Append the updated state
        self.game_states.append({
            'Period': self.current_period,
            'Stock_Price': self.stock_price_history[-1],
            'Bond_Price': self.bond_price_history[-1],
            'Fed_Rate': self.fed_rate_history[-1],
            'Inflation': self.inflation_price_history[-1],
            'Cash': self.money,
            'Stock_Value': stock_value,
            'Bond_Value': bond_value,
            'Portfolio_Value': portfolio_value,
            'Stock_Weight': stock_weight,
            'Bond_Weight': bond_weight,
            'Cash_Weight': cash_weight
        })
    def stock_value(self):
        """
        Calculate and return the value of the stocks in the portfolio.
        """
        return self.stock_share * self.get_stock_price()
    def bond_value(self):
        """
        Calculate and return the value of the bonds in the portfolio.
        """
        return self.bond_share * self.get_bond_price()

    def buy_stock(self, amount):
        """
        Buy stocks with the given amount of money.
        """
        stock_price = self.get_stock_price()
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
                pass
                #print("Not enough money or bonds to buy stocks.")

    def buy_bond(self, amount):
        """
        Buy bonds with the given amount of money.
        """
        bond_price = self.get_bond_price()
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
                pass
                #print("Not enough money or stocks to buy bonds.")

    def sell_stock(self, amount):
        """
        Sell stocks for the given amount of money.
        """
        stock_price = self.get_stock_price()
        shares_to_sell = amount / stock_price
        if self.stock_share >= shares_to_sell:
            self.stock_share -= shares_to_sell
            self.money += amount
        else:
            pass
            #print("Not enough stocks to sell.")

    def sell_bond(self, amount):
        """
        Sell bonds for the given amount of money.
        """
        bond_price = self.get_bond_price()
        shares_to_sell = amount / bond_price
        if self.bond_share >= shares_to_sell:
            self.bond_share -= shares_to_sell
            self.money += amount
        else:
            pass
            #print("Not enough bonds to sell.")

    def increase_cash(self,change_amount):
        if self.stock_value() >= change_amount/2 and self.bond_value() >= change_amount/2:
            self.sell_stock(change_amount/2)
            self.sell_bond(change_amount/2)
        elif self.stock_value() < change_amount/2 <= self.bond_value():
            if self.bond_value() >= change_amount - self.stock_value():
                change = change_amount - self.stock_value()
                self.sell_stock(self.stock_value())
                self.sell_bond(change)
            else:
                self.sell_stock(self.stock_value())
                self.sell_bond(self.bond_value())

        elif self.bond_value() < change_amount/2 <= self.stock_value():
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

