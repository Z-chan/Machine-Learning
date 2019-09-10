import absl.logging as log
import os.path
from time import time

import numpy as np
import tensorflow as tf
from scipy.spatial import distance
from tensorflow.python.keras.callbacks import TensorBoard, EarlyStopping
from tensorflow.python.keras.models import Sequential

from Models.Utils import Preprocessing
from Models.exeptions import DataNotEqual, InvalidShapes
from Models.AMI import AbstractModelInterface
from config import DEFAULT_SCALER, DEFAULT_MONITOR, DEFAULT_MODE, EPOCHS, BATCH_SIZE, VERBOSE, DELTA, PATIENCE


log.set_verbosity(log.INFO)


class DLAbstractModel(AbstractModelInterface):
    def __init__(self, healthy_data: np.ndarray, broken_data: np.ndarray, data_labels: np.array, dataset_name: str,
                 windows_size: int) -> None:
        """
        Abstract neural network model for anomaly detection.
        Init the dataset, dataset shapes and pre-processing.

        :param healthy_data: healthy data csv location
        :param broken_data: data with anomalies csv location
        :param dataset_name: unique dataset name for models
        :param windows_size: step in time per example
        """
        self.data_name = dataset_name
        self.normal_data = healthy_data
        self.anomaly_data = broken_data
        self.Y = data_labels

        scaler = Preprocessing(scaler=DEFAULT_SCALER)
        self.normal_data = scaler.scale_data(data=self.normal_data)
        self.anomaly_data = scaler.scale_data(data=self.anomaly_data)

        self.window_size = windows_size

        self.model = None
        self.model_name = None
        self.dim = None
        self.samples = None
        self.threshold = 0

    @staticmethod
    def define_model() -> Sequential:
        """
        Abstract method to override in each specific model.
        :return: Sequential
        """
        return Sequential()

    def reshape_data(self) -> None:
        """
        Reshaping data for regression.
        :return: None
        """
        normal_samples = len(self.normal_data)
        normal_dim = len(self.normal_data[0])

        try:
            self.normal_data.shape = (int(normal_samples / self.window_size), self.window_size, normal_dim)
        except InvalidShapes:
            raise InvalidShapes("Something wrong with dataset shapes -_-")

        anomaly_samples = len(self.anomaly_data)
        anomaly_dim = len(self.anomaly_data[0])
        try:
            self.anomaly_data.shape = (int(anomaly_samples / self.window_size), self.window_size, anomaly_dim)
        except InvalidShapes:
            raise InvalidShapes("Something wrong with dataset shapes -_-")

        self.dim = self.normal_data.shape[2]
        self.samples = self.normal_data.shape[0]

    def train(self, retrain: bool = False) -> None:
        """
        Training deep learning model.
        :param retrain: Optional param, default False, if true network will train model even if one already exist.
        :return: None, saving the network model file if not exist or retrain is True
        """
        callbacks = []
        name = f"{self.model_name}-{self.data_name}-{int(time())}"
        tb = TensorBoard(log_dir='logs/{}'.format(name))
        callbacks.append(tb)

        cb = EarlyStopping(monitor=DEFAULT_MONITOR,
                           min_delta=DELTA,
                           patience=PATIENCE,
                           verbose=VERBOSE,
                           mode=DEFAULT_MODE,
                           restore_best_weights=True)
        callbacks.append(cb)

        data = self.normal_data

        if os.path.exists(self.data_name + f"__{self.model_name}_model"):
            log.info(f"Trained {self.model_name} model detected")
            if retrain:
                log.info(f"Start training {self.model_name} Network.....")
                self.model.fit(data, data, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(data, data),
                               callbacks=callbacks, verbose=VERBOSE)
                self.save_model()
                log.info(f"Training {self.model_name} done!")
            else:
                self.load_model()
        else:
            log.info(f"Start training {self.model_name} Network.....")
            self.model.fit(data, data, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(data, data),
                           callbacks=callbacks, verbose=VERBOSE)
            self.save_model()
            log.info(f"Training {self.model_name} done!")
        self.stats(data=data)

    def score(self, data: np.array) -> np.array:
        """
        :param data: Data for prediction
        :return: Value matrix (numpy ndarray)
        """
        log.info(f"Calculate {self.model_name} Score...")
        yhat = self.model.predict(data)
        yhat.shape = (data.shape[0] * data.shape[1], data.shape[2])
        data.shape = (data.shape[0] * data.shape[1], data.shape[2])
        log.info(f"Calculate {self.model_name} Score complete")
        return yhat

    def save_model(self):
        """
        Save trained model to file
        :return: None
        """
        log.info(f"Saving {self.model_name} model...")
        self.model.save(self.data_name + '__{}_model'.format(self.model_name))

    def load_model(self):
        """
        Load model from file
        :return: None
        """
        log.info(f"Load {self.model_name} model...")
        self.model = tf.keras.models.load_model(self.data_name + '__{}_model'.format(self.model_name))

    def get_normal_data(self) -> np.array:
        """
        Give healthy data, training one
        :return: Healthy data
        """
        return self.normal_data

    def get_anomaly_data(self) -> np.array:
        """
        Give broken data with anomalie to detect
        :return: Broken data
        """
        return self.anomaly_data

    def stats(self, data: np.array) -> None:
        """
        :param data: Data to validate the trained models
        :return: None
        """
        val_loss = self.model.evaluate(data, data, batch_size=BATCH_SIZE, verbose=VERBOSE)
        log.info(f"Validation {self.model_name} Loss: " + str(val_loss))

    def calculate_threshold(self, helth: np.array):
        """
        Calculate and set threshold for anomaly detection
        :param helth: Health matrix value from predict
        :return: None
        """
        log.info(f"Calculate {self.model_name} threshold...")
        actual = self.normal_data
        dists = []
        if len(helth) == len(actual):
            for i in range(len(helth)):
                helth[i] = helth[i].tolist()
                actual[i] = actual[i].tolist()
                dist = distance.euclidean(helth[i], actual[i])
                dists.append(dist)
            self.threshold = max(dists)
            log.info('Threshold calculated {}: {}'.format(self.model_name, self.threshold))
        else:
            raise DataNotEqual("Both sets should have the same number of samples")

    def anomaly_score(self, pred: np.array):
        """
        Anomaly detector, basing on calculated distance and threshold deciding if data is normal or with anomaly.
        :param pred: Matrix values from predicted anomaly set
        :return: None, saving files with pointed anomaly and real ones per calculated distance.
        """
        log.info('Calculating distance to anomaly...')
        dists = []
        actual = self.anomaly_data
        Y = self.Y
        if len(pred) == len(actual):
            for i in range(len(pred)):
                pred[i] = pred[i].tolist()
                actual[i] = actual[i].tolist()
                dist = distance.euclidean(pred[i], actual[i])
                if dist > self.threshold:
                    score = 'Anomaly'
                else:
                    score = 'Normal'
                dists.append((dist, Y[i], score))
            with open(r'{}_detected_'.format(self.model_name) + self.data_name + '.csv', 'w') as file:
                for each in dists:
                    file.write(str(each[0]) + ',' + each[1] + ',' + each[2] + '\n')
            log.info('Anomaly score calculated')
        else:
            raise DataNotEqual("Both sets should have the same number of samples")