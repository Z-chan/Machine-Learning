import logging as log

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import *


class NaiveBayesClassifier:
    """
    Naive Bayes Classification
    """
    def __init__(self, trainfile):
        """
        Naive Bayes Constructor
        Loading and preparing data
        :param trainfile: iris data csv path
        """
        log.getLogger().setLevel(log.INFO)
        log.info('Naive Bayes Classifier')

        # Load set
        self.trainFile = trainfile
        trainDataFrame = pd.read_csv(self.trainFile)
        trainArray = trainDataFrame.values

        # Shuffle Data
        np.random.shuffle(trainArray)

        # Extract values to numpy.Arrays
        self.X = trainArray[:, 0:4]
        self.Y = trainArray[:, 4]

        self.nbc = None

        # Map string labels to numeric
        self.Y = self.map_labels(self.Y)

        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=0.3,
                                                                                random_state=0)

    def __str__(self):
        """
        Printing data
        :return: None
        """
        print("Features: {}, Labels: {}".format(self.X, self.Y))

    @staticmethod
    def map_labels(labels):
        """
        Maping iris data labels to numeric
        :param labels: numpy.Arrays contains labels
        :return: list of mapped values
        """
        maped = [0.0 if x == 'Iris-setosa' else 1.0 if x == 'Iris-versicolor' else 2.0 for x in labels]
        return maped

    def rescale(self):
        """
        Rescaling data in dataset to [0,1]
        :return: None
        """
        scaler = MinMaxScaler(feature_range=(0, 1))
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.fit_transform(self.X_test)

    def normalize(self):
        """
        Normalizing data in dataset
        :return: None
        """
        scaler = Normalizer()
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.fit_transform(self.X_test)

    def standalizer(self):
        """
        Standardlizing data in dataset
        :return: None
        """
        scaler = StandardScaler()
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.fit_transform(self.X_test)

    def train_model(self):
        """
        Fiting model with grid search hyper-parameters
        :return: None
        """
        self.nbc = GaussianNB()
        self.nbc.fit(self.X_train, self.Y_train)

    def output(self):
        """
        Calculating and logging accuracy score
        :return: None
        """
        log.info(f"Accuracy: {self.nbc.score(self.X_test, self.Y_test):.2f}")
