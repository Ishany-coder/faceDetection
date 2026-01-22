"""Main application window with camera and face detection."""

import tkinter as tk
from tkinter import messagebox

import cv2
from PIL import Image, ImageTk

from face.detector import FaceDetector


class FaceDetectionApp:
    """Main application showing camera with face detection."""

    def __init__(self):
        """Initialize the face detection application."""
        self.detector = FaceDetector()
        self.cap = None
        self.running = False

        # Create main window
        self.root = tk.Tk()
        self.root.title("Face Detection")
        self.root.geometry("700x550")
        self.root.configure(bg="#2b2b2b")
        self.root.resizable(False, False)

        # Title label
        title = tk.Label(
            self.root,
            text="Face Detection",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#2b2b2b"
        )
        title.pack(pady=10)

        # Video display
        self.video_label = tk.Label(self.root, bg="#1e1e1e")
        self.video_label.pack(pady=10)

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Starting camera...",
            font=("Helvetica", 12),
            fg="#888888",
            bg="#2b2b2b"
        )
        self.status_label.pack(pady=5)

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Start camera
        self._start_camera()

    def _start_camera(self) -> None:
        """Initialize and start the webcam capture."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam")
            self.status_label.config(text="Camera not available", fg="#ff6b6b")
            return

        self.running = True
        self.status_label.config(text="Camera active - detecting faces", fg="#4ecdc4")
        self._update_frame()

    def _update_frame(self) -> None:
        """Capture and display a frame with face detection."""
        if not self.running or self.cap is None:
            return

        ret, frame = self.cap.read()
        if ret:
            # Process frame for face detection
            frame = self.detector.process_frame(frame)

            # Convert BGR to RGB for display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize for display
            frame_rgb = cv2.resize(frame_rgb, (640, 480))

            # Convert to PhotoImage
            image = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(image=image)

            # Update display
            self.video_label.config(image=photo)
            self.video_label.image = photo

        # Schedule next update (~30 FPS)
        self.root.after(33, self._update_frame)

    def _on_close(self) -> None:
        """Handle window close event."""
        self.running = False
        if self.cap is not None:
            self.cap.release()
        self.root.destroy()

    def run(self) -> None:
        """Start the application main loop."""
        self.root.mainloop()
