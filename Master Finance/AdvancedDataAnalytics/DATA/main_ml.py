# Importing necessary libraries
import tensorflow as tf
import pickle
from data_processing import DataProcessing
from nn_model import create_model
from train_model import train_model, test_model
from scenes_ai import InvestmentScene
import keras_tuner as kt

OPTIMIZER = 'adam'
LOSS = 'mean_squared_error'

'''Neural network with two layers, with respectively 64 and 32 nodes.'''
LAYERS = [64,32]

'''Each node is given a 20% chance of being turned off at each training step.'''
DROPOUT = 0.20



# Function to save the model and scaler
def save_model_and_scaler(model, scaler, model_path, scaler_path):
    '''Save the model and scaler.

    Args:
        model (Model): The model to save.
        scaler (Scaler): The scaler to save.
        model_path (str): The path where the model should be saved.
        scaler_path (str): The path where the scaler should be saved.
    '''
    model.save(model_path)

    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)


# Function to load the model and scaler
def load_model_and_scaler(model_path, scaler_path):
    '''Load the model and scaler.

    Args:
        model_path (str): The path from where the model should be loaded.
        scaler_path (str): The path from where the scaler should be loaded.

    Returns:
        tuple: The loaded model and scaler.
    '''
    model = tf.keras.models.load_model(model_path)

    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    return model, scaler


# Create the investment scene
print('Create scene')
scene = InvestmentScene()

# Start data processing
print('Start data processing')
data_processing = DataProcessing(scene, rolling_window=6)

# From here on the version you can use to test that our code runs correctly
# The Hyper-tuning Method we used to train the model can be found bellow, and is commented out
# Also to avoid overriding the actual trained model, we commented out the saving part
# We have hardcoded the optimal param we found for our model when doing the tuning method

# Get the training and testing data
X_train, X_test, y_train, y_test = data_processing.get_train_test_split()
print('Ending data processing...')

# Get the shape of the input data
input_shape = (X_train.shape[1], X_train.shape[2])
print('End data processing')

# Create the model
print('Create model')
model = create_model(input_shape, LAYERS, DROPOUT, OPTIMIZER, LOSS)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,  # number of epochs with no improvement after which training will be stopped
    restore_best_weights=True
)
# Train the model
print('Train model')
train_model(model, X_train, y_train, epochs=100, callbacks=[early_stopping])

# Test the model
print('Test model')
test_model(model, X_test, y_test)

# Here the Saving part that has been commented out to avoid overriding the saved model when testing our code
# # Save the model and scaler
# print('Save model')
# save_model_and_scaler(model, data_processing.scaler_X, '../DATA/model/model1', '../DATA/model/scaler.pkl')
# print('Model saved')
#
# # Load the saved model and scaler
# model, scaler = load_model_and_scaler('../DATA/model/model1', '../DATA/model/scaler.pkl')


# This is the Version with Hyper-tuning of the Parameters, we trained the model using this code part
# You can find th output of the console as a .pdf in the .tar folder
# X_train, X_test, y_train, y_test = data_processing.get_train_test_split()
# print('Ending data processing...')
#
# # Get the shape of the input data
# input_shape = (X_train.shape[1], X_train.shape[2])
# print('End data processing')
#
# def model_builder(hp):
#     layers = []
#     for i in range(hp.Int('num_layers', 1, 3)):
#         layers.append(hp.Choice(f'layer_{i+1}_units', values=[16, 32, 64, 128]))
#     dropout = hp.Float('dropout', 0, 0.5, step=0.1)
#     model = create_model(input_shape, layers, dropout, OPTIMIZER, LOSS)
#     return model
#
# # Keras Tuner's RandomSearch
# tuner = kt.RandomSearch(
#     model_builder,
#     objective='val_loss',
#     max_trials=32,  # Number of models to test
# )
#
# # Define early stopping
# early_stopping = tf.keras.callbacks.EarlyStopping(
#     monitor='val_loss',
#     patience=3,  # number of epochs with no improvement after which training will be stopped
#     restore_best_weights=True
# )
#
# # Start the hyperparameter tuning
# tuner.search(X_train, y_train, epochs=100, validation_data=(X_test, y_test), callbacks=[early_stopping])
#
# # Get the best hyperparameters
# best_hps = tuner.get_best_hyperparameters()[0]
#
# print('The hyperparameters of the best model are:')
# print(best_hps.values)
#
# # Rebuild the model with the best hyperparameters
# model = tuner.hypermodel.build(best_hps)
#
# # Train the model
# print('Train model')
# history = train_model(model, X_train, y_train, epochs=100, callbacks=[early_stopping])
#
# # Test the model
# print('Test model')
# test_model(model, X_test, y_test)
#
# # Save the model and scaler
# print('Save model')
# save_model_and_scaler(model, data_processing.scaler_X, '../DATA/model/model1', '../DATA/model/scaler.pkl')
# print('Model saved')
#
# # Load the saved model and scaler
# model, scaler = load_model_and_scaler('../DATA/model/model1', '../DATA/model/scaler.pkl')
