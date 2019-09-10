DEFAULT_SCALER = 'Min-Max'
DEFAULT_MODE = 'min'
DEFAULT_MONITOR = 'val_loss'

LSTM_NETWORK = 'LSTM'
LSTM_CELLS_NUMBER = 100
LSTM_LAYERS_NUMBER = 10

GRU_NETWORK = 'GRU'
GRU_CELLS_NUMBER = 100
GRU_LAYERS_NUMBER = 10

CONV_NETWORK = 'CONVOLUTIONAL'
CONV_CELLS_NUMBER = 32
CONV_KERNEL_SIZE = (3, 3)
CONV_POOL_SIZE = (2, 3)
SINGLE_UNIT = 1

FORWARD_NETWORK = 'FORWARD'
PRIMARY_UNITS_SIZE = 1024
SECONDARY_UNITS_SIZE = 512
TERTIARY_UNITS_SIZE = 256
QUATERNARY_UNITS_SIZE = 128

DEFAULT_N_FUZZY_PARTS = 5

ISOLATION_MODEL = 'IsolationForrest'
ISOLATION_ESTIMATORS_NUMBER = 20
ISOLATION_CORES = 4

ONECLASSSVM_MODEL = 'OneClassSVM'

MEAN_ABSOLUTE_ERROR = 'mae'
ADAM_OPTIMIZER = 'adam'

EPOCHS = 1000
BATCH_SIZE = 16
VERBOSE = 0
DELTA = 0.0001
PATIENCE = 50


WINDOW_SIZE = 2