#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script makes a scatterplot of four scenarios, where the busy fraction is
plotted on the x-axis and the mean response time on the y-axis.

Parameters
----------
DATA_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the input data is located.
RESULTS_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the output files should be saved.
SCENARIO_NAMES : list[str]
    A list with the scenario names that should be considered.
MEAN_RESPONSE_TIME_FILE_1 : str
    The name of the file that contains the first data set with the mean
    response times. To facilitate running the script with multiple lambda
    values (i.e., arrival rates), note that the files should have a "Li"
    suffix, where "i" stands for the lambda rate "1/i".
MEAN_RESPONSE_TIME_FILE_2 : str
    The name of the file that contains the second data set with the mean
    response times. To facilitate running the script with multiple lambda
    values (i.e., arrival rates), note that the files should have a "Li"
    suffix, where "i" stands for the lambda rate "1/i".
MEAN_RESPONSE_TIME_FILE_3 : str
    The name of the file that contains the third data set with the mean
    response times. To facilitate running the script with multiple lambda
    values (i.e., arrival rates), note that the files should have a "Li"
    suffix, where "i" stands for the lambda rate "1/i".
MEAN_RESPONSE_TIME_FILE_4 : str
    The name of the file that contains the fourth data set with the mean
    response times. To facilitate running the script with multiple lambda
    values (i.e., arrival rates), note that the files should have a "Li"
    suffix, where "i" stands for the lambda rate "1/i".
BUSY_FRACTION_FILE_1 : str
    The name of the file that contains the first data set with the busy
    fractions. To facilitate running the script with multiple lambda
    values (i.e., arrival rates), note that the files should have a "Li"
    suffix, where "i" stands for the lambda rate "1/i".
BUSY_FRACTION_FILE_2 : str
    The name of the file that contains the second data set with the busy
    fractions. To facilitate running the script with multiple lambda
    values (i.e., arrival rates), note that the files should have a "Li"
    suffix, where "i" stands for the lambda rate "1/i".
BUSY_FRACTION_FILE_3 : str
    TThe name of the file that contains the third data set with the busy
    fractions. To facilitate running the script with multiple lambda
    values (i.e., arrival rates), note that the files should have a "Li"
    suffix, where "i" stands for the lambda rate "1/i".
BUSY_FRACTION_FILE_4 : str
    The name of the file that contains the fourth data set with the busy
    fractions. To facilitate running the script with multiple lambda
    values (i.e., arrival rates), note that the files should have a "Li"
    suffix, where "i" stands for the lambda rate "1/i".
PLOT_NAME : str
    The name of the plot if it is saved.
RUN_PARAMETERS_FILE_NAME : str
    The name of the text file with the script parameters if ``SAVE_PLOT=True``.
NUM_RUNS : int
    The number of runs that should be plotted.
LAMBDA_SCENARIOS_COUNTER : list[int] | None
    A list with the lambda values without "1/". Thus, if a lambda value of 1/4
    is used, provide "4".
COLOUR_RUNS : list[str]
    The colour of each scenario. The first scenario is coloured according to
    the first colour, the second scenario according to the second colour, etc.
SAVE_PLOT : bool
    Whether the plot should be saved or not.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

################################Directories####################################
ROOT_DIRECTORY: str = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))
)

DATA_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "results/")
RESULTS_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "results/")
#################################File names####################################
SCENARIO_NAMES: list[str] = ["Diesel", "FB1_FH1", "RB1_RH1", "RB1"]
MEAN_RESPONSE_TIME_FILE_1: str = (
    f"mean_response_times_all_runs_{SCENARIO_NAMES[0]}_L"
)
MEAN_RESPONSE_TIME_FILE_2: str = (
    f"mean_response_times_all_runs_{SCENARIO_NAMES[1]}_L"
)
MEAN_RESPONSE_TIME_FILE_3: str = (
    f"mean_response_times_all_runs_{SCENARIO_NAMES[2]}_L"
)
MEAN_RESPONSE_TIME_FILE_4: str = (
    f"mean_response_times_all_runs_{SCENARIO_NAMES[3]}_L"
)

