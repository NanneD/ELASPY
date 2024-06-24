battery_plot_mruns.py
=====================

This script makes a plot of the state of charge (SoC) of all ambulances for multiple runs. Figure 4 of the paper by Dieleman and Jagtenberg was generated with this script.

Running ``battery_plot_mruns.py``
++++++++++++++++++++++++++++++++++++++++++++++++++

You can run the script by using the command line or an IDE such as Spyder. To run the script on the command line, first move to your local ELASPY folder and then run the following:

.. code-block:: shell

	python elaspy/advanced_plotting/battery_plot_mruns.py

or, depending on your Python installation:

.. code-block:: shell

	python3 elaspy/advanced_plotting/battery_plot_mruns.py

If you use an IDE, you can simply open the file and press "Run file".

Input
+++++
The script requires several data sets and parameters to work. The ambulance dataframe that is saved according to the variable ``SIMULATION_AMBULANCE_OUTPUT_FILE_NAME`` of multiple runs is used. The parameters of the script are explained in the :ref:`API<batteryplotmrunsapi>`.

Output
++++++
The output, if ``SAVE_OUTPUT=True``, consists of the plot (named according to ``PLOT_NAME``) and a text (.txt) file that contains the used parameters (named according to ``RUN_PARAMETERS_FILE_NAME``). If ``SAVE_OUTPUT=False``, then the plot is provided, but not saved.