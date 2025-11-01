DROP_OFF_TIMES_FILE
===================

CSV file that contains the handover at hospital duration of each patient if historical data is used (``LOAD_INPUT_DATA=True``) in minutes. The table contains an example. In the example, patients 0, 1 and 2 have a handover time of 24.9004, 43.4301 and 35.4312 minutes, respectively. Note that each patient requires a handover time *even if the patient does not have to be transported to the hospital*. You can simply assign a dummy value in this case.

.. list-table:: Example DROP_OFF_TIMES_FILE.
   :widths: 5
   :header-rows: 1

   * - 0
   * - 24.9004
   * - 43.4301
   * - 35.4312