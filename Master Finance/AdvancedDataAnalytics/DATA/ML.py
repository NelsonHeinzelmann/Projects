import matplotlib.pyplot as plt
import pickle
import numpy as np
from scenes_ai import InvestmentScene
from tensorflow.keras.models import load_model
import random
ROLLING_WINDOW = 6


def adjust_portfolio(scene, predicted_prices, portfolio_value):
    """
    Adjusts the portfolio based on predicted prices.

    Args:
        scene (InvestmentScene): Investment scene object.
        predicted_prices (ndarray): Predicted prices of assets.
        portfolio_value (float): Current portfolio value.
    """
    current_prices = [scene.get_stock_price(), scene.get_bond_price()]
    current_weights = scene.get_portfolio_weights()
    predicted_returns = (predicted_prices - current_prices) / current_prices

    # Here, we treat negative or zero returns as not desirable, and therefore set their allocation to 0
    predicted_returns = np.where(predicted_returns > 0, predicted_returns, 0)
    sum_returns = np.sum(predicted_returns)

    # If sum_returns is zero, it means none of the assets are expected to have positive returns, we can keep cash in this case
    if sum_returns == 0:
        predicted_weights = [0, 0, 1]  # all weight to cash
    else:
        predicted_weights = np.append(predicted_returns, 0) / sum_returns  # normalize weights
    print("current weights", current_weights)
    print("predicted weights", predicted_weights)

    differences = [pw - cw for pw, cw in zip(predicted_weights, current_weights)]

    for i in range(len(differences)):
        change_amount = differences[i] * portfolio_value
        if differences[i] > 0:
            if i == 0:
                scene.handle_events('buy_stock', change_amount)
            elif i == 1:
                scene.handle_events('buy_bond', change_amount)
        elif differences[i] < 0:
            if i == 0:
                scene.handle_events('sell_stock', -change_amount)
            elif i == 1:
                scene.handle_events('sell_bond', -change_amount)
    scene.handle_events('end_turn', 0)


def preprocess_state_values(state, state_order, scaler):
    """
    Preprocesses state values.

    Args:
        state (dict): State values.
        state_order (list): Order of state keys.
        scaler: Scaler object for state transformation.

    Returns:
        ndarray: Preprocessed state values.
    """
    state_values = np.array([state[key] for key in state_order]).reshape(1, -1)

    # Scale the state values before predicting
    state_values = scaler.transform(state_values)

    return state_values


def run_multiple_games(num_games, model, scaler):
    """
    Runs multiple games and returns the results.

    Args:
        num_games (int): Number of games to run.
        model: Trained model for prediction.
        scaler: Scaler object for state transformation.

    Returns:
        tuple: Final portfolio values and the fraction of winning scenarios.
    """
    game_results = []
    scene = InvestmentScene()
    num_win = 0
    state_order = ['Stock_Price', 'Bond_Price', 'Fed_Rate', 'Inflation']
    pred_prices = []
    curr_prices = []
    for _ in range(num_games):
        print("Game number", _)
        scene.reset_game()
        recent_periods = scene.get_state()[-ROLLING_WINDOW:]  # Initial periods

        for per in range(scene.MAX_PERIODS):  # Starting from the first period
            state_values = np.array([state[key] for state in recent_periods for key in state_order]).reshape(1, -1)
            state_values = scaler.transform(state_values)
            state_values = state_values.reshape(1, ROLLING_WINDOW, -1)
            predicted_prices = model.predict(state_values)
            adjust_portfolio(scene, predicted_prices[0], scene.get_portfolio_value())
            print("Predicted Prices:", predicted_prices)
            print("Current Weights:", scene.get_portfolio_weights())
            print("Portfolio Value:", scene.get_portfolio_value())
            print("Current Bond Prices;", scene.get_bond_price())
            print("Current Stock Prices;", scene.get_stock_price())
            recent_periods.pop(0)  # Remove the oldest period
            recent_periods.append(scene.get_last_state())  # Append the most recent period
            print("Recent var", recent_periods)
            # Move to the next period
            if per < scene.MAX_PERIODS -1:
                pred_prices.append(predicted_prices)
            if per > 0:
                curr_prices.append([scene.get_stock_price(), scene.get_bond_price()])
        if scene.get_portfolio_value() > 500000:
            num_win += 1
        game_results.append(scene.get_portfolio_value())

    percent_win = num_win / num_games
    return game_results, percent_win, pred_prices,curr_prices

