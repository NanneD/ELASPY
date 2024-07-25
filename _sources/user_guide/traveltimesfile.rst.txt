.. _traveltimesfile:

TRAVEL_TIMES_FILE
=================

CSV file that contains the data with the travel times between nodes *with siren on* (in minutes). The columns and rows contain the nodes of the region. Selecting a cell is equal to selecting the travel time between the row node to the column node. The table below contains a small example of valid input. For example, the travel time with siren on between node 1 and 3 is 18 minutes.

.. list-table:: Example TRAVEL_TIMES_FILE.
   :widths: 5 5 5 5
   :header-rows: 1

   * - Node
     - 1
     - 2
     - 3
   * - 1
     - 0
     - 20
     - 18
   * - 2
     - 12
     - 0
     - 5
   * - 3
     - 17
     - 15
     - 0