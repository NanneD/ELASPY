#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 13:37:16 2023

@author: nanne
"""

import os
import numpy as np
import pandas as pd

from ambulance import Ambulance
from ambulance_simulation import run_simulation
from input_output_functions import calculate_response_time_ecdf


def test_calculate_charging_time():
    """
    Suppose a car requires A kWh until it has a full battery and that the
    charging speed is B kW. The required time (in minutes) to charge until
    full is equal to A/B*60 (minutes).
    """

    assert 123 / 11 * 60 == Ambulance.calculate_charging_time(123, 11)
    assert 150 / 50 * 60 == Ambulance.calculate_charging_time(150, 50)


def test_calculate_battery_reduction_idling():
    """
    Suppose a car uses A kWh per hour, and you use it for B minutes,
    then it will use B/60*A kWh of energy.
    """

    assert 5.21 / 60 * 5 == Ambulance.calculate_battery_reduction_idling(
        5.21, {"IDLE_USAGE": 5.0, "PRINT": False}
    )
    assert 123.65 / 60 * 7.21 == Ambulance.calculate_battery_reduction_idling(
        123.65, {"IDLE_USAGE": 7.21, "PRINT": False}
    )


def test_run_simulation_electric_4():

    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/")
    SIMULATION_INPUT_DIRECTORY = os.path.join(
        ROOT_DIRECTORY, "data/unit_tests/"
    )
    SIMULATED_DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/unit_tests/")

    TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
    DISTANCE_FILE: str = "distance_matrix_2022.csv"
    NODES_FILE: str = "nodes_Utrecht_2021.csv"
    HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
    BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
    AMBULANCE_BASE_LOCATIONS_FILE: str = (
        "Base_Locations_Ambulances_MEXCLP_21_22_24.csv"
    )
    CHARGING_SCENARIO_FILE: str = "charging_scenario_21_22_RB50_FH50.csv"

    INTERARRIVAL_TIMES_FILE = (
        "interarrival_times_test_run_simulation_electric_4.csv"
    )
    ON_SITE_AID_TIMES_FILE = (
        "on_site_aid_times_test_run_simulation_electric_4.csv"
    )
    DROP_OFF_TIMES_FILE = "drop_off_times_test_run_simulation_electric_4.csv"
    LOCATION_IDS_FILE = "location_IDs_test_run_simulation_electric_4.csv"
    TO_HOSPITAL_FILE = "to_hospital_bool_test_run_simulation_electric_4.csv"

    PROCESS_NUM_CALLS = 2500
    NUM_AMBULANCES = 24
    AID_PARAMETERS = [88]  # Cut-off value
    ENGINE_TYPE = "electric"
    IDLE_USAGE = 5  # kW
    DRIVING_USAGE = 0.4  # kWh/km
    if ENGINE_TYPE == "electric":
        BATTERY_CAPACITY = 150.0
    else:
        BATTERY_CAPACITY = np.inf
    NO_SIREN_PENALTY = 0.95
    LOAD_INPUT_DATA = True
    INTERVAL_CHECK_WP = 1
    TIME_AFTER_LAST_ARRIVAL = 100

    PRINT = False
    DATA_COLUMNS_PATIENT = [
        "patient_ID",
        "response_time",
        "arrival_time",
        "location_ID",
        "nr_ambulances_available",
        "nr_ambulances_not_assignable",
        "assigned_to_ambulance_nr",
        "waiting_time_before_assigned",
        "driving_time_to_patient",
        "ambulance_arrival_time",
        "on_site_aid_time",
        "to_hospital",
        "hospital_ID",
        "driving_time_to_hospital",
        "drop_off_time_hospital",
        "finish_time",
    ]
    DATA_COLUMNS_AMBULANCE = [
        "ambulance_ID",
        "time",
        "battery_level_before",
        "battery_level_after",
        "use_or_charge",
        "idle_or_driving_decrease",
        "idle_time",
        "source_location_ID",
        "target_location_ID",
        "driven_km",
        "battery_decrease",
        "charging_type",
        "charging_location_ID",
        "speed_charger",
        "charging_success",
        "waiting_time",
        "charging_interrupted",
        "charging_time",
        "battery_increase",
    ]

    SIMULATION_PARAMETERS = {
        "PROCESS_NUM_CALLS": PROCESS_NUM_CALLS,
        "NUM_AMBULANCES": NUM_AMBULANCES,
        "AID_PARAMETERS": AID_PARAMETERS,
        "ENGINE_TYPE": ENGINE_TYPE,
        "IDLE_USAGE": IDLE_USAGE,
        "DRIVING_USAGE": DRIVING_USAGE,
        "BATTERY_CAPACITY": BATTERY_CAPACITY,
        "NO_SIREN_PENALTY": NO_SIREN_PENALTY,
        "PRINT": PRINT,
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
        "TRAVEL_TIMES_FILE": TRAVEL_TIMES_FILE,
        "DISTANCE_FILE": DISTANCE_FILE,
        "NODES_FILE": NODES_FILE,
        "HOSPITAL_FILE": HOSPITAL_FILE,
        "BASE_LOCATIONS_FILE": BASE_LOCATIONS_FILE,
        "AMBULANCE_BASE_LOCATIONS_FILE": AMBULANCE_BASE_LOCATIONS_FILE,
        "CHARGING_SCENARIO_FILE": CHARGING_SCENARIO_FILE,
        "DATA_DIRECTORY": DATA_DIRECTORY,
        "LOAD_INPUT_DATA": LOAD_INPUT_DATA,
        "SIMULATION_INPUT_DIRECTORY": SIMULATION_INPUT_DIRECTORY,
        "INTERARRIVAL_TIMES_FILE": INTERARRIVAL_TIMES_FILE,
        "ON_SITE_AID_TIMES_FILE": ON_SITE_AID_TIMES_FILE,
        "DROP_OFF_TIMES_FILE": DROP_OFF_TIMES_FILE,
        "LOCATION_IDS_FILE": LOCATION_IDS_FILE,
        "TO_HOSPITAL_FILE": TO_HOSPITAL_FILE,
        "INTERVAL_CHECK_WP": INTERVAL_CHECK_WP,
        "TIME_AFTER_LAST_ARRIVAL": TIME_AFTER_LAST_ARRIVAL,
    }
    SIMULATION_DATA = {
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
    }

    # Run simulation and cast output to dataframe.
    run_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)
    df_patient = pd.DataFrame(
        SIMULATION_DATA["output_patient"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"],
    )
    df_patient = calculate_response_time_ecdf(df_patient)
    df_ambulance = pd.DataFrame(
        SIMULATION_DATA["output_ambulance"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"],
    )

    # Get saved dataframes
    df_test_patient = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Patient_Test_Electric_4.csv",
        index_col=0,
        float_precision="round_trip",
    )
    df_test_ambulance = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Ambulance_Test_Electric_4.csv",
        index_col=0,
        float_precision="round_trip",
    )

    pd.testing.assert_frame_equal(
        df_patient, df_test_patient, rtol=1e-20, atol=1e-20
    )
    pd.testing.assert_frame_equal(
        df_ambulance, df_test_ambulance, rtol=1e-20, atol=1e-20
    )


def test_run_simulation_electric_5():

    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/")
    SIMULATION_INPUT_DIRECTORY = os.path.join(
        ROOT_DIRECTORY, "data/unit_tests/"
    )
    SIMULATED_DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/unit_tests/")

    TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
    DISTANCE_FILE: str = "distance_matrix_2022.csv"
    NODES_FILE: str = "nodes_Utrecht_2021.csv"
    HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
    BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
    AMBULANCE_BASE_LOCATIONS_FILE: str = (
        "Base_Locations_Ambulances_MEXCLP_21_22_24.csv"
    )
    CHARGING_SCENARIO_FILE: str = "charging_scenario_21_22_RB50_RH50.csv"

    INTERARRIVAL_TIMES_FILE = (
        "interarrival_times_test_run_simulation_electric_5.csv"
    )
    ON_SITE_AID_TIMES_FILE = (
        "on_site_aid_times_test_run_simulation_electric_5.csv"
    )
    DROP_OFF_TIMES_FILE = "drop_off_times_test_run_simulation_electric_5.csv"
    LOCATION_IDS_FILE = "location_IDs_test_run_simulation_electric_5.csv"
    TO_HOSPITAL_FILE = "to_hospital_bool_test_run_simulation_electric_5.csv"

    PROCESS_NUM_CALLS = 800
    NUM_AMBULANCES = 24
    AID_PARAMETERS = [88]  # Cut-off value
    ENGINE_TYPE = "electric"
    IDLE_USAGE = 5  # kW
    DRIVING_USAGE = 0.4  # kWh/km
    if ENGINE_TYPE == "electric":
        BATTERY_CAPACITY = 150.0
    else:
        BATTERY_CAPACITY = np.inf
    NO_SIREN_PENALTY = 0.95
    LOAD_INPUT_DATA = True
    INTERVAL_CHECK_WP = 1
    TIME_AFTER_LAST_ARRIVAL = 100

    PRINT = False
    DATA_COLUMNS_PATIENT = [
        "patient_ID",
        "response_time",
        "arrival_time",
        "location_ID",
        "nr_ambulances_available",
        "nr_ambulances_not_assignable",
        "assigned_to_ambulance_nr",
        "waiting_time_before_assigned",
        "driving_time_to_patient",
        "ambulance_arrival_time",
        "on_site_aid_time",
        "to_hospital",
        "hospital_ID",
        "driving_time_to_hospital",
        "drop_off_time_hospital",
        "finish_time",
    ]
    DATA_COLUMNS_AMBULANCE = [
        "ambulance_ID",
        "time",
        "battery_level_before",
        "battery_level_after",
        "use_or_charge",
        "idle_or_driving_decrease",
        "idle_time",
        "source_location_ID",
        "target_location_ID",
        "driven_km",
        "battery_decrease",
        "charging_type",
        "charging_location_ID",
        "speed_charger",
        "charging_success",
        "waiting_time",
        "charging_interrupted",
        "charging_time",
        "battery_increase",
    ]

    SIMULATION_PARAMETERS = {
        "PROCESS_NUM_CALLS": PROCESS_NUM_CALLS,
        "NUM_AMBULANCES": NUM_AMBULANCES,
        "AID_PARAMETERS": AID_PARAMETERS,
        "ENGINE_TYPE": ENGINE_TYPE,
        "IDLE_USAGE": IDLE_USAGE,
        "DRIVING_USAGE": DRIVING_USAGE,
        "BATTERY_CAPACITY": BATTERY_CAPACITY,
        "NO_SIREN_PENALTY": NO_SIREN_PENALTY,
        "PRINT": PRINT,
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
        "TRAVEL_TIMES_FILE": TRAVEL_TIMES_FILE,
        "DISTANCE_FILE": DISTANCE_FILE,
        "NODES_FILE": NODES_FILE,
        "HOSPITAL_FILE": HOSPITAL_FILE,
        "BASE_LOCATIONS_FILE": BASE_LOCATIONS_FILE,
        "AMBULANCE_BASE_LOCATIONS_FILE": AMBULANCE_BASE_LOCATIONS_FILE,
        "CHARGING_SCENARIO_FILE": CHARGING_SCENARIO_FILE,
        "DATA_DIRECTORY": DATA_DIRECTORY,
        "LOAD_INPUT_DATA": LOAD_INPUT_DATA,
        "SIMULATION_INPUT_DIRECTORY": SIMULATION_INPUT_DIRECTORY,
        "INTERARRIVAL_TIMES_FILE": INTERARRIVAL_TIMES_FILE,
        "ON_SITE_AID_TIMES_FILE": ON_SITE_AID_TIMES_FILE,
        "DROP_OFF_TIMES_FILE": DROP_OFF_TIMES_FILE,
        "LOCATION_IDS_FILE": LOCATION_IDS_FILE,
        "TO_HOSPITAL_FILE": TO_HOSPITAL_FILE,
        "INTERVAL_CHECK_WP": INTERVAL_CHECK_WP,
        "TIME_AFTER_LAST_ARRIVAL": TIME_AFTER_LAST_ARRIVAL,
    }
    SIMULATION_DATA = {
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
    }

    # Run simulation and cast output to dataframe.
    run_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)
    df_patient = pd.DataFrame(
        SIMULATION_DATA["output_patient"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"],
    )
    df_patient = calculate_response_time_ecdf(df_patient)
    df_ambulance = pd.DataFrame(
        SIMULATION_DATA["output_ambulance"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"],
    )

    # Get saved dataframes
    df_test_patient = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Patient_Test_Electric_5.csv",
        index_col=0,
        float_precision="round_trip",
    )
    df_test_ambulance = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Ambulance_Test_Electric_5.csv",
        index_col=0,
        float_precision="round_trip",
    )

    pd.testing.assert_frame_equal(
        df_patient, df_test_patient, rtol=1e-20, atol=1e-20
    )
    pd.testing.assert_frame_equal(
        df_ambulance, df_test_ambulance, rtol=1e-20, atol=1e-20
    )


def test_run_simulation_electric_6():

    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/")
    SIMULATION_INPUT_DIRECTORY = os.path.join(
        ROOT_DIRECTORY, "data/unit_tests/"
    )
    SIMULATED_DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/unit_tests/")

    TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
    DISTANCE_FILE: str = "distance_matrix_2022.csv"
    NODES_FILE: str = "nodes_Utrecht_2021.csv"
    HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
    BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
    AMBULANCE_BASE_LOCATIONS_FILE: str = (
        "Base_Locations_Ambulances_MEXCLP_21_22_24.csv"
    )
    CHARGING_SCENARIO_FILE: str = "charging_scenario_21_22_RB1_RH1.csv"

    INTERARRIVAL_TIMES_FILE = (
        "interarrival_times_test_run_simulation_electric_6.csv"
    )
    ON_SITE_AID_TIMES_FILE = (
        "on_site_aid_times_test_run_simulation_electric_6.csv"
    )
    DROP_OFF_TIMES_FILE = "drop_off_times_test_run_simulation_electric_6.csv"
    LOCATION_IDS_FILE = "location_IDs_test_run_simulation_electric_6.csv"
    TO_HOSPITAL_FILE = "to_hospital_bool_test_run_simulation_electric_6.csv"

    PROCESS_NUM_CALLS = 950
    NUM_AMBULANCES = 24
    AID_PARAMETERS = [88]  # Cut-off value
    ENGINE_TYPE = "electric"
    IDLE_USAGE = 5  # kW
    DRIVING_USAGE = 0.4  # kWh/km
    if ENGINE_TYPE == "electric":
        BATTERY_CAPACITY = 150.0
    else:
        BATTERY_CAPACITY = np.inf
    NO_SIREN_PENALTY = 0.95
    LOAD_INPUT_DATA = True
    INTERVAL_CHECK_WP = 1
    TIME_AFTER_LAST_ARRIVAL = 100

    PRINT = False
    DATA_COLUMNS_PATIENT = [
        "patient_ID",
        "response_time",
        "arrival_time",
        "location_ID",
        "nr_ambulances_available",
        "nr_ambulances_not_assignable",
        "assigned_to_ambulance_nr",
        "waiting_time_before_assigned",
        "driving_time_to_patient",
        "ambulance_arrival_time",
        "on_site_aid_time",
        "to_hospital",
        "hospital_ID",
        "driving_time_to_hospital",
        "drop_off_time_hospital",
        "finish_time",
    ]
    DATA_COLUMNS_AMBULANCE = [
        "ambulance_ID",
        "time",
        "battery_level_before",
        "battery_level_after",
        "use_or_charge",
        "idle_or_driving_decrease",
        "idle_time",
        "source_location_ID",
        "target_location_ID",
        "driven_km",
        "battery_decrease",
        "charging_type",
        "charging_location_ID",
        "speed_charger",
        "charging_success",
        "waiting_time",
        "charging_interrupted",
        "charging_time",
        "battery_increase",
    ]

    SIMULATION_PARAMETERS = {
        "PROCESS_NUM_CALLS": PROCESS_NUM_CALLS,
        "NUM_AMBULANCES": NUM_AMBULANCES,
        "AID_PARAMETERS": AID_PARAMETERS,
        "ENGINE_TYPE": ENGINE_TYPE,
        "IDLE_USAGE": IDLE_USAGE,
        "DRIVING_USAGE": DRIVING_USAGE,
        "BATTERY_CAPACITY": BATTERY_CAPACITY,
        "NO_SIREN_PENALTY": NO_SIREN_PENALTY,
        "PRINT": PRINT,
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
        "TRAVEL_TIMES_FILE": TRAVEL_TIMES_FILE,
        "DISTANCE_FILE": DISTANCE_FILE,
        "NODES_FILE": NODES_FILE,
        "HOSPITAL_FILE": HOSPITAL_FILE,
        "BASE_LOCATIONS_FILE": BASE_LOCATIONS_FILE,
        "AMBULANCE_BASE_LOCATIONS_FILE": AMBULANCE_BASE_LOCATIONS_FILE,
        "CHARGING_SCENARIO_FILE": CHARGING_SCENARIO_FILE,
        "DATA_DIRECTORY": DATA_DIRECTORY,
        "LOAD_INPUT_DATA": LOAD_INPUT_DATA,
        "SIMULATION_INPUT_DIRECTORY": SIMULATION_INPUT_DIRECTORY,
        "INTERARRIVAL_TIMES_FILE": INTERARRIVAL_TIMES_FILE,
        "ON_SITE_AID_TIMES_FILE": ON_SITE_AID_TIMES_FILE,
        "DROP_OFF_TIMES_FILE": DROP_OFF_TIMES_FILE,
        "LOCATION_IDS_FILE": LOCATION_IDS_FILE,
        "TO_HOSPITAL_FILE": TO_HOSPITAL_FILE,
        "INTERVAL_CHECK_WP": INTERVAL_CHECK_WP,
        "TIME_AFTER_LAST_ARRIVAL": TIME_AFTER_LAST_ARRIVAL,
    }
    SIMULATION_DATA = {
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
    }

    # Run simulation and cast output to dataframe.
    run_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)
    df_patient = pd.DataFrame(
        SIMULATION_DATA["output_patient"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"],
    )
    df_patient = calculate_response_time_ecdf(df_patient)
    df_ambulance = pd.DataFrame(
        SIMULATION_DATA["output_ambulance"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"],
    )

    # Get saved dataframes
    df_test_patient = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Patient_Test_Electric_6.csv",
        index_col=0,
        float_precision="round_trip",
    )
    df_test_ambulance = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Ambulance_Test_Electric_6.csv",
        index_col=0,
        float_precision="round_trip",
    )

    pd.testing.assert_frame_equal(
        df_patient, df_test_patient, rtol=1e-20, atol=1e-20
    )
    pd.testing.assert_frame_equal(
        df_ambulance, df_test_ambulance, rtol=1e-20, atol=1e-20
    )


def test_run_simulation_electric_7():

    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/")
    SIMULATION_INPUT_DIRECTORY = os.path.join(
        ROOT_DIRECTORY, "data/unit_tests/"
    )
    SIMULATED_DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/unit_tests/")

    TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
    DISTANCE_FILE: str = "distance_matrix_2022.csv"
    NODES_FILE: str = "nodes_Utrecht_2021.csv"
    HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
    BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
    AMBULANCE_BASE_LOCATIONS_FILE: str = (
        "Base_Locations_Ambulances_MEXCLP_21_22_24.csv"
    )
    CHARGING_SCENARIO_FILE: str = "charging_scenario_21_22_RB1_RH1.csv"

    INTERARRIVAL_TIMES_FILE = (
        "interarrival_times_test_run_simulation_electric_7.csv"
    )
    ON_SITE_AID_TIMES_FILE = (
        "on_site_aid_times_test_run_simulation_electric_7.csv"
    )
    DROP_OFF_TIMES_FILE = "drop_off_times_test_run_simulation_electric_7.csv"
    LOCATION_IDS_FILE = "location_IDs_test_run_simulation_electric_7.csv"
    TO_HOSPITAL_FILE = "to_hospital_bool_test_run_simulation_electric_7.csv"

    PROCESS_NUM_CALLS = 750
    NUM_AMBULANCES = 24
    AID_PARAMETERS = [88]  # Cut-off value
    ENGINE_TYPE = "electric"
    IDLE_USAGE = 5  # kW
    DRIVING_USAGE = 0.4  # kWh/km
    if ENGINE_TYPE == "electric":
        BATTERY_CAPACITY = 150.0
    else:
        BATTERY_CAPACITY = np.inf
    NO_SIREN_PENALTY = 0.95
    LOAD_INPUT_DATA = True
    INTERVAL_CHECK_WP = 1
    TIME_AFTER_LAST_ARRIVAL = 100

    PRINT = False
    DATA_COLUMNS_PATIENT = [
        "patient_ID",
        "response_time",
        "arrival_time",
        "location_ID",
        "nr_ambulances_available",
        "nr_ambulances_not_assignable",
        "assigned_to_ambulance_nr",
        "waiting_time_before_assigned",
        "driving_time_to_patient",
        "ambulance_arrival_time",
        "on_site_aid_time",
        "to_hospital",
        "hospital_ID",
        "driving_time_to_hospital",
        "drop_off_time_hospital",
        "finish_time",
    ]
    DATA_COLUMNS_AMBULANCE = [
        "ambulance_ID",
        "time",
        "battery_level_before",
        "battery_level_after",
        "use_or_charge",
        "idle_or_driving_decrease",
        "idle_time",
        "source_location_ID",
        "target_location_ID",
        "driven_km",
        "battery_decrease",
        "charging_type",
        "charging_location_ID",
        "speed_charger",
        "charging_success",
        "waiting_time",
        "charging_interrupted",
        "charging_time",
        "battery_increase",
    ]

    SIMULATION_PARAMETERS = {
        "PROCESS_NUM_CALLS": PROCESS_NUM_CALLS,
        "NUM_AMBULANCES": NUM_AMBULANCES,
        "AID_PARAMETERS": AID_PARAMETERS,
        "ENGINE_TYPE": ENGINE_TYPE,
        "IDLE_USAGE": IDLE_USAGE,
        "DRIVING_USAGE": DRIVING_USAGE,
        "BATTERY_CAPACITY": BATTERY_CAPACITY,
        "NO_SIREN_PENALTY": NO_SIREN_PENALTY,
        "PRINT": PRINT,
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
        "TRAVEL_TIMES_FILE": TRAVEL_TIMES_FILE,
        "DISTANCE_FILE": DISTANCE_FILE,
        "NODES_FILE": NODES_FILE,
        "HOSPITAL_FILE": HOSPITAL_FILE,
        "BASE_LOCATIONS_FILE": BASE_LOCATIONS_FILE,
        "AMBULANCE_BASE_LOCATIONS_FILE": AMBULANCE_BASE_LOCATIONS_FILE,
        "CHARGING_SCENARIO_FILE": CHARGING_SCENARIO_FILE,
        "DATA_DIRECTORY": DATA_DIRECTORY,
        "LOAD_INPUT_DATA": LOAD_INPUT_DATA,
        "SIMULATION_INPUT_DIRECTORY": SIMULATION_INPUT_DIRECTORY,
        "INTERARRIVAL_TIMES_FILE": INTERARRIVAL_TIMES_FILE,
        "ON_SITE_AID_TIMES_FILE": ON_SITE_AID_TIMES_FILE,
        "DROP_OFF_TIMES_FILE": DROP_OFF_TIMES_FILE,
        "LOCATION_IDS_FILE": LOCATION_IDS_FILE,
        "TO_HOSPITAL_FILE": TO_HOSPITAL_FILE,
        "INTERVAL_CHECK_WP": INTERVAL_CHECK_WP,
        "TIME_AFTER_LAST_ARRIVAL": TIME_AFTER_LAST_ARRIVAL,
    }
    SIMULATION_DATA = {
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
    }

    # Run simulation and cast output to dataframe.
    run_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)
    df_patient = pd.DataFrame(
        SIMULATION_DATA["output_patient"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"],
    )
    df_patient = calculate_response_time_ecdf(df_patient)
    df_ambulance = pd.DataFrame(
        SIMULATION_DATA["output_ambulance"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"],
    )

    # Get saved dataframes
    df_test_patient = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Patient_Test_Electric_7.csv",
        index_col=0,
        float_precision="round_trip",
    )
    df_test_ambulance = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Ambulance_Test_Electric_7.csv",
        index_col=0,
        float_precision="round_trip",
    )

    pd.testing.assert_frame_equal(
        df_patient, df_test_patient, rtol=1e-20, atol=1e-20
    )
    pd.testing.assert_frame_equal(
        df_ambulance, df_test_ambulance, rtol=1e-20, atol=1e-20
    )


def test_run_simulation_electric_8():

    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/")
    SIMULATION_INPUT_DIRECTORY = os.path.join(
        ROOT_DIRECTORY, "data/unit_tests/"
    )
    SIMULATED_DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/unit_tests/")

    TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
    DISTANCE_FILE: str = "distance_matrix_2022.csv"
    NODES_FILE: str = "nodes_Utrecht_2021.csv"
    HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
    BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
    AMBULANCE_BASE_LOCATIONS_FILE: str = (
        "Base_Locations_Ambulances_MEXCLP_21_22_23.csv"
    )
    CHARGING_SCENARIO_FILE: str = "charging_scenario_21_22_RB1_RH1.csv"

    INTERARRIVAL_TIMES_FILE = (
        "interarrival_times_test_run_simulation_electric_8.csv"
    )
    ON_SITE_AID_TIMES_FILE = (
        "on_site_aid_times_test_run_simulation_electric_8.csv"
    )
    DROP_OFF_TIMES_FILE = "drop_off_times_test_run_simulation_electric_8.csv"
    LOCATION_IDS_FILE = "location_IDs_test_run_simulation_electric_8.csv"
    TO_HOSPITAL_FILE = "to_hospital_bool_test_run_simulation_electric_8.csv"

    PROCESS_NUM_CALLS = 900
    NUM_AMBULANCES = 23
    AID_PARAMETERS = [88]  # Cut-off value
    ENGINE_TYPE = "electric"
    IDLE_USAGE = 5  # kW
    DRIVING_USAGE = 0.4  # kWh/km
    if ENGINE_TYPE == "electric":
        BATTERY_CAPACITY = 150.0
    else:
        BATTERY_CAPACITY = np.inf
    NO_SIREN_PENALTY = 0.95
    LOAD_INPUT_DATA = True
    INTERVAL_CHECK_WP = 1
    TIME_AFTER_LAST_ARRIVAL = 100

    PRINT = False
    DATA_COLUMNS_PATIENT = [
        "patient_ID",
        "response_time",
        "arrival_time",
        "location_ID",
        "nr_ambulances_available",
        "nr_ambulances_not_assignable",
        "assigned_to_ambulance_nr",
        "waiting_time_before_assigned",
        "driving_time_to_patient",
        "ambulance_arrival_time",
        "on_site_aid_time",
        "to_hospital",
        "hospital_ID",
        "driving_time_to_hospital",
        "drop_off_time_hospital",
        "finish_time",
    ]
    DATA_COLUMNS_AMBULANCE = [
        "ambulance_ID",
        "time",
        "battery_level_before",
        "battery_level_after",
        "use_or_charge",
        "idle_or_driving_decrease",
        "idle_time",
        "source_location_ID",
        "target_location_ID",
        "driven_km",
        "battery_decrease",
        "charging_type",
        "charging_location_ID",
        "speed_charger",
        "charging_success",
        "waiting_time",
        "charging_interrupted",
        "charging_time",
        "battery_increase",
    ]

    SIMULATION_PARAMETERS = {
        "PROCESS_NUM_CALLS": PROCESS_NUM_CALLS,
        "NUM_AMBULANCES": NUM_AMBULANCES,
        "AID_PARAMETERS": AID_PARAMETERS,
        "ENGINE_TYPE": ENGINE_TYPE,
        "IDLE_USAGE": IDLE_USAGE,
        "DRIVING_USAGE": DRIVING_USAGE,
        "BATTERY_CAPACITY": BATTERY_CAPACITY,
        "NO_SIREN_PENALTY": NO_SIREN_PENALTY,
        "PRINT": PRINT,
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
        "TRAVEL_TIMES_FILE": TRAVEL_TIMES_FILE,
        "DISTANCE_FILE": DISTANCE_FILE,
        "NODES_FILE": NODES_FILE,
        "HOSPITAL_FILE": HOSPITAL_FILE,
        "BASE_LOCATIONS_FILE": BASE_LOCATIONS_FILE,
        "AMBULANCE_BASE_LOCATIONS_FILE": AMBULANCE_BASE_LOCATIONS_FILE,
        "CHARGING_SCENARIO_FILE": CHARGING_SCENARIO_FILE,
        "DATA_DIRECTORY": DATA_DIRECTORY,
        "LOAD_INPUT_DATA": LOAD_INPUT_DATA,
        "SIMULATION_INPUT_DIRECTORY": SIMULATION_INPUT_DIRECTORY,
        "INTERARRIVAL_TIMES_FILE": INTERARRIVAL_TIMES_FILE,
        "ON_SITE_AID_TIMES_FILE": ON_SITE_AID_TIMES_FILE,
        "DROP_OFF_TIMES_FILE": DROP_OFF_TIMES_FILE,
        "LOCATION_IDS_FILE": LOCATION_IDS_FILE,
        "TO_HOSPITAL_FILE": TO_HOSPITAL_FILE,
        "INTERVAL_CHECK_WP": INTERVAL_CHECK_WP,
        "TIME_AFTER_LAST_ARRIVAL": TIME_AFTER_LAST_ARRIVAL,
    }
    SIMULATION_DATA = {
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
    }

    # Run simulation and cast output to dataframe.
    run_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)
    df_patient = pd.DataFrame(
        SIMULATION_DATA["output_patient"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"],
    )
    df_patient = calculate_response_time_ecdf(df_patient)
    df_ambulance = pd.DataFrame(
        SIMULATION_DATA["output_ambulance"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"],
    )

    # Get saved dataframes
    df_test_patient = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Patient_Test_Electric_8.csv",
        index_col=0,
        float_precision="round_trip",
    )
    df_test_ambulance = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Ambulance_Test_Electric_8.csv",
        index_col=0,
        float_precision="round_trip",
    )

    pd.testing.assert_frame_equal(
        df_patient, df_test_patient, rtol=1e-20, atol=1e-20
    )
    pd.testing.assert_frame_equal(
        df_ambulance, df_test_ambulance, rtol=1e-20, atol=1e-20
    )


def test_run_simulation_electric_9():

    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/")
    SIMULATION_INPUT_DIRECTORY = os.path.join(
        ROOT_DIRECTORY, "data/unit_tests/"
    )
    SIMULATED_DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/unit_tests/")

    TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
    DISTANCE_FILE: str = "distance_matrix_2022.csv"
    NODES_FILE: str = "nodes_Utrecht_2021.csv"
    HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
    BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
    AMBULANCE_BASE_LOCATIONS_FILE: str = (
        "Base_Locations_Ambulances_MEXCLP_21_22_23.csv"
    )
    CHARGING_SCENARIO_FILE: str = "charging_scenario_21_22_RB50_FH50.csv"

    INTERARRIVAL_TIMES_FILE = (
        "interarrival_times_test_run_simulation_electric_9.csv"
    )
    ON_SITE_AID_TIMES_FILE = (
        "on_site_aid_times_test_run_simulation_electric_9.csv"
    )
    DROP_OFF_TIMES_FILE = "drop_off_times_test_run_simulation_electric_9.csv"
    LOCATION_IDS_FILE = "location_IDs_test_run_simulation_electric_9.csv"
    TO_HOSPITAL_FILE = "to_hospital_bool_test_run_simulation_electric_9.csv"

    PROCESS_NUM_CALLS = 1500
    NUM_AMBULANCES = 23
    AID_PARAMETERS = [88]  # Cut-off value
    ENGINE_TYPE = "electric"
    IDLE_USAGE = 5  # kW
    DRIVING_USAGE = 0.4  # kWh/km
    if ENGINE_TYPE == "electric":
        BATTERY_CAPACITY = 150.0
    else:
        BATTERY_CAPACITY = np.inf
    NO_SIREN_PENALTY = 0.95
    LOAD_INPUT_DATA = True
    INTERVAL_CHECK_WP = 1
    TIME_AFTER_LAST_ARRIVAL = 100

    PRINT = False
    DATA_COLUMNS_PATIENT = [
        "patient_ID",
        "response_time",
        "arrival_time",
        "location_ID",
        "nr_ambulances_available",
        "nr_ambulances_not_assignable",
        "assigned_to_ambulance_nr",
        "waiting_time_before_assigned",
        "driving_time_to_patient",
        "ambulance_arrival_time",
        "on_site_aid_time",
        "to_hospital",
        "hospital_ID",
        "driving_time_to_hospital",
        "drop_off_time_hospital",
        "finish_time",
    ]
    DATA_COLUMNS_AMBULANCE = [
        "ambulance_ID",
        "time",
        "battery_level_before",
        "battery_level_after",
        "use_or_charge",
        "idle_or_driving_decrease",
        "idle_time",
        "source_location_ID",
        "target_location_ID",
        "driven_km",
        "battery_decrease",
        "charging_type",
        "charging_location_ID",
        "speed_charger",
        "charging_success",
        "waiting_time",
        "charging_interrupted",
        "charging_time",
        "battery_increase",
    ]

    SIMULATION_PARAMETERS = {
        "PROCESS_NUM_CALLS": PROCESS_NUM_CALLS,
        "NUM_AMBULANCES": NUM_AMBULANCES,
        "AID_PARAMETERS": AID_PARAMETERS,
        "ENGINE_TYPE": ENGINE_TYPE,
        "IDLE_USAGE": IDLE_USAGE,
        "DRIVING_USAGE": DRIVING_USAGE,
        "BATTERY_CAPACITY": BATTERY_CAPACITY,
        "NO_SIREN_PENALTY": NO_SIREN_PENALTY,
        "PRINT": PRINT,
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
        "TRAVEL_TIMES_FILE": TRAVEL_TIMES_FILE,
        "DISTANCE_FILE": DISTANCE_FILE,
        "NODES_FILE": NODES_FILE,
        "HOSPITAL_FILE": HOSPITAL_FILE,
        "BASE_LOCATIONS_FILE": BASE_LOCATIONS_FILE,
        "AMBULANCE_BASE_LOCATIONS_FILE": AMBULANCE_BASE_LOCATIONS_FILE,
        "CHARGING_SCENARIO_FILE": CHARGING_SCENARIO_FILE,
        "DATA_DIRECTORY": DATA_DIRECTORY,
        "LOAD_INPUT_DATA": LOAD_INPUT_DATA,
        "SIMULATION_INPUT_DIRECTORY": SIMULATION_INPUT_DIRECTORY,
        "INTERARRIVAL_TIMES_FILE": INTERARRIVAL_TIMES_FILE,
        "ON_SITE_AID_TIMES_FILE": ON_SITE_AID_TIMES_FILE,
        "DROP_OFF_TIMES_FILE": DROP_OFF_TIMES_FILE,
        "LOCATION_IDS_FILE": LOCATION_IDS_FILE,
        "TO_HOSPITAL_FILE": TO_HOSPITAL_FILE,
        "INTERVAL_CHECK_WP": INTERVAL_CHECK_WP,
        "TIME_AFTER_LAST_ARRIVAL": TIME_AFTER_LAST_ARRIVAL,
    }
    SIMULATION_DATA = {
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
    }

    # Run simulation and cast output to dataframe.
    run_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)
    df_patient = pd.DataFrame(
        SIMULATION_DATA["output_patient"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"],
    )
    df_patient = calculate_response_time_ecdf(df_patient)
    df_ambulance = pd.DataFrame(
        SIMULATION_DATA["output_ambulance"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"],
    )

    # Get saved dataframes
    df_test_patient = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Patient_Test_Electric_9.csv",
        index_col=0,
        float_precision="round_trip",
    )
    df_test_ambulance = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Ambulance_Test_Electric_9.csv",
        index_col=0,
        float_precision="round_trip",
    )

    pd.testing.assert_frame_equal(
        df_patient, df_test_patient, rtol=1e-20, atol=1e-20
    )
    pd.testing.assert_frame_equal(
        df_ambulance, df_test_ambulance, rtol=1e-20, atol=1e-20
    )


def test_run_simulation_electric_10():

    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/")
    SIMULATION_INPUT_DIRECTORY = os.path.join(
        ROOT_DIRECTORY, "data/unit_tests/"
    )
    SIMULATED_DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/unit_tests/")

    TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
    DISTANCE_FILE: str = "distance_matrix_2022.csv"
    NODES_FILE: str = "nodes_Utrecht_2021.csv"
    HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
    BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
    AMBULANCE_BASE_LOCATIONS_FILE: str = (
        "Base_Locations_Ambulances_MEXCLP_21_22_20.csv"
    )
    CHARGING_SCENARIO_FILE: str = "charging_scenario_21_22_RB1.csv"

    INTERARRIVAL_TIMES_FILE = (
        "interarrival_times_test_run_simulation_electric_10.csv"
    )
    ON_SITE_AID_TIMES_FILE = (
        "on_site_aid_times_test_run_simulation_electric_10.csv"
    )
    DROP_OFF_TIMES_FILE = "drop_off_times_test_run_simulation_electric_10.csv"
    LOCATION_IDS_FILE = "location_IDs_test_run_simulation_electric_10.csv"
    TO_HOSPITAL_FILE = "to_hospital_bool_test_run_simulation_electric_10.csv"

    PROCESS_NUM_CALLS = 300
    NUM_AMBULANCES = 20
    AID_PARAMETERS = [88]  # Cut-off value
    ENGINE_TYPE = "electric"
    IDLE_USAGE = 5  # kW
    DRIVING_USAGE = 0.4  # kWh/km
    if ENGINE_TYPE == "electric":
        BATTERY_CAPACITY = 150.0
    else:
        BATTERY_CAPACITY = np.inf
    NO_SIREN_PENALTY = 0.95
    LOAD_INPUT_DATA = True
    INTERVAL_CHECK_WP = 1
    TIME_AFTER_LAST_ARRIVAL = 1000

    PRINT = False
    DATA_COLUMNS_PATIENT = [
        "patient_ID",
        "response_time",
        "arrival_time",
        "location_ID",
        "nr_ambulances_available",
        "nr_ambulances_not_assignable",
        "assigned_to_ambulance_nr",
        "waiting_time_before_assigned",
        "driving_time_to_patient",
        "ambulance_arrival_time",
        "on_site_aid_time",
        "to_hospital",
        "hospital_ID",
        "driving_time_to_hospital",
        "drop_off_time_hospital",
        "finish_time",
    ]
    DATA_COLUMNS_AMBULANCE = [
        "ambulance_ID",
        "time",
        "battery_level_before",
        "battery_level_after",
        "use_or_charge",
        "idle_or_driving_decrease",
        "idle_time",
        "source_location_ID",
        "target_location_ID",
        "driven_km",
        "battery_decrease",
        "charging_type",
        "charging_location_ID",
        "speed_charger",
        "charging_success",
        "waiting_time",
        "charging_interrupted",
        "charging_time",
        "battery_increase",
    ]

    SIMULATION_PARAMETERS = {
        "PROCESS_NUM_CALLS": PROCESS_NUM_CALLS,
        "NUM_AMBULANCES": NUM_AMBULANCES,
        "AID_PARAMETERS": AID_PARAMETERS,
        "ENGINE_TYPE": ENGINE_TYPE,
        "IDLE_USAGE": IDLE_USAGE,
        "DRIVING_USAGE": DRIVING_USAGE,
        "BATTERY_CAPACITY": BATTERY_CAPACITY,
        "NO_SIREN_PENALTY": NO_SIREN_PENALTY,
        "PRINT": PRINT,
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
        "TRAVEL_TIMES_FILE": TRAVEL_TIMES_FILE,
        "DISTANCE_FILE": DISTANCE_FILE,
        "NODES_FILE": NODES_FILE,
        "HOSPITAL_FILE": HOSPITAL_FILE,
        "BASE_LOCATIONS_FILE": BASE_LOCATIONS_FILE,
        "AMBULANCE_BASE_LOCATIONS_FILE": AMBULANCE_BASE_LOCATIONS_FILE,
        "CHARGING_SCENARIO_FILE": CHARGING_SCENARIO_FILE,
        "DATA_DIRECTORY": DATA_DIRECTORY,
        "LOAD_INPUT_DATA": LOAD_INPUT_DATA,
        "SIMULATION_INPUT_DIRECTORY": SIMULATION_INPUT_DIRECTORY,
        "INTERARRIVAL_TIMES_FILE": INTERARRIVAL_TIMES_FILE,
        "ON_SITE_AID_TIMES_FILE": ON_SITE_AID_TIMES_FILE,
        "DROP_OFF_TIMES_FILE": DROP_OFF_TIMES_FILE,
        "LOCATION_IDS_FILE": LOCATION_IDS_FILE,
        "TO_HOSPITAL_FILE": TO_HOSPITAL_FILE,
        "INTERVAL_CHECK_WP": INTERVAL_CHECK_WP,
        "TIME_AFTER_LAST_ARRIVAL": TIME_AFTER_LAST_ARRIVAL,
    }
    SIMULATION_DATA = {
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
    }

    # Run simulation and cast output to dataframe.
    run_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)
    df_patient = pd.DataFrame(
        SIMULATION_DATA["output_patient"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"],
    )
    df_patient = calculate_response_time_ecdf(df_patient)
    df_ambulance = pd.DataFrame(
        SIMULATION_DATA["output_ambulance"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"],
    )

    # Get saved dataframes
    df_test_patient = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Patient_Test_Electric_10.csv",
        index_col=0,
        float_precision="round_trip",
    )
    df_test_ambulance = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Ambulance_Test_Electric_10.csv",
        index_col=0,
        float_precision="round_trip",
    )

    pd.testing.assert_frame_equal(
        df_patient, df_test_patient, rtol=1e-20, atol=1e-20
    )
    pd.testing.assert_frame_equal(
        df_ambulance, df_test_ambulance, rtol=1e-20, atol=1e-20
    )


def test_run_simulation_electric_11():

    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/")
    SIMULATION_INPUT_DIRECTORY = os.path.join(
        ROOT_DIRECTORY, "data/unit_tests/"
    )
    SIMULATED_DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/unit_tests/")

    TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
    DISTANCE_FILE: str = "distance_matrix_2022.csv"
    NODES_FILE: str = "nodes_Utrecht_2021.csv"
    HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
    BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
    AMBULANCE_BASE_LOCATIONS_FILE: str = (
        "Base_Locations_Ambulances_MEXCLP_21_22_20.csv"
    )
    CHARGING_SCENARIO_FILE: str = "charging_scenario_21_22_RB1.csv"

    INTERARRIVAL_TIMES_FILE = (
        "interarrival_times_test_run_simulation_electric_11.csv"
    )
    ON_SITE_AID_TIMES_FILE = (
        "on_site_aid_times_test_run_simulation_electric_11.csv"
    )
    DROP_OFF_TIMES_FILE = "drop_off_times_test_run_simulation_electric_11.csv"
    LOCATION_IDS_FILE = "location_IDs_test_run_simulation_electric_11.csv"
    TO_HOSPITAL_FILE = "to_hospital_bool_test_run_simulation_electric_11.csv"

    PROCESS_NUM_CALLS = 400
    NUM_AMBULANCES = 20
    AID_PARAMETERS = [88]  # Cut-off value
    ENGINE_TYPE = "electric"
    IDLE_USAGE = 5  # kW
    DRIVING_USAGE = 0.4  # kWh/km
    if ENGINE_TYPE == "electric":
        BATTERY_CAPACITY = 150.0
    else:
        BATTERY_CAPACITY = np.inf
    NO_SIREN_PENALTY = 0.95
    LOAD_INPUT_DATA = True
    INTERVAL_CHECK_WP = 1
    TIME_AFTER_LAST_ARRIVAL = 1000

    PRINT = False
    DATA_COLUMNS_PATIENT = [
        "patient_ID",
        "response_time",
        "arrival_time",
        "location_ID",
        "nr_ambulances_available",
        "nr_ambulances_not_assignable",
        "assigned_to_ambulance_nr",
        "waiting_time_before_assigned",
        "driving_time_to_patient",
        "ambulance_arrival_time",
        "on_site_aid_time",
        "to_hospital",
        "hospital_ID",
        "driving_time_to_hospital",
        "drop_off_time_hospital",
        "finish_time",
    ]
    DATA_COLUMNS_AMBULANCE = [
        "ambulance_ID",
        "time",
        "battery_level_before",
        "battery_level_after",
        "use_or_charge",
        "idle_or_driving_decrease",
        "idle_time",
        "source_location_ID",
        "target_location_ID",
        "driven_km",
        "battery_decrease",
        "charging_type",
        "charging_location_ID",
        "speed_charger",
        "charging_success",
        "waiting_time",
        "charging_interrupted",
        "charging_time",
        "battery_increase",
    ]

    SIMULATION_PARAMETERS = {
        "PROCESS_NUM_CALLS": PROCESS_NUM_CALLS,
        "NUM_AMBULANCES": NUM_AMBULANCES,
        "AID_PARAMETERS": AID_PARAMETERS,
        "ENGINE_TYPE": ENGINE_TYPE,
        "IDLE_USAGE": IDLE_USAGE,
        "DRIVING_USAGE": DRIVING_USAGE,
        "BATTERY_CAPACITY": BATTERY_CAPACITY,
        "NO_SIREN_PENALTY": NO_SIREN_PENALTY,
        "PRINT": PRINT,
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
        "TRAVEL_TIMES_FILE": TRAVEL_TIMES_FILE,
        "DISTANCE_FILE": DISTANCE_FILE,
        "NODES_FILE": NODES_FILE,
        "HOSPITAL_FILE": HOSPITAL_FILE,
        "BASE_LOCATIONS_FILE": BASE_LOCATIONS_FILE,
        "AMBULANCE_BASE_LOCATIONS_FILE": AMBULANCE_BASE_LOCATIONS_FILE,
        "CHARGING_SCENARIO_FILE": CHARGING_SCENARIO_FILE,
        "DATA_DIRECTORY": DATA_DIRECTORY,
        "LOAD_INPUT_DATA": LOAD_INPUT_DATA,
        "SIMULATION_INPUT_DIRECTORY": SIMULATION_INPUT_DIRECTORY,
        "INTERARRIVAL_TIMES_FILE": INTERARRIVAL_TIMES_FILE,
        "ON_SITE_AID_TIMES_FILE": ON_SITE_AID_TIMES_FILE,
        "DROP_OFF_TIMES_FILE": DROP_OFF_TIMES_FILE,
        "LOCATION_IDS_FILE": LOCATION_IDS_FILE,
        "TO_HOSPITAL_FILE": TO_HOSPITAL_FILE,
        "INTERVAL_CHECK_WP": INTERVAL_CHECK_WP,
        "TIME_AFTER_LAST_ARRIVAL": TIME_AFTER_LAST_ARRIVAL,
    }
    SIMULATION_DATA = {
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
    }

    # Run simulation and cast output to dataframe.
    run_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)
    df_patient = pd.DataFrame(
        SIMULATION_DATA["output_patient"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"],
    )
    df_patient = calculate_response_time_ecdf(df_patient)
    df_ambulance = pd.DataFrame(
        SIMULATION_DATA["output_ambulance"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"],
    )

    # Get saved dataframes
    df_test_patient = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Patient_Test_Electric_11.csv",
        index_col=0,
        float_precision="round_trip",
    )
    df_test_ambulance = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Ambulance_Test_Electric_11.csv",
        index_col=0,
        float_precision="round_trip",
    )

    pd.testing.assert_frame_equal(
        df_patient, df_test_patient, rtol=1e-20, atol=1e-20
    )
    pd.testing.assert_frame_equal(
        df_ambulance, df_test_ambulance, rtol=1e-20, atol=1e-20
    )


def test_run_simulation_diesel_3():
    ## Simulation parameters

    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/")
    SIMULATION_INPUT_DIRECTORY = os.path.join(
        ROOT_DIRECTORY, "data/unit_tests/"
    )
    SIMULATED_DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/unit_tests/")

    TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
    DISTANCE_FILE: str = "distance_matrix_2022.csv"
    NODES_FILE: str = "nodes_Utrecht_2021.csv"
    HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
    BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
    AMBULANCE_BASE_LOCATIONS_FILE: str = (
        "Base_Locations_Ambulances_MEXCLP_21_22_23.csv"
    )
    CHARGING_SCENARIO_FILE: str = "charging_scenario_21_22_Diesel.csv"

    INTERARRIVAL_TIMES_FILE = (
        "interarrival_times_test_run_simulation_diesel_3.csv"
    )
    ON_SITE_AID_TIMES_FILE = (
        "on_site_aid_times_test_run_simulation_diesel_3.csv"
    )
    DROP_OFF_TIMES_FILE = "drop_off_times_test_run_simulation_diesel_3.csv"
    LOCATION_IDS_FILE = "location_IDs_test_run_simulation_diesel_3.csv"
    TO_HOSPITAL_FILE = "to_hospital_bool_test_run_simulation_diesel_3.csv"

    PROCESS_NUM_CALLS = 1400
    NUM_AMBULANCES = 23
    ENGINE_TYPE = "diesel"
    if ENGINE_TYPE == "electric":
        BATTERY_CAPACITY = 150.0
    else:
        BATTERY_CAPACITY = np.inf
    NO_SIREN_PENALTY = 0.95
    LOAD_INPUT_DATA = True

    PRINT = False
    DATA_COLUMNS_PATIENT = [
        "patient_ID",
        "response_time",
        "arrival_time",
        "location_ID",
        "nr_ambulances_available",
        "nr_ambulances_not_assignable",
        "assigned_to_ambulance_nr",
        "waiting_time_before_assigned",
        "driving_time_to_patient",
        "ambulance_arrival_time",
        "on_site_aid_time",
        "to_hospital",
        "hospital_ID",
        "driving_time_to_hospital",
        "drop_off_time_hospital",
        "finish_time",
    ]
    DATA_COLUMNS_AMBULANCE = [
        "ambulance_ID",
        "time",
        "battery_level_before",
        "battery_level_after",
        "use_or_charge",
        "idle_or_driving_decrease",
        "idle_time",
        "source_location_ID",
        "target_location_ID",
        "driven_km",
        "battery_decrease",
        "charging_type",
        "charging_location_ID",
        "speed_charger",
        "charging_success",
        "waiting_time",
        "charging_interrupted",
        "charging_time",
        "battery_increase",
    ]

    SIMULATION_PARAMETERS = {
        "PROCESS_NUM_CALLS": PROCESS_NUM_CALLS,
        "NUM_AMBULANCES": NUM_AMBULANCES,
        "ENGINE_TYPE": ENGINE_TYPE,
        "BATTERY_CAPACITY": BATTERY_CAPACITY,
        "NO_SIREN_PENALTY": NO_SIREN_PENALTY,
        "PRINT": PRINT,
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
        "TRAVEL_TIMES_FILE": TRAVEL_TIMES_FILE,
        "DISTANCE_FILE": DISTANCE_FILE,
        "NODES_FILE": NODES_FILE,
        "HOSPITAL_FILE": HOSPITAL_FILE,
        "BASE_LOCATIONS_FILE": BASE_LOCATIONS_FILE,
        "AMBULANCE_BASE_LOCATIONS_FILE": AMBULANCE_BASE_LOCATIONS_FILE,
        "CHARGING_SCENARIO_FILE": CHARGING_SCENARIO_FILE,
        "DATA_DIRECTORY": DATA_DIRECTORY,
        "LOAD_INPUT_DATA": LOAD_INPUT_DATA,
        "SIMULATION_INPUT_DIRECTORY": SIMULATION_INPUT_DIRECTORY,
        "INTERARRIVAL_TIMES_FILE": INTERARRIVAL_TIMES_FILE,
        "ON_SITE_AID_TIMES_FILE": ON_SITE_AID_TIMES_FILE,
        "DROP_OFF_TIMES_FILE": DROP_OFF_TIMES_FILE,
        "LOCATION_IDS_FILE": LOCATION_IDS_FILE,
        "TO_HOSPITAL_FILE": TO_HOSPITAL_FILE,
    }
    SIMULATION_DATA = {
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
    }

    # Run simulation and cast output to dataframe.
    run_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)
    df_patient = pd.DataFrame(
        SIMULATION_DATA["output_patient"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"],
    )
    df_patient = calculate_response_time_ecdf(df_patient)
    df_ambulance = pd.DataFrame(
        SIMULATION_DATA["output_ambulance"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"],
    )

    # Get saved dataframes
    df_test_patient = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Patient_Test_Diesel_3.csv",
        index_col=0,
        float_precision="round_trip",
    )
    df_test_ambulance = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Ambulance_Test_Diesel_3.csv",
        index_col=0,
        float_precision="round_trip",
    )

    pd.testing.assert_frame_equal(
        df_patient, df_test_patient, rtol=1e-20, atol=1e-20
    )
    pd.testing.assert_frame_equal(
        df_ambulance, df_test_ambulance, rtol=1e-20, atol=1e-20
    )


def test_run_simulation_diesel_4():
    ## Simulation parameters

    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/")
    SIMULATION_INPUT_DIRECTORY = os.path.join(
        ROOT_DIRECTORY, "data/unit_tests/"
    )
    SIMULATED_DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/unit_tests/")

    TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
    DISTANCE_FILE: str = "distance_matrix_2022.csv"
    NODES_FILE: str = "nodes_Utrecht_2021.csv"
    HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
    BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
    AMBULANCE_BASE_LOCATIONS_FILE: str = (
        "Base_Locations_Ambulances_MEXCLP_21_22_24.csv"
    )
    CHARGING_SCENARIO_FILE: str = "charging_scenario_21_22_Diesel.csv"

    INTERARRIVAL_TIMES_FILE = (
        "interarrival_times_test_run_simulation_diesel_4.csv"
    )
    ON_SITE_AID_TIMES_FILE = (
        "on_site_aid_times_test_run_simulation_diesel_4.csv"
    )
    DROP_OFF_TIMES_FILE = "drop_off_times_test_run_simulation_diesel_4.csv"
    LOCATION_IDS_FILE = "location_IDs_test_run_simulation_diesel_4.csv"
    TO_HOSPITAL_FILE = "to_hospital_bool_test_run_simulation_diesel_4.csv"

    PROCESS_NUM_CALLS = 3500
    NUM_AMBULANCES = 24
    ENGINE_TYPE = "diesel"
    if ENGINE_TYPE == "electric":
        BATTERY_CAPACITY = 150.0
    else:
        BATTERY_CAPACITY = np.inf
    NO_SIREN_PENALTY = 0.95
    LOAD_INPUT_DATA = True

    PRINT = False
    DATA_COLUMNS_PATIENT = [
        "patient_ID",
        "response_time",
        "arrival_time",
        "location_ID",
        "nr_ambulances_available",
        "nr_ambulances_not_assignable",
        "assigned_to_ambulance_nr",
        "waiting_time_before_assigned",
        "driving_time_to_patient",
        "ambulance_arrival_time",
        "on_site_aid_time",
        "to_hospital",
        "hospital_ID",
        "driving_time_to_hospital",
        "drop_off_time_hospital",
        "finish_time",
    ]
    DATA_COLUMNS_AMBULANCE = [
        "ambulance_ID",
        "time",
        "battery_level_before",
        "battery_level_after",
        "use_or_charge",
        "idle_or_driving_decrease",
        "idle_time",
        "source_location_ID",
        "target_location_ID",
        "driven_km",
        "battery_decrease",
        "charging_type",
        "charging_location_ID",
        "speed_charger",
        "charging_success",
        "waiting_time",
        "charging_interrupted",
        "charging_time",
        "battery_increase",
    ]

    SIMULATION_PARAMETERS = {
        "PROCESS_NUM_CALLS": PROCESS_NUM_CALLS,
        "NUM_AMBULANCES": NUM_AMBULANCES,
        "ENGINE_TYPE": ENGINE_TYPE,
        "BATTERY_CAPACITY": BATTERY_CAPACITY,
        "NO_SIREN_PENALTY": NO_SIREN_PENALTY,
        "PRINT": PRINT,
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
        "TRAVEL_TIMES_FILE": TRAVEL_TIMES_FILE,
        "DISTANCE_FILE": DISTANCE_FILE,
        "NODES_FILE": NODES_FILE,
        "HOSPITAL_FILE": HOSPITAL_FILE,
        "BASE_LOCATIONS_FILE": BASE_LOCATIONS_FILE,
        "AMBULANCE_BASE_LOCATIONS_FILE": AMBULANCE_BASE_LOCATIONS_FILE,
        "CHARGING_SCENARIO_FILE": CHARGING_SCENARIO_FILE,
        "DATA_DIRECTORY": DATA_DIRECTORY,
        "LOAD_INPUT_DATA": LOAD_INPUT_DATA,
        "SIMULATION_INPUT_DIRECTORY": SIMULATION_INPUT_DIRECTORY,
        "INTERARRIVAL_TIMES_FILE": INTERARRIVAL_TIMES_FILE,
        "ON_SITE_AID_TIMES_FILE": ON_SITE_AID_TIMES_FILE,
        "DROP_OFF_TIMES_FILE": DROP_OFF_TIMES_FILE,
        "LOCATION_IDS_FILE": LOCATION_IDS_FILE,
        "TO_HOSPITAL_FILE": TO_HOSPITAL_FILE,
    }
    SIMULATION_DATA = {
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
    }

    # Run simulation and cast output to dataframe.
    run_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)
    df_patient = pd.DataFrame(
        SIMULATION_DATA["output_patient"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"],
    )
    df_patient = calculate_response_time_ecdf(df_patient)
    df_ambulance = pd.DataFrame(
        SIMULATION_DATA["output_ambulance"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"],
    )

    # Get saved dataframes
    df_test_patient = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Patient_Test_Diesel_4.csv",
        index_col=0,
        float_precision="round_trip",
    )
    df_test_ambulance = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Ambulance_Test_Diesel_4.csv",
        index_col=0,
        float_precision="round_trip",
    )

    pd.testing.assert_frame_equal(
        df_patient, df_test_patient, rtol=1e-20, atol=1e-20
    )
    pd.testing.assert_frame_equal(
        df_ambulance, df_test_ambulance, rtol=1e-20, atol=1e-20
    )


def test_run_simulation_diesel_5():
    ## Simulation parameters

    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/")
    SIMULATION_INPUT_DIRECTORY = os.path.join(
        ROOT_DIRECTORY, "data/unit_tests/"
    )
    SIMULATED_DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/unit_tests/")

    TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
    DISTANCE_FILE: str = "distance_matrix_2022.csv"
    NODES_FILE: str = "nodes_Utrecht_2021.csv"
    HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
    BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
    AMBULANCE_BASE_LOCATIONS_FILE: str = (
        "Base_Locations_Ambulances_MEXCLP_21_22_20.csv"
    )
    CHARGING_SCENARIO_FILE: str = "charging_scenario_21_22_Diesel.csv"

    INTERARRIVAL_TIMES_FILE = (
        "interarrival_times_test_run_simulation_diesel_5.csv"
    )
    ON_SITE_AID_TIMES_FILE = (
        "on_site_aid_times_test_run_simulation_diesel_5.csv"
    )
    DROP_OFF_TIMES_FILE = "drop_off_times_test_run_simulation_diesel_5.csv"
    LOCATION_IDS_FILE = "location_IDs_test_run_simulation_diesel_5.csv"
    TO_HOSPITAL_FILE = "to_hospital_bool_test_run_simulation_diesel_5.csv"

    PROCESS_NUM_CALLS = 800
    NUM_AMBULANCES = 20
    ENGINE_TYPE = "diesel"
    if ENGINE_TYPE == "electric":
        BATTERY_CAPACITY = 150.0
    else:
        BATTERY_CAPACITY = np.inf
    NO_SIREN_PENALTY = 0.95
    LOAD_INPUT_DATA = True

    PRINT = False
    DATA_COLUMNS_PATIENT = [
        "patient_ID",
        "response_time",
        "arrival_time",
        "location_ID",
        "nr_ambulances_available",
        "nr_ambulances_not_assignable",
        "assigned_to_ambulance_nr",
        "waiting_time_before_assigned",
        "driving_time_to_patient",
        "ambulance_arrival_time",
        "on_site_aid_time",
        "to_hospital",
        "hospital_ID",
        "driving_time_to_hospital",
        "drop_off_time_hospital",
        "finish_time",
    ]
    DATA_COLUMNS_AMBULANCE = [
        "ambulance_ID",
        "time",
        "battery_level_before",
        "battery_level_after",
        "use_or_charge",
        "idle_or_driving_decrease",
        "idle_time",
        "source_location_ID",
        "target_location_ID",
        "driven_km",
        "battery_decrease",
        "charging_type",
        "charging_location_ID",
        "speed_charger",
        "charging_success",
        "waiting_time",
        "charging_interrupted",
        "charging_time",
        "battery_increase",
    ]

    SIMULATION_PARAMETERS = {
        "PROCESS_NUM_CALLS": PROCESS_NUM_CALLS,
        "NUM_AMBULANCES": NUM_AMBULANCES,
        "ENGINE_TYPE": ENGINE_TYPE,
        "BATTERY_CAPACITY": BATTERY_CAPACITY,
        "NO_SIREN_PENALTY": NO_SIREN_PENALTY,
        "PRINT": PRINT,
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
        "TRAVEL_TIMES_FILE": TRAVEL_TIMES_FILE,
        "DISTANCE_FILE": DISTANCE_FILE,
        "NODES_FILE": NODES_FILE,
        "HOSPITAL_FILE": HOSPITAL_FILE,
        "BASE_LOCATIONS_FILE": BASE_LOCATIONS_FILE,
        "AMBULANCE_BASE_LOCATIONS_FILE": AMBULANCE_BASE_LOCATIONS_FILE,
        "CHARGING_SCENARIO_FILE": CHARGING_SCENARIO_FILE,
        "DATA_DIRECTORY": DATA_DIRECTORY,
        "LOAD_INPUT_DATA": LOAD_INPUT_DATA,
        "SIMULATION_INPUT_DIRECTORY": SIMULATION_INPUT_DIRECTORY,
        "INTERARRIVAL_TIMES_FILE": INTERARRIVAL_TIMES_FILE,
        "ON_SITE_AID_TIMES_FILE": ON_SITE_AID_TIMES_FILE,
        "DROP_OFF_TIMES_FILE": DROP_OFF_TIMES_FILE,
        "LOCATION_IDS_FILE": LOCATION_IDS_FILE,
        "TO_HOSPITAL_FILE": TO_HOSPITAL_FILE,
    }
    SIMULATION_DATA = {
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
    }

    # Run simulation and cast output to dataframe.
    run_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)
    df_patient = pd.DataFrame(
        SIMULATION_DATA["output_patient"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"],
    )
    df_patient = calculate_response_time_ecdf(df_patient)
    df_ambulance = pd.DataFrame(
        SIMULATION_DATA["output_ambulance"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"],
    )

    # Get saved dataframes
    df_test_patient = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Patient_Test_Diesel_5.csv",
        index_col=0,
        float_precision="round_trip",
    )
    df_test_ambulance = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Ambulance_Test_Diesel_5.csv",
        index_col=0,
        float_precision="round_trip",
    )

    pd.testing.assert_frame_equal(
        df_patient, df_test_patient, rtol=1e-20, atol=1e-20
    )
    pd.testing.assert_frame_equal(
        df_ambulance, df_test_ambulance, rtol=1e-20, atol=1e-20
    )


def test_run_simulation_diesel_6():
    ## Simulation parameters

    ROOT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
    DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/")
    SIMULATION_INPUT_DIRECTORY = os.path.join(
        ROOT_DIRECTORY, "data/unit_tests/"
    )
    SIMULATED_DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "data/unit_tests/")

    TRAVEL_TIMES_FILE: str = "siren_driving_matrix_2022.csv"
    DISTANCE_FILE: str = "distance_matrix_2022.csv"
    NODES_FILE: str = "nodes_Utrecht_2021.csv"
    HOSPITAL_FILE: str = "Hospital_Postal_Codes_Utrecht_2021.csv"
    BASE_LOCATIONS_FILE: str = "RAVU_base_locations_Utrecht_2021.csv"
    AMBULANCE_BASE_LOCATIONS_FILE: str = (
        "Base_Locations_Ambulances_MEXCLP_21_22_20.csv"
    )
    CHARGING_SCENARIO_FILE: str = "charging_scenario_21_22_Diesel.csv"

    INTERARRIVAL_TIMES_FILE = (
        "interarrival_times_test_run_simulation_diesel_6.csv"
    )
    ON_SITE_AID_TIMES_FILE = (
        "on_site_aid_times_test_run_simulation_diesel_6.csv"
    )
    DROP_OFF_TIMES_FILE = "drop_off_times_test_run_simulation_diesel_6.csv"
    LOCATION_IDS_FILE = "location_IDs_test_run_simulation_diesel_6.csv"
    TO_HOSPITAL_FILE = "to_hospital_bool_test_run_simulation_diesel_6.csv"

    PROCESS_NUM_CALLS = 550
    NUM_AMBULANCES = 20
    ENGINE_TYPE = "diesel"
    if ENGINE_TYPE == "electric":
        BATTERY_CAPACITY = 150.0
    else:
        BATTERY_CAPACITY = np.inf
    NO_SIREN_PENALTY = 0.95
    LOAD_INPUT_DATA = True

    PRINT = False
    DATA_COLUMNS_PATIENT = [
        "patient_ID",
        "response_time",
        "arrival_time",
        "location_ID",
        "nr_ambulances_available",
        "nr_ambulances_not_assignable",
        "assigned_to_ambulance_nr",
        "waiting_time_before_assigned",
        "driving_time_to_patient",
        "ambulance_arrival_time",
        "on_site_aid_time",
        "to_hospital",
        "hospital_ID",
        "driving_time_to_hospital",
        "drop_off_time_hospital",
        "finish_time",
    ]
    DATA_COLUMNS_AMBULANCE = [
        "ambulance_ID",
        "time",
        "battery_level_before",
        "battery_level_after",
        "use_or_charge",
        "idle_or_driving_decrease",
        "idle_time",
        "source_location_ID",
        "target_location_ID",
        "driven_km",
        "battery_decrease",
        "charging_type",
        "charging_location_ID",
        "speed_charger",
        "charging_success",
        "waiting_time",
        "charging_interrupted",
        "charging_time",
        "battery_increase",
    ]

    SIMULATION_PARAMETERS = {
        "PROCESS_NUM_CALLS": PROCESS_NUM_CALLS,
        "NUM_AMBULANCES": NUM_AMBULANCES,
        "ENGINE_TYPE": ENGINE_TYPE,
        "BATTERY_CAPACITY": BATTERY_CAPACITY,
        "NO_SIREN_PENALTY": NO_SIREN_PENALTY,
        "PRINT": PRINT,
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
        "TRAVEL_TIMES_FILE": TRAVEL_TIMES_FILE,
        "DISTANCE_FILE": DISTANCE_FILE,
        "NODES_FILE": NODES_FILE,
        "HOSPITAL_FILE": HOSPITAL_FILE,
        "BASE_LOCATIONS_FILE": BASE_LOCATIONS_FILE,
        "AMBULANCE_BASE_LOCATIONS_FILE": AMBULANCE_BASE_LOCATIONS_FILE,
        "CHARGING_SCENARIO_FILE": CHARGING_SCENARIO_FILE,
        "DATA_DIRECTORY": DATA_DIRECTORY,
        "LOAD_INPUT_DATA": LOAD_INPUT_DATA,
        "SIMULATION_INPUT_DIRECTORY": SIMULATION_INPUT_DIRECTORY,
        "INTERARRIVAL_TIMES_FILE": INTERARRIVAL_TIMES_FILE,
        "ON_SITE_AID_TIMES_FILE": ON_SITE_AID_TIMES_FILE,
        "DROP_OFF_TIMES_FILE": DROP_OFF_TIMES_FILE,
        "LOCATION_IDS_FILE": LOCATION_IDS_FILE,
        "TO_HOSPITAL_FILE": TO_HOSPITAL_FILE,
    }
    SIMULATION_DATA = {
        "DATA_COLUMNS_PATIENT": DATA_COLUMNS_PATIENT,
        "DATA_COLUMNS_AMBULANCE": DATA_COLUMNS_AMBULANCE,
    }

    # Run simulation and cast output to dataframe.
    run_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)
    df_patient = pd.DataFrame(
        SIMULATION_DATA["output_patient"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_PATIENT"],
    )
    df_patient = calculate_response_time_ecdf(df_patient)
    df_ambulance = pd.DataFrame(
        SIMULATION_DATA["output_ambulance"],
        columns=SIMULATION_PARAMETERS["DATA_COLUMNS_AMBULANCE"],
    )

    # Get saved dataframes
    df_test_patient = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Patient_Test_Diesel_6.csv",
        index_col=0,
        float_precision="round_trip",
    )
    df_test_ambulance = pd.read_csv(
        f"{SIMULATED_DATA_DIRECTORY}Ambulance_Test_Diesel_6.csv",
        index_col=0,
        float_precision="round_trip",
    )

    pd.testing.assert_frame_equal(
        df_patient, df_test_patient, rtol=1e-20, atol=1e-20
    )
    pd.testing.assert_frame_equal(
        df_ambulance, df_test_ambulance, rtol=1e-20, atol=1e-20
    )
