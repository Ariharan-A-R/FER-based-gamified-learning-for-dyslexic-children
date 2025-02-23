import cv2
import numpy as np
import tensorflow as tf
import pygame
import random
import threading
import time

# Constants
IMG_SIZE = 48  # Image size for both models
emotion_labels_m1 = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise']
emotion_labels_m2 = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# Load Models
model_path_m1 = r"F:\Downloads\model_file1.keras"
model_m1 = tf.keras.models.load_model(model_path_m1)

model_path_m2 = r"C:\Users\Lenovo\Documents\CIP\copy\model_file.h5"
model_m2 = tf.keras.models.load_model(model_path_m2)

# Load Haarcascade for face detection
cascade_path = r"C:\Users\Lenovo\Documents\CIP\copy\haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    raise IOError("Error loading Haar cascade file. Check the path!")

# Global variable for screen switching
switch_screen = False  

# Function to preprocess frames
def preprocess_frame(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 3)
    
    if len(faces) == 0:
        return None
    
    x, y, w, h = faces[0]
    face_img = gray_frame[y:y+h, x:x+w]
    resized_frame = cv2.resize(face_img, (IMG_SIZE, IMG_SIZE))
    return resized_frame.reshape(1, IMG_SIZE, IMG_SIZE, 1) / 255.0  # Normalize

# Emotion decision logic
def get_final_emotion(m1_emotion, m2_emotion):
    if m1_emotion in ['fear', 'angry', 'disgust','sad']:
        return m1_emotion
    elif m2_emotion in ['fear', 'angry', 'disgust','sad']:
        return m2_emotion
    elif m1_emotion in ['happy', 'surprise'] and m2_emotion == 'neutral':
        return 'happy'
    elif m1_emotion in ['happy', 'surprise'] and m2_emotion in ['happy', 'surprise']:
        return 'happy'
    return 'neutral'  # Default case

# Emotion detection function
def detect_emotion():
    global switch_screen  
    cap = cv2.VideoCapture(0)  # Open webcam
    
    while True:
        time.sleep(10)  # Check emotion every 10 seconds
        ret, frame = cap.read()
        if not ret:
            continue
        
        input_frame = preprocess_frame(frame)
        if input_frame is None:
            continue
        
        # Predict emotions from both models
        prediction_m1 = model_m1.predict(input_frame)
        prediction_m2 = model_m2.predict(input_frame)

        # Get the predicted emotions
        emotion_idx_m1 = np.argmax(prediction_m1)
        emotion_idx_m2 = np.argmax(prediction_m2)
        predicted_emotion_m1 = emotion_labels_m1[emotion_idx_m1]
        predicted_emotion_m2 = emotion_labels_m2[emotion_idx_m2]

        # Print predictions from both models
        print(f"Model 1 Prediction: {predicted_emotion_m1} (Confidence: {prediction_m1[0][emotion_idx_m1]:.2f})")
        print(f"Model 2 Prediction: {predicted_emotion_m2} (Confidence: {prediction_m2[0][emotion_idx_m2]:.2f})")

        # Get the final emotion decision
        final_emotion = get_final_emotion(predicted_emotion_m1, predicted_emotion_m2)
        print("Final Detected Emotion:", final_emotion)

        # Switch screen if necessary
        if final_emotion in ['disgust', 'angry', 'sad', 'fear']:
            switch_screen = True
            time.sleep(5)  # Show motivational message for 5 seconds
            switch_screen = False

    cap.release()

# Start emotion detection in a separate thread
t = threading.Thread(target=detect_emotion, daemon=True)
t.start()

# Pygame Jigsaw Puzzle
def get_random_alphabet():
    return random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def load_new_puzzle():
    global current_letter, IMAGE_PATH, original_image, preview_image, tiles, correct_positions, shuffled_positions

    current_letter = get_random_alphabet()
    IMAGE_PATH = f"alphabet_images/{current_letter}.png"
    
    try:
        original_image = pygame.image.load(IMAGE_PATH)
    except pygame.error:
        print(f"Error loading {IMAGE_PATH}, using default A.png")
        original_image = pygame.image.load("alphabet_images/A.png")  # Fallback to 'A'

    original_image = pygame.transform.scale(original_image, (400, 400))
    preview_image = pygame.transform.scale(original_image, (100, 100))
    
    tiles = []
    correct_positions = []
    shuffled_positions = []
    
    for row in range(2):
        for col in range(2):
            rect = pygame.Rect(col * 200, row * 200, 200, 200)
            tile = original_image.subsurface(rect).copy()
            tiles.append(tile)
            correct_positions.append((col * 200, row * 200))
    
    shuffled_positions = correct_positions[:]
    while shuffled_positions == correct_positions:
        random.shuffle(shuffled_positions)
