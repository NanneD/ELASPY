#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import simpy as sp
import numpy as np
import pandas as pd
import numpy.random as rnd

from typing import Any
from ambulance import Ambulance
from patient import Patient
from collections import deque
from coordinate_methods import (
    calculate_new_coordinate,
    select_closest_location_ID,
)


def initialize_simulation(
    SIMULATION_PARAMETERS: dict[str, Any], SIMULATION_DATA: dict[str, Any]
) -> tuple[
    np.ndarray,
    dict[str, np.ndarray],
    list[Ambulance],
    dict[str, dict[str, list[sp.resources.resource.Resource | float]]],
    sp.core.Environment,
    np.ndarray,
    deque,
]:
    """
    Initializes all data and required objects of the simulation.

    Note that the ``SIMULATION_DATA`` dataframe will contain the data that is
    initialized.

    Parameters
    ----------
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``DATA_DIRECTORY``,
        ``TRAVEL_TIMES_FILE``, ``DISTANCE_FILE``, ``NODES_FILE``,
        ``HOSPITAL_FILE``, ``BASE_LOCATIONS_FILE``,
        ``AMBULANCE_BASE_LOCATIONS_FILE``, ``CHARGING_SCENARIO_FILE``,
        ``LOAD_INPUT_DATA`` and ``PRINT`` are at least necessary.
        If no historical data is used, the parameters
        ``PROB_GO_TO_HOSPITAL``, ``CRN_GENERATOR``, ``SEED_VALUE``,
        ``CALL_LAMBDA``, ``PROCESS_TYPE``, ``PROCESS_NUM_CALLS``,
        ``PROCESS_TIME``, ``AID_PARAMETERS``, ``DROP_OFF_PARAMETERS`` are also
        necessary. If historical data is used, the parameters
        ``INTERARRIVAL_TIMES_FILE``, ``ON_SITE_AID_TIMES_FILE``,
        ``DROP_OFF_TIMES_FILE``, ``LOCATION_IDS_FILE`` and ``TO_HOSPITAL_FILE``
        are also necessary. Note that methods that are called within this
        method may require more parameters. See ``main.py`` for parameter
        explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``DATA_COLUMNS_PATIENT`` and
        ``DATA_COLUMNS_AMBULANCE`` are at least necessary. See ``main.py`` for
        explanations. Note that methods that are called within this method may
        require more data.

    Raises
    ------
    Exception
        If invalid input parameters are detected.

    Returns
    -------
    location_IDs : np.ndarray
        Contains the initial location IDs of the patients.
    simulation_times : dict[str, np.ndarray]
        Contains the interarrival times, the on-site aid times and the drop-off
        times.
    ambulances : list[Ambulance]
        A list of initialized ambulances.
    charging_stations : dict[str, dict[str, list[sp.resources.resource.Resource | float]]]
        The charging stations resources at all bases and all hospitals together
        with their charging speeds.
    env : sp.core.Environment
        The SimPy environment.
    to_hospital_bool : np.ndarray
        Specifies for each patient whether transportation to the hospital is
        required or not.
    patient_queue : collections.deque
        The patient queue.

    """

    SIREN_DRIVING_MATRIX = pd.read_csv(
        f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
        f"{SIMULATION_PARAMETERS['TRAVEL_TIMES_FILE']}",
        index_col=0,
    )
    SIREN_DRIVING_MATRIX.columns = SIREN_DRIVING_MATRIX.columns.astype(int)

    DISTANCE_MATRIX = pd.read_csv(
        f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
        f"{SIMULATION_PARAMETERS['DISTANCE_FILE']}",
        index_col=0,
    )
    DISTANCE_MATRIX.columns = DISTANCE_MATRIX.columns.astype(int)

    NODES_REGION = pd.read_csv(
        f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
        f"{SIMULATION_PARAMETERS['NODES_FILE']}",
        index_col=0,
    )
    NODES_HOSPITAL = pd.read_csv(
        f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
        f"{SIMULATION_PARAMETERS['HOSPITAL_FILE']}"
    )
    NODES_BASE_LOCATIONS = pd.read_csv(
        f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
        f"{SIMULATION_PARAMETERS['BASE_LOCATIONS_FILE']}"
    )
    AMBULANCE_BASE_LOCATIONS = pd.read_csv(
        f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
        f"{SIMULATION_PARAMETERS['AMBULANCE_BASE_LOCATIONS_FILE']}",
        index_col=0,
    )
    CHARGING_STATIONS_SCENARIO = pd.read_csv(
        f"{SIMULATION_PARAMETERS['DATA_DIRECTORY']}"
        f"{SIMULATION_PARAMETERS['CHARGING_SCENARIO_FILE']}",
        index_col=0,
    )

    SIMULATION_DATA["SIREN_DRIVING_MATRIX"] = SIREN_DRIVING_MATRIX
    SIMULATION_DATA["DISTANCE_MATRIX"] = DISTANCE_MATRIX
    SIMULATION_DATA["NODES_REGION"] = NODES_REGION
    SIMULATION_DATA["NODES_HOSPITAL"] = NODES_HOSPITAL
    SIMULATION_DATA["NODES_BASE_LOCATIONS"] = NODES_BASE_LOCATIONS
    SIMULATION_DATA["AMBULANCE_BASE_LOCATIONS"] = AMBULANCE_BASE_LOCATIONS
    SIMULATION_DATA["CHARGING_STATIONS_SCENARIO"] = CHARGING_STATIONS_SCENARIO

    if SIMULATION_PARAMETERS["LOAD_INPUT_DATA"]:
        interarrival_times = (
            pd.read_csv(
                f"{SIMULATION_PARAMETERS['SIMULATION_INPUT_DIRECTORY']}"
                f"{SIMULATION_PARAMETERS['INTERARRIVAL_TIMES_FILE']}",
                float_precision="round_trip",
            )
            .to_numpy()
            .flatten()
        )
        on_site_aid_times = (
            pd.read_csv(
                f"{SIMULATION_PARAMETERS['SIMULATION_INPUT_DIRECTORY']}"
                f"{SIMULATION_PARAMETERS['ON_SITE_AID_TIMES_FILE']}",
                float_precision="round_trip",
            )
            .to_numpy()
            .flatten()
        )
        drop_off_times = (
            pd.read_csv(
                f"{SIMULATION_PARAMETERS['SIMULATION_INPUT_DIRECTORY']}"
                f"{SIMULATION_PARAMETERS['DROP_OFF_TIMES_FILE']}",
                float_precision="round_trip",
            )
            .to_numpy()
            .flatten()
        )
        location_IDs = (
            pd.read_csv(
                f"{SIMULATION_PARAMETERS['SIMULATION_INPUT_DIRECTORY']}"
                f"{SIMULATION_PARAMETERS['LOCATION_IDS_FILE']}",
                float_precision="round_trip",
            )
            .to_numpy()
            .flatten()
        )
        to_hospital_bool = (
            pd.read_csv(
                f"{SIMULATION_PARAMETERS['SIMULATION_INPUT_DIRECTORY']}"
                f"{SIMULATION_PARAMETERS['TO_HOSPITAL_FILE']}",
                float_precision="round_trip",
            )
            .to_numpy()
            .flatten()
        )

        SIMULATION_PARAMETERS["NUM_CALLS"] = SIMULATION_PARAMETERS[
            "PROCESS_NUM_CALLS"
        ]
    else:

        rng: rnd._generator.Generator | rnd.mtrand.RandomState

        if SIMULATION_PARAMETERS["CRN_GENERATOR"] == "RandomState":
            rng = rnd.RandomState(SIMULATION_PARAMETERS["SEED_VALUE"])
        elif SIMULATION_PARAMETERS["CRN_GENERATOR"] == "Generator":
            rng = rnd.default_rng(SIMULATION_PARAMETERS["SEED_VALUE"])
        else:
            raise Exception(
                "Invalid CRN_GENERATOR specified. Please change it."
            )

        if SIMULATION_PARAMETERS["PROCESS_TYPE"] == "Number":
            interarrival_times = rng.exponential(
                1 / SIMULATION_PARAMETERS["CALL_LAMBDA"],
                size=SIMULATION_PARAMETERS["PROCESS_NUM_CALLS"],
            )
        elif SIMULATION_PARAMETERS["PROCESS_TYPE"] == "Time":
            interarrival_times = generate_interarrival_times_process_type_time(
                rng, SIMULATION_PARAMETERS
            )
        else:
            raise Exception(
                "The PROCESS_TYPE variable should be 'Number' "
                "or 'Time', but it is not. Please change this."
            )

        SIMULATION_PARAMETERS["NUM_CALLS"] = len(interarrival_times)
        if SIMULATION_PARAMETERS["NUM_CALLS"] <= 0:
            raise Exception(
                "NUM_CALLS is smaller or equal to 0. This indicates"
                " PROCESS_TIME is too small or PROCESS_NUM_CALLS is"
                " smaller or equal to 0. Please make a change."
            )

        on_site_aid_times = generate_service_times(
            SIMULATION_PARAMETERS["AID_PARAMETERS"][0],
            SIMULATION_PARAMETERS["AID_PARAMETERS"][1],
            SIMULATION_PARAMETERS["AID_PARAMETERS"][2],
            rng,
            SIMULATION_PARAMETERS["NUM_CALLS"],
            SIMULATION_PARAMETERS["AID_PARAMETERS"][3],
        )
        drop_off_times = generate_service_times(
            SIMULATION_PARAMETERS["DROP_OFF_PARAMETERS"][0],
            SIMULATION_PARAMETERS["DROP_OFF_PARAMETERS"][1],
            SIMULATION_PARAMETERS["DROP_OFF_PARAMETERS"][2],
            rng,
            SIMULATION_PARAMETERS["NUM_CALLS"],
            SIMULATION_PARAMETERS["DROP_OFF_PARAMETERS"][3],
        )

        location_IDs = location_generator(
            rng, SIMULATION_PARAMETERS, SIMULATION_DATA
        )
        to_hospital_bool = (
            rng.uniform(0, 1, size=SIMULATION_PARAMETERS["NUM_CALLS"])
            < SIMULATION_PARAMETERS["PROB_GO_TO_HOSPITAL"]
        )

    simulation_times = {
        "interarrival": interarrival_times,
        "on_site": on_site_aid_times,
        "drop_off": drop_off_times,
    }

    print(f"NUM_CALLS: {SIMULATION_PARAMETERS['NUM_CALLS']}.")

    output_patient = np.full(
        (
            SIMULATION_PARAMETERS["NUM_CALLS"],
            len(SIMULATION_DATA["DATA_COLUMNS_PATIENT"]),
        ),
        np.nan,
    )
    output_ambulance = np.empty(
        (0, len(SIMULATION_DATA["DATA_COLUMNS_AMBULANCE"])), dtype=float
    )

    SIMULATION_DATA["output_patient"] = output_patient
    SIMULATION_DATA["output_ambulance"] = output_ambulance
    SIMULATION_DATA["nr_times_no_fast_no_regular_available"] = 0

    SIMULATION_DATA["TIME_LAST_ARRIVAL"] = np.inf

    env = sp.Environment()
    ambulances = ambulance_initialization(
        env, SIMULATION_PARAMETERS, SIMULATION_DATA
    )
    charging_stations = charging_stations_initialization(env, SIMULATION_DATA)

    patient_queue: deque = deque()

    return (
        location_IDs,
        simulation_times,
        ambulances,
        charging_stations,
        env,
        to_hospital_bool,
        patient_queue,
    )


