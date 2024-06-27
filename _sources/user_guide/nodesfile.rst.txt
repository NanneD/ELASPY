.. _nodesfile:

NODES_FILE
==========

CSV file that contains the data about the nodes of the region. It contains four columns called ``x`` ``y``, ``inhabitants`` and ``inhabitantsIncreasing``. The ``x`` and ``y`` columns contain the x-coordinate and y-coordinate of the node, respectively. The ``inhabitants`` column provides the normalized number of inhabitants (i.e., the column-sum is equal to 1). The ``inhabitantsIncreasing`` column is simply the cumulative sum of the ``inhabitants`` column. The table illustrates an example.

.. list-table:: Example NODES_FILE.
   :widths: 5 5 5 5 5
   :header-rows: 1

   * - postal code
     - x
     - y
     - inhabitants
     - inhabitantsIncreasing
   * - 1
     - 100000.00
     - 200000.00
     - 0.10
     - 0.10
   * - 2
     - 100100.00
     - 200100.00
     - 0.50
     - 0.60
   * - 3
     - 100200.00
     - 200200.00
     - 0.40
     - 1.00