pygame.init()
GRID_SIZE = 2
TILE_SIZE = 200
MARGIN = 30
SCREEN_WIDTH = TILE_SIZE * GRID_SIZE + 200
SCREEN_HEIGHT = TILE_SIZE * GRID_SIZE + 100

def get_random_alphabet():
    return random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def load_new_puzzle():
    """Loads a new puzzle with a random alphabet image."""
    global current_letter, IMAGE_PATH, original_image, preview_image, tiles, correct_positions, shuffled_positions

    # Get a new random letter
    current_letter = get_random_alphabet()
    IMAGE_PATH = f"alphabet_images/{current_letter}.png"

    # Load new image
    original_image = pygame.image.load(IMAGE_PATH)
    original_image = pygame.transform.scale(original_image, (TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE))
    
    # Reset preview image
    preview_image = pygame.transform.scale(original_image, (100, 100))

    # Reset puzzle pieces
    tiles = []
    correct_positions = []
    shuffled_positions = []

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            tile = original_image.subsurface(rect).copy()
            tiles.append(tile)
            correct_positions.append((col * TILE_SIZE, row * TILE_SIZE))

    # Shuffle positions but ensure it's different from the original
    shuffled_positions = correct_positions[:]
    while shuffled_positions == correct_positions:
        random.shuffle(shuffled_positions)

# Initial puzzle load
current_letter = get_random_alphabet()
load_new_puzzle()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"{current_letter} Alphabet Jigsaw Puzzle")

dragging = False
selected_index = None
switch_screen = False  # Track when to show motivation message

def draw_tiles():
    for i, pos in enumerate(shuffled_positions):
        screen.blit(tiles[i], pos)

def is_solved():
    return shuffled_positions == correct_positions

running = True
while running:
    screen.fill((255, 255, 255))
    
    if switch_screen:
        font = pygame.font.Font(None, 50)
        text = font.render("You can do it!", True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
    else:
        for pos in correct_positions:
            pygame.draw.rect(screen, (0, 0, 0), (pos[0], pos[1], TILE_SIZE, TILE_SIZE), 2)
        screen.blit(preview_image, (SCREEN_WIDTH - 110, 20))  # Preview in top-right
        pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH - 110, 20, 100, 100), 2)
        draw_tiles()

        if is_solved():
            font = pygame.font.Font(None, 60)
            text = font.render("Puzzle Solved!", True, (0, 200, 0))
            screen.blit(text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT - 80))
            pygame.display.flip()
            pygame.time.delay(2000)  # Show message for 2 seconds
            load_new_puzzle()  # Load new puzzle

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, pos in enumerate(shuffled_positions):
                rect = pygame.Rect(pos[0], pos[1], TILE_SIZE, TILE_SIZE)
                if rect.collidepoint(event.pos):
                    dragging = True
                    selected_index = i
                    offset_x = event.pos[0] - pos[0]
                    offset_y = event.pos[1] - pos[1]
                    break
        elif event.type == pygame.MOUSEMOTION and dragging:
            shuffled_positions[selected_index] = (event.pos[0] - offset_x, event.pos[1] - offset_y)
        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            dragging = False
            if selected_index is not None:
                x, y = shuffled_positions[selected_index]
                snapped_x = round(x / TILE_SIZE) * TILE_SIZE
                snapped_y = round(y / TILE_SIZE) * TILE_SIZE
                snapped_position = (snapped_x, snapped_y)

                if snapped_position in shuffled_positions and snapped_position != shuffled_positions[selected_index]:
                    shuffled_positions[selected_index] = correct_positions[selected_index]
                else:
                    shuffled_positions[selected_index] = snapped_position
                
                selected_index = None
    
    pygame.display.flip()

pygame.quit()
