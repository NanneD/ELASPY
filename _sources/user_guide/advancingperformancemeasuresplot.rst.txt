advancing_performance_measures_plot.py
======================================

This script calculates the mean and corresponding 95% confidence interval cumulatively for two performance measures (mean and 95% empirical quantile of the response times) for each run. Figure 10 of the paper by Dieleman and Jagtenberg was generated with this script.

Running ``advancing_performance_measures_plot.py``
++++++++++++++++++++++++++++++++++++++++++++++++++

You can run the script by using the command line or an IDE such as Spyder. To run the script on the command line, first move to your local ELASPY folder and then run the following:

.. code-block:: shell

	python elaspy/advanced_plotting/advancing_performance_measures_plot.py

or, depending on your Python installation:

.. code-block:: shell

	python3 elaspy/advanced_plotting/advancing_performance_measures_plot.py

If you use an IDE, you can simply open the file and press "Run file".

Input
+++++
The script requires several data sets and parameters to work. The data sets of the mean and 95% empirical quantiles of each run (saved according to the variables ``MEAN_RESPONSE_TIMES_FILE_NAME`` and ``EMP_QUANTILE_RESPONSE_TIMES_FILE_NAME``) are used. To create Figure 10, three different runs were performed, each with a different number of diesel ambulances. The parameters of the script are explained in the :ref:`API<advancingperformancemeasuresplotapi>`.

Output
++++++
The output, if ``SAVE_OUTPUT=True``, consists of the plot (named according to ``PLOT_NAME``) and a text (.txt) file that contains the used parameters (named according to ``RUN_PARAMETERS_FILE_NAME``). If ``SAVE_OUTPUT=False``, then the plot is provided, but not saved.