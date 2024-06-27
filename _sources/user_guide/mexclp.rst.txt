.. _mexclp:

MEXCLP
======

The Maximum Expected Coverage Location Problem (MEXCLP) can be used to distribute ambulances over bases.

Running ``MEXCLP.py``
+++++++++++++++++++++++++

You can run the script by using the command line. To run the script on the command line, first move to your local ELASPY folder and then run the following:

.. code-block:: shell

	python elaspy/mexclp/MEXCLP.py

or, depending on your Python installation:

.. code-block:: shell

	python3 elaspy/mexclp/MEXCLP.py

.. tip::

   If you run into problems using the ``PULP_CBC_CMD`` solver, you can do the following:

   1. Activate the ELASPY environment in the command line.

   2. Use the following command to remove pulp from the environment:

   .. code-block:: shell
      
      conda remove pulp

   3. Re-install pulp by using the following command:

   .. code-block:: shell
      
      pip install 'pulp==2.7.0'

   4. Done! The ``PULP_CBC_CMD`` should now work.

Input
+++++
The script requires several data sets and parameters to work. The parameters are explained in the :ref:`API<mexclpapi>`, and the data sets that are required are :ref:`NODES_FILE<nodesfile>`, :ref:`BASE_LOCATIONS_FILE<baselocationsfile>` and :ref:`TRAVEL_TIMES_FILE<traveltimesfile>`.

Output
++++++
The script provides the solved model in an .lp format and also a csv file with the number of ambulances stationed at the postal codes (i.e., nodes). Both named according to the variable ``RESULTS_FILE``. The table below provides an example of such an output file. In the example, two ambulances have their base at node 1, one ambulance at node 5 and three ambulances at node 3. The script also provides some prints with information about the optimization.

.. list-table:: Example mexclp output csv file.
   :widths: 5 5 
   :header-rows: 1

   * - Postal code
     - number of ambulances
   * - 1
     - 2
   * - 5
     - 1
   * - 3
     - 3