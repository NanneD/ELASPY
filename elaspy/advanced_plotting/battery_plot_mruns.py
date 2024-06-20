#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script makes a plot of the state of charge (SoC) of all ambulances for
multiple runs.

Parameters
----------
DATA_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the input data is located.
RESULTS_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the output files should be saved.
DF_AMBULANCE_FILE : str
    The name of the file that contains the ambulance dataframe. Note that the
    run number is automatically added by the script in a for-loop.
PLOT_NAME : str
    The name of the plot if it is saved.
RUN_PARAMETERS_FILE_NAME : str
    The name of the text file with the script parameters if ``SAVE_PLOT=True``.
NUM_RUNS : int
    The number of runs that should be plotted.
NUM_AMBULANCES : int
    The number of ambulances.
BATTERY_CAPACITY : int
    The maximum battery capacity of the ambulances in kWh.
NUM_COLS : int
    The numner of columns the plot should have.
SAVE_PLOT : bool
    Whether the plot should be saved or not.
COLOUR_RUNS : list[str]
    The colours of the simulation runs. The first run is coloured according to
    the first colour, the second run according to the second colour, etc.
XLIM : int
    The limit of the x-axis.
"""

import os
import math
import pandas as pd
import matplotlib.pyplot as plt

################################Directories####################################
ROOT_DIRECTORY: str = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))
)

DATA_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "results/")
RESULTS_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "results/")
#################################File names####################################
DF_AMBULANCE_FILE: str = "Ambulance_df_run_"
PLOT_NAME: str = "battery_plot_mruns"
RUN_PARAMETERS_FILE_NAME: str = f"run_parameters_{PLOT_NAME}"
##################################Parameters###################################
NUM_RUNS: int = 5
NUM_AMBULANCES: int = 20
BATTERY_CAPACITY: float = 150
NUM_COLS: int = 5  # Number of columns of the plot
SAVE_PLOT: bool = False
COLOUR_RUNS: list[str] = [
    "tab:red",
    "tab:blue",
    "tab:green",
    "tab:purple",
    "tab:orange",
]
XLIM: int = 720
################################Save parameters################################
if __name__ == "__main__":
    if SAVE_PLOT:
        with open(
            f"{RESULTS_DIRECTORY}{RUN_PARAMETERS_FILE_NAME}.txt",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(f"DATA_DIRECTORY: {DATA_DIRECTORY}\n")
            f.write(f"RESULTS_DIRECTORY: {RESULTS_DIRECTORY}\n")
            f.write(f"DF_AMBULANCE_FILE: {DF_AMBULANCE_FILE}\n")
            f.write(f"PLOT_NAME: {PLOT_NAME}\n")
            f.write(f"RUN_PARAMETERS_FILE_NAME: {RUN_PARAMETERS_FILE_NAME}\n")
            f.write(f"NUM_RUNS: {NUM_RUNS}\n")
            f.write(f"NUM_AMBULANCES: {NUM_AMBULANCES}\n")
            f.write(f"BATTERY_CAPACITY: {BATTERY_CAPACITY}\n")
            f.write(f"NUM_COLS: {NUM_COLS}\n")
            f.write(f"SAVE_PLOT: {SAVE_PLOT}\n")
            f.write(f"COLOUR_RUNS: {COLOUR_RUNS}\n")
            f.write(f"XLIM: {XLIM}\n")
            f.close()
    ##################################Read data################################
    if len(COLOUR_RUNS) != NUM_RUNS:
        raise Exception(
            "The number of colours does not match the number of runs."
        )

    dfs_ambulances = []

    for i in range(NUM_RUNS):
        dfs_ambulances.append(
            pd.read_csv(
                f"{DATA_DIRECTORY}{DF_AMBULANCE_FILE}{i}.csv", index_col=0
            )
        )
    ##################################Make plot################################
    NUM_ROWS = math.ceil(NUM_AMBULANCES / NUM_COLS)

    fig, axs = plt.subplots(
        NUM_ROWS, NUM_COLS, sharex=True, sharey=True, figsize=(12, 10)
    )

    for j in range(NUM_RUNS):
        hor_count = 0
        vert_count = 0
        for i in range(NUM_AMBULANCES):
            time_data = dfs_ambulances[j].loc[
                dfs_ambulances[j]["ambulance_ID"] == i, "time"
            ]
            battery_data = dfs_ambulances[j].loc[
                dfs_ambulances[j]["ambulance_ID"] == i, "battery_level_after"
            ]
            axs[vert_count, hor_count].plot(
                time_data,
                battery_data,
                label=f"Run {j}",
                color=COLOUR_RUNS[j],
                alpha=0.8,
            )
            axs[vert_count, hor_count].set_title(f"Ambulance {i}", fontsize=12)
            axs[vert_count, hor_count].set_xlim(0, XLIM)
            axs[vert_count, hor_count].set_ylim(0, BATTERY_CAPACITY + 5)
            if hor_count + 1 == NUM_COLS:
                vert_count += 1
                hor_count = 0
            else:
                hor_count += 1

    handles, labels = axs[0, 0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="center right",
        bbox_to_anchor=(1.1, 0.86),
        fontsize=12,
    )
    fig.suptitle("SoC per ambulance for five runs", fontsize=18)
    fig.supxlabel("Time (min)", fontsize=14)
    fig.supylabel("SoC (kWh)", fontsize=14)

    plt.tight_layout()
    if SAVE_PLOT:
        plt.savefig(f"{RESULTS_DIRECTORY}{PLOT_NAME}.pdf", bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()
