#!/bin/bash

# Step 1: Navigate to /visualization directory from the current directory
echo "Navigating to /visualization directory..."
cd /Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization || { echo "Failed to navigate to /visualization"; exit 1; }

# Step 2: Activate the virtual environment
echo "Activating the virtual environment..."
source /Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/.venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# Step 3: Navigate to /execution directory
echo "Navigating to /execution directory..."
cd /Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution || { echo "Failed to navigate to /execution"; exit 1; }

# Step 4: Execute the Python script
echo "Executing yourScene.py..."
python3 /Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution/yourScene.py || { echo "Failed to execute yourScene.py"; exit 1; }


echo "Executing speech execution.py..."
python3 /Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution/script/speech_exec.py || { echo "Failed to execute speechexec.py"; exit 1; }


ffmpeg -i /Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution/customStore/manim_output.mp4 -i /Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution/speech.mp3 -c:v copy -c:a aac -strict experimental final_output.mp4 -y

echo "Executing upload to cloudinary.py..."
python3 /Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution/uploadToCloudinary.py || { echo "Failed to upload to cloudinary.py"; exit 1; }


echo "Script execution completed successfully!"