BUSY_FRACTION_FILE_1: str = f"busy_fractions_all_runs_{SCENARIO_NAMES[0]}_L"
BUSY_FRACTION_FILE_2: str = f"busy_fractions_all_runs_{SCENARIO_NAMES[1]}_L"
BUSY_FRACTION_FILE_3: str = f"busy_fractions_all_runs_{SCENARIO_NAMES[2]}_L"
BUSY_FRACTION_FILE_4: str = f"busy_fractions_all_runs_{SCENARIO_NAMES[3]}_L"

PLOT_NAME: str = "scatterplot_rt_bf"
RUN_PARAMETERS_FILE_NAME: str = "run_parameters_scatterplot_rt_bf"
##################################Parameters###################################
# counter for lambda scenarios file names
NUM_RUNS: int = 1000
LAMBDA_SCENARIOS_COUNTER: list[int] = [4, 5, 6]
COLORS_PLOT: list[str] = ["black", "tab:orange", "tab:green", "tab:red"]
SAVE_PLOT: bool = False
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
            f.write(f"SCENARIO_NAMES: {SCENARIO_NAMES}\n")
            f.write(
                f"MEAN_RESPONSE_TIME_FILE_1: {MEAN_RESPONSE_TIME_FILE_1}\n"
            )
            f.write(
                f"MEAN_RESPONSE_TIME_FILE_2: {MEAN_RESPONSE_TIME_FILE_2}\n"
            )
            f.write(
                f"MEAN_RESPONSE_TIME_FILE_3: {MEAN_RESPONSE_TIME_FILE_3}\n"
            )
            f.write(
                f"MEAN_RESPONSE_TIME_FILE_4: {MEAN_RESPONSE_TIME_FILE_4}\n"
            )
            f.write(f"BUSY_FRACTION_FILE_1: {BUSY_FRACTION_FILE_1}\n")
            f.write(f"BUSY_FRACTION_FILE_2: {BUSY_FRACTION_FILE_2}\n")
            f.write(f"BUSY_FRACTION_FILE_3: {BUSY_FRACTION_FILE_3}\n")
            f.write(f"BUSY_FRACTION_FILE_4: {BUSY_FRACTION_FILE_4}\n")
            f.write(f"PLOT_NAME: {PLOT_NAME}\n")
            f.write(f"RUN_PARAMETERS_FILE_NAME: {RUN_PARAMETERS_FILE_NAME}\n")
            f.write(f"NUM_RUNS: {NUM_RUNS}\n")
            f.write(f"LAMBDA_SCENARIOS_COUNTER: {LAMBDA_SCENARIOS_COUNTER}\n")
            f.write(f"COLORS_PLOT: {COLORS_PLOT}\n")
            f.write(f"SAVE_PLOT: {SAVE_PLOT}\n")
            f.close()
    ##################################Read data################################
    dfs_mean_response_times_1 = []
    dfs_busy_fractions_1 = []
    dfs_mean_response_times_2 = []
    dfs_busy_fractions_2 = []
    dfs_mean_response_times_3 = []
    dfs_busy_fractions_3 = []
    dfs_mean_response_times_4 = []
    dfs_busy_fractions_4 = []

    for i in LAMBDA_SCENARIOS_COUNTER:
        dfs_mean_response_times_1.append(
            pd.read_csv(
                f"{DATA_DIRECTORY}{MEAN_RESPONSE_TIME_FILE_1}{i}.csv",
                index_col=0,
            )
        )
        dfs_busy_fractions_1.append(
            pd.read_csv(
                f"{DATA_DIRECTORY}{BUSY_FRACTION_FILE_1}{i}.csv",
                index_col=0,
            )
        )

        dfs_mean_response_times_2.append(
            pd.read_csv(
                f"{DATA_DIRECTORY}{MEAN_RESPONSE_TIME_FILE_2}{i}.csv",
                index_col=0,
            )
        )
        dfs_busy_fractions_2.append(
            pd.read_csv(
                f"{DATA_DIRECTORY}{BUSY_FRACTION_FILE_2}{i}.csv",
                index_col=0,
            )
        )

        dfs_mean_response_times_3.append(
            pd.read_csv(
                f"{DATA_DIRECTORY}{MEAN_RESPONSE_TIME_FILE_3}{i}.csv",
                index_col=0,
            )
        )
        dfs_busy_fractions_3.append(
            pd.read_csv(
                f"{DATA_DIRECTORY}{BUSY_FRACTION_FILE_3}{i}.csv",
                index_col=0,
            )
        )

        dfs_mean_response_times_4.append(
            pd.read_csv(
                f"{DATA_DIRECTORY}{MEAN_RESPONSE_TIME_FILE_4}{i}.csv",
                index_col=0,
            )
        )
        dfs_busy_fractions_4.append(
            pd.read_csv(
                f"{DATA_DIRECTORY}{BUSY_FRACTION_FILE_4}{i}.csv",
                index_col=0,
            )
        )

    flattened_mean_response_times_1 = np.concatenate(
        dfs_mean_response_times_1
    ).flatten()
    flattened_busy_fractions_1 = np.concatenate(dfs_busy_fractions_1).flatten()
    flattened_mean_response_times_2 = np.concatenate(
        dfs_mean_response_times_2
    ).flatten()
    flattened_busy_fractions_2 = np.concatenate(dfs_busy_fractions_2).flatten()
    flattened_mean_response_times_3 = np.concatenate(
        dfs_mean_response_times_3
    ).flatten()
    flattened_busy_fractions_3 = np.concatenate(dfs_busy_fractions_3).flatten()
    flattened_mean_response_times_4 = np.concatenate(
        dfs_mean_response_times_4
    ).flatten()
    flattened_busy_fractions_4 = np.concatenate(dfs_busy_fractions_4).flatten()
    ##################################Make plot################################
    fig, ax = plt.subplots(figsize=(7, 7))

    ax.scatter(
        flattened_busy_fractions_1[:NUM_RUNS],
        flattened_mean_response_times_1[:NUM_RUNS],
        s=65,
        marker="1",
        label=f"{SCENARIO_NAMES[0]}",
        color=COLORS_PLOT[0],
    )
    ax.scatter(
        flattened_busy_fractions_2[:NUM_RUNS],
        flattened_mean_response_times_2[:NUM_RUNS],
        s=65,
        marker="2",
        label=f"{SCENARIO_NAMES[1]}",
        color=COLORS_PLOT[1],
    )
    ax.scatter(
        flattened_busy_fractions_3[:NUM_RUNS],
        flattened_mean_response_times_3[:NUM_RUNS],
        s=65,
        marker="3",
        label=f"{SCENARIO_NAMES[2]}",
        color=COLORS_PLOT[2],
    )
    ax.scatter(
        flattened_busy_fractions_4[:NUM_RUNS],
        flattened_mean_response_times_4[:NUM_RUNS],
        s=65,
        marker="4",
        label=f"{SCENARIO_NAMES[3]}",
        color=COLORS_PLOT[3],
    )

    ax.set_title(
        "Mean response time versus busy fraction four scenarios",
        fontsize=16,
    )
    ax.set_xlabel("Busy fraction", fontsize=14)
    ax.set_ylabel("Mean response time (min)", fontsize=14)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.legend()

    plt.tight_layout()
    if SAVE_PLOT:
        plt.savefig(f"{RESULTS_DIRECTORY}{PLOT_NAME}.pdf")
        plt.close(fig)
    else:
        plt.show()
