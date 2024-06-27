.. _installation:

Installation
============

ELASPY can be installed in two ways: using a ZIP file or manually.

Using ZIP
+++++++++

You can easily download all files from the GitHub repository. Follow these steps:

1. Navigate to the `GitHub repository <https://github.com/NanneD/ELASPY>`_.
2. Select the green "Code" button, select "Local" and then "Download ZIP". This downloads the whole repository to your local machine.
3. Open the ZIP and rename the resulting folder to ``ELASPY``. Move the folder to a location of your preference, such as the ``documents`` folder.
4. Move to the ``ELASPY`` folder with the command line. For example, if you placed the ``ELASPY`` folder in the ``documents`` folder, you can use the following command:

.. code-block:: shell
   
   cd documents/ELASPY

5. Use an environment manager to create an environment in which you can run the code, such as `Anaconda <https://anaconda.org>`_ or `Miniconda <https://docs.anaconda.com/miniconda/>`_. You can use the following command to create an environment called ``ELASPY`` by using the ``requirements.yml`` file that is also part of your ``ELASPY`` folder:

.. code-block:: shell

   conda env create -f environment.yml

Installing the environment takes a few minutes.

6. Activate the environment. If you use Anaconda or Miniconda, you can use the following command:

.. code-block:: shell

   conda activate ELASPY

7. Done! See the :ref:`Quickstart<quickstart>` for information on how to run your first simulation.

.. note::

   If you use a different environment manager than Anaconda or Miniconda, please refer to the documentation of your environment manager on how to create an environment using a ``requirements.txt`` or ``environment.yml`` file.

Manually
++++++++

1. Create a folder on your desktop computer called ``ELASPY`` with three subfolders: ``data``, ``elaspy`` and ``results``.
2. Download the data from the `GitHub repository <https://github.com/NanneD/ELASPY>`_ and place these in your local ``data`` folder.
3. Download the Python files from the `GitHub repository <https://github.com/NanneD/ELASPY>`_ and place these in your local ``elaspy`` folder. If you also want to use the MEXCLP and/or advanced plotting scripts, download and place these Python files in separate folders in your local ``elaspy`` folder named ``mexclp`` and ``advanced_plotting``, respectively.
4. Move to the ``ELASPY`` folder with the command line. For example, if you placed the ``ELASPY`` folder in the documents folder, you can use the following command:

.. code-block:: shell
   
   cd documents/ELASPY

5. Use an environment manager to create an environment in which you can run the code, such as `Anaconda <https://anaconda.org>`_ or `Miniconda <https://docs.anaconda.com/miniconda/>`_. You can use the following command to create an environment called ``ELASPY`` by using the ``requirements.yml`` file that can be downloaded from the GitHub repository:

.. code-block:: shell

   conda env create -f environment.yml

Installing the environment takes a few minutes.

6. Activate the environment. If you use Anaconda or Miniconda, you can use the following command:

.. code-block:: shell

   conda activate ELASPY

7. Done! See the :ref:`Quickstart<quickstart>` for information on how to run your first simulation.

.. note::

   If you use a different environment manager than Anaconda or Miniconda, please refer to the documentation of your environment manager on how to create an environment using a ``requirements.txt`` or ``environment.yml`` file.

Checking the installation
+++++++++++++++++++++++++

You can check whether the installation was successful by running the included test suite. Follow these steps to do so:

1. Open the command line and move to the ``ELASPY`` folder.
2. Run the tests by using the following command:

.. code-block:: shell

	pytest elaspy/tests.py

3. If all tests pass: done! If not, please read the test output carefully to finish the installation.

.. note::

   It might be the case that pytest provides some warnings in the test results. If these are ``DepreciationWarnings`` of packages other than ``ELASPY``, you can ignore these.

Dependencies
++++++++++++
The package is dependent on several other Python packages, such as NumPy and pandas. These packages and their versions can be found in the requirement files (``requirements.txt`` and ``environment.yml``) in the `GitHub repository <https://github.com/NanneD/ELASPY>`_.