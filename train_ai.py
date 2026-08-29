import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, BatchNormalization

# 1. Load Dataset
df = pd.read_csv('neuro_semantic_dataset.csv')

# 2. Features and Labels
X = df[['alpha', 'beta', 'theta']].values
y = df['trigger_image_name'].values

# Encode and Scale
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
np.save('classes.npy', label_encoder.classes_)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, 'scaler.pkl')

# 3. Windowing (Increased window to 20 for better pattern recognition)
window_size = 20 
X_windows, y_windows = [], []
for i in range(0, len(X_scaled) - window_size, 5): # Step of 5 to reduce overlap noise
    X_windows.append(X_scaled[i : i + window_size])
    y_windows.append(y_encoded[i + window_size])

X_windows, y_windows = np.array(X_windows), np.array(y_windows)

# 4. Deeper 1D-CNN Architecture (Added BatchNormalization for stability)
model = Sequential([
    Conv1D(128, kernel_size=3, activation='relu', input_shape=(window_size, 3)),
    BatchNormalization(),
    MaxPooling1D(pool_size=2),
    
    Conv1D(64, kernel_size=3, activation='relu'),
    BatchNormalization(),
    Dropout(0.4),
    
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(len(label_encoder.classes_), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 5. Intense Training (100 Epochs)
print("\n🚀 Training Deep Neuro-CNN. This will take a moment...")
model.fit(X_windows, y_windows, epochs=100, batch_size=64, verbose=1)

model.save('neuro_cnn_model.h5')
print("\n✅ High-Precision Model Saved!")