.. _quickstart:

Quickstart
==========

For installation instructions, please see the :ref:`installation<installation>` section.

The simulator works through the main interface found in ``elaspy/main.py``. All simulation parameters and input data can be set in this script. The simulation can be run by simply running ``elaspy/main.py`` either through an IDE or through the command line.

IDE Spyder
++++++++++

The IDE Spyder is automatically installed if you installed the ``ELASPY`` environment by using the ``environment.yml`` file (see :ref:`installation instructions<installation>`). First, activate the ``ELASPY`` environment by using the following command in the command line (assuming you use `Anaconda <https://anaconda.org>`_ or `Miniconda <https://docs.anaconda.com/miniconda/>`_):

.. code-block:: shell

   conda activate ELASPY

Start Spyder by using the following command:

.. code-block:: shell

   spyder

Next, open the ``elaspy/main.py`` file in Spyder. You can then run a simulation by pressing the "run file" button.

Command line
++++++++++++
First, open the command line and move to the ELASPY folder on your computer (see the :ref:`installation instructions<installation>`). You can run the code through the command line by using:

.. code-block:: shell

	python elaspy/main.py

or, depending on your Python set-up:

.. code-block:: shell

	python3 elaspy/main.py

Input and output
++++++++++++++++
Simulation runs are saved in the ``results`` folder, but the location can be changed in the script. You can easily experiment with different parameters and input data as well. The code includes an input validator that automatically checks upon running whether the provided data and parameters are valid. If invalid input is detected, an ``Exception`` is thrown with an explanation that specifies which input is invalid and how the problem can be solved. The required parameters are both explained in the ``elaspy/main.py`` script itself and in the :ref:`API<mainapi>`.

The simulator requires input data to work. Input data based on the province of Utrecht, the Netherlands, is provided in the `GitHub repository <https://github.com/NanneD/ELASPY>`_. More information on the input data can be found in the :ref:`input data<inputdata>` section.

That's it! Have fun running electric ambulance simulations.