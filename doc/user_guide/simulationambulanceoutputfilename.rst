SIMULATION_AMBULANCE_OUTPUT_FILE_NAME
=====================================

If ``SAVE_DFS=True``, a CSV file is generated where each row represents an ambulance. The ambulance events are documented in this dataframe according to the columns of ``DATA_COLUMNS_AMBULANCE``. The file is named according to the variable ``SIMULATION_AMBULANCE_OUTPUT_FILE_NAME``. The data columns are explained in the table below.  Note that during the simulation, this dataframe is called ``output_ambulance``.

.. list-table:: ambulance dataframe columns.
   :widths: 5 5
   :header-rows: 1

   * - Column/feature
     - Explanation
   * - ambulance_ID
     - The ambulance ID.
   * - time
     - The time of the event.
   * - battery_level_before
     - The battery level before the event.
   * - battery_level_after
     - The battery level after the event.
   * - use_or_charge
     - "1" if the battery was charged, "0" if the battery was used.
   * - idle_or_driving_decrease
     - "1" if the ambulance drove, "0" if the ambulance was idle.
   * - idle_time
     - The idle time of the ambulance.
   * - source_location_ID
     - The initial location (i.e., source) of the ambulance.
   * - target_location_ID
     - The target location the ambulance drove to.
   * - driven_km
     - The number of kilometers driven.
   * - battery_decrease
     - The battery decrease in kWh.
   * - charging_type
     - The charging type. "2" for charging at the base, "1" for charging at the hospital after treating a patient and "0" for charging during patient handover.
   * - charging_location_ID
     - The charging location ID.
   * - speed_charger
     - The speed of the charger (in kW).
   * - charging_success
     - "1" if the ambulance could charge, "0" if the ambulance could not charge during the charging session.
   * - waiting_time
     - The waiting time in minutes before an ambulance could charge or was assigned to another patient while waiting to charge.
   * - charging_interrupted
     - "1" if the charging session was interrupted, "0" if it was not interrupted.
   * - charging_time
     - The time the ambulance charged. It is 0 if the ambulance could not charge before it was assigned to a new patient.
   * - battery_increase
     - The battery increase in kWh.