def generate_service_times(
    s: float,
    loc: float,
    scale: float,
    rng: rnd._generator.Generator | rnd.mtrand.RandomState,
    size: int,
    CUT_OFF: float,
) -> np.ndarray:
    """
    Generates service times from the lognormal distribution.

    Note that a new data value is generated until it is between 0
    and the ``CUT_OFF`` value. Only then it is added to the service_times
    output array.

    Parameters
    ----------
    s : float
        The sigma parameter.
    loc : float
        The location parameter.
    scale : float
        The scale parameter.
    rng : rnd._generator.Generator | rnd.mtrand.RandomState
        An initialized random number generator.
    size : int
        The number of service times to generate.
    CUT_OFF : float
        The cut off/maximum value.

    Returns
    -------
    service_times : np.ndarray
        The generated service times.

    """

    service_times = np.zeros(size)

    for i in np.arange(size):
        service_time = rng.lognormal(mean=np.log(scale), sigma=s, size=1) + loc
        while (service_time < 0) or (service_time > CUT_OFF):
            service_time = (
                rng.lognormal(mean=np.log(scale), sigma=s, size=1) + loc
            )
        service_times[i] = service_time

    return service_times


def generate_interarrival_times_process_type_time(
    rng: rnd._generator.Generator | rnd.mtrand.RandomState,
    SIMULATION_PARAMETERS: dict[str, Any],
) -> np.ndarray:
    """
    Generates the interarrival times if ``PROCESS_TYPE='Time'``.

    Parameters
    ----------
    rng : rnd._generator.Generator | rnd.mtrand.RandomState
        An initialized common random number generator.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``PROCESS_TIME`` and
        ``CALL_LAMBDA`` are at least necessary. See ``main.py`` for parameter
        explanations.

    Raises
    ------
    Exception
        If generated times are such that patients arrive after ``PROCESS_TIME``.

    Returns
    -------
    interarrival_times : np.ndarray
        The generated interarrival times.

    """

    interarrival_times = np.empty(0, dtype=float)
    interarrival_sum = 0.0
    while interarrival_sum <= SIMULATION_PARAMETERS["PROCESS_TIME"]:
        interarrival_times = np.append(
            interarrival_times,
            rng.exponential(1 / SIMULATION_PARAMETERS["CALL_LAMBDA"]),
        )
        interarrival_sum = np.sum(interarrival_times)

    # Remove last patient, as its arrival time will exceed PROCESS_TIME.
    # If used for security.
    if interarrival_sum > SIMULATION_PARAMETERS["PROCESS_TIME"]:
        interarrival_times = interarrival_times[:-1]

    if np.sum(interarrival_times) > SIMULATION_PARAMETERS["PROCESS_TIME"]:
        raise Exception("Patient(s) arrive after PROCESS_TIME. Error.")

    return interarrival_times


