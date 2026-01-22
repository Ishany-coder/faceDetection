"""Real-time face detection and matching."""

import cv2
import face_recognition
import numpy as np


class FaceDetector:
    """Detects faces in video frames and matches against a reference."""

    def __init__(self, match_tolerance: float = 0.6):
        """
        Initialize the face detector.

        Args:
            match_tolerance: How much distance between faces to consider a match.
                            Lower is more strict. Default 0.6 is standard.
        """
        self.match_tolerance = match_tolerance
        self.reference_encoding: np.ndarray | None = None

    def set_reference(self, encoding: np.ndarray) -> None:
        """Set the reference face encoding to match against."""
        self.reference_encoding = encoding

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Process a video frame: detect faces and draw bounding boxes.

        Args:
            frame: BGR image from OpenCV (numpy array).

        Returns:
            Frame with face boxes drawn (green for match, red for no match).
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Scale down for faster processing
        small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Scale back up face locations
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Check if this face matches the reference
            is_match = False
            if self.reference_encoding is not None:
                matches = face_recognition.compare_faces(
                    [self.reference_encoding],
                    face_encoding,
                    tolerance=self.match_tolerance
                )
                is_match = matches[0]

            # Draw box and label
            if is_match:
                color = (0, 255, 0)  # Green for match
                label = "MATCH"
            else:
                color = (0, 0, 255)  # Red for no match
                label = "NO MATCH"

            # Draw rectangle around face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Draw label background
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), color, cv2.FILLED)

            # Draw label text
            cv2.putText(
                frame,
                label,
                (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_DUPLEX,
                0.6,
                (255, 255, 255),
                1
            )

        return frame
