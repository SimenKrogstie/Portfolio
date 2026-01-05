# Import statements (no need for ! here)
import time
import h5py
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.metrics import FalseNegatives, FalsePositives, TrueNegatives, TruePositives, MeanMetricWrapper
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2DTranspose, concatenate, Conv2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import VGG16
from tensorflow.keras import backend as K

# Custom F1 score
def F1_score(y_true, y_pred):
    TP = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    P = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = TP / (P + K.epsilon())

    Pred_P = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = TP / (Pred_P + K.epsilon())
    return 2*((precision*recall)/(precision+recall+K.epsilon()))


# Importing training data
FILE_PATH = "tree_train.h5"

with h5py.File(FILE_PATH,'r') as f:
    print('Datasets in file:', list(f.keys()))
    X = f['X'][:]
    y = f['y'][:]


# Verifying the shape of features and masks
print("X shape:", X.shape)
print("y shape:", y.shape)


# Normalizing pixel values between 0 and 1
X = X / 255.0

# Splitting the dataset in training and validation sets (80% training, 20% validation)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)


# Converting mask labels to float32
y_train = y_train.astype('float32')
y_val = y_val.astype('float32')

# Setting augmentation parameters for both images and masks
data_gen_args = dict(rotation_range=10,
                     width_shift_range=0.1,
                     height_shift_range=0.1,
                     shear_range=0.1,
                     zoom_range=0.1,
                     horizontal_flip=True,
                     fill_mode='nearest') 

# Initializing generators to apply identical augemtations to images and masks
image_datagen = ImageDataGenerator(**data_gen_args)
mask_datagen = ImageDataGenerator(**data_gen_args)

# Fitting generators on the training data
image_datagen.fit(X_train)
mask_datagen.fit(y_train)

# Defining metrics to measure model performance
metrics = [FalseNegatives(),
                           FalsePositives(),
                           TrueNegatives(),
                           TruePositives(),
                           F1_score]



# Function for building the U-net
def build_unet_model2(base_model, filters, dropout_rate, learning_rate, list_of_metrics):
    # Freezing the base model layers to prevent updating their weights during training
    base_model.trainable = False 

    # Encoder layers (from VGG16)
    # Encoder layers from VGG16 to use for skip cnonnections
    encoder_outputs = [
        base_model.get_layer("block1_conv2").output,
        base_model.get_layer("block2_conv2").output,
        base_model.get_layer("block3_conv3").output,
        base_model.get_layer("block4_conv3").output,
        base_model.get_layer("block5_conv3").output,
    ]

    # Decoder layers with skip connections
    # Begins with output of the deepest encoder layer
    x = encoder_outputs[-1] 

    # Decoder block 1, upsampling and skip connection
    x = Conv2DTranspose(filters * 8, (3, 3), strides=2, padding="same", activation='relu')(x)
    x = concatenate([x, encoder_outputs[-2]])  # Skip connection

    # Decoder block 2, upsampling and skip connection
    x = Conv2DTranspose(filters * 4, (3, 3), strides=2, padding="same", activation='relu')(x)
    x = concatenate([x, encoder_outputs[-3]])  # Skip connection

    # Decoder block 3, upsamling and skip connection
    x = Conv2DTranspose(filters * 2, (3, 3), strides=2, padding="same", activation='relu')(x)
    x = concatenate([x, encoder_outputs[-4]])  # Skip connection

    # Decoder block 4, adjusting strides to avoid oversampling and skip connection
    x = Conv2DTranspose(filters, (3, 3), strides=2, padding="same", activation='relu')(x)
    x = concatenate([x, encoder_outputs[-5]])  # Skip connection

    # Final upsampling to reach the output size of 128x128
    x = Conv2DTranspose(filters // 2, (3, 3), strides=1, padding="same", activation='relu')(x)  # Removed extra upsampling step
    x = Dropout(dropout_rate)(x)

    # Final output layer with 1 outputchannel for binary segmentation
    outputs = Conv2D(1, (1, 1), activation='sigmoid')(x)  # Output shape should now be (128, 128, 1)

    # Defining U-Net model
    model = Model(inputs=base_model.input, outputs=outputs)

    # Compile the model with custom metrics
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='binary_crossentropy',
        metrics=list_of_metrics
    )

    return model

# Initialize the base model
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))

# Build U-Net on top of base model with specified hyperparameters
model = build_unet_model2(base_model=base_model,
                          filters=64,
                          dropout_rate=0.2,
                          learning_rate=0.001,
                          list_of_metrics=metrics)

#Start time before training
start_time = time.time()

# Train with all layers in base model frozen
history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=15, batch_size=16, verbose=1)

# Unfreeze last 20 layers in base model for fine-tuning
for layer in base_model.layers[:-20]:  # Freeze all layers except the last 20
    layer.trainable = False

# Recompile model with lower learning rate for fine-tuning
model.compile(optimizer=Adam(learning_rate=0.001),
              loss='binary_crossentropy',
              metrics=metrics)

# Continue training with fine-tuning for more epochs
fine_tuning_history = model.fit(
    X_train, y_train,                   # Training data
    validation_data=(X_val, y_val),     # Validation data
    epochs=15,                          # Number of epochs
    batch_size=16,                      # Batch size
    verbose=1)                          # Dispøaying progress

# End timer and print training time
end_time = time.time()
print("Total training time:", end_time - start_time, "seconds")

# Save the model
model.save('my_trained_model.h5')