def run_simulation(
    SIMULATION_PARAMETERS: dict[str, Any], SIMULATION_DATA: dict[str, Any]
) -> None:
    """
    Performs a single simulation run.

    Parameters
    ----------
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameter ``ENGINE_TYPE`` is at least
        necessary. Note that methods that are called within this method may
        require more parameters. See ``main.py`` for parameter explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``output_ambulance``, ``output_patient``,
        ``nr_times_no_fast_no_regular_available``, ``TIME_LAST_ARRIVAL`` are at
        least necessary. See ``main.py`` and the input data section
        on the ELASPY website for explanations. Note that methods that are
        called within this method may require more data.

    Raises
    ------
    Exception
        1. If the patient queue is not empty after completing the simulation run.
        2. If the input data (``SIMULATION_DATA``) has been changed during the
        simulation run.

    """

    (
        location_IDs,
        simulation_times,
        ambulances,
        charging_stations,
        env,
        to_hospital_bool,
        patient_queue,
    ) = initialize_simulation(SIMULATION_PARAMETERS, SIMULATION_DATA)

    copy_simulation_data = copy.deepcopy(SIMULATION_DATA)

    env.process(
        patient_generator(
            env,
            ambulances,
            charging_stations,
            location_IDs,
            simulation_times,
            to_hospital_bool,
            patient_queue,
            SIMULATION_PARAMETERS,
            SIMULATION_DATA,
        )
    )

    if SIMULATION_PARAMETERS["ENGINE_TYPE"] == "electric":
        env.process(
            help_waiting_patients(
                env,
                ambulances,
                charging_stations,
                simulation_times,
                to_hospital_bool,
                patient_queue,
                SIMULATION_PARAMETERS,
                SIMULATION_DATA,
            )
        )

    env.run()
    if len(patient_queue) != 0:
        raise Exception(
            "The patient_queue should be empty, but there are "
            f"{len(patient_queue)} waiting patients."
        )

    for key in copy_simulation_data.keys():
        if key in [
            "output_ambulance",
            "output_patient",
            "nr_times_no_fast_no_regular_available",
            "TIME_LAST_ARRIVAL",
        ]:
            # These objects are changed in the simulation.
            pass
        elif type(copy_simulation_data[key]) == pd.DataFrame:
            pd.testing.assert_frame_equal(
                copy_simulation_data[key],
                SIMULATION_DATA[key],
                rtol=1e-20,
                atol=1e-20,
            )
        elif copy_simulation_data[key] != SIMULATION_DATA[key]:
            raise Exception(
                "The SIMULATION_DATA were altered during "
                "the simulation. This should not happen. Error."
            )


