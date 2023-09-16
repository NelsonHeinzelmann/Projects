# Title
Advanced Data Analytics Coursework : LSTM Model to predict returns in a trading game : May-June 2023

# How to
To run this model please refer to the RunningTheCode.txt file in the /Data folder

# Overview
Abstract:
This paper presents an AI that aims to predict the optimal prices in our trading game developed in the Advanced Programming class. The trading game involves investment decisions of a portfolio consisting of bonds, stocks, and cash based on four variable pieces of information: inflation, Fed rate, bond prices, and stock prices. The player has to adjust the weights of the portfolio at each period to attain a maximal return at the last period of the game. The main challenge is that these variables are randomly generated each game, and thus creating new optimal decisions for each game. The AI needs to process large amounts of data to determine the best portfolio prices. Our objective is to develop an LSTM model that utilizes the current state of the four primary variables to forecast future prices. To achieve this, we employ a rolling window technique to consider past values. Additionally, since our game is implemented in Python, we will utilize TensorFlow for its development. Despite notably elevated Mean Squared Error (MSE) and Mean Absolute Error (MAE) values, particularly in the case of bond prices, our LSTM model still significantly outperforms a random decision model. 

