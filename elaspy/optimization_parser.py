#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script calculates the utilization and probability that at least one
charger is available at each charging location and then proposes on which
charging location a charger can be removed. For details, see the manuscript.

Parameters
----------
DATA_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the input data is located.
SIM_RESULTS_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the simulation output files are located.
OUTPUT_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the output files should be saved.
SAVE_OUTPUT : bool
    Whether the output should be saved or not.
NUM_RUNS : int
    The number of runs that should be parsed.
SCENARIO : str
    The scenario. Corresponds to the SCENARIO that was used in the simulation
    run.
SIMULATION_AMBULANCE_OUTPUT_FILE_NAME : str
    The name of the file where the ambulance dataframe is saved. Note that the
    run number is automatically added by the script in a for-loop.
CHARGING_SCENARIO_FILE : str
    The name of the file that contains the charging scenario data.
HOSPITAL_FILE : str
    The name of the file that contains the nodes where hospitals are located.
AMBULANCE_BASE_LOCATIONS_FILE : str:
    The name of the file that contains the assignment of ambulances to bases.
OUTPUT_FILE_NAME
    The name of the file where the result dataframe will be saved if
    ``SAVE_OUTPUT=True``.
OUTPUT_FILE_NAME_2
    The name of the file where the location where a charger can be removed is
    saved if ``SAVE_OUTPUT=True``.
RUN_PARAMETERS_FILE_NAME
    The name of the text file with the script parameters if
    ``SAVE_OUTPUT=True``.