def charging_stations_initialization(
    env: sp.core.Environment, SIMULATION_DATA: dict[str, Any]
) -> dict[str, dict[str, list[sp.resources.resource.Resource | float]]]:
    """
    Initializes the charging stations dictionary.

    Parameters
    ----------
    env : sp.core.Environment
        The SimPy environment.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``CHARGING_STATIONS_SCENARIO`` is at least
        necessary. It is based on ``CHARGING_SCENARIO_FILE``. See ``main.py``
        and the input data section on the ELASPY website for explanations.

    Raises
    ------
    Exception
        If the index of the row does not contain "H" (hospital) or "B" (base).

    Returns
    -------
    dict
        The charging station dictionary.

    """

    charging_stations_hospitals = {}
    charging_stations_bases = {}
    for index, row in SIMULATION_DATA["CHARGING_STATIONS_SCENARIO"].iterrows():
        if "H" in index:
            if (
                row["Number of fast chargers"] != 0
                or row["Number of regular chargers"] != 0
            ):

                charging_stations_hospitals[f"{index[:-1]}"] = [
                    (
                        sp.Resource(
                            env, capacity=row["Number of fast chargers"]
                        )
                        if row["Number of fast chargers"] != 0
                        else np.nan
                    ),
                    row["Speed fast chargers (kW)"],
                    (
                        sp.Resource(
                            env, capacity=row["Number of regular chargers"]
                        )
                        if row["Number of regular chargers"] != 0
                        else np.nan
                    ),
                    row["Speed regular chargers (kW)"],
                ]
        elif "B" in index:
            charging_stations_bases[f"{index[:-1]}"] = [
                (
                    sp.Resource(env, capacity=row["Number of fast chargers"])
                    if row["Number of fast chargers"] != 0
                    else np.nan
                ),
                row["Speed fast chargers (kW)"],
                (
                    sp.Resource(
                        env, capacity=row["Number of regular chargers"]
                    )
                    if row["Number of regular chargers"] != 0
                    else np.nan
                ),
                row["Speed regular chargers (kW)"],
            ]
        else:
            raise Exception(
                f"Index {index} lacks the location type "
                "('H' or 'B'). Exit code."
            )

    return {
        "charging_stations_hospitals": charging_stations_hospitals,
        "charging_stations_bases": charging_stations_bases,
    }


def ambulance_initialization(
    env: sp.core.Environment,
    SIMULATION_PARAMETERS: dict[str, Any],
    SIMULATION_DATA: dict[str, Any],
) -> list[Ambulance]:
    """
    Initializes the ambulances and saves these in a list.

    Parameters
    ----------
    env : sp.core.Environment
        The SimPy environment.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``ENGINE_TYPE``,
        ``BATTERY_CAPACITY`` and ``NUM_AMBULANCES`` are at least necessary.
        See ``main.py`` for parameter explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``AMBULANCE_BASE_LOCATIONS`` is at least necessary.
        It is based on ``AMBULANCE_BASE_LOCATIONS_FILE``. See ``main.py`` and
        the input data section on the ELASPY website for explanations.

    Returns
    -------
    list[Ambulance]
        A list of initialized ambulances.

    """

    return [
        Ambulance(
            env,
            int(SIMULATION_DATA["AMBULANCE_BASE_LOCATIONS"].loc[i]),
            SIMULATION_PARAMETERS["ENGINE_TYPE"],
            i,
            SIMULATION_PARAMETERS["BATTERY_CAPACITY"],
        )
        for i in range(SIMULATION_PARAMETERS["NUM_AMBULANCES"])
    ]


def patient_generator(
    env: sp.core.Environment,
    ambulances: list[Ambulance],
    charging_stations: dict[
        str, dict[str, list[sp.resources.resource.Resource | float]]
    ],
    location_IDs: np.ndarray,
    simulation_times: dict[str, np.ndarray],
    to_hospital_bool: np.ndarray,
    patient_queue: deque,
    SIMULATION_PARAMETERS: dict[str, Any],
    SIMULATION_DATA: dict[str, Any],
):
    """
    Generates new patients and starts their aid process.

    The patients are generated according to their interarrival times.
    If the patient can be helped immediately by an ambulance, the patient is
    assigned to an ambulance and the aid process starts. If this is not
    possible, then the patient waits in the patient queue until it can be
    helped.

    Parameters
    ----------
    env : sp.core.Environment
        The SimPy environment.
    ambulances : list[Ambulance]
        A list of initialized ambulances.
    charging_stations : dict[str, dict[str, list[sp.resources.resource.Resource | float]]]
        The charging stations resources at all bases and all hospitals together
        with their charging speeds.
    location_IDs : np.ndarray
        Contains the initial location IDs of the patients.
    simulation_times : dict[str, np.ndarray]
        Contains the interarrival times, the on-site aid times and the drop-off
        times.
    to_hospital_bool : np.ndarray
        Specifies for each patient whether transportation to the hospital is
        required or not.
    patient_queue : collections.deque
        The patient queue.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``NUM_CALLS`` and ``PRINT``
        are at least necessary. Note that methods that are called within this
        method may require more parameters. See ``main.py`` for parameter
        explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``TIME_LAST_ARRIVAL`` (float) is at least
        necessary. It is the time of the last patient arrival. At the start of
        this method, this should be ``np.inf``, since it is set in this method.
        Note that methods that are called within this method may require more
        data.

    """
    for i in range(SIMULATION_PARAMETERS["NUM_CALLS"]):
        yield env.timeout(simulation_times["interarrival"][i])

        patient_ID = i
        patient_location_ID = location_IDs[i]

        hospital_location_ID, new_patient = patient_arrival(
            env,
            patient_ID,
            patient_location_ID,
            patient_queue,
            SIMULATION_PARAMETERS,
            SIMULATION_DATA,
        )

        PATIENT_ASSIGNED, ambulance_ID = check_select_ambulance(
            env,
            ambulances,
            new_patient,
            charging_stations["charging_stations_hospitals"],
            SIMULATION_PARAMETERS,
            SIMULATION_DATA,
        )

        if PATIENT_ASSIGNED:
            if SIMULATION_PARAMETERS["PRINT"]:
                print(
                    f"Remove patient {patient_ID} from the deque "
                    f"{patient_queue}."
                )
            patient_queue.remove(new_patient)
            # set_assigned_to_patient necessary for correctly working
            # while and for-loops help_waiting_patients().
            ambulances[ambulance_ID].set_assigned_to_patient()
            if SIMULATION_PARAMETERS["PRINT"]:
                print(f"After removal the deque is {patient_queue}.")
            env.process(
                ambulance_aid_process(
                    env,
                    new_patient,
                    ambulances[ambulance_ID],
                    patient_queue,
                    charging_stations,
                    simulation_times,
                    to_hospital_bool,
                    SIMULATION_PARAMETERS,
                    SIMULATION_DATA,
                )
            )
        else:
            if SIMULATION_PARAMETERS["PRINT"]:
                print(
                    f"Patient {new_patient.patient_ID} cannot be helped by an "
                    f"ambulance. The deque is {patient_queue}."
                )

    SIMULATION_DATA["TIME_LAST_ARRIVAL"] = env.now
    if SIMULATION_PARAMETERS["PRINT"]:
        print(
            "All patients have arrived at time "
            f"{SIMULATION_DATA['TIME_LAST_ARRIVAL']}."
        )


