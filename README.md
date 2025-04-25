# Orbitron-Multiplet

An advanced scientific application for multiplet calculations and orbital analysis.

## Overview

Orbitron-Multiplet is a GUI application that provides a user-friendly interface for the Multiplet2 code, enabling scientists and researchers to perform complex calculations related to electron orbitals and atomic structure.

The application allows users to:
- Create input files for Multiplet2 calculations
- Run the Multiplet2 executable with customized parameters
- Convert output files for further analysis

## Features

- **Intuitive GUI**: Built with PyQt6 for a modern, user-friendly interface
- **Cross-Platform**: Compatible with macOS, Linux, and Windows (with appropriate build tools)
- **Versatile Input Creation**: Create complex input files through a simple interface
- **Real-time Calculation**: Run multiplet calculations directly from the GUI
- **Data Conversion**: Convert rpesalms.dat output files to rpesalms.edac format

## Installation

See the detailed installation and build instructions in:
- [BUILD_README.md](RPES/BUILD_README.md) - Basic build instructions
- [CROSS_PLATFORM_README.md](RPES/CROSS_PLATFORM_README.md) - Cross-platform build instructions

## Requirements

- Python 3.6+
- gfortran & gcc compilers
- PyQt6
- Platform-specific dependencies (see build instructions)

## Quick Start

1. **Compile the multiplet executable**:
   ```
   cd RPES/src
   ./compile
   cp multiplet ..
   ```

2. **Run the GUI**:
   ```
   cd RPES
   ./run_gui.sh
   ```

3. **Build a standalone application** (optional):
   ```
   cd RPES
   source venv/bin/activate
   python build_app.py
   ```

## Directory Structure

- `/RPES`: Main application directory
  - `/src`: Source code for the multiplet executable
  - `/Test_Output2`: Output files from tests
  - `multiplet_gui.py`: Main GUI application
  - `build_app.py`: Script to build standalone application
  - `cross_platform_compile.py`: Cross-platform compilation script
  - `cross_platform_build.py`: Cross-platform build script

## License

[Specify license information]

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## Acknowledgements

[Add acknowledgements and credits as appropriate] 