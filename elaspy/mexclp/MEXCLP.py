"""
This is an implemenation of the MEXCLP model.

By solving MEXCLP (Maximum Expected Coverage Location Problem), ambulances
are assigned to bases to maximize on-time arrivals. Below, all parameters are 
discussed.

Parameters
----------
q : float
    Input parameter called the busy fraction. Can be interpreted as the
    probability that any ambulance is busy at any time.
NUM_AMBULANCES : int
    The number of ambulances that should be assigned to bases.
TIME_THRESHOLD : float
    Represents the threshold for the driving time in minutes.
DATA_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the input data is located.
OUTPUT_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the output files should be saved.
NODES_FILE : str
    The name of the file that contains the data with the nodes of the region.
BASE_LOCATIONS_FILE : str
    The name of the file that contains the nodes where bases are located.
TRAVEL_TIMES_FILE : str
    The name of the file that contains the data with the siren travel times
    between nodes.
RESULTS_FILE : str
    The name of the lp and csv output files.
SOLVER_NAME: str
    The name of the solver that should be used. Examples are "GUROBI_CMD" and
    "PULP_CBC_CMD".
"""

import os
import numpy as np
import pandas as pd
import csv
import pulp

####################################Input######################################
q: float = 0.6  # busy fraction
NUM_AMBULANCES: int = 19  # input
TIME_THRESHOLD: float = 12  # input in minutes

ROOT_DIRECTORY: str = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))
)
DATA_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "data/")
OUTPUT_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "results/")

NODES_FILE: str = "Nodes_Utrecht_2021.csv"
BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
RESULTS_FILE: str = f"MEXCLP_{TIME_THRESHOLD}mins_{NUM_AMBULANCES}ambusUtrecht"

SOLVER_NAME: str = "PULP_CBC_CMD"
###################################LP##########################################
if __name__ == "__main__":
    regionAllDemandNodes = pd.read_csv(f"{DATA_DIRECTORY}{NODES_FILE}")
    AllPCs = np.array(regionAllDemandNodes.loc[:, "postal code"]).astype("int")
    NUM_LOCATIONS = len(AllPCs)

    # bases = range(n_locations) use this if you want every postal code to be a potential base
    regionBasePCs = pd.read_csv(f"{DATA_DIRECTORY}{BASE_LOCATIONS_FILE}")
    BasesPcs = np.array(regionBasePCs.loc[:, "Base Locations"]).astype("int")
    BaseIndices = []
    for i in range(NUM_LOCATIONS):
        if AllPCs[i] in BasesPcs:
            BaseIndices.append(i)
    print("The bases are located at location indices", BaseIndices)

    DrivingTimes = pd.read_csv(
        f"{DATA_DIRECTORY}{TRAVEL_TIMES_FILE}", index_col=0
    )
    DrivingTimes.columns = DrivingTimes.columns.astype(int)
    # you can now access a driving time by e.g. DrivingTimes.loc[1391,3433]
    PCsInDrivingTimeFile = DrivingTimes.columns.values.astype("int")
    # check files are ordering the postal codes in the same way:
    for i in range(NUM_LOCATIONS):
        if AllPCs[i] != PCsInDrivingTimeFile[i]:
            print(PCsInDrivingTimeFile)
            raise Exception(
                "error: data files are not ordering the "
                "postal codes in the same way"
            )

    print(
        "OK: your data files are ordering the postal codes in the same way;"
        "we can proceed"
    )

    inhab = regionAllDemandNodes[
        "inhabitants"
    ]  # inhabitants of the first postal code are a fraction inhab[0] of the total inhabitants of the region.
    if sum(inhab) < 0.9999999:
        print("Warning, sum of inhabitants is not 1 but ", sum(inhab))

    # Creates the 'mip' element to contain the problem data
    mip = pulp.LpProblem("MEXCLP", pulp.LpMaximize)
    x = pulp.LpVariable.dicts(
        "x", (BaseIndices), cat=pulp.LpInteger
    )  # nof ambus at base

    y = pulp.LpVariable.dicts(
        "y",
        (range(NUM_LOCATIONS), range(1, NUM_AMBULANCES + 1)),
        cat=pulp.LpBinary,
    )  # y_ik = 1 if i is within reach of at least k vehicles

    # The objective function is added to the mip first
    mip += (
        pulp.lpSum(
            [
                inhab[i] * (1 - q) * q ** (k - 1) * y[i][k]
                for i in range(NUM_LOCATIONS)
                for k in range(1, NUM_AMBULANCES + 1)
            ]
        ),
        "coverage",
    )

    for i in range(NUM_LOCATIONS):
        mip += pulp.lpSum(
            x[j]
            for j in BaseIndices
            if DrivingTimes.loc[AllPCs[i], AllPCs[j]] <= TIME_THRESHOLD
        ) >= pulp.lpSum(y[i][k] for k in range(1, NUM_AMBULANCES + 1))

    mip += pulp.lpSum(x[j] for j in BaseIndices) <= NUM_AMBULANCES

    for b in BaseIndices:
        mip += x[b] >= 0

    # The problem data is written to an .lp file
    mip.writeLP(f"{OUTPUT_DIRECTORY}{RESULTS_FILE}.lp")
    solver = pulp.getSolver(SOLVER_NAME)
    mip.solve(solver)
    if pulp.LpStatus[mip.status] != "Optimal":
        print(f"Status: {pulp.LpStatus[mip.status]}")
        raise Exception(
            "Error: exiting early because you are "
            "looking at a suboptimal solution!"
        )

    ####################################Output#################################
    for v in mip.variables():
        print(f"{v.name} = {v.varValue}")  # print all to console

    print(
        f"total coverage (objective of this MIP) = {pulp.value(mip.objective)}"
    )

    for i in range(NUM_LOCATIONS):
        cov = sum(
            (1 - q) * q ** (k - 1) * y[i][k].varValue
            for k in range(1, NUM_AMBULANCES + 1)
        )
        print("coverage of demand node ", i, " = ", cov)

    nof_ambus_placed = 0
    for v in mip.variables():
        if v.name.startswith("x"):
            nof_ambus_placed += v.varValue
    print(f"\nambus placed = {nof_ambus_placed}")
    print(f"allowed nr of ambus = {NUM_AMBULANCES}")
    print(f"TIME_THRESHOLD = {TIME_THRESHOLD} minutes\n")

    f = open(f"{OUTPUT_DIRECTORY}{RESULTS_FILE}.csv", "w")
    writer = csv.writer(f)
    writer.writerow(["Postal code", "number of ambulances"])
    for v in mip.variables():
        if v.varValue > 0 and v.name.startswith("x"):
            index = int(v.name[2:])
            print(
                f"The base at postal code {AllPCs[index]} gets "
                f"{int(v.varValue)} ambulances"
            )
            writer.writerow(
                [AllPCs[index], v.varValue]
            )  # only print the ones I'm interested in to file
    f.close()