def location_generator(
    rng: rnd._generator.Generator | rnd.mtrand.RandomState,
    SIMULATION_PARAMETERS: dict[str, Any],
    SIMULATION_DATA: dict[str, Any],
) -> np.ndarray:
    """
    Generates the patient arrival locations.

    The patient's locations are generated according to the inhabitant's
    proportion at each node.

    Parameters
    ----------
    rng : rnd._generator.Generator | rnd.mtrand.RandomState
        An initialized random number generator.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``NUM_CALLS`` and ``PRINT``
        are at least necessary. See ``main.py`` for parameter explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``NODES_REGION`` is at least necessary. It is
        based on ``NODES_FILE``. See ``main.py`` and the input data section on
        the ELASPY website for explanations.

    Returns
    -------
    location_IDs : np.ndarray
        Contains the initial location IDs of the patients.

    """

    location_uniforms = rng.uniform(
        0, 1, size=SIMULATION_PARAMETERS["NUM_CALLS"]
    )
    location_IDs = np.zeros(SIMULATION_PARAMETERS["NUM_CALLS"], dtype=int)

    for i in range(SIMULATION_PARAMETERS["NUM_CALLS"]):
        location_ID = SIMULATION_DATA["NODES_REGION"][
            SIMULATION_DATA["NODES_REGION"]["inhabitantsIncreasing"]
            > location_uniforms[i]
        ].index[0]
        location_IDs[i] = location_ID
        if SIMULATION_PARAMETERS["PRINT"]:
            print(
                f"The probability is {location_uniforms[i]} and thus "
                f"the location is {location_ID}."
            )

    return location_IDs


def patient_arrival(
    env: sp.core.Environment,
    patient_ID: int,
    patient_location_ID: int,
    patient_queue: deque,
    SIMULATION_PARAMETERS: dict[str, Any],
    SIMULATION_DATA: dict[str, Any],
) -> tuple[int, Patient]:
    """
    Processes a patient arrival.

    The patient is assigned to a hospital (in case the patient needs to be
    transported), a new Patient object is created and the Patient is appended
    to the patient_queue.

    Parameters
    ----------
    env : sp.core.Environment
        The SimPy environment.
    patient_ID : int
        The patient ID.
    patient_location_ID : int
        The arrival location of the patient.
    patient_queue : deque
        The patient queue.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameter ``PRINT`` is at least
        necessary. Note that methods that are called within this method may
        require more parameters. See ``main.py`` for parameter explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``output_patient`` is at least necessary. See
        ``main.py`` and the input data section on the ELASPY website for
        explanations. Note that methods that are called within this method may
        require more data.

    Returns
    -------
    hospital_location_ID : int
        The assigned hospital location ID.
    new_patient : Patient
        The new Patient object.

    """

    if SIMULATION_PARAMETERS["PRINT"]:
        print(f"{env.now}: Call for patient {patient_ID}.")
    arrival_time_patient = env.now

    SIMULATION_DATA["output_patient"][patient_ID, 0] = patient_ID
    SIMULATION_DATA["output_patient"][patient_ID, 2] = arrival_time_patient
    SIMULATION_DATA["output_patient"][patient_ID, 3] = patient_location_ID

    hospital_location_ID = select_hospital(
        patient_location_ID, SIMULATION_PARAMETERS, SIMULATION_DATA
    )

    new_patient = Patient(
        patient_ID,
        arrival_time_patient,
        patient_location_ID,
        hospital_location_ID,
    )

    patient_queue.append(new_patient)
    if SIMULATION_PARAMETERS["PRINT"]:
        print(
            f"In patient_arrival, patient {new_patient.patient_ID} is"
            f" added to the deque. The deque is {patient_queue}."
        )

    return hospital_location_ID, new_patient


