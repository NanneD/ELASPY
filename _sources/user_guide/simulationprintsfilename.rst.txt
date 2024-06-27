SIMULATION_PRINTS_FILE_NAME
===========================

If ``SAVE_PRINTS_TXT=True``, the prints of the simulation are saved to a text (.txt) file. The file is named according to the variable ``SIMULATION_PRINTS_FILE_NAME``.  Prints are always provided on the run number, the number of calls, the mean estimates and the 95% confidence intervals (if applicable) of the performance measures and the running times of various components of the simulation.

There are two extra print options. If ``PRINT=True``, debug prints are printed that provide detailed information on the events of the simulation run. If ``PRINT_STATISTICS=True``, several extra simulation statistics are provided. It is also possible to set both print variables to ``True`` simultaneously.