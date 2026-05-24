@"
Contributing Guide
==================

We welcome contributions! Here's how you can help improve FaceID.

Reporting Issues
----------------

- Use the GitHub issue tracker: https://github.com/attendance1978-wq/faceid_library/issues
- Include your Python version and operating system
- Provide a minimal code example that reproduces the issue
- Include any error messages or logs

Feature Requests
----------------

We're always open to new ideas! To request a feature:

1. Check if the feature already exists or is planned
2. Create a detailed issue describing the feature
3. Explain the use case and benefits

Pull Requests
-------------

1. Fork the repository
2. Create a feature branch:
   .. code-block:: bash
   
      git checkout -b feature/amazing-feature

3. Make your changes
4. Run tests if available
5. Commit with clear messages:
   .. code-block:: bash
   
      git commit -m "Add amazing feature"

6. Push to your fork:
   .. code-block:: bash
   
      git push origin feature/amazing-feature

7. Open a Pull Request

Development Setup
-----------------

.. code-block:: bash

   git clone https://github.com/attendance1978-wq/faceid_library.git
   cd faceid_library
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -e .[dev]

Coding Standards
----------------

- Follow PEP 8 guidelines
- Write docstrings for all public functions
- Add type hints where possible
- Keep functions focused and small (single responsibility)
- Use meaningful variable names

Testing
-------

Run tests with pytest:

.. code-block:: bash

   pip install pytest pytest-cov
   pytest tests/ -v --cov=faceid

Code Style
----------

We use Black for code formatting:

.. code-block:: bash

   pip install black
   black faceid/

Documentation
-------------

To build documentation locally:

.. code-block:: bash

   pip install sphinx sphinx-rtd-theme
   cd docs
   make html

License
-------

By contributing, you agree that your contributions will be licensed under the MIT License.

Code of Conduct
---------------

Please be respectful and constructive. We follow the Python Community Code of Conduct:

https://www.python.org/psf/codeofconduct/

Questions?
----------

Feel free to open an issue or contact the maintainers:

- GitHub: https://github.com/attendance1978-wq
- Project: https://github.com/attendance1978-wq/faceid_library

Thank you for contributing! 🚀
"@ | Out-File -FilePath contributing.rst -Encoding UTF8