def help_waiting_patients(
    env: sp.core.Environment,
    ambulances: list[Ambulance],
    charging_stations: dict[
        str, dict[str, list[sp.resources.resource.Resource | float]]
    ],
    simulation_times: dict[str, np.ndarray],
    to_hospital_bool: np.ndarray,
    patient_queue: deque,
    SIMULATION_PARAMETERS: dict[str, Any],
    SIMULATION_DATA: dict[str, Any],
):
    """
    Checks in time intervals whether there are waiting patients that can be
    helped by ambulances.

    Parameters
    ----------
    env : sp.core.Environment
        The SimPy environment.
    ambulances : list[Ambulance]
        A list of ambulances.
    charging_stations : dict[str, dict[str, list[sp.resources.resource.Resource | float]]]
        The charging stations resources at all bases and all hospitals together
        with their charging speeds.
    simulation_times : dict[str, np.ndarray]
        Contains the interarrival times, the on-site aid times and the drop-off
        times.
    to_hospital_bool : np.ndarray
        Specifies for each patient whether transportation to the hospital is
        required or not.
    patient_queue : deque
        The patient queue.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``TIME_AFTER_LAST_ARRIVAL``,
        ``PRINT`` and ``INTERVAL_CHECK_WP`` are at least necessary. Note that
        methods that are called within this method may require more parameters.
        See ``main.py`` for parameter explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``TIME_LAST_ARRIVAL`` is at least necessary. It
        represents the arrival time of the last patient.

    """

    while env.now < (
        SIMULATION_DATA["TIME_LAST_ARRIVAL"]
        + SIMULATION_PARAMETERS["TIME_AFTER_LAST_ARRIVAL"]
    ):
        if SIMULATION_PARAMETERS["PRINT"]:
            print(f"\n{env.now}: check for waiting patients.")
        while len(patient_queue) > 0:
            wp_counter = 0
            if SIMULATION_PARAMETERS["PRINT"]:
                print(
                    "There are waiting patients. "
                    f"The waiting patient queue is {patient_queue}."
                )
            for w_patient in patient_queue:
                wp_counter += 1
                if SIMULATION_PARAMETERS["PRINT"]:
                    print(f"Patient {w_patient.patient_ID} is in the queue.")
                PATIENT_ASSIGNED, ambulance_ID = check_select_ambulance(
                    env,
                    ambulances,
                    w_patient,
                    charging_stations["charging_stations_hospitals"],
                    SIMULATION_PARAMETERS,
                    SIMULATION_DATA,
                )
                if PATIENT_ASSIGNED:
                    if SIMULATION_PARAMETERS["PRINT"]:
                        print(
                            f"Remove w_patient {w_patient.patient_ID} "
                            f"from the deque {patient_queue}."
                        )
                    patient_queue.remove(w_patient)
                    # set_assigned_to_patient necessary for correctly working
                    # while and for-loops help_waiting_patients().
                    ambulances[ambulance_ID].set_assigned_to_patient()
                    if SIMULATION_PARAMETERS["PRINT"]:
                        print(
                            f"Ambulance {ambulance_ID} is assigned to "
                            f"patient {w_patient.patient_ID}."
                        )
                        print(f"After removal the deque is {patient_queue}.")
                    env.process(
                        ambulance_aid_process(
                            env,
                            w_patient,
                            ambulances[ambulance_ID],
                            patient_queue,
                            charging_stations,
                            simulation_times,
                            to_hospital_bool,
                            SIMULATION_PARAMETERS,
                            SIMULATION_DATA,
                        )
                    )
                    wp_counter = 0
                    break
                else:
                    if SIMULATION_PARAMETERS["PRINT"]:
                        print(
                            f"Patient {w_patient.patient_ID} cannot be "
                            "helped by an ambulance. The deque is "
                            f"{patient_queue}."
                        )

            if wp_counter == len(patient_queue):
                if SIMULATION_PARAMETERS["PRINT"]:
                    print(
                        "Currently, no waiting patients can be "
                        "helped by the ambulances."
                    )
                break

        yield env.timeout(SIMULATION_PARAMETERS["INTERVAL_CHECK_WP"])


def ambulance_aid_process(
    env: sp.core.Environment,
    assigned_patient: Patient,
    ambulance: Ambulance,
    patient_queue: deque,
    charging_stations: dict[
        str, dict[str, list[sp.resources.resource.Resource | float]]
    ],
    simulation_times: dict[str, np.ndarray],
    to_hospital_bool: np.ndarray,
    SIMULATION_PARAMETERS: dict[str, Any],
    SIMULATION_DATA: dict[str, Any],
):
    """
    The ambulance aid process.

    A patient is helped by the ambulance, after which the ambulance checks
    whether there are waiting patients that it can help. This repeats until
    it cannot help any patients in the waiting line. Then, the ambulance drive
    process is started.

    Parameters
    ----------
    env : sp.core.Environment
        The SimPy environment.
    assigned_patient : Patient
        The patient (object) that was assigned to the ambulance.
    ambulance : Ambulance
        The ambulance object.
    patient_queue : deque
        The patient queue.
    charging_stations : dict[str, dict[str, list[sp.resources.resource.Resource | float]]]
        The charging stations resources at all bases and all hospitals together
        with their charging speeds.
    simulation_times : dict[str, np.ndarray]
        Contains the interarrival times, the on-site aid times and the drop-off
        times.
    to_hospital_bool : np.ndarray
        Specifies for each patient whether transportation to the hospital is
        required or not.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameter ``PRINT`` is at least
        necessary. Note that methods that are called within this method may
        require more parameters. See ``main.py`` for parameter explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. Methods that are called within this method require
        data. See these methods for explanations.

    """

    yield env.process(
        ambulance.process_patient(
            assigned_patient.patient_ID,
            assigned_patient.patient_location_ID,
            assigned_patient.hospital_location_ID,
            simulation_times,
            charging_stations["charging_stations_hospitals"],
            to_hospital_bool,
            SIMULATION_PARAMETERS,
            SIMULATION_DATA,
        )
    )

    while len(patient_queue) > 0:
        if SIMULATION_PARAMETERS["PRINT"]:
            print(f"w_patient loop for ambulance {ambulance.ambulance_ID}.")
            print(
                "There are waiting patients in the queue. "
                f"The patient queue is {patient_queue}."
            )
            print(f"The queue length is {len(patient_queue)}.")
        wp_counter = 0
        for w_patient in patient_queue:
            wp_counter += 1
            # Loop through patients in FCFS manner and check whether ambu is assignable.
            if SIMULATION_PARAMETERS["PRINT"]:
                print(f"Patient {w_patient.patient_ID} is in the queue.")
            if ambulance.check_patient_reachable(
                ambulance.current_location_ID,
                w_patient.patient_location_ID,
                w_patient.hospital_location_ID,
                charging_stations["charging_stations_hospitals"],
                SIMULATION_PARAMETERS,
                SIMULATION_DATA,
            ):

                if SIMULATION_PARAMETERS["PRINT"]:
                    print(
                        f"Patient {w_patient.patient_ID} is assignable to "
                        f"Ambulance {ambulance.ambulance_ID}."
                    )
                    print(
                        f"Remove patient {w_patient.patient_ID} "
                        f"from the deque {patient_queue}."
                    )
                patient_queue.remove(w_patient)
                # set_assigned_to_patient necessary for correctly working
                # while and for-loops help_waiting_patients().
                ambulance.set_assigned_to_patient()
                if SIMULATION_PARAMETERS["PRINT"]:
                    print(f"After removal the deque is {patient_queue}.")
                yield env.process(
                    ambulance.process_patient(
                        w_patient.patient_ID,
                        w_patient.patient_location_ID,
                        w_patient.hospital_location_ID,
                        simulation_times,
                        charging_stations["charging_stations_hospitals"],
                        to_hospital_bool,
                        SIMULATION_PARAMETERS,
                        SIMULATION_DATA,
                    )
                )
                if SIMULATION_PARAMETERS["PRINT"]:
                    print(
                        f"Ambulance {ambulance.ambulance_ID} has finished "
                        f"treating patient {w_patient.patient_ID}."
                    )
                wp_counter = 0
                break

        if SIMULATION_PARAMETERS["PRINT"]:
            print(
                f"The wp_counter is {wp_counter} and "
                f"the queue length is {len(patient_queue)}."
            )
        if wp_counter == len(patient_queue):
            if SIMULATION_PARAMETERS["PRINT"]:
                print(
                    f"Ambulance {ambulance.ambulance_ID} cannot "
                    "help any patient."
                )
            break

    yield env.process(
        ambulance_drive_process(
            env,
            ambulance,
            charging_stations,
            SIMULATION_PARAMETERS,
            SIMULATION_DATA,
        )
    )


