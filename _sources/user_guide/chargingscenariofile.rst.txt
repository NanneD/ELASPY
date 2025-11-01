CHARGING_SCENARIO_FILE
======================

CSV file that contains the number of fast and regular chargers at each base and hospital together with their charging speeds/power outputs. It contains five columns called ``Location``, ``Number of regular chargers``, ``Speed regular chargers (kW)``, ``Number of fast chargers`` and ``Speed fast chargers (kW)``. A ``location`` consists of the node number together with a ``B`` for "base" or ``H`` for "hospital". You can specify the number of regular and fast chargers and their speed at the location by filling in the rest of the columns.

The table below shows an example. In the example, there is one regular charger at the base at node 2 with a power output of 11 kW. There is no fast charger at this base. At the hospital at node 4, there are 2 regular chargers with a power output of 20 kW and one fast charger with a power output of 50 kW.

.. list-table:: Example CHARGING_SCENARIO_FILE.
   :widths: 5 5 5 5 5
   :header-rows: 1

   * - Location
     - Number of regular chargers
     - Speed regular chargers (kW)
     - Number of fast chargers
     - Speed fast chargers (kW)
   * - 2B
     - 1
     - 11
     - 0
     - 50
   * - 4H
     - 2
     - 20
     - 1
     - 50