def random_games(num_games):
    """
    Runs multiple random games and returns the results.

    Args:
        num_games (int): Number of games to run.

    Returns:
        tuple: Final portfolio values and the fraction of winning scenarios.
    """
    game_results_random = []
    scene = InvestmentScene()
    num_win = 0

    for _ in range(num_games):
        print("Game number", _)
        scene.reset_game()

        for per in range(scene.MAX_PERIODS):
            decision = random.choice(['buy_stock', 'buy_bond', 'increase_cash'])
            change_amount = random.uniform(0.1, 0.4) * scene.get_portfolio_value()

            scene.handle_events(decision, change_amount)
            scene.handle_events("end_turn", 0)

        if scene.get_portfolio_value() > 500000:
            num_win += 1
        game_results_random.append(scene.get_portfolio_value())

    percent_win = num_win / num_games
    return game_results_random, percent_win


# Load the trained model
model = load_model('../DATA/model/model1')

# Load the scaler
scaler_file = '../DATA/model/scaler.pkl'
with open(scaler_file, 'rb') as f:
    scaler = pickle.load(f)

final_portfolio_values, percent_win, pred_list, curr_list = run_multiple_games(100, model, scaler)  # Pass the model to run_multiple_games
random_port, random_percent_win = random_games(100)
print("pred P",pred_list)
print("CURR P",curr_list)
print("LEN pred P",len(pred_list))
print("LEN CURR P",len(curr_list))
percent_win *= 100.00
random_percent_win *= 100
mean_portfolio_value = np.mean(final_portfolio_values)  # Calculate the mean final portfolio value
mean_random_portfolio = np.mean(random_port)
print(f"On average the portfolio value is {mean_portfolio_value} ")
print(f"On the 100 simulated games, {percent_win}% were winning scenarios")
print(f"On average the random portfolio value is {mean_random_portfolio} ")
print(f"On the 100 simulated games of the random model, {random_percent_win}% were winning scenarios")

fig, ax = plt.subplots()
ax.plot(final_portfolio_values, label='Final portfolio value')
ax.axhline(mean_portfolio_value, color='r', linestyle='--', label='Mean value')  # Add a horizontal line for the mean value
ax.axhline(mean_random_portfolio, color='b', linestyle='--', label='Mean random value')
ax.set_xlabel('Game number')
ax.set_ylabel('Final portfolio value')
ax.legend()
plt.tight_layout()

# Save the figure
plt.savefig('pngfiles/portfolio_values.png', dpi=300)

# Show the plot
plt.show()

pred_stock_prices = np.array([price[0][0] for price in pred_list])
pred_bond_prices = np.array([price[0][1] for price in pred_list])
curr_stock_prices = np.array([price[0] for price in curr_list])
curr_bond_prices = np.array([price[1] for price in curr_list])

periods_pred = np.arange(1, pred_stock_prices.shape[0] + 1)
periods_curr = np.arange(1, curr_stock_prices.shape[0] + 1)

fig1, ax1 = plt.subplots()
ax1.plot(periods_curr, curr_bond_prices, label='Actual bond prices')
ax1.plot(periods_pred, pred_bond_prices, label='Predicted bond prices')
ax1.set_xlabel('Periods')
ax1.set_ylabel('Price')
ax1.legend()
plt.savefig('pngfiles/actual_predicted_bond_prices.png', dpi=300)

fig4, ax4 = plt.subplots()
ax4.plot(periods_curr, curr_stock_prices, label='Actual stock prices')
ax4.plot(periods_pred, pred_stock_prices, label='Predicted stock prices')
ax4.set_xlabel('Periods')
ax4.set_ylabel('Price')
ax4.legend()
plt.savefig('pngfiles/actual_predicted_stock_prices.png', dpi=300)

fig2, ax2 = plt.subplots()
ax2.plot(periods_pred, np.abs(pred_bond_prices - curr_bond_prices), label='Absolute difference (bond)')
ax2.set_xlabel('Periods')
ax2.set_ylabel('Absolute Difference In Bond Prices')
plt.savefig('pngfiles/absolute_difference_bond_prices.png', dpi=300)

fig3, ax3 = plt.subplots()
ax3.plot(periods_curr, np.abs(pred_stock_prices - curr_stock_prices), label='Absolute difference (stock)')
ax3.set_xlabel('Periods')
ax3.set_ylabel('Absolute Difference In Stock Prices')
plt.savefig('pngfiles/absolute_difference_stock_prices.png', dpi=300)

plt.show()