def ambulance_drive_process(
    env: sp.core.Environment,
    ambulance: Ambulance,
    charging_stations: dict[
        str, dict[str, list[sp.resources.resource.Resource | float]]
    ],
    SIMULATION_PARAMETERS: dict[str, Any],
    SIMULATION_DATA: dict[str, Any],
):
    """
    The ambulance drive process to its base.

    If the ambulance is a diesel vehicle, the ambulance immediately drives to
    its base. If the ambulance is an electric vehicle, it is first checked
    whether the ambulance can reach its base without charging. If not, the
    ambulance first charges at the hospital. Otherwise, it droves to
    its base. Once arrived, it starts charging. Note that charging and driving
    to the base are interruptible.

    Parameters
    ----------
    env : sp.core.Environment
        The SimPy environment.
    ambulance : Ambulance
        The ambulance object.
    charging_stations : dict[str, dict[str, list[sp.resources.resource.Resource | float]]]
        The charging stations resources at all bases and all hospitals together
        with their charging speeds.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``ENGINE_TYPE`` and ``PRINT``
        are at least necessary. Note that methods that are called within this
        method may require more parameters. See ``main.py`` for parameter
        explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``NODES_HOSPITAL`` is at least necessary. It is
        based on ``HOSPITAL_FILE``. See ``main.py`` and the input data section
        on the ELASPY website for explanations. Note that methods that are
        called within this method may require more data.

    Raises
    ------
    Exception
        1. If the base is not reachable, but the ambulance is not at the hospital.
        2. If the base is not reachable, but there are no chargers at the hospital.
        3. If charging at the hospital is interrupted, since this cannot
            happen with the implemented check_patient_reachable() method.

    """

    if SIMULATION_PARAMETERS["ENGINE_TYPE"] == "diesel":
        yield env.process(
            ambulance.go_to_base_station(
                SIMULATION_PARAMETERS, SIMULATION_DATA
            )
        )
    else:  # Ambulance is electric.
        # Check whether ambulance can go to its base. If not, first charge at the hospital.
        if not ambulance.check_base_reachable(
            SIMULATION_PARAMETERS, SIMULATION_DATA
        ):
            if (
                ambulance.current_location_ID
                not in SIMULATION_DATA["NODES_HOSPITAL"].Hospital.values
            ):
                raise Exception(
                    "The ambulance base is not reachable, but the "
                    "ambulance is not at the hospital. Error."
                )

            if (
                str(ambulance.current_location_ID)
                in charging_stations["charging_stations_hospitals"].keys()
            ):
                charging_hospital_interrupted = yield env.process(
                    ambulance.charge_at_hospital(
                        ambulance.current_location_ID,
                        charging_stations["charging_stations_hospitals"],
                        SIMULATION_PARAMETERS,
                        SIMULATION_DATA,
                    )
                )
            else:
                raise Exception(
                    f"At hospital {ambulance.current_location_ID}, "
                    "there are no chargers."
                    "However, the ambulance cannot reach its base. Error."
                )
        else:
            charging_hospital_interrupted = False

        if not charging_hospital_interrupted:
            driving_interrupted = yield env.process(
                ambulance.go_to_base_station(
                    SIMULATION_PARAMETERS, SIMULATION_DATA
                )
            )
            if not driving_interrupted:
                if SIMULATION_PARAMETERS["PRINT"]:
                    print(
                        f"For ambulance {ambulance.ambulance_ID}, "
                        "driving_to_base was processed without an interrupt."
                    )

                yield env.process(
                    ambulance.charge_at_base(
                        charging_stations["charging_stations_bases"],
                        SIMULATION_PARAMETERS,
                        SIMULATION_DATA,
                    )
                )
        else:
            raise Exception(
                "Charging at hospital is interrupted. "
                "With the current check_patient_reachable() "
                "method, this cannot be happening."
            )


