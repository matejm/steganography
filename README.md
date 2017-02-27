# Steganography

Simple python program for hiding text file into least significant bits of an image.


# Dependencies

- [Pillow](https://python-pillow.org/)
- [PyCrypto](https://www.dlitz.net/software/pycrypto/)
- [Tkinter](http://tkinter.unpythonic.net/)
- [Sphinx](http://www.sphinx-doc.org/)

# Usage

    cd src/

    # command line interface
    python3 steganography.py hide <input_image> <output_image> <secret_file>
    python3 steganography.py find <input_image> <secret_file_output>

    # graphical interface
    python3 GUI.py

# Documentation

    cd docs/
    make html
