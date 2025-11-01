EMP_QUANTILE_RESPONSE_TIMES_FILE_NAME
=====================================

If ``SAVE_OUTPUT=True``, a CSV file is generated where each row represents the 95% empirical quantile of the response time of one simulation run in minutes. The file is named according to the variable ``EMP_QUANTILE_RESPONSE_TIMES_FILE_NAME``. In the example below, the 95% empirical quantile of the response time of the first run is 17.312 minutes, of the second run 20.431 minutes and of the third run 27.921 minutes.

.. list-table:: Example output 95% empirical quantile of the response times.
   :widths: 5 5
   :header-rows: 1

   * -
     - 0
   * - 0
     - 17.312
   * - 1
     - 20.431
   * - 2
     - 27.921