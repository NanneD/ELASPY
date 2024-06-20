#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any
from pathlib import Path

import datetime
import numpy as np
import pandas as pd


def print_parameters(SIMULATION_PARAMETERS: dict[str, Any]) -> None:
    """
    Prints the simulation parameters.

    Parameters
    ----------
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters.

    """

    print(f"The script is run at {datetime.datetime.now()})\n")
    print("The used parameters are:")

    for key, value in SIMULATION_PARAMETERS.items():
        print(f"{key} is: {value}")

    print("\n")


def save_input_parameters(SIMULATION_PARAMETERS: dict[str, Any]) -> None:
    """
    Saves the simulation parameters in a text file.

    The text file is saved in directory SIMULATION_OUTPUT_DIRECTORY with name
    RUN_PARAMETERS_FILE_NAME.

    Parameters
    ----------
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``SIMULATION_OUTPUT_DIRECTORY``
        and ``RUN_PARAMETERS_FILE_NAME ``are at least necessary. See
        ``main.py`` for parameter explanations.

    """

    with open(
        f"{SIMULATION_PARAMETERS['SIMULATION_OUTPUT_DIRECTORY']}"
        f"{SIMULATION_PARAMETERS['RUN_PARAMETERS_FILE_NAME']}.txt",
        "w",
        encoding="utf-8",
    ) as f:
        for key, value in SIMULATION_PARAMETERS.items():
            f.write(f"{key}: {value}\n")

        f.close()


