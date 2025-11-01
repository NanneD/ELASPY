SIMULATION_PATIENT_OUTPUT_FILE_NAME
===================================

If ``SAVE_DFS=True``, a CSV file is generated where each row represents a patient. Each column contains information on the patient process according to the column names in ``DATA_COLUMNS_PATIENT``. The file is named according to the variable ``SIMULATION_PATIENT_OUTPUT_FILE_NAME``. The data columns are explained in the table below. Note that during the simulation, this dataframe is called ``output_patient``.

.. list-table:: patient dataframe columns.
   :widths: 5 5
   :header-rows: 1

   * - Column/feature
     - Explanation
   * - patient_ID
     - The patient ID.
   * - response_time
     - The response time for the patient.
   * - arrival_time
     - The arrival time of the patient.
   * - location_ID
     - The arrival location of the patient.
   * - nr_ambulances_available
     - The number of ambulances that are available when the patient is assigned to an ambulance. Note: this feature is not set if an ambulance can help a new patient when it just has finished helping another patient.
   * - nr_ambulances_not_assignable
     - The number of ambulances that are not assignable due to their batteries when the patient is assigned to an ambulance. Note: this feature is not set if an ambulance can help a new patient when it just has finished helping another patient.
   * - assigned_to_ambulance_nr
     - The ID of the ambulance the patient is assigned to.
   * - waiting_time_before_assigned
     - The waiting time of the patient before it is assigned.
   * - driving_time_to_patient
     - The driving time from the ambulance location to the patient.
   * - ambulance_arrival_time
     - The arrival time of the ambulance at the patient's location.
   * - on_site_aid_time
     - The on-site treatment time.
   * - to_hospital
     - Whether the patient has to be brought to hospital or not.
   * - hospital_ID
     - The assigned hospital (in case the patient needs to be transported). 
   * - driving_time_to_hospital
     - The driving time to the hospital from the patient's location.
   * - drop_off_time_hospital
     - The handover time at the hospital.
   * - finish_time
     - The time when the ambulance has finished helping the patient.
