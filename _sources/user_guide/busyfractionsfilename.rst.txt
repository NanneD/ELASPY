BUSY_FRACTIONS_FILE_NAME
========================

If ``SAVE_OUTPUT=True``, a CSV file is generated where each row represents the empirical busy fraction of one simulation run. The file is named according to the variable ``BUSY_FRACTIONS_FILE_NAME``. The busy fraction is a value between 0 and 1, where 1 indicates that the ambulances are busy full-time. A warm-up and cool-down period is used for the calculation of the busy fraction. These can be determined by the parameters ``AT_BOUNDARY`` (warm-up) and ``FT_BOUNDARY`` (cool-down). In the example below, the busy fraction of the first run is 0.390, of the second run 0.445 and of the third run 0.312.

.. list-table:: Example output busy fraction.
   :widths: 5 5
   :header-rows: 1

   * -
     - 0
   * - 0
     - 0.390
   * - 1
     - 0.445
   * - 2
     - 0.312