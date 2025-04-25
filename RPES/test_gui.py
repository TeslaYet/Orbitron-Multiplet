#!/usr/bin/env python3
"""
Test script to verify PyQt6 installation and GUI module import
"""

import sys

try:
    print("Importing PyQt6...")
    from PyQt6.QtWidgets import QApplication, QLabel
    print("PyQt6 imported successfully!")
    
    print("Creating simple PyQt6 window...")
    app = QApplication(sys.argv)
    label = QLabel("PyQt6 is working correctly!")
    label.show()
    
    print("Attempting to import GUI module...")
    from multiplet_gui import MultipletGUI
    print("GUI module imported successfully!")
    
    print("All tests passed! The GUI should work correctly.")
    print("Press Ctrl+C to exit this test or close the window.")
    
    sys.exit(app.exec())
    
except ImportError as e:
    print(f"Import error: {e}")
    print("PyQt6 may not be installed or there might be issues with the GUI module.")
    print("Try installing the required packages with: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1) 