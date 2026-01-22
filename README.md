# Face Detection

A privacy-focused face recognition application that runs entirely locally on your machine. Upload a reference photo, then use your webcam to detect and identify matching faces in real-time.

## Features

- **Local Processing**: All face detection and recognition happens on your device - no cloud uploads or external services
- **Reference Image Matching**: Upload a photo of yourself, and the app will highlight when your face appears on camera
- **Real-time Detection**: Live webcam feed with instant face detection and matching
- **Adjustable Settings**: Fine-tune brightness and matching strictness to your environment
- **Visual Feedback**: Green boxes indicate a match, red boxes indicate no match

## How It Works

1. **Upload Stage**: Select a reference image containing your face
2. **Detection Stage**: The app opens your webcam and continuously scans for faces
3. **Matching**: Each detected face is compared against your reference image
4. **Display**: Matching faces get a green "MATCH" label, others get red "NO MATCH"

## Installation

### Prerequisites

- Python 3.9 or higher
- A webcam

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Ishany-coder/faceDetection.git
   cd faceDetection
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

   Note: The `dlib` library (required by `face_recognition`) may take a few minutes to build from source.

## Usage

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Run the application:
   ```bash
   python3 main.py
   ```

3. Click "Browse Image" to select a reference photo with your face

4. Once the face is detected, click "Start Detection" to begin

5. Adjust settings as needed (see below)

## Settings

### Brightness
Adjusts the camera feed brightness. Useful for compensating in dark or overly bright environments.

- **Range**: -100 to +100
- **Default/Recommended**: 0

### Strictness
Controls how strict the face matching is. Higher values require faces to be more similar to count as a match.

- **Range**: 0 (Loose) to 100 (Strict)
- **Default/Recommended**: 25
- **Loose (0-32)**: More lenient matching, may have false positives
- **Medium (33-65)**: Balanced matching
- **Strict (66-100)**: Very strict matching, may miss some true matches

If the app is confusing you with someone else, increase the strictness. If it's not recognizing you reliably, decrease it.

## Use Cases

- **Security Demos**: Demonstrate face recognition concepts
- **Access Control Prototyping**: Test face-based identification systems
- **Learning Tool**: Understand how face recognition technology works
- **Fun Projects**: See how well the algorithm can distinguish between people

## Project Structure

```
faceDetection/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── face/
│   ├── encoder.py       # Reference image face encoding
│   └── detector.py      # Real-time face detection and matching
└── gui/
    └── app.py           # User interface
```

## Dependencies

- **face_recognition**: Face detection and encoding (uses dlib)
- **opencv-python**: Webcam capture and image processing
- **Pillow**: Image loading and display
- **numpy**: Array operations
- **tkinter**: GUI framework (included with Python)

## Troubleshooting

**"No face detected in the image"**
- Ensure the reference image has a clear, front-facing view of the face
- The image should have good lighting
- If multiple faces are detected, the largest one is used

**Camera not working**
- Grant camera permissions to your terminal/Python
- On macOS: System Settings > Privacy & Security > Camera

**Face not being recognized**
- Try adjusting the strictness slider (lower = more lenient)
- Ensure good lighting on your face
- Use a clear, well-lit reference photo

## License

MIT License
