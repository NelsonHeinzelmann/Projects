import datetime
from matplotlib import pyplot as plt
import tensorflow as tf
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def train_model(model, X_train, y_train, epochs=100, batch_size=32, val_split=0.2,callbacks=None):
    '''Train the model and display a plot of training and validation loss.

    Args:
        model (tf.keras.Model): The model to train.
        X_train (numpy.ndarray): Training data.
        y_train (numpy.ndarray): Labels for the training data.
        epochs (int): Number of epochs to train the model. Default is 100.
        batch_size (int): Batch size for training. Default is 32.
        val_split (float): Fraction of the training data to be used as validation data. Default is 0.2.
        # dsadasdasd CALLBACK ATTENTION ENLEVE APRES SI BESOIN!
        callbacks (list): List of callbacks to apply during training.

    Returns:
        history (History): History object. Its History.history attribute is a record of training loss values 
                           and metrics values at successive epochs.
    '''
    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    # tensorboard for debugging/graph of the NN, this was for our own purpose (also used in create_model)
    # tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    history = model.fit(
        X_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        verbose=1,
        validation_split=val_split,
        # callbacks=[tensorboard_callback]
        callbacks=callbacks
    )

    plt.figure(figsize=(12, 6))
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()
    plt.savefig('Loss Function', dpi=300)
    return history


def test_model(model, X_test, y_test):
    '''Test the model and print performance metrics.

    Args:
        model (tf.keras.Model): The model to test.
        X_test (numpy.ndarray): Test data.
        y_test (numpy.ndarray): Labels for the test data.

    Returns:
        metrics (dict): A dictionary containing 'mse', 'mae' and 'r2_score' for the test data.
    '''
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred, multioutput='raw_values')
    mae = mean_absolute_error(y_test, y_pred, multioutput='raw_values')
    r2 = r2_score(y_test, y_pred, multioutput='raw_values')

    print("Mean Squared Error for each output: ", mse)
    print("Mean Absolute Error for each output: ", mae)
    print("R-squared for each output: ", r2)

    return {'mse': mse, 'mae': mae, 'r2_score': r2}
