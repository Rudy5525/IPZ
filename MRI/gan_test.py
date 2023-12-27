import os
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import pickle
from sklearn.model_selection import train_test_split
from tensorflow import keras 
from keras import layers, models
from mri_read import *

# Funkcja wczytująca obrazy z pliku .pkl
def load_images_from_pickle(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)

    images = []
    labels = []
    for patient in data:
        patientData = getData(patient['data'])
        for i in range(patientData.shape[-1]):
            images.append(patientData[:,:,:,i])
            labels.append(patient['hasAdhd'])

    return np.array(images), np.array(labels)
# Funkcja generująca losowy szum jako dane wejściowe dla generatora
def generate_noise(batch_size, noise_dim):
    return np.random.normal(0, 1, size=(batch_size, noise_dim))

# Funkcja tworząca generator
def build_generator(noise_dim, output_dim):
    model = models.Sequential()
    model.add(layers.Dense(128, input_dim=noise_dim, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dense(np.prod(output_dim), activation='sigmoid'))
    model.add(layers.Reshape(output_dim))  # Dodaj warstwę Reshape
    return model

# Funkcja tworząca dyskryminator
def build_discriminator(input_dim):
    model = models.Sequential()
    model.add(layers.Flatten(input_shape=input_dim))
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    return model

# Funkcja tworząca model GAN
def build_gan(generator, discriminator):
    discriminator.trainable = False
    model = models.Sequential()
    model.add(generator)
    model.add(discriminator)
    return model

# Parametry
noise_dim = 100
image_dim = (128, 120, 32, 1)  # Rozmiar obrazu po dodaniu warstwy Reshape
batch_size = 64
epochs = 10

# Wczytanie danych z pliku .pkl
data_path = 'lista.pkl'
X_data, y_data = load_images_from_pickle(data_path)
print(X_data.shape, y_data.shape)
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.20, shuffle=True)
print(X_train.shape, y_train.shape)
# Tworzenie i kompilacja modeli
discriminator = build_discriminator(image_dim)
discriminator.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

generator = build_generator(noise_dim, image_dim)
generator.compile(optimizer='adam', loss='binary_crossentropy')

gan = build_gan(generator, discriminator)
gan.compile(optimizer='adam', loss='binary_crossentropy')

# Pętla ucząca
for epoch in range(epochs):
  
    # Trening dyskryminatora
    noise = generate_noise(batch_size, noise_dim)
    generated_images = generator.predict(noise)
    labels_fake = np.zeros((batch_size, 1))

    d_loss_real = discriminator.train_on_batch(X_train, y_train)
    d_loss_fake = discriminator.train_on_batch(generated_images, labels_fake)
    d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

    # Trening generatora
    noise = generate_noise(batch_size, noise_dim)
    labels_gan = np.ones((batch_size, 1))
    g_loss = gan.train_on_batch(noise, labels_gan)

    # Wydruk statystyk co kilka epok
    #if epoch % 100 == 0:
    print(f"Epoch {epoch}, D Loss: {d_loss[0]}, G Loss: {g_loss}")

'''
# Generowanie przykładowego obrazka po zakończeniu treningu
sample_noise = generate_noise(1, noise_dim)
generated_sample = generator.predict(sample_noise).reshape(128, 120, 32)

# Wyświetlenie przykładowego obrazka
plt.imshow(generated_sample[:, :, 16], cmap='gray')  # Wybierz warstwę 16 z wymiaru 32
plt.show()

# Zapisanie wygenerowanego obrazka w formacie NIfTI
output_path = 'generated_image.nii.gz'
nifti_image = nib.Nifti1Image(generated_sample, np.eye(4))
nib.save(nifti_image, output_path)
'''