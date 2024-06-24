strip_plots.py
====================

This script makes a strip plot of the mean and 95% empirical quantile of the response times for increasing energy consumption. Figure 8 of the paper by Dieleman and Jagtenberg were generated with this script.

Running ``strip_plots.py``
++++++++++++++++++++++++++++++++++++++++++++++++++

You can run the script by using the command line or an IDE such as Spyder. To run the script on the command line, first move to your local ELASPY folder and then run the following:

.. code-block:: shell

	python elaspy/advanced_plotting/strip_plots.py

or, depending on your Python installation:

.. code-block:: shell

	python3 elaspy/advanced_plotting/strip_plots.py

If you use an IDE, you can simply open the file and press "Run file".

Input
+++++
The script requires several data sets and parameters to work. The data sets of the mean and 95% empirical quantiles of each run (saved according to the variables ``MEAN_RESPONSE_TIMES_FILE_NAME`` and ``EMP_QUANTILE_RESPONSE_TIMES_FILE_NAME``) of multiple energy consumption levels are used. The parameters of the script are explained in the :ref:`API<stripplotsapi>`.

Output
++++++
The output, if ``SAVE_OUTPUT=True``, consists of the plot (named according to ``PLOT_NAME``) and a text (.txt) file that contains the used parameters (named according to ``RUN_PARAMETERS_FILE_NAME``). If ``SAVE_OUTPUT=False``, then the plot is provided, but not saved.