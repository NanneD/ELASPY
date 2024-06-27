jitter_plots_scenarios.py
=========================

This script makes two jitter plots for all scenarios; one for the mean and one for the 95% empirical quantile of the response times. Figures 11, 12 and 13 of the paper by Dieleman and Jagtenberg were generated with this script.

Running ``jitter_plots_scenarios.py``
++++++++++++++++++++++++++++++++++++++++++++++++++

You can run the script by using the command line or an IDE such as Spyder. To run the script on the command line, first move to your local ELASPY folder and then run the following:

.. code-block:: shell

	python elaspy/advanced_plotting/jitter_plots_scenarios.py

or, depending on your Python installation:

.. code-block:: shell

	python3 elaspy/advanced_plotting/jitter_plots_scenarios.py

If you use an IDE, you can simply open the file and press "Run file".

Input
+++++
The script requires several data sets and parameters to work. The data sets of the mean and 95% empirical quantiles of each run (saved according to the variables ``MEAN_RESPONSE_TIMES_FILE_NAME`` and ``EMP_QUANTILE_RESPONSE_TIMES_FILE_NAME``) of multiple scenarios are used. The parameters of the script are explained in the :ref:`API<jitterplotsscenariosapi>`.

Output
++++++
The output, if ``SAVE_OUTPUT=True``, consists of the plot (named according to ``PLOT_NAME``) and a text (.txt) file that contains the used parameters (named according to ``RUN_PARAMETERS_FILE_NAME``). If ``SAVE_OUTPUT=False``, then the plot is provided, but not saved.