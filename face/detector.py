"""Real-time face detection."""

import cv2
import face_recognition
import numpy as np


class FaceDetector:
    """Detects faces in video frames."""

    def __init__(self):
        """Initialize the face detector."""
        pass

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Process a video frame: detect faces and draw bounding boxes.

        Args:
            frame: BGR image from OpenCV (numpy array).

        Returns:
            Frame with face boxes drawn.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Scale down for faster processing
        small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

        face_locations = face_recognition.face_locations(small_frame)

        for (top, right, bottom, left) in face_locations:
            # Scale back up face locations
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            color = (0, 255, 0)  # Green

            # Draw rectangle around face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Draw label background
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), color, cv2.FILLED)

            # Draw label text
            cv2.putText(
                frame,
                "Face",
                (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_DUPLEX,
                0.6,
                (255, 255, 255),
                1
            )

        return frame
