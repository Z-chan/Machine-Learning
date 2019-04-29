from RR.RRClassifier import RRClassifier
from RR.RRRegressor import RRRegressor


def main():
    """
    Main function. Run Ridge Regression classification and regression tusks.
    train.csv: iris dataset
    train.tsv: Poznań flats prices
    :return: None
    """
    # SVR Classification
    train_file_location_classification = r'train.csv'
    rrclassifier = RRClassifier(trainfile=train_file_location_classification)
    rrclassifier.standalizer()
    rrclassifier.grid_search()
    rrclassifier.train_model()

    # SVR Regressor
    train_file_location_regression = r'train.tsv'
    rrregressor = RRRegressor(trainfile=train_file_location_regression)
    rrregressor.standalizer()
    rrregressor.grid_search()
    rrregressor.train_model()

    # Results
    rrregressor.output()
    rrclassifier.output()