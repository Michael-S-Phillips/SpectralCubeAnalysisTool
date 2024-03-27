# Demo_app

GUI Tool for Advanced Analysis of Hyperspectral Image Cubes. This application is designed to facilitate advanced management and analysis of hyperspectral image data, offering features such as ROI management, spectral plotting, session management, and multi-image handling with geospatial context.

## Overview

Demo_app integrates PyQt for its GUI components, with Python libraries like NumPy, SciPy, and GDAL for backend processing, aiming to provide a comprehensive tool for hyperspectral image analysis. The project includes main windows for application control, widgets for specific functionalities like ROI management and spectral analysis, and dialogues for session management.

## Features

- **Enhanced Regions of Interest (ROIs) Management**: Facilitates easy management and annotation of ROIs.
- **Advanced Spectral Plotting**: Supports plotting mean, standard deviation, and comparison with reference spectra.
- **Session Management**: Allows saving and loading of analysis sessions.
- **Multiple Image Windows**: Enables opening and managing multiple hyperspectral image cubes simultaneously.
- **Geospatial Information Display**: Displays lat/lon coordinates on image hover, providing a rich geospatial context.

## Getting Started

### Requirements

- Python 3.x
- PyQt5
- NumPy, SciPy, GDAL

### Quickstart

1. Clone the repository to your local machine.
2. Install required Python packages: `pip install PyQt5 numpy scipy GDAL`.
3. Run the application: `python main_window.py`.

### License

Copyright (c) 2024.