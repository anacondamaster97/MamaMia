import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from groq import Groq
from dotenv import load_dotenv  

def get_dishes(ingredients):
    prompt = "Given the following list of ingredients, provide three dishes I can make using these ingredients. For each dish, include the history of the dish and a description of how to prepare it. Return the response only in the following JSON format without any extra text or explanations: {'data': [{'dish1': 'history of the dish and how to make the dish'},{'dish2': 'history of the dish and how to make the dish'},{'dish3': 'history of the dish and how to make the dish'}]} Here are the ingredients: " + str(ingredients)
    load_dotenv() 
    print("KEY", os.getenv("GROQ_KEY"))
    client = Groq(
    api_key=os.getenv("GROQ_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

def load_and_prepare_model(num_classes):
    base_model = MobileNetV2(weights='imagenet', include_top=False)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    
    for layer in base_model.layers:
        layer.trainable = False
    
    return model

def fine_tune_model(model, train_dir, epochs=10, batch_size=32):
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    validation_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )

    model.compile(optimizer=Adam(learning_rate=0.0001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // batch_size,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // batch_size,
        epochs=epochs
    )

    return model, train_generator.class_indices

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array)

def predict_ingredient(model, img_array, class_indices):
    predictions = model.predict(img_array)
    class_names = {v: k for k, v in class_indices.items()}
    top_3 = np.argsort(predictions[0])[-3:][::-1]
    return [(class_names[i], predictions[0][i]) for i in top_3]

def process_images_in_folder(folder_path, model, class_indices):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            img_path = os.path.join(folder_path, filename)
            img_array = preprocess_image(img_path)
            predictions = predict_ingredient(model, img_array, class_indices)

            print(f"\nDetected ingredients in {filename}:")
            for i, (label, score) in enumerate(predictions):
                print(f"{i + 1}: {label} ({score:.2f})")

def main():
    train_dir = 'image_train'
    test_dir = 'images'

    if not os.path.exists(train_dir):
        print(f"Error: The training folder '{train_dir}' does not exist.")
        return

    if not os.path.exists(test_dir):
        print(f"Error: The test folder '{test_dir}' does not exist.")
        return

    num_classes = len([name for name in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, name))])
    model = load_and_prepare_model(num_classes)
    
    print("Fine-tuning the model...")
    model, class_indices = fine_tune_model(model, train_dir)
    print("Fine-tuning completed.")

    print("\nProcessing test images...")
    process_images_in_folder(test_dir, model, class_indices)

if __name__ == "__main__":
    main()