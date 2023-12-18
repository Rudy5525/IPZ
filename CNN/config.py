EEG_DATA_PATH = 'CNN/EEG'                                                           # Folder z danymi
EEG_SUBFOLDERS = ['ADHD', 'CONTROL']                                                # Wszystkie podfoldery z głównego folderu z danymi
EEG_POS_PHRASE = 'ADHD'                                                             # Fraza zawierająca się w nazwie folderu z grupą chorych pacjentów
EEG_NEG_PHRASE = 'CONTROL'                                                          # Fraza zawierająca się w nazwie folderu z grupą kontrolną
EEG_SIGNAL_FRAME_SIZE = 100                                                         # wielkość pojedyńczej próbki pobieranej z danych elektrody
CNN_MODELS_PATH = './trained_models'                                                # folder do zapisywania modeli
CNN_POS_LABEL = 1                                                                   # wyjście pozytywne z modelu
CNN_NEG_LABEL = 0                                                                   # wyjście negatywne
CNN_TEST_RATIO = 0.2                                                                # proporcja ilości próbek danych testowych do treningowych 
CNN_INPUT_SHAPE = (19, EEG_SIGNAL_FRAME_SIZE, 1)                                    # 19 - ilość elektrod ; wielkość ramki danych ; 1 - magiczna liczba którą wymaga keras
CNN_EPOCHS = 5                                                                      # Ilość przejść do przodu przez model
CUTOFFS = [(8,10), (10,13), (13,15), (15,18), (18,30)]                              # Przedziały częstotliwości