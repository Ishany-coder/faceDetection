"""Main application window with upload and detection stages."""

import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk

from face.encoder import FaceEncoder
from face.detector import FaceDetector


class FaceDetectionApp:
    """Main application with image upload and camera detection."""

    def __init__(self):
        """Initialize the face detection application."""
        self.encoder = FaceEncoder()
        self.detector = FaceDetector()
        self.cap = None
        self.running = False
        self.brightness = 0  # -100 to 100

        # Create main window
        self.root = tk.Tk()
        self.root.title("Face Detection")
        self.root.geometry("700x650")
        self.root.configure(bg="#2b2b2b")
        self.root.resizable(False, False)

        # Create frames for each stage
        self.upload_frame = tk.Frame(self.root, bg="#2b2b2b")
        self.detection_frame = tk.Frame(self.root, bg="#2b2b2b")

        self._setup_upload_stage()
        self._setup_detection_stage()

        # Start with upload stage
        self._show_upload_stage()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_upload_stage(self) -> None:
        """Setup the upload stage UI."""
        # Title
        title = tk.Label(
            self.upload_frame,
            text="Upload Reference Image",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#2b2b2b"
        )
        title.pack(pady=20)

        # Instructions
        instructions = tk.Label(
            self.upload_frame,
            text="Select an image with a face to match against",
            font=("Helvetica", 12),
            fg="#888888",
            bg="#2b2b2b"
        )
        instructions.pack(pady=5)

        # Preview area
        self.preview_label = tk.Label(
            self.upload_frame,
            bg="#1e1e1e",
            width=40,
            height=15
        )
        self.preview_label.pack(pady=20)

        # Status label
        self.upload_status = tk.Label(
            self.upload_frame,
            text="",
            font=("Helvetica", 11),
            fg="#888888",
            bg="#2b2b2b"
        )
        self.upload_status.pack(pady=5)

        # Buttons frame
        btn_frame = tk.Frame(self.upload_frame, bg="#2b2b2b")
        btn_frame.pack(pady=10)

        # Browse button
        browse_btn = tk.Button(
            btn_frame,
            text="Browse Image",
            font=("Helvetica", 12),
            command=self._browse_image,
            bg="#4a4a4a",
            fg="white",
            padx=20,
            pady=8
        )
        browse_btn.pack(side=tk.LEFT, padx=10)

        # Start button (initially disabled)
        self.start_btn = tk.Button(
            btn_frame,
            text="Start Detection",
            font=("Helvetica", 12),
            command=self._show_detection_stage,
            bg="#2ecc71",
            fg="white",
            padx=20,
            pady=8,
            state=tk.DISABLED
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)

    def _setup_detection_stage(self) -> None:
        """Setup the detection stage UI."""
        # Title
        title = tk.Label(
            self.detection_frame,
            text="Face Detection",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#2b2b2b"
        )
        title.pack(pady=5)

        # Video display
        self.video_label = tk.Label(self.detection_frame, bg="#1e1e1e")
        self.video_label.pack(pady=5)

        # Brightness control frame
        brightness_frame = tk.Frame(self.detection_frame, bg="#2b2b2b")
        brightness_frame.pack(pady=5)

        brightness_label = tk.Label(
            brightness_frame,
            text="Brightness:",
            font=("Helvetica", 11),
            fg="white",
            bg="#2b2b2b"
        )
        brightness_label.pack(side=tk.LEFT, padx=5)

        self.brightness_slider = tk.Scale(
            brightness_frame,
            from_=-100,
            to=100,
            orient=tk.HORIZONTAL,
            length=300,
            bg="#2b2b2b",
            fg="white",
            highlightthickness=0,
            troughcolor="#1e1e1e",
            command=self._on_brightness_change
        )
        self.brightness_slider.set(0)
        self.brightness_slider.pack(side=tk.LEFT, padx=5)

        # Status label
        self.detection_status = tk.Label(
            self.detection_frame,
            text="",
            font=("Helvetica", 12),
            fg="#888888",
            bg="#2b2b2b"
        )
        self.detection_status.pack(pady=5)

        # Back button
        back_btn = tk.Button(
            self.detection_frame,
            text="Back to Upload",
            font=("Helvetica", 12),
            command=self._show_upload_stage,
            bg="#4a4a4a",
            fg="white",
            padx=20,
            pady=8
        )
        back_btn.pack(pady=5)

    def _on_brightness_change(self, value: str) -> None:
        """Handle brightness slider change."""
        self.brightness = int(value)

    def _browse_image(self) -> None:
        """Open file dialog to select an image."""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("All files", "*.*")
        ]
        filepath = filedialog.askopenfilename(filetypes=filetypes)

        if filepath:
            self._load_image(filepath)

    def _load_image(self, filepath: str) -> None:
        """Load and validate the selected image."""
        # Show preview
        try:
            image = Image.open(filepath)
            image.thumbnail((300, 250))
            photo = ImageTk.PhotoImage(image)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo
        except Exception as e:
            self.upload_status.config(text=f"Error loading preview: {e}", fg="#ff6b6b")
            return

        # Load face encoding
        self.upload_status.config(text="Analyzing face...", fg="#f1c40f")
        self.root.update()

        success, message = self.encoder.load_reference_image(filepath)

        if success:
            self.upload_status.config(text=message, fg="#2ecc71")
            self.start_btn.config(state=tk.NORMAL)
        else:
            self.upload_status.config(text=message, fg="#ff6b6b")
            self.start_btn.config(state=tk.DISABLED)

    def _show_upload_stage(self) -> None:
        """Show the upload stage."""
        self._stop_camera()
        self.detection_frame.pack_forget()
        self.upload_frame.pack(expand=True, fill="both")

    def _show_detection_stage(self) -> None:
        """Show the detection stage and start camera."""
        # Set reference in detector
        encoding = self.encoder.get_encoding()
        if encoding is not None:
            self.detector.set_reference(encoding)

        self.upload_frame.pack_forget()
        self.detection_frame.pack(expand=True, fill="both")
        self._start_camera()

    def _start_camera(self) -> None:
        """Initialize and start the webcam capture."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open webcam")
            self.detection_status.config(text="Camera not available", fg="#ff6b6b")
            return

        self.running = True
        self.detection_status.config(text="Green = Match | Red = No Match", fg="#4ecdc4")
        self._update_frame()

    def _stop_camera(self) -> None:
        """Stop the webcam capture."""
        self.running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def _adjust_brightness(self, frame: np.ndarray) -> np.ndarray:
        """Adjust frame brightness."""
        if self.brightness == 0:
            return frame

        # Convert to float, adjust, and clip
        adjusted = frame.astype(np.float32) + self.brightness
        adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
        return adjusted

    def _update_frame(self) -> None:
        """Capture and display a frame with face detection."""
        if not self.running or self.cap is None:
            return

        ret, frame = self.cap.read()
        if ret:
            # Adjust brightness
            frame = self._adjust_brightness(frame)

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
        self._stop_camera()
        self.root.destroy()

    def run(self) -> None:
        """Start the application main loop."""
        self.root.mainloop()
