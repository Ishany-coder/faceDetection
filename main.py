#!/usr/bin/env python3
"""
Face Detection Application

A simple face detection app that runs entirely locally.
Uses your webcam to detect and highlight faces in real-time.
"""

from gui.app import FaceDetectionApp


def main():
    """Entry point for the face detection application."""
    app = FaceDetectionApp()
    app.run()


if __name__ == "__main__":
    main()
