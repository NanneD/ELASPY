#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import datetime
import numpy as np
import matplotlib.pyplot as plt

from typing import Any


def plot_response_times(
    df_patient, run_nr: int, SIMULATION_PARAMETERS: dict[str, Any]
) -> None:
    """
    Makes three different plots of the response time data.

    1. A plot of the response time (y-axis) per patient (x-axis). Saved as
       "scatter_response_time_{run_nr}.pdf" if ``SAVE_PLOTS=True``.
    2. A histogram of the response times. Saved as
       "histogram_response_time_{run_nr}.pdf" if ``SAVE_PLOTS=True``.
    3. A bar plot of the waiting time before assigned and driving time per
       patient. Saved as "bar_waiting_driving_time_{run_nr}.pdf" if
       ``SAVE_PLOTS=True``.

    Parameters
    ----------
    df_patient : pandas.DataFrame
        A dataframe with the patient data where each row represents a patient.
        At least columns "response_time", "waiting_time_before_assigned" and
        "driving_time_to_patient" are necessary. See the output data section
        on the ELASPY website for explanations.
    run_nr : int
        The simulation run number.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``SAVE_PLOTS``,
        ``SIMULATION_OUTPUT_DIRECTORY`` and ``NUM_CALLS`` are at least
        necessary. See ``main.py`` for parameter explanations.

    """

    start_time = datetime.datetime.now()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        df_patient["response_time"],
        color="darkblue",
        marker="o",
        ms=5,
        linestyle="none",
    )
    ax.axhline(y=12, color="grey")

    ax.text(1, 12.5, "Response time target", color="grey")
    ax.set_title("Response time per patient", fontsize=14)
    ax.set_xlabel("Patient number", fontsize=12)
    ax.set_ylabel("Response time (min)", fontsize=12)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if SIMULATION_PARAMETERS["SAVE_PLOTS"]:
        plt.savefig(
            f"{SIMULATION_PARAMETERS['SIMULATION_OUTPUT_DIRECTORY']}"
            f"scatter_response_time_{run_nr}.pdf"
        )
        plt.close(fig)
    else:
        plt.show()

    fig = plt.figure(figsize=(10, 5))
    plt.hist(df_patient["response_time"], color="darkblue", bins=20)
    plt.axvline(x=12, color="red", linestyle="--")
    plt.title("Histogram of response times", size=14)
    plt.xlabel("Response time", size=12)
    plt.ylabel("Frequency", size=12)
    if SIMULATION_PARAMETERS["SAVE_PLOTS"]:
        plt.savefig(
            f"{SIMULATION_PARAMETERS['SIMULATION_OUTPUT_DIRECTORY']}"
            f"histogram_response_time_{run_nr}.pdf"
        )
        plt.close(fig)
    else:
        plt.show()

    fig = plt.figure(figsize=(15, 5))
    x = np.arange(SIMULATION_PARAMETERS["NUM_CALLS"])
    b1 = plt.bar(
        x,
        df_patient["waiting_time_before_assigned"],
        width=0.5,
        color="deepskyblue",
    )
    b2 = plt.bar(
        x,
        df_patient["driving_time_to_patient"],
        bottom=df_patient["waiting_time_before_assigned"],
        width=0.5,
        color="darkblue",
    )
    plt.xticks(
        ticks=np.arange(
            start=0, stop=len(df_patient), step=round(len(df_patient) / 10)
        ),
        rotation=90,
    )
    plt.xlabel("Patient nr.", size=12)
    plt.ylabel("Time", size=12)
    plt.title(
        "Response times: distribution of waiting time and driving time",
        size=14,
    )
    plt.legend((b1[0], b2[0]), ("waiting_time", "driving_time"))

    if SIMULATION_PARAMETERS["SAVE_PLOTS"]:
        plt.savefig(
            f"{SIMULATION_PARAMETERS['SIMULATION_OUTPUT_DIRECTORY']}"
            f"bar_waiting_driving_time_{run_nr}.pdf"
        )
        plt.close(fig)
    else:
        plt.show()

    print(
        "The running time for plotting the response time "
        f"figures is: {datetime.datetime.now()-start_time}."
    )


