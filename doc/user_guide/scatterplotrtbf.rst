scatterplot_rt_bf.py
=========================

This script makes a scatterplot of four scenarios, where the busy fraction is plotted on the x-axis and the mean response time on the y-axis. Figures 5 and 6 of the paper by Dieleman and Jagtenberg were generated with this script.

Running ``scatterplot_rt_bf.py``
++++++++++++++++++++++++++++++++++++++++++++++++++

You can run the script by using the command line or an IDE such as Spyder. To run the script on the command line, first move to your local ELASPY folder and then run the following:

.. code-block:: shell

	python elaspy/advanced_plotting/scatterplot_rt_bf.py

or, depending on your Python installation:

.. code-block:: shell

	python3 elaspy/advanced_plotting/scatterplot_rt_bf.py

If you use an IDE, you can simply open the file and press "Run file".

Input
+++++
The script requires several data sets and parameters to work. Four different data sets of the mean and 95% empirical quantiles of each run (saved according to the variables ``MEAN_RESPONSE_TIMES_FILE_NAME`` and ``EMP_QUANTILE_RESPONSE_TIMES_FILE_NAME``) are used. The parameters of the script are explained in the :ref:`API<scatterplotrtbfapi>`.

Output
++++++
The output, if ``SAVE_OUTPUT=True``, consists of the plot (named according to ``PLOT_NAME``) and a text (.txt) file that contains the used parameters (named according to ``RUN_PARAMETERS_FILE_NAME``). If ``SAVE_OUTPUT=False``, then the plot is provided, but not saved.