def check_input_parameters(SIMULATION_PARAMETERS: dict[str, Any]) -> None:
    """
    Checks the simulation parameters for invalid input parameters.

    Parameters
    ----------
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters.

    Raises
    ------
    KeyError
        If the parameter used in a check is not present in the
        ``SIMULATION_PARAMETERS`` dictionary.

    Exception
        If invalid input parameters are detected.

    """

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["START_SEED_VALUE"] is not None
    ):
        raise Exception(
            "The LOAD_INPUT_DATA option is True, but "
            "START_SEED_VALUE is not None. Please make "
            "it None."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["START_SEED_VALUE"] is None
    ):
        raise Exception(
            "The LOAD_INPUT_DATA option is False, but "
            "START_SEED_VALUE is None. Please make "
            "it not None."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["START_SEED_VALUE"] < 0
    ):
        raise Exception(
            "The value of START_SEED_VALUE should be equal to "
            "or larger than 0 but is "
            f'{SIMULATION_PARAMETERS["START_SEED_VALUE"]}.'
        )

    if not Path(SIMULATION_PARAMETERS["DATA_DIRECTORY"]).exists():
        raise Exception(
            "The directory "
            f'{SIMULATION_PARAMETERS["DATA_DIRECTORY"]}'
            " does not exist. "
            "Please specify a different DATA_DIRECTORY."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["SIMULATION_INPUT_DIRECTORY"] is None
    ):
        raise Exception(
            "The LOAD_INPUT_DATA option is True, but "
            "SIMULATION_INPUT_DIRECTORY is None. Please specify "
            "a directory."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and not Path(
            SIMULATION_PARAMETERS["SIMULATION_INPUT_DIRECTORY"]
        ).exists()
    ):
        raise Exception(
            "The directory "
            f'{SIMULATION_PARAMETERS["SIMULATION_INPUT_DIRECTORY"]}'
            " does not exist. Please specify a different"
            " SIMULATION_INPUT_DIRECTORY."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["SIMULATION_INPUT_DIRECTORY"] is not None
    ):
        raise Exception(
            "The LOAD_INPUT_DATA option is False, but "
            "SIMULATION_INPUT_DIRECTORY is not None. Please make "
            "it None."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["INTERARRIVAL_TIMES_FILE"] is not None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is False, but "
            "INTERARRIVAL_TIMES_FILE is not None. Please make "
            "it None."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["ON_SITE_AID_TIMES_FILE"] is not None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is False, but "
            "ON_SITE_AID_TIMES_FILE is not None. Please make "
            "it None."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["DROP_OFF_TIMES_FILE"] is not None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is False, but "
            "DROP_OFF_TIMES_FILE is not None. Please make "
            "it None."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["LOCATION_IDS_FILE"] is not None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is False, but "
            "LOCATION_IDS_FILE is not None. Please make "
            "it None."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["TO_HOSPITAL_FILE"] is not None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is False, but "
            "TO_HOSPITAL_FILE is not None. Please make "
            "it None."
        )

    if not Path(SIMULATION_PARAMETERS["SIMULATION_OUTPUT_DIRECTORY"]).exists():
        raise Exception(
            "The directory "
            f'{SIMULATION_PARAMETERS["SIMULATION_OUTPUT_DIRECTORY"]}'
            " does not exist. Please specify a different"
            " SIMULATION_OUTPUT_DIRECTORY."
        )

    if not Path(
        SIMULATION_PARAMETERS["DATA_DIRECTORY"]
        + SIMULATION_PARAMETERS["TRAVEL_TIMES_FILE"]
    ).exists():
        raise Exception(
            "The TRAVEL_TIMES_FILE "
            f'({SIMULATION_PARAMETERS["TRAVEL_TIMES_FILE"]})'
            " points to a non-existing file."
        )

    if not Path(
        SIMULATION_PARAMETERS["DATA_DIRECTORY"]
        + SIMULATION_PARAMETERS["DISTANCE_FILE"]
    ).exists():
        raise Exception(
            "The DISTANCE_FILE "
            f'({SIMULATION_PARAMETERS["DISTANCE_FILE"]})'
            " points to a non-existing file."
        )

    if not Path(
        SIMULATION_PARAMETERS["DATA_DIRECTORY"]
        + SIMULATION_PARAMETERS["NODES_FILE"]
    ).exists():
        raise Exception(
            "The NODES_FILE "
            f'({SIMULATION_PARAMETERS["NODES_FILE"]})'
            " points to a non-existing file."
        )

    if not Path(
        SIMULATION_PARAMETERS["DATA_DIRECTORY"]
        + SIMULATION_PARAMETERS["HOSPITAL_FILE"]
    ).exists():
        raise Exception(
            "The HOSPITAL_FILE "
            f'({SIMULATION_PARAMETERS["HOSPITAL_FILE"]})'
            " points to a non-existing file."
        )

    if not Path(
        SIMULATION_PARAMETERS["DATA_DIRECTORY"]
        + SIMULATION_PARAMETERS["BASE_LOCATIONS_FILE"]
    ).exists():
        raise Exception(
            "The BASE_LOCATIONS_FILE "
            f'({SIMULATION_PARAMETERS["BASE_LOCATIONS_FILE"]})'
            " points to a non-existing file."
        )

    if not Path(
        SIMULATION_PARAMETERS["DATA_DIRECTORY"]
        + SIMULATION_PARAMETERS["AMBULANCE_BASE_LOCATIONS_FILE"]
    ).exists():
        raise Exception(
            "The AMBULANCE_BASE_LOCATIONS_FILE "
            f'({SIMULATION_PARAMETERS["AMBULANCE_BASE_LOCATIONS_FILE"]})'
            " points to a non-existing file."
        )

    if not Path(
        SIMULATION_PARAMETERS["DATA_DIRECTORY"]
        + SIMULATION_PARAMETERS["CHARGING_SCENARIO_FILE"]
    ).exists():
        raise Exception(
            "The CHARGING_SCENARIO_FILE "
            f'({SIMULATION_PARAMETERS["CHARGING_SCENARIO_FILE"]})'
            " points to a non-existing file."
        )

    postal_codes = pd.read_csv(
        f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
        f"{SIMULATION_PARAMETERS['NODES_FILE']}",
        index_col=0,
    ).index.values

    if not np.all(
        np.isin(
            pd.read_csv(
                f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
                f"{SIMULATION_PARAMETERS['HOSPITAL_FILE']}"
            ),
            postal_codes,
        )
    ):
        raise Exception("Not all hospitals are present in the postal codes.")

    if not np.all(
        np.isin(
            pd.read_csv(
                f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
                f"{SIMULATION_PARAMETERS['AMBULANCE_BASE_LOCATIONS_FILE']}",
                index_col=0,
            ),
            postal_codes,
        )
    ):
        raise Exception(
            "Not all assigned ambulance bases are present "
            "in the postal codes."
        )

    if not np.all(
        np.isin(
            pd.read_csv(
                f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
                f"{SIMULATION_PARAMETERS['BASE_LOCATIONS_FILE']}"
            ),
            postal_codes,
        )
    ):
        raise Exception(
            "Not all ambulance bases are present in the postal codes."
        )

    if not np.all(
        np.isin(
            postal_codes,
            pd.read_csv(
                f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
                f"{SIMULATION_PARAMETERS['DISTANCE_FILE']}",
                index_col=0,
            ).index,
        )
    ):
        raise Exception(
            "Not all postal codes are present in the distance matrix."
        )

    if not np.all(
        np.isin(
            postal_codes,
            pd.read_csv(
                f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
                f"{SIMULATION_PARAMETERS['TRAVEL_TIMES_FILE']}",
                index_col=0,
            ).index,
        )
    ):
        raise Exception(
            "Not all postal codes are present in the travel times matrix."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["INTERARRIVAL_TIMES_FILE"] is None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is true, but INTERARRIVAL_TIMES_FILE "
            "is None. Please make it not None."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["ON_SITE_AID_TIMES_FILE"] is None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is true, but ON_SITE_AID_TIMES_FILE "
            "is None. Please make it not None."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["DROP_OFF_TIMES_FILE"] is None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is true, but DROP_OFF_TIMES_FILE "
            "is None. Please make it not None."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["LOCATION_IDS_FILE"] is None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is true, but LOCATION_IDS_FILE "
            "is None. Please make it not None."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["TO_HOSPITAL_FILE"] is None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is true, but TO_HOSPITAL_FILE "
            "is None. Please make it not None."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and not Path(
            SIMULATION_PARAMETERS["SIMULATION_INPUT_DIRECTORY"]
            + SIMULATION_PARAMETERS["INTERARRIVAL_TIMES_FILE"]
        ).exists()
    ):
        raise Exception(
            "LOAD_INPUT_DATA is true, but INTERARRIVAL_TIMES_FILE "
            f"({SIMULATION_PARAMETERS['INTERARRIVAL_TIMES_FILE']})"
            " points to a non-existing file."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and not Path(
            SIMULATION_PARAMETERS["SIMULATION_INPUT_DIRECTORY"]
            + SIMULATION_PARAMETERS["ON_SITE_AID_TIMES_FILE"]
        ).exists()
    ):
        raise Exception(
            "LOAD_INPUT_DATA is true, but ON_SITE_AID_TIMES_FILE "
            f"({SIMULATION_PARAMETERS['ON_SITE_AID_TIMES_FILE']}) "
            "points to a non-existing file."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and not Path(
            SIMULATION_PARAMETERS["SIMULATION_INPUT_DIRECTORY"]
            + SIMULATION_PARAMETERS["DROP_OFF_TIMES_FILE"]
        ).exists()
    ):
        raise Exception(
            "LOAD_INPUT_DATA is true, but DROP_OFF_TIMES_FILE "
            f"({SIMULATION_PARAMETERS['DROP_OFF_TIMES_FILE']}) "
            "points to a non-existing file."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and not Path(
            SIMULATION_PARAMETERS["SIMULATION_INPUT_DIRECTORY"]
            + SIMULATION_PARAMETERS["LOCATION_IDS_FILE"]
        ).exists()
    ):
        raise Exception(
            "LOAD_INPUT_DATA is true, but LOCATION_IDS_FILE "
            f"({SIMULATION_PARAMETERS['LOCATION_IDS_FILE']}) "
            "points to a non-existing file."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and not Path(
            SIMULATION_PARAMETERS["SIMULATION_INPUT_DIRECTORY"]
            + SIMULATION_PARAMETERS["TO_HOSPITAL_FILE"]
        ).exists()
    ):
        raise Exception(
            "LOAD_INPUT_DATA is true, but TO_HOSPITAL_FILE "
            f"({SIMULATION_PARAMETERS['TO_HOSPITAL_FILE']}) "
            "points to a non-existing file."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["NUM_RUNS"] != 1
    ):
        raise Exception(
            "LOAD_INPUT_DATA is true and the value of NUM_RUNS "
            "should be equal to 1, but it is "
            f"{SIMULATION_PARAMETERS['NUM_RUNS']}."
        )

    if SIMULATION_PARAMETERS["SCENARIO"] not in [
        "RB1",
        "RB2",
        "FB1",
        "RB1_FB1",
        "RB1_RH1",
        "RB1_FH1",
        "FB1_RH1",
        "FB1_FH1",
        "RB50_RH50",
        "Diesel",
    ]:
        raise Exception(
            "A non-existing SCENARIO "
            f"({SIMULATION_PARAMETERS['SCENARIO']}) is selected. "
            "Please change it or add it to the allowed list."
        )

    if (
        SIMULATION_PARAMETERS["SCENARIO"] == "Diesel"
        and SIMULATION_PARAMETERS["ENGINE_TYPE"] != "diesel"
    ):
        raise Exception(
            "SCENARIO is 'Diesel', but ENGINE_TYPE is not 'diesel'."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "diesel"
        and SIMULATION_PARAMETERS["SCENARIO"] != "Diesel"
    ):
        raise Exception(
            "ENGINE_TYPE is 'diesel', but SCENARIO is not 'Diesel'."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric"
        and SIMULATION_PARAMETERS["SCENARIO"] == "Diesel"
    ):
        raise Exception("ENGINE_TYPE is 'electric', but SCENARIO is 'Diesel'.")

    if (
        SIMULATION_PARAMETERS["SCENARIO"] != "Diesel"
        and SIMULATION_PARAMETERS["ENGINE_TYPE"] != "electric"
    ):
        raise Exception(
            "SCENARIO is not 'Diesel', but ENGINE_TYPE is not 'electric'."
        )

    if SIMULATION_PARAMETERS["NUM_RUNS"] <= 0:
        raise Exception(
            "The value of NUM_RUNS should be larger than "
            f'0 but is {SIMULATION_PARAMETERS["NUM_RUNS"]}.'
        )

    if SIMULATION_PARAMETERS["NUM_AMBULANCES"] <= 0:
        raise Exception(
            "The value of NUM_AMBULANCES should be larger than "
            f'0 but is {SIMULATION_PARAMETERS["NUM_AMBULANCES"]}.'
        )

    if (
        pd.read_csv(
            f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
            f"{SIMULATION_PARAMETERS['AMBULANCE_BASE_LOCATIONS_FILE']}",
            index_col=0,
        ).shape[0]
        != SIMULATION_PARAMETERS["NUM_AMBULANCES"]
    ):
        raise Exception(
            "The number of assigned ambulances by "
            "AMBULANCE_BASE_LOCATIONS_FILE does not correspond "
            "to NUM_AMMBULANCES."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["PROB_GO_TO_HOSPITAL"] is not None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is True, but PROB_GO_TO_HOSPITAL "
            "is not None. Please make it None."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["PROB_GO_TO_HOSPITAL"] is None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is False, but PROB_GO_TO_HOSPITAL "
            "is None. Please make it not None."
        )

    if not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"] and not (
        SIMULATION_PARAMETERS["PROB_GO_TO_HOSPITAL"] >= 0
        and SIMULATION_PARAMETERS["PROB_GO_TO_HOSPITAL"] <= 1
    ):
        raise Exception(
            "The value of PROB_GO_TO_HOSPITAL should be between "
            "0 and 1, but it is "
            f"{SIMULATION_PARAMETERS['PROB_GO_TO_HOSPITAL']}."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["CALL_LAMBDA"] is not None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is True, but CALL_LAMBDA "
            "is not None. Please make it None."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["CALL_LAMBDA"] is None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is False, but CALL_LAMBDA "
            "is None. Please make it not None."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["CALL_LAMBDA"] <= 0
    ):
        raise Exception(
            "The value of CALL_LAMBDA should be larger than "
            f'0 but is {SIMULATION_PARAMETERS["CALL_LAMBDA"]}.'
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and len(SIMULATION_PARAMETERS["AID_PARAMETERS"]) != 1
    ):
        raise Exception(
            "LOAD_INPUT_DATA is True, but AID_PARAMETERS does not have "
            "length 1. Please (only) provide the cut-off value."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["DROP_OFF_PARAMETERS"] is not None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is True, but DROP_OFF_PARAMETERS is not None. "
            "Please make it None."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["DROP_OFF_PARAMETERS"] is None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is False, but DROP_OFF_PARAMETERS is None. "
            "Please make it not None."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and len(SIMULATION_PARAMETERS["AID_PARAMETERS"]) != 4
    ):
        raise Exception(
            "The length of the AID_PARAMETERS is not equal to 4, "
            "but is "
            f"{len(SIMULATION_PARAMETERS['AID_PARAMETERS'])}."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and len(SIMULATION_PARAMETERS["DROP_OFF_PARAMETERS"]) != 4
    ):
        raise Exception(
            "The length of the DROP_OFF_PARAMETERS is not "
            "equal to 4, but is "
            f"{len(SIMULATION_PARAMETERS['DROP_OFF_PARAMETERS'])}."
        )

    if SIMULATION_PARAMETERS["AID_PARAMETERS"][-1] <= 0:
        raise Exception(
            "The CUT_OFF value of AID_PARAMETERS should be larger "
            "than 0, but is "
            f"{SIMULATION_PARAMETERS['AID_PARAMETERS'][-1]}. "
            "Please change the final value of AID_PARAMETERS."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["DROP_OFF_PARAMETERS"][-1] <= 0
    ):
        raise Exception(
            "The CUT_OFF value of DROP_OFF_PARAMETERS should "
            "be larger than 0, but is "
            f"{SIMULATION_PARAMETERS['DROP_OFF_PARAMETERS'][-1]}."
            " Please change the final value of "
            "DROP_OFF_PARAMETERS."
        )

    if not (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "diesel"
        or SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric"
    ):
        raise Exception(
            "The value of ENGINE_TYPE should be 'diesel' or "
            "'electric', but it is "
            f"{SIMULATION_PARAMETERS['ENGINE_TYPE']}."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric"
        and SIMULATION_PARAMETERS["IDLE_USAGE"] is None
    ):
        raise Exception(
            'The ENGINE_TYPE is "electric", but IDLE_USAGE is '
            "None. Please make it not None."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric"
        and SIMULATION_PARAMETERS["DRIVING_USAGE"] is None
    ):
        raise Exception(
            'The ENGINE_TYPE is "electric", but DRIVING_USAGE is '
            "None. Please make it not None."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric"
        and SIMULATION_PARAMETERS["IDLE_USAGE"] < 0
    ):
        raise Exception(
            "The value of IDLE_USAGE should be equal to "
            "or larger than 0 but is "
            f'{SIMULATION_PARAMETERS["IDLE_USAGE"]}.'
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric"
        and SIMULATION_PARAMETERS["DRIVING_USAGE"] < 0
    ):
        raise Exception(
            "The value of DRIVING_USAGE should be equal "
            "to or larger than "
            f'0 but is {SIMULATION_PARAMETERS["DRIVING_USAGE"]}.'
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric"
        and SIMULATION_PARAMETERS["BATTERY_CAPACITY"] <= 0
    ):
        raise Exception(
            "The value of BATTERY_CAPACITY should be larger than"
            " 0 but is "
            f'{SIMULATION_PARAMETERS["BATTERY_CAPACITY"]}.'
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "diesel"
        and SIMULATION_PARAMETERS["DRIVING_USAGE"] is not None
    ):
        raise Exception(
            'The ENGINE_TYPE is "diesel", but DRIVING_USAGE is '
            "not None. Please make it None."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "diesel"
        and SIMULATION_PARAMETERS["IDLE_USAGE"] is not None
    ):
        raise Exception(
            'The ENGINE_TYPE is "diesel", but IDLE_USAGE is '
            "not None. Please make it None."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "diesel"
        and SIMULATION_PARAMETERS["BATTERY_CAPACITY"] != np.inf
    ):
        raise Exception(
            "The ENGINE_TYPE is 'diesel' and the BATTERY_CAPACITY"
            " should be np.inf, but is"
            f" {SIMULATION_PARAMETERS['BATTERY_CAPACITY']}."
        )

    if (
        SIMULATION_PARAMETERS["NO_SIREN_PENALTY"] <= 0
        or SIMULATION_PARAMETERS["NO_SIREN_PENALTY"] > 1.0
    ):
        raise Exception(
            "The value of NO_SIREN_PENALTY should be "
            "larger than 0 and smaller or equal to 1, but it is "
            f"{SIMULATION_PARAMETERS['NO_SIREN_PENALTY']}."
        )

    if (
        not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["CRN_GENERATOR"] is None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is False, but CRN_GENERATOR "
            "is None. Please make it not None."
        )

    if not SIMULATION_PARAMETERS["LOAD_INPUT_DATA"] and not (
        SIMULATION_PARAMETERS["CRN_GENERATOR"] == "Generator"
        or SIMULATION_PARAMETERS["CRN_GENERATOR"] == "RandomState"
    ):
        raise Exception(
            "The value of CRN_GENERATOR should be 'Generator' or "
            "'RandomState', but it is "
            f"{SIMULATION_PARAMETERS['CRN_GENERATOR']}."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["CRN_GENERATOR"] is not None
    ):
        raise Exception(
            "LOAD_INPUT_DATA is True, but CRN_GENERATOR "
            "is not None. Please make it None."
        )

    if (
        SIMULATION_PARAMETERS["SAVE_PLOTS"]
        and not SIMULATION_PARAMETERS["PLOT_FIGURES"]
    ):
        raise Exception(
            "The SAVE_PLOTS parameter is True, but the "
            "PLOT_FIGURES parameter is False. "
            "This is not possible. Please change this."
        )

    if not (
        SIMULATION_PARAMETERS["PROCESS_TYPE"] == "Time"
        or SIMULATION_PARAMETERS["PROCESS_TYPE"] == "Number"
    ):
        raise Exception(
            "The PROCESS_TYPE should be 'Time' or 'Number', but it is not."
        )

    if (
        SIMULATION_PARAMETERS["PROCESS_TYPE"] == "Time"
        and SIMULATION_PARAMETERS["PROCESS_NUM_CALLS"] is not None
    ):
        raise Exception(
            "The PROCESS_TYPE is 'Time', but the "
            "PROCESS_NUM_CALLS is not None. Please make it None."
        )

    if (
        SIMULATION_PARAMETERS["PROCESS_TYPE"] == "Time"
        and SIMULATION_PARAMETERS["PROCESS_TIME"] is None
    ):
        raise Exception(
            "The PROCESS_TYPE is 'Time', but the "
            "PROCESS_TIME is None. Please give it a value."
        )

    if (
        SIMULATION_PARAMETERS["PROCESS_TYPE"] == "Number"
        and SIMULATION_PARAMETERS["PROCESS_NUM_CALLS"] is None
    ):
        raise Exception(
            "The PROCESS_TYPE is 'Number', but the "
            "PROCESS_NUM_CALLS is None. Please give it a value."
        )

    if (
        SIMULATION_PARAMETERS["PROCESS_TYPE"] == "Number"
        and SIMULATION_PARAMETERS["PROCESS_TIME"] is not None
    ):
        raise Exception(
            "The PROCESS_TYPE is 'Number', but the "
            "PROCESS_TIME is not None. Please make it None."
        )

    if (
        SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]
        and SIMULATION_PARAMETERS["PROCESS_TYPE"] == "Time"
    ):
        raise Exception(
            "LOAD_INPUT_DATA is True, but then PROCESS_TYPE"
            " cannot be 'Time'. Change it to 'Number'."
        )

    if (
        SIMULATION_PARAMETERS["PROCESS_TYPE"] == "Number"
        and SIMULATION_PARAMETERS["PROCESS_NUM_CALLS"] <= 0
    ):
        raise Exception(
            "The value of PROCESS_NUM_CALLS should be "
            "larger than 0 but is "
            f'{SIMULATION_PARAMETERS["PROCESS_NUM_CALLS"]}.'
        )

    if (
        SIMULATION_PARAMETERS["PROCESS_TYPE"] == "Time"
        and SIMULATION_PARAMETERS["PROCESS_TIME"] <= 0
    ):
        raise Exception(
            "The value of PROCESS_TIME should be larger than "
            f'0 but is {SIMULATION_PARAMETERS["PROCESS_TIME"]}.'
        )

    if Path(
        SIMULATION_PARAMETERS["SIMULATION_OUTPUT_DIRECTORY"]
        + SIMULATION_PARAMETERS["SIMULATION_PATIENT_OUTPUT_FILE_NAME"]
        + "_run_0.csv"
    ).exists():
        raise Exception(
            "The SIMULATION_PATIENT_OUTPUT_FILE_NAME already "
            "exists and will be overwritten if SAVE_DFS is True."
        )

    if Path(
        SIMULATION_PARAMETERS["SIMULATION_OUTPUT_DIRECTORY"]
        + SIMULATION_PARAMETERS["SIMULATION_AMBULANCE_OUTPUT_FILE_NAME"]
        + "_run_0.csv"
    ).exists():
        raise Exception(
            "The SIMULATION_AMBULANCE_OUTPUT_FILE_NAME already "
            "exists and will be overwritten if SAVE_DFS is True."
        )

    if Path(
        SIMULATION_PARAMETERS["SIMULATION_OUTPUT_DIRECTORY"]
        + SIMULATION_PARAMETERS["RUN_PARAMETERS_FILE_NAME"]
        + ".txt"
    ).exists():
        raise Exception(
            "The RUN_PARAMETERS_FILE_NAME already exists and "
            "will be overwritten if SAVE_OUTPUT is True."
        )

    if Path(
        SIMULATION_PARAMETERS["SIMULATION_OUTPUT_DIRECTORY"]
        + SIMULATION_PARAMETERS["RUNNING_TIME_FILE_NAME"]
        + ".csv"
    ).exists():
        raise Exception(
            "The RUNNING_TIME_FILE_NAME already exists and "
            "will be overwritten if SAVE_OUTPUT is True."
        )

    if Path(
        SIMULATION_PARAMETERS["SIMULATION_OUTPUT_DIRECTORY"]
        + SIMULATION_PARAMETERS["SIMULATION_PRINTS_FILE_NAME"]
        + ".txt"
    ).exists():
        raise Exception(
            "The SIMULATION_PRINTS_FILE_NAME already exists and "
            "will be overwritten if SAVE_PRINTS_TXT is True."
        )

    if Path(
        SIMULATION_PARAMETERS["SIMULATION_OUTPUT_DIRECTORY"]
        + SIMULATION_PARAMETERS["MEAN_RESPONSE_TIMES_FILE_NAME"]
        + ".csv"
    ).exists():
        raise Exception(
            "The MEAN_RESPONSE_TIMES_FILE_NAME already exists and "
            "will be overwritten if SAVE_OUTPUT is True."
        )

    if Path(
        SIMULATION_PARAMETERS["SIMULATION_OUTPUT_DIRECTORY"]
        + SIMULATION_PARAMETERS["EMP_QUANTILE_RESPONSE_TIMES_FILE_NAME"]
        + ".csv"
    ).exists():
        raise Exception(
            "The EMP_QUANTILE_RESPONSE_TIMES_FILE_NAME already "
            "exists and will be overwritten if SAVE_OUTPUT is True"
        )

    if Path(
        SIMULATION_PARAMETERS["SIMULATION_OUTPUT_DIRECTORY"]
        + SIMULATION_PARAMETERS["BUSY_FRACTIONS_FILE_NAME"]
        + ".csv"
    ).exists():
        raise Exception(
            "The BUSY_FRACTIONS_FILE_NAME already exists and "
            "will be overwritten if SAVE_OUTPUT is True."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "diesel"
        and SIMULATION_PARAMETERS["INTERVAL_CHECK_WP"] is not None
    ):
        raise Exception(
            "The ENGINE_TYPE is 'diesel', but the "
            "INTERVAL_CHECK_WP is not None. Please make it None."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric"
        and SIMULATION_PARAMETERS["INTERVAL_CHECK_WP"] is None
    ):
        raise Exception(
            "The ENGINE_TYPE is 'electric', but the "
            "INTERVAL_CHECK_WP is None. Please make it not None."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric"
        and SIMULATION_PARAMETERS["INTERVAL_CHECK_WP"] <= 0
    ):
        raise Exception(
            "INTERVAL_CHECK_WP should be larger than 0, "
            f"but is {SIMULATION_PARAMETERS['INTERVAL_CHECK_WP']}."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric"
        and SIMULATION_PARAMETERS["INTERVAL_CHECK_WP"] >= 20
    ):
        raise Exception(
            "It is most realistic if INTERVAL_CHECK_WP is small, "
            "but it has value "
            f"{SIMULATION_PARAMETERS['INTERVAL_CHECK_WP']}. "
            "Please make it smaller or change this input check if "
            "you are really sure."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "diesel"
        and SIMULATION_PARAMETERS["TIME_AFTER_LAST_ARRIVAL"] is not None
    ):
        raise Exception(
            "The ENGINE_TYPE is 'diesel', but the "
            "TIME_AFTER_LAST_ARRIVAL is not None. "
            "Please make it None."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric"
        and SIMULATION_PARAMETERS["TIME_AFTER_LAST_ARRIVAL"] is None
    ):
        raise Exception(
            "The ENGINE_TYPE is 'electric', but the "
            "TIME_AFTER_LAST_ARRIVAL is None. "
            "Please make it not None."
        )

    if (
        SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric"
        and SIMULATION_PARAMETERS["TIME_AFTER_LAST_ARRIVAL"] < 0
    ):
        raise Exception(
            "TIME_AFTER_LAST_ARRIVAL should be larger or equal to "
            "0, but has it has value "
            f"{SIMULATION_PARAMETERS['TIME_AFTER_LAST_ARRIVAL']}."
        )

    if SIMULATION_PARAMETERS["AT_BOUNDARY"] < 0:
        raise Exception(
            "AT_BOUNDARY should be larger or equal to 0, but is "
            f"{SIMULATION_PARAMETERS['AT_BOUNDARY']}."
        )

    if SIMULATION_PARAMETERS["FT_BOUNDARY"] < 0:
        raise Exception(
            "FT_BOUNDARY should be larger or equal to 0, but is "
            f"{SIMULATION_PARAMETERS['FT_BOUNDARY']}."
        )

    if (
        SIMULATION_PARAMETERS["FT_BOUNDARY"]
        <= SIMULATION_PARAMETERS["AT_BOUNDARY"]
    ):
        raise Exception(
            "FT_BOUNDARY is smaller or equal to AT_BOUNDARY. This "
            "is not possible. Please make FT_BOUNDARY larger than "
            "AT_BOUNDARY."
        )

    if len(SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"]) != 16:
        raise Exception(
            "The number of entries of DATA_COLUMNS_PATIENT is "
            "not equal to 16. Determine whether the correct "
            "entries are provided."
        )

    if len(SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"]) != 19:
        raise Exception(
            "The number of entries of DATA_COLUMNS_AMBULANCE is "
            "not equal to 19. Determine whether the correct "
            "entries are provided."
        )


def save_simulation_output(
    directory: str, file_name_output: str, output_dataframe, run_nr: int
) -> None:
    """
    Saves an output dataframe as a csv file.

    Parameters
    ----------
    directory : str
        The output directory where the csv file will be saved.
    file_name_output : str
        The name of the csv file.
    output_dataframe : pandas.DataFrame
        The output dataframe that will be saved.
    run_nr : int
        The simulation run number.

    """

    output_dataframe.to_csv(f"{directory}{file_name_output}_run_{run_nr}.csv")


def calculate_response_time_ecdf(df_patient):
    """
    Calculates the empirical cumulative distribution of the response time.

    Parameters
    ----------
    df_patient : pandas.DataFrame
        A dataframe with the patient data where each row represents a patient.
        At least a column "response_time" is necessary. See the output data
        section on the ELASPY website for explanations.

    Returns
    -------
    df_patient : pandas.DataFrame
        A dataframe with the patient data. It now also contains the column
        "ecdf_rt", which is the empirical cumulative distribution of the
        response time.

    """

    df_patient["ecdf_rt"] = [
        df_patient[df_patient["response_time"] <= t].shape[0]
        / float(df_patient["response_time"].size)
        for t in df_patient["response_time"]
    ]

    return df_patient


def calculate_busy_fraction(
    df_patient, SIMULATION_PARAMETERS: dict[str, Any]
) -> float:
    """
    Calculates the busy fraction of a simulation run.

    A warm-up period of AT_BOUNDARY and cool-down period of FT_BOUNDARY
    is used, which means that the calculation does not consider data before
    the warm-up period and after the cool-down period.

    Parameters
    ----------
    df_patient : pandas.DataFrame
        A dataframe with the patient data where each row represents a patient.
        At least columns "arrival_time", "waiting_time_before_assigned" and
        "finish_time" are necessary. See the output data section on the ELASPY
        website for explanations.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``AT_BOUNDARY``,
        ``FT_BOUNDARY`` and ``NUM_AMBULANCES`` are at least necessary.
        See ``main.py`` for parameter explanations.

    Raises
    ------
    Exception
        If the busy fraction calculation uses the same data more than once.

    Returns
    -------
    float
        The busy fraction.

    """

    # Note that the assignment time is used as then the ambu becomes active.
    df_patient["assignment_time"] = (
        df_patient["arrival_time"] + df_patient["waiting_time_before_assigned"]
    )

    busy_time = 0

    # Case 1: patient is processed by ambulance completely within the interval
    # (AT_BOUNDARY, FT_BOUNDARY).
    case_1 = (
        df_patient["assignment_time"] >= SIMULATION_PARAMETERS["AT_BOUNDARY"]
    ) & (df_patient["finish_time"] <= SIMULATION_PARAMETERS["FT_BOUNDARY"])

    busy_time += np.sum(
        (
            df_patient.loc[case_1]["finish_time"]
            - df_patient.loc[case_1]["assignment_time"]
        )
    )

    # Case 2: the assignment time is before AT_BOUNDARY, the finish time before
    # FT_BOUNDARY but after AT_BOUNDARY.
    case_2 = (
        df_patient["assignment_time"] < SIMULATION_PARAMETERS["AT_BOUNDARY"]
    ) & (
        (df_patient["finish_time"] > SIMULATION_PARAMETERS["AT_BOUNDARY"])
        & (df_patient["finish_time"] <= SIMULATION_PARAMETERS["FT_BOUNDARY"])
    )

    busy_time += np.sum(
        df_patient.loc[case_2]["finish_time"]
        - SIMULATION_PARAMETERS["AT_BOUNDARY"]
    )

    # Case 3: the assignment time is before AT_BOUNDARY, the finish time after
    # FT_BOUNDARY.
    case_3 = (
        df_patient["assignment_time"] < SIMULATION_PARAMETERS["AT_BOUNDARY"]
    ) & (df_patient["finish_time"] > SIMULATION_PARAMETERS["FT_BOUNDARY"])

    busy_time += np.sum(case_3) * (
        SIMULATION_PARAMETERS["FT_BOUNDARY"]
        - SIMULATION_PARAMETERS["AT_BOUNDARY"]
    )

    # Case:4 the assignment time is after AT_BOUNDARY but before FT_BOUNDARY,
    # the finish time after FT_BOUNDARY.
    case_4 = (
        (df_patient["assignment_time"] >= SIMULATION_PARAMETERS["AT_BOUNDARY"])
        & (
            df_patient["assignment_time"]
            < SIMULATION_PARAMETERS["FT_BOUNDARY"]
        )
    ) & (df_patient["finish_time"] > SIMULATION_PARAMETERS["FT_BOUNDARY"])

    busy_time += np.sum(
        SIMULATION_PARAMETERS["FT_BOUNDARY"]
        - df_patient.loc[case_4]["assignment_time"]
    )

    total_time = (
        SIMULATION_PARAMETERS["FT_BOUNDARY"]
        - SIMULATION_PARAMETERS["AT_BOUNDARY"]
    ) * SIMULATION_PARAMETERS["NUM_AMBULANCES"]

    df_patient.drop(["assignment_time"], axis=1, inplace=True)

    if not np.isin(
        np.sum([case_1, case_2, case_3, case_4], axis=0), [0, 1]
    ).all():
        raise Exception(
            "Error: in the busy_fraction calculation, some data "
            "is considered more than once."
        )

    return busy_time / total_time


def simulation_statistics(
    df_patient,
    df_ambulance,
    start_time_simulation: datetime.datetime,
    end_time_simulation: datetime.datetime,
    nr_times_no_fast_no_regular_available: int,
    SIMULATION_PARAMETERS: dict[str, Any],
) -> None:
    """
    Prints some simulation statistics.

    Parameters
    ----------
    df_patient : pandas.DataFrame
        A dataframe with the patient data where each row represents a patient.
        At least columns "response_time", "waiting_time_before_assigned" and
        "ecdf_rt" are necessary. See the output data section on the ELASPY
        website for explanations.
    df_ambulance : Pandas.DataFrame
        A dataframe with the ambulance data where each row represents an
        ambulance event. At least columns "charging_type", "charging_success",
        "charging_interrupted", "charging_time" and "waiting_time" are
        necessary. See the output data section on the ELASPY website for
        explanations.
    start_time_simulation : datetime.datetime
        The start time of the simulation run.
    end_time_simulation : datetime.datetime
        The end time of the simulation run.
    nr_times_no_fast_no_regular_available : int
        The number of times no fast and no regular chargers were available when
        an ambulance wanted to charge during the simulation run.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameter ``ENGINE_TYPE`` is at least
        necessary. See ``main.py`` for parameter explanations.

    """

    # Patient output

    print(
        f"The average response time is: {np.mean(df_patient['response_time'])}."
    )
    print(
        "The 95% empirical quantile of the response time is: "
        f"{np.min(df_patient.loc[df_patient['ecdf_rt'] >= 0.95]['response_time'])}."
    )
    print(
        "The average waiting time before a patient is assigned to an ambulance"
        f" is: {np.mean(df_patient['waiting_time_before_assigned'])}."
    )

    if SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric":
        # Ambulance output
        for key, value in dict(
            df_ambulance["charging_type"].value_counts()
        ).items():
            print(
                f"The charging type {key} had {value} occurrences in "
                "df_ambulance."
            )

        print(
            "In total, "
            f"{len(df_ambulance[df_ambulance['charging_success']==1])} "
            "charging sessions were successful, "
            f"{len(df_ambulance[df_ambulance['charging_success']==0])} "
            "charging sessions were not succesful."
        )

        print(
            "In total, "
            f"{len(df_ambulance[df_ambulance['charging_interrupted']==1])} "
            "charging sessions were interrupted, "
            f"{len(df_ambulance[df_ambulance['charging_interrupted']==0])} "
            "charging sessions were not interrupted."
        )

        print(
            "The average charging time is: "
            f"{round(np.nanmean(df_ambulance['charging_time']),5)}."
        )

        print(
            "The average waiting time before a charger is assigned is: "
            f"{round(np.nanmean(df_ambulance['waiting_time']),5)}."
        )

        print(
            "The value of nr_times_no_fast_no_regular_available is: "
            f"{nr_times_no_fast_no_regular_available}."
        )

    print(
        "The simulation run running time was: "
        f"{end_time_simulation-start_time_simulation}."
    )