"""

import os
import datetime
import numpy as np
import pandas as pd

################################Directories####################################

ROOT_DIRECTORY: str = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))
)
DATA_DIRECTORY: str = os.path.join(
    ROOT_DIRECTORY, "data/"
)
SIM_RESULTS_DIRECTORY: str = os.path.join(
    ROOT_DIRECTORY, "results/"
)
OUTPUT_DIRECTORY: str = os.path.join(
    ROOT_DIRECTORY, "results/"
)
################################Parameters#####################################
SAVE_OUTPUT: bool = False
NUM_RUNS: int = 500
#################################File names####################################
SCENARIO: str = "opt_iteration_1"
SIMULATION_AMBULANCE_OUTPUT_FILE_NAME: str = f"Ambulance_df_{SCENARIO}"
CHARGING_SCENARIO_FILE: str = f"charging_scenario_21_22_{SCENARIO}.csv"
HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
AMBULANCE_BASE_LOCATIONS_FILE: str = (
    "Base_Locations_Ambulances_MEXCLP_21_22_20.csv"
)
OUTPUT_FILE_NAME: str = f"result_df_{SCENARIO}.csv"
OUTPUT_FILE_NAME_2: str = f"remove_location_{SCENARIO}.csv"
RUN_PARAMETERS_FILE_NAME: str = f"optimization_parser_{SCENARIO}"
##############################Save parameters##################################
start_running_time = datetime.datetime.now()
if SAVE_OUTPUT:
    with open(
        f"{OUTPUT_DIRECTORY}{RUN_PARAMETERS_FILE_NAME}.txt",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"DATA_DIRECTORY: {DATA_DIRECTORY}\n")
        f.write(f"SIM_RESULTS_DIRECTORY: {SIM_RESULTS_DIRECTORY}\n")
        f.write(f"OUTPUT_DIRECTORY: {OUTPUT_DIRECTORY}\n")
        f.write(f"SAVE_OUTPUT: {SAVE_OUTPUT}\n")
        f.write(f"NUM_RUNS: {NUM_RUNS}\n")
        f.write(f"SCENARIO: {SCENARIO}\n")
        f.write(
            f"SIMULATION_AMBULANCE_OUTPUT_FILE_NAME: {SIMULATION_AMBULANCE_OUTPUT_FILE_NAME}\n"
        )
        f.write(f"CHARGING_SCENARIO_FILE: {CHARGING_SCENARIO_FILE}\n")
        f.write(f"HOSPITAL_FILE: {HOSPITAL_FILE}\n")
        f.write(
            f"AMBULANCE_BASE_LOCATIONS_FILE: {AMBULANCE_BASE_LOCATIONS_FILE}\n"
        )
        f.write(f"OUTPUT_FILE_NAME: {OUTPUT_FILE_NAME}\n")
        f.write(f"OUTPUT_FILE_NAME_2: {OUTPUT_FILE_NAME_2}\n")
        f.write(f"RUN_PARAMETERS_FILE_NAME: {RUN_PARAMETERS_FILE_NAME}\n")
        f.close()

################################Reading data###################################
chargers_df = pd.read_csv(
    f"{DATA_DIRECTORY}{CHARGING_SCENARIO_FILE}", index_col=0
)
hospital_df = pd.read_csv(f"{DATA_DIRECTORY}{HOSPITAL_FILE}").astype(str) + "H"
base_locations_df = (
    pd.read_csv(f"{DATA_DIRECTORY}{AMBULANCE_BASE_LOCATIONS_FILE}").astype(str)
    + "B"
)
#############################Processing data###################################
hospitals = list(hospital_df["Hospital"])
bases = list(base_locations_df["Base"].unique())

# Only consider hospitals with chargers
charger_hospital_df = chargers_df.loc[hospitals]
filtered_hospitals = list(
    charger_hospital_df.loc[
        charger_hospital_df["Number of regular chargers"] > 0
    ].index
)

locations = filtered_hospitals + bases

result_df = pd.DataFrame(locations, columns=["Location"])
result_df["Utilization"] = np.nan
result_df["Probability"] = np.nan
result_df["Number of regular chargers"] = np.nan

for index, row in result_df.iterrows():
    location = row.Location
    postal_code = int(location[0:4])
    loc_type = location[4]

    number_of_reg_chargers = chargers_df.loc[location][
        "Number of regular chargers"
    ]

    utilizations = []
    probabilities = []

    for i in range(NUM_RUNS):
        ambulance_df = pd.read_csv(
            f"{SIM_RESULTS_DIRECTORY}{SIMULATION_AMBULANCE_OUTPUT_FILE_NAME}_run_{i}.csv",
            index_col=0,
        )

        total_simulation_time = ambulance_df.iloc[-1]["time"]

        if loc_type == "B":
            selected_data = ambulance_df.loc[
                (ambulance_df["charging_location_ID"] == postal_code)
                & (ambulance_df["charging_type"] == 2)
            ]
            total_charge_time = selected_data["charging_time"].sum()
        elif loc_type == "H":
            selected_data = ambulance_df.loc[
                (ambulance_df["charging_location_ID"] == postal_code)
                & (
                    (ambulance_df["charging_type"] == 0)
                    | (ambulance_df["charging_type"] == 1)
                )
            ]
            total_charge_time = selected_data["charging_time"].sum()
        else:
            raise RuntimeError(
                "Incorrect value for the location type provided."
            )

        utilization = total_charge_time / (
            number_of_reg_chargers * total_simulation_time
        )

        probability = 1 - np.power(utilization, number_of_reg_chargers)

        utilizations.append(utilization)
        probabilities.append(probability)

    result_df.at[index, "Utilization"] = np.mean(utilizations)
    result_df.at[index, "Probability"] = np.mean(probabilities)
    result_df.at[index, "Number of regular chargers"] = number_of_reg_chargers

filter_hospitals_df = result_df[result_df["Location"].str.endswith("H")]

# Only consider bases with more than 1 charger.
filter_bases_df = result_df[result_df["Location"].str.endswith("B")]
filter_bases_df = filter_bases_df.loc[
    filter_bases_df["Number of regular chargers"] > 1
]

filtered_results_df = pd.concat((filter_hospitals_df, filter_bases_df))

max_probability_index = filtered_results_df["Probability"].idxmax()
max_probability_row = filtered_results_df.loc[max_probability_index]

print(
    f"The location where a charger should be removed is: {max_probability_row['Location']}"
)

if SAVE_OUTPUT:
    result_df.to_csv(f"{OUTPUT_DIRECTORY}{OUTPUT_FILE_NAME}")
    pd.DataFrame(
        {
            "location_remove_charger": [max_probability_row["Location"]],
        }
    ).to_csv(f"{OUTPUT_DIRECTORY}{OUTPUT_FILE_NAME_2}")

print(
    f"The total running time is: {datetime.datetime.now()-start_running_time}"
)
