# Steganography

Simple python program for hiding text file into least significant bits of an image.


# Dependencies

- [Pillow](https://python-pillow.org/)
- [PyCrypto](https://www.dlitz.net/software/pycrypto/)
- [Sphinx](http://www.sphinx-doc.org/)

# Usage

    python3 steganography.py hide <input_image> <output_image> <secret_file>
    python3 steganography.py find <input_image> <secret_file_output>

# Documentation

    cd docs/
    make html

# Todo

- add GUI
- implement exceptions
- speed optimization