def check_select_ambulance(
    env: sp.core.Environment,
    ambulances: list[Ambulance],
    patient: Patient,
    charging_stations_hospitals: dict[
        str, list[sp.resources.resource.Resource | float]
    ],
    SIMULATION_PARAMETERS: dict[str, Any],
    SIMULATION_DATA: dict[str, Any],
) -> tuple[bool, int]:
    """
    Checks whether ambulances are available. If so, an ambulance is selected.

    The closest ambulance that can be assigned is selected. In case of a tie,
    the ambulance with the lowest ID number is selected.

    Parameters
    ----------
    env : sp.core.Environment
        The SimPy environment.
    ambulances : list[Ambulance]
        A list of ambulances.
    patient : Patient
        The patient object.
    charging_stations_hospitals : dict[str, list[sp.resources.resource.Resource | float]]
        The charging stations resources at all hospitals together with their
        charging speeds.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameter ``PRINT`` is at least
        necessary. Note that methods that are called within this method may
        require more parameters. See ``main.py`` for parameter explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``output_patient`` and ``SIREN_DRIVING_MATRIX``
        are at least necessary. ``SIREN_DRIVING_MATRIX`` is based on
        ``TRAVEL_TIMES_FILE``. See ``main.py`` and the input data section on
        the ELASPY website for explanations. Note that methods that are called
        within this method may require more data.

    Raises
    ------
    Exception
        If the ambulance drives to base but its resource is not used.

    Returns
    -------
    PATIENT_ASSIGNED: bool
        Indicates whether the patient was assigned to an ambulance or not.
    ambulance_ID : int
        The ambulance ID of the assigned ambulance. It is -1 if no ambulance
        was assigned.

    """

    nr_ambulances_available = 0
    assignable_ambulances = []
    assignable_locations = []
    nr_ambulances_not_assignable = 0

    for j in range(len(ambulances)):
        if not (
            ambulances[j].helps_patient or ambulances[j].assigned_to_patient
        ):
            nr_ambulances_available += 1
            if ambulances[j].drives_to_base:
                if SIMULATION_PARAMETERS["PRINT"]:
                    print(
                        "Driving since: "
                        f"{ambulances[j].resource.users[0].usage_since}."
                    )

                if ambulances[j].resource.users[0].usage_since is None:
                    raise Exception(
                        "The ambulance is not being used. This is incorrect."
                    )

                driven_time = env.now - ambulances[j].resource.users[0].usage_since  # type: ignore
                (new_x, new_y) = calculate_new_coordinate(
                    driven_time,
                    ambulances[j].current_location_ID,
                    ambulances[j].base_location_ID,
                    True,
                    SIMULATION_PARAMETERS,
                    SIMULATION_DATA,
                )
                ambulance_location_ID = select_closest_location_ID(
                    (new_x, new_y), SIMULATION_PARAMETERS, SIMULATION_DATA
                )
            else:
                ambulance_location_ID = ambulances[j].current_location_ID

            if ambulances[j].check_patient_reachable(
                ambulance_location_ID,
                patient.patient_location_ID,
                patient.hospital_location_ID,
                charging_stations_hospitals,
                SIMULATION_PARAMETERS,
                SIMULATION_DATA,
            ):
                assignable_ambulances.append(j)
                assignable_locations.append(ambulance_location_ID)
            else:
                nr_ambulances_not_assignable += 1

    if SIMULATION_PARAMETERS["PRINT"]:
        print(f"The nr_ambulances_available is {nr_ambulances_available}.")
        print(
            f"The assignable ambulances are: {assignable_ambulances} "
            f"and the assignable locations are: {assignable_locations}."
        )
        print(
            "The nr of ambulances not assignable are: "
            f"{nr_ambulances_not_assignable}."
        )

    if len(assignable_ambulances) == 0:
        PATIENT_ASSIGNED = False
        ambulance_ID = -1
        if SIMULATION_PARAMETERS["PRINT"]:
            print(
                f"There are no ambulances that can help patient "
                f"{patient.patient_ID}. The patient remains in the queue."
            )
    else:
        SIMULATION_DATA["output_patient"][
            patient.patient_ID, 4
        ] = nr_ambulances_available
        SIMULATION_DATA["output_patient"][
            patient.patient_ID, 5
        ] = nr_ambulances_not_assignable
        PATIENT_ASSIGNED = True
        postal_code_shortest_time = (
            SIMULATION_DATA["SIREN_DRIVING_MATRIX"]
            .loc[assignable_locations, patient.patient_location_ID]
            .idxmin()
        )
        ambulance_ID = assignable_ambulances[
            assignable_locations.index(postal_code_shortest_time)
        ]

        if SIMULATION_PARAMETERS["PRINT"]:
            print(
                "The times from all assignable ambulances to the patient are: "
            )
            print(
                SIMULATION_DATA["SIREN_DRIVING_MATRIX"].loc[
                    assignable_locations, patient.patient_location_ID
                ]
            )
            print(
                "The postal code with the shortest time is: "
                f"{postal_code_shortest_time}."
            )
            print(
                "The corresponding ambulance is (first in order): "
                f"{ambulance_ID}."
            )

    return PATIENT_ASSIGNED, ambulance_ID


def select_hospital(
    source_location_ID: int,
    SIMULATION_PARAMETERS: dict[str, Any],
    SIMULATION_DATA: dict[str, Any],
) -> int:
    """
    Selects the closest hospital based on a source location.

    The closest hospital is based on the driving time with sirens on.

    Parameters
    ----------
    source_location_ID : int
        The location ID of the source.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameter ``PRINT`` is at least
        necessary. See ``main.py`` for parameter explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``SIREN_DRIVING_MATRIX`` and ``NODES_HOSPITAL``
        are at least necessary. ``SIREN_DRIVING_MATRIX`` is based on
        ``TRAVEL_TIMES_FILE``. ``NODES_HOSPITAL`` is based on ``HOSPITAL_FILE``.
        See ``main.py`` and the input data section on the ELASPY website for
        explanations.

    Returns
    -------
    int
        The selected hospital ID.

    """

    if SIMULATION_PARAMETERS["PRINT"]:
        print(f"The source location is {source_location_ID}.")

        print("The time from the source location to all hospitals is: ")
        print(
            SIMULATION_DATA["SIREN_DRIVING_MATRIX"].loc[
                source_location_ID, SIMULATION_DATA["NODES_HOSPITAL"].Hospital
            ]
        )

    return (
        SIMULATION_DATA["SIREN_DRIVING_MATRIX"]
        .loc[source_location_ID, SIMULATION_DATA["NODES_HOSPITAL"].Hospital]
        .idxmin()
    )
