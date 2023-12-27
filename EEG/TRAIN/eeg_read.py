import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from scipy.io import loadmat
from sklearn.model_selection import train_test_split
import math

from EEG.TRAIN.eeg_filter import *
from EEG.config import *

    
def readEEGRaw(folder_path):

    subfolders = EEG_SUBFOLDERS

    ADHD_DATA = []
    CONTROL_DATA = []

    for subfolder in subfolders:

        current_folder = os.path.join(folder_path, subfolder)

        mat_files = [f for f in os.listdir(current_folder) if f.endswith('.mat')]

        for mat_file in mat_files:
            file_path = os.path.join(current_folder, mat_file)

            loaded_data = loadmat(file_path, mat_dtype=True)

            file_name, _ = os.path.splitext(mat_file)

            if EEG_POS_PHRASE in subfolder:
                arr = loaded_data[file_name]
                ADHD_DATA.append(arr.T)
            elif EEG_NEG_PHRASE in subfolder:
                arr = loaded_data[file_name]
                CONTROL_DATA.append(arr.T)

    return ADHD_DATA, CONTROL_DATA


def prepareForCNN(ADHD_DATA, CONTROL_DATA):

    ADHD_in_one = np.concatenate(ADHD_DATA, axis=1)
    CONTROL_in_one = np.concatenate(CONTROL_DATA, axis=1)

    ADHD_range = (math.floor(ADHD_in_one.shape[1] / EEG_SIGNAL_FRAME_SIZE))
    CONTROL_range = (math.floor(CONTROL_in_one.shape[1] / EEG_SIGNAL_FRAME_SIZE))

    ADHD_framed = np.zeros((ADHD_range, ADHD_in_one.shape[0], EEG_SIGNAL_FRAME_SIZE))
    CONTROL_framed = np.zeros((CONTROL_range, CONTROL_in_one.shape[0], EEG_SIGNAL_FRAME_SIZE))

    for i in range(ADHD_range):
        ADHD_framed[i, :, :] = ADHD_in_one[:, i * EEG_SIGNAL_FRAME_SIZE: (i + 1) * EEG_SIGNAL_FRAME_SIZE]

    for i in range(CONTROL_range):
        CONTROL_framed[i, :, :] = CONTROL_in_one[:, i * EEG_SIGNAL_FRAME_SIZE: (i + 1) * EEG_SIGNAL_FRAME_SIZE]

    y_ADHD = [CNN_POS_LABEL for x in range(ADHD_framed.shape[0])]
    y_CONTROL = [CNN_NEG_LABEL for x in range(CONTROL_framed.shape[0])]


    X = np.concatenate((CONTROL_framed, ADHD_framed))
    y = np.concatenate((np.array(y_CONTROL), np.array(y_ADHD)))

    X_4D = np.reshape(X,(X.shape[0],X.shape[1],X.shape[2],1))

    X_train, X_test, y_train, y_test = train_test_split(X_4D, y, test_size=0.3, shuffle=True)

    return X_train, y_train, X_test, y_test