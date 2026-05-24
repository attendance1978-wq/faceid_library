@"
Installation
============

Requirements
------------

- Python 3.11 or higher (TensorFlow doesn't support Python 3.14+)
- 4GB RAM minimum
- Webcam (optional, for real-time recognition)
- Windows, Linux, or macOS

Install from PyPI
-----------------

The easiest way to install FaceID is via pip:

.. code-block:: bash

   pip install faceid-lib

Install from GitHub
-------------------

For the latest development version:

.. code-block:: bash

   git clone https://github.com/attendance1978-wq/faceid_library.git
   cd faceid_library
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .

Install with Poetry
-------------------

.. code-block:: bash

   poetry add faceid-lib

Troubleshooting
---------------

MediaPipe Compatibility
~~~~~~~~~~~~~~~~~~~~~~~

If you see warnings about MediaPipe, install the compatible version:

.. code-block:: bash

   pip uninstall mediapipe
   pip install mediapipe==0.8.10

Python Version
~~~~~~~~~~~~~~

Make sure you're using Python 3.11:

.. code-block:: bash

   python --version
   # Should show Python 3.11.x

DLL Load Errors (Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~

If you encounter DLL errors, install the Microsoft Visual C++ Redistributable:

https://aka.ms/vs/17/release/vc_redist.x64.exe
"@ | Out-File -FilePath installation.rst -Encoding UTF8