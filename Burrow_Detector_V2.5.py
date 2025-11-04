# Lowered lr,

import os; os.system("cls")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import matplotlib.pyplot as plt
from datetime import datetime
import tensorflow as tf
from keras import layers, models, callbacks

# Load datasets
train_ds = tf.keras.utils.image_dataset_from_directory(
    "Training Images",
    image_size=(100, 100),
    batch_size=32
)
test_ds = tf.keras.utils.image_dataset_from_directory(
    "Testing Images",
    image_size = (100, 100),
    batch_size = 32
)

# Normalize
train_ds = train_ds.map(lambda x, y: (x/255.0, y))
test_ds = test_ds.map(lambda x, y: (x/255.0, y))

# Data augmentation
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),  # flip both axes
    layers.RandomRotation(0.4),                    # slight rotation
    layers.RandomZoom(0.2),                        # Random zoom
    layers.RandomTranslation(0.2, 0.2),            # random shift in width & height
    layers.RandomContrast(0.3),                    # small contrast changes
])

# Model
model = models.Sequential([
    data_augmentation,
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(100, 100, 3)),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(128, (3,3), activation='relu'),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compile Model
model.compile(
    optimizer = 'adam',
    loss = 'binary_crossentropy',
    metrics = ['accuracy'])

# Training
callback = tf.keras.callbacks.EarlyStopping(
    monitor = 'val_loss', 
    patience = 4,
    restore_best_weights = True,
)

reduce_lr = callbacks.ReduceLROnPlateau(
    monitor = 'val_loss',
    factor = 0.7,
    patience = 4,
    min_lr = 1e-3,
    verbose = 1
)

# Fit model
history = model.fit(
    train_ds, 
    validation_data = test_ds, 
    epochs = 30, 
    callbacks = [callback, reduce_lr]
)

# Evaluation
test_loss, test_acc = model.evaluate(test_ds, verbose=2)

# Add segment to classify unknown images

# Print Acc
print(f"Test accuracy: {test_acc:.2f}")

# Save weights and graph if accuracy is above 80%
if test_acc >= 0.80:
    model.save_weights(f"Weights {test_acc:.2f} {datetime.now().strftime("%Y%m%d_%H%M%S")}.weights.h5")

    # Plot training and validation accuracy and loss, save graph
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(acc) + 1)

    # Accuracy plot
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, 'b-', label='Training Accuracy')
    plt.plot(epochs, val_acc, 'r-', label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)

    # Loss plot
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, 'b-', label='Training Loss')
    plt.plot(epochs, val_loss, 'r-', label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"Accuracy and Loss graphs {test_acc:.2f} {datetime.now().strftime("%Y%m%d_%H%M%S")}.png", dpi = 300)