import tensorflow as tf

def create_model(input_shape, layers=[128, 64, 32], dropout_rate=0.25, optimizer='adam', loss='mean_squared_error'):
    '''Create a Sequential LSTM model.

    This function creates a Keras Sequential model with LSTM layers for time series prediction.

    Args:
        input_shape (tuple): Shape of the input data.
            It's a tuple of the form (timesteps, features).
        layers (list): List of layer sizes for the LSTM layers. Default is [128, 64, 32].
        dropout_rate (float): The rate for dropout layers to avoid overfitting. Default is 0.25.
        optimizer (str): The optimizer to use for training the model. Default is 'adam'.
        loss (str): The loss function to use for training the model. Default is 'mean_squared_error'.

    Returns:
        model (tf.keras.Sequential): A compiled Keras model.
    '''
    model = tf.keras.models.Sequential(name='LSTM_Model')
    # Use of name was for Tensorboard debugging
    # Add the first LSTM layer with input shape
    model.add(tf.keras.layers.LSTM(layers[0], return_sequences=True, input_shape=input_shape, name='LSTM_1'))
    model.add(tf.keras.layers.Dropout(dropout_rate, name='Dropout_1'))

    # Add additional LSTM layers
    for i, layer_size in enumerate(layers[1:-1], start=2):
        model.add(tf.keras.layers.LSTM(layer_size, return_sequences=True, name=f'LSTM_{i}'))
        model.add(tf.keras.layers.Dropout(dropout_rate, name=f'Dropout_{i}'))

    # The last LSTM layer should not return sequences
    model.add(tf.keras.layers.LSTM(layers[-1], name='LSTM_Final'))

    # Final Dense layer to produce output
    model.add(tf.keras.layers.Dense(2, activation='linear', name='Dense_Output'))

    # Compile the model with the given optimizer and loss function
    model.compile(loss=loss, optimizer=optimizer)

    return model
