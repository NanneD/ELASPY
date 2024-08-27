#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any

import numpy as np


def calculate_new_coordinate(
    driven_time: float,
    source_location_ID: int,
    target_location_ID: int,
    siren_off: bool,
    SIMULATION_PARAMETERS: dict[str, Any],
    SIMULATION_DATA: dict[str, Any],
) -> tuple[float, float]:

    """
    Calculates the coordinate of a driving ambulance.

    The fraction of driven time compared to the total driving time is used for
    determining the new coordinate.

    Parameters
    ----------
    driven_time : float
        The time that the ambulance has been driving until now.
    source_location_ID : int
        The ID of the source location.
    target_location_ID : int
        The ID of the target location.
    siren_off : bool
        Whether the ambulance is driving without or with sirens on.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``NO_SIREN_PENALTY`` and
        ``PRINT`` are at least necessary. See ``main.py`` for parameter
        explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``SIREN_DRIVING_MATRIX`` and ``NODES_REGION`` are
        at least necessary. See ``main.py`` and the input data section on the
        ELASPY website for explanations.

    Returns
    -------
    tuple[float, float]
        A tuple with the new x and y coordinate.

    """

    if siren_off:
        total_driving_time = (
            SIMULATION_DATA["SIREN_DRIVING_MATRIX"].loc[
                source_location_ID, target_location_ID
            ]
            / SIMULATION_PARAMETERS["NO_SIREN_PENALTY"]
        )
    else:
        total_driving_time = SIMULATION_DATA["SIREN_DRIVING_MATRIX"].loc[
            source_location_ID, target_location_ID
        ]

    fraction_driven = driven_time / total_driving_time

    source_coordinate = (
        SIMULATION_DATA["NODES_REGION"].loc[source_location_ID, "x"],
        SIMULATION_DATA["NODES_REGION"].loc[source_location_ID, "y"],
    )
    target_coordinate = (
        SIMULATION_DATA["NODES_REGION"].loc[target_location_ID, "x"],
        SIMULATION_DATA["NODES_REGION"].loc[target_location_ID, "y"],
    )

    new_x_coordinate = (1 - fraction_driven) * source_coordinate[
        0
    ] + fraction_driven * target_coordinate[0]
    new_y_coordinate = (1 - fraction_driven) * source_coordinate[
        1
    ] + fraction_driven * target_coordinate[1]

    if SIMULATION_PARAMETERS["PRINT"]:
        print(f"The source was: {source_coordinate}")
        print(f"The target was: {target_coordinate}")
        print(f"The new coordinate is {new_x_coordinate, new_y_coordinate}")

    return (new_x_coordinate, new_y_coordinate)


def select_closest_location_ID(
    coordinate: tuple[float, float],
    SIMULATION_PARAMETERS: dict[str, Any],
    SIMULATION_DATA: dict[str, Any],
) -> int:

    """
    Given a coordinate, the closest location ID is returned.

    The Euclidian distance is used.

    Parameters
    ----------
    coordinate : tuple[float, float]
        A tuple containing the x and y coordinates.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameter ``PRINT`` is at least
        necessary. See ``main.py`` for parameter explanations.
    SIMULATION_DATA : dict[str, Any]
        The simulation data. ``NODES_REGION`` is at least necessary. See
        ``main.py`` and the input data section on the ELASPY website for
        explanations.

    Returns
    -------
    location_ID: int
        The closest location ID.

    """

    distances = np.sqrt(
        np.power(SIMULATION_DATA["NODES_REGION"]["x"] - coordinate[0], 2)
        + np.power(SIMULATION_DATA["NODES_REGION"]["y"] - coordinate[1], 2)
    )

    location_ID = distances.idxmin()
    if SIMULATION_PARAMETERS["PRINT"]:
        print(f"The closest location to the coordinate is: {location_ID}")
    return location_ID
