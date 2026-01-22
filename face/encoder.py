"""Face encoding from reference images."""

import face_recognition
import numpy as np


class FaceEncoder:
    """Loads reference images and extracts face encodings."""

    def __init__(self):
        """Initialize the face encoder."""
        self.reference_encoding: np.ndarray | None = None

    def _get_largest_face(self, face_locations: list) -> tuple:
        """Get the largest face from a list of face locations."""
        largest_area = 0
        largest_face = None

        for (top, right, bottom, left) in face_locations:
            area = (bottom - top) * (right - left)
            if area > largest_area:
                largest_area = area
                largest_face = (top, right, bottom, left)

        return largest_face

    def load_reference_image(self, image_path: str) -> tuple[bool, str]:
        """
        Load a reference image and extract the face encoding.

        Args:
            image_path: Path to the image file.

        Returns:
            Tuple of (success, message).
        """
        try:
            image = face_recognition.load_image_file(image_path)

            # Use HOG model with upsampling (lighter on memory than CNN)
            face_locations = face_recognition.face_locations(
                image,
                number_of_times_to_upsample=1,
                model="hog"
            )

            if len(face_locations) == 0:
                return False, "No face detected in the image"

            # If multiple faces detected, use the largest one
            if len(face_locations) > 1:
                largest_face = self._get_largest_face(face_locations)
                face_locations = [largest_face]

            encodings = face_recognition.face_encodings(image, face_locations)
            if len(encodings) == 0:
                return False, "Could not encode the face"

            self.reference_encoding = encodings[0]

            return True, "Face loaded successfully"

        except Exception as e:
            return False, f"Error loading image: {str(e)}"

    def get_encoding(self) -> np.ndarray | None:
        """Return the stored face encoding."""
        return self.reference_encoding

    def has_reference(self) -> bool:
        """Check if a reference encoding is loaded."""
        return self.reference_encoding is not None

    def clear(self) -> None:
        """Clear the current reference encoding."""
        self.reference_encoding = None
