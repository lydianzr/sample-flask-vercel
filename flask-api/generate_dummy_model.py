import tensorflow as tf
from tensorflow import keras
import numpy as np

# Create a simple model
model = keras.Sequential([
    keras.layers.Dense(16, activation='relu', input_shape=(10,)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Generate dummy data
X_dummy = np.random.rand(100, 10)
y_dummy = np.random.randint(0, 2, 100)

# Train the model briefly
model.fit(X_dummy, y_dummy, epochs=3, verbose=0)

# Save the model
model.save("dummy_model.h5")