def plot_battery_levels(
    df_ambulance,
    run_nr: int,
    SIMULATION_PARAMETERS: dict[str, Any],
    NUM_COLS: int = 5,
) -> None:
    """
    Plots the battery levels over time of the each ambulance.

    Saved as "battery_levels_ambus_{run_nr}.pdf" if ``SAVE_PLOTS=True``.

    Parameters
    ----------
    df_ambulance : pandas.DataFrame
        A dataframe with the ambulance data where each row represents an
        ambulance event. At least columns "ambulance_ID",
        "battery_level_after" and "time" are necessary. See the output data
        section on the ELASPY website for explanations.
    run_nr : int
        The simulation run number.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``NUM_AMBULANCES``,
        ``SAVE_PLOTS`` and ``SIMULATION_OUTPUT_DIRECTORY`` are at least
        necessary. See ``main.py`` for parameter explanations.
    NUM_COLS : int, optional
        The number of plot columns you want the plot to have. The default is 5.

    """

    start_time = datetime.datetime.now()

    NUM_ROWS = math.ceil(SIMULATION_PARAMETERS["NUM_AMBULANCES"] / NUM_COLS)

    fig, axs = plt.subplots(
        NUM_ROWS, NUM_COLS, sharex=True, sharey=True, figsize=(12, 10)
    )

    hor_count = 0
    vert_count = 0
    for i in range(SIMULATION_PARAMETERS["NUM_AMBULANCES"]):
        time_data = df_ambulance.loc[df_ambulance["ambulance_ID"] == i, "time"]
        battery_data = df_ambulance.loc[
            df_ambulance["ambulance_ID"] == i, "battery_level_after"
        ]
        axs[vert_count, hor_count].plot(
            time_data, battery_data, color="darkblue"
        )
        axs[vert_count, hor_count].set_title(f"Ambulance {i}", fontsize=12)
        if hor_count + 1 == NUM_COLS:
            vert_count += 1
            hor_count = 0
        else:
            hor_count += 1

    fig.suptitle("Battery levels per ambulance", fontsize=14)
    fig.supxlabel("Time", fontsize=14)
    fig.supylabel("Battery levels (kWh)", fontsize=14)

    plt.tight_layout()
    if SIMULATION_PARAMETERS["SAVE_PLOTS"]:
        plt.savefig(
            f"{SIMULATION_PARAMETERS['SIMULATION_OUTPUT_DIRECTORY']}"
            f"battery_levels_ambus_{run_nr}.pdf"
        )
        plt.close(fig)
    else:
        plt.show()

    print(
        "The running time for plotting the battery levels "
        f"figure is: {datetime.datetime.now()-start_time}."
    )


def hist_battery_increase_decrease(
    df_ambulance, run_nr: int, SIMULATION_PARAMETERS: dict[str, Any]
) -> None:
    """
    Makes histograms of the battery decreases and increases.

    The battery decrease histogram is saved as
    "histogram_battery_decrease_{run_nr}.pdf" and the battery increase
    histogram is saved as "histogram_battery_increase_{run_nr}.pdf" if
    ``SAVE_PLOTS=True``.

    Parameters
    ----------
    df_ambulance : pandas.DataFrame
        A dataframe with the ambulance data where each row represents an
        ambulance event. At least columns "battery_decrease" and
        "battery_increase" are necessary. See the output data section on the
        ELASPY website for explanations.
    run_nr : int
        The simulation run number.
    SIMULATION_PARAMETERS : dict[str, Any]
        The simulation parameters. The parameters ``SAVE_PLOTS`` and
        ``SIMULATION_OUTPUT_DIRECTORY`` are at least necessary. See
        ``main.py`` for parameter explanations.

    """
    start_time = datetime.datetime.now()

    fig = plt.figure(figsize=(10, 5))
    plt.hist(df_ambulance["battery_decrease"], bins=10, color="darkblue")
    plt.title("Histogram of the battery decreases")
    plt.xlabel("Battery decrease (kWh)")
    plt.ylabel("Count")
    if SIMULATION_PARAMETERS["SAVE_PLOTS"]:
        plt.savefig(
            f"{SIMULATION_PARAMETERS['SIMULATION_OUTPUT_DIRECTORY']}"
            f"histogram_battery_decrease_{run_nr}.pdf"
        )
        plt.close(fig)
    else:
        plt.show()

    fig = plt.figure(figsize=(10, 5))
    plt.hist(df_ambulance["battery_increase"], bins=10, color="darkblue")
    plt.title("Histogram of the battery increases")
    plt.xlabel("Battery increase (kWh)")
    plt.ylabel("Count")
    if SIMULATION_PARAMETERS["SAVE_PLOTS"]:
        plt.savefig(
            f"{SIMULATION_PARAMETERS['SIMULATION_OUTPUT_DIRECTORY']}"
            f"histogram_battery_increase_{run_nr}.pdf"
        )
        plt.close(fig)
    else:
        plt.show()

    print(
        "The running time for plotting the battery increase/decrease "
        f"figures is: {datetime.datetime.now()-start_time}."
    )
