#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script makes two jitter plots for all scenarios; one for the mean and one
for the 95% empirical quantile of the response times.

Parameters
----------
DATA_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the input data is located.
RESULTS_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the output files should be saved.
SCENARIO : str
    The scenario names that should be considered.
MEAN_RESPONSE_TIME_FILE : str
    The name of the file that contains the data set with the mean
    response times. Note that the files should have a "Ei" suffix, where "i"
    stands for the percentage increase of the energy consumption compared to
    the base. For example, if a 20% increase should be considered, use "20".
    The scenario name is automatically added by the script according
    to the value of ``SCENARIO`` in a for-loop.
EMP_Q_FILE : str
    The name of the file that contains the data set with the 95% empirical
    quantile of the response times. Note that the files should have a "Ei"
    suffix, where "i" stands for the percentage increase of the energy
    consumption compared to the base. For example, if a 20% increase should be
    considered, use "20". The scenario name is automatically added by the
    script according to the value of ``SCENARIO`` in a for-loop.
PLOT_NAME : str
    The name of the plot if it is saved.
RUN_PARAMETERS_FILE_NAME : str
    The name of the text file with the script parameters if ``SAVE_PLOT=True``.
ENERGY_COUNTER : list[int] | None
    A list with the percentage increase of the energy consumption compared to
    the base. For example, if a 20% increase should be considered, use "20".
SAVE_PLOT : bool
    Whether the plot should be saved or not.
MEAN_SPACING : float
    The spacing of the mean bar.
BORDER : float
    Extra padding for the x-axis limits.
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
SCENARIO: str = "RB1"
MEAN_RESPONSE_TIME_FILE: str = "mean_response_times_all_runs_"
EMP_Q_FILE: str = "emp_quantile_response_times_all_runs_"

PLOT_NAME: str = "strip_plots"
RUN_PARAMETERS_FILE_NAME: str = "run_parameters_strip_plots"
##################################Parameters###################################
ENERGY_COUNTER: list[int] = [0, 20, 40, 60, 80, 100, 120, 140]
SAVE_PLOT: bool = False
MEAN_SPACING: float = 0.1
BORDER: float = 0.8
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
            f.write(f"SCENARIO: {SCENARIO}\n")
            f.write(f"MEAN_RESPONSE_TIME_FILE: {MEAN_RESPONSE_TIME_FILE}\n")
            f.write(f"EMP_Q_FILE: {EMP_Q_FILE}\n")
            f.write(f"PLOT_NAME: {PLOT_NAME}\n")
            f.write(f"RUN_PARAMETERS_FILE_NAME: {RUN_PARAMETERS_FILE_NAME}\n")
            f.write(f"ENERGY_COUNTER: {ENERGY_COUNTER}\n")
            f.write(f"SAVE_PLOT: {SAVE_PLOT}\n")
            f.write(f"MEAN_SPACING: {MEAN_SPACING}\n")
            f.write(f"BORDER: {BORDER}\n")
            f.close()
    ##################################Read data################################
    dfs_mean_response_times = []
    dfs_emp_q_response_times = []

    for energy_value in ENERGY_COUNTER:
        dfs_mean_response_times.append(
            pd.read_csv(
                f"{DATA_DIRECTORY}"
                f"{MEAN_RESPONSE_TIME_FILE}"
                f"{SCENARIO}_E"
                f"{energy_value}.csv",
                index_col=0,
            )
            .to_numpy()
            .flatten()
        )
        dfs_emp_q_response_times.append(
            pd.read_csv(
                f"{DATA_DIRECTORY}"
                f"{EMP_Q_FILE}"
                f"{SCENARIO}_E"
                f"{energy_value}.csv",
                index_col=0,
            )
            .to_numpy()
            .flatten()
        )
    ##################################Make plot################################
    NUM_ENERGIES = len(ENERGY_COUNTER)
    NUM_RUNS: int = len(dfs_mean_response_times[0])

    fig, axs = plt.subplots(1, 2, figsize=(12, 8))
    x_ints = np.arange(NUM_ENERGIES)
    x_values = np.tile(x_ints, (NUM_RUNS, 1))

    for i in range(NUM_ENERGIES):
        axs[0].scatter(
            x_values[:, i],
            dfs_mean_response_times[i],
            color="white",
            edgecolors="grey",
            alpha=0.5,
        )
        mean_rt = np.mean(dfs_mean_response_times[i])
        axs[0].hlines(
            mean_rt,
            x_ints[i] - MEAN_SPACING,
            x_ints[i] + MEAN_SPACING,
            color="tab:blue",
            linewidth=2,
            label="mean",
        )
        axs[0].text(
            x_ints[i] + MEAN_SPACING,
            mean_rt,
            f"{mean_rt:.2f}",
            color="tab:blue",
            weight="bold",
        )
        axs[0].set_xlim(-BORDER, NUM_ENERGIES - (1 - BORDER))

        axs[1].scatter(
            x_values[:, i],
            dfs_emp_q_response_times[i],
            color="white",
            edgecolors="grey",
            alpha=0.5,
        )
        mean_qrt = np.mean(dfs_emp_q_response_times[i])
        axs[1].hlines(
            mean_qrt,
            x_ints[i] - MEAN_SPACING,
            x_ints[i] + MEAN_SPACING,
            color="tab:blue",
            linewidth=2,
            label="mean",
        )
        axs[1].text(
            x_ints[i] + MEAN_SPACING,
            mean_qrt,
            f"{mean_qrt:.2f}",
            color="tab:blue",
            weight="bold",
        )
        axs[1].set_xlim(-BORDER, NUM_ENERGIES - (1 - BORDER))

    axs[0].set_title("Mean response time", fontsize=14)
    axs[0].set_ylabel("Time (min)", fontsize=14)
    axs[0].set_xticks(np.arange(NUM_ENERGIES), ENERGY_COUNTER, fontsize=14)
    axs[0].tick_params(axis="y", which="major", labelsize=12)
    handles, labels = axs[0].get_legend_handles_labels()
    axs[0].legend([handles[0]], [labels[0]], loc="upper left")
    axs[0].spines["top"].set_visible(False)
    axs[0].spines["right"].set_visible(False)

    axs[1].set_title("95% emprical quantile response time", fontsize=14)
    axs[1].set_xticks(np.arange(NUM_ENERGIES), ENERGY_COUNTER, fontsize=14)
    axs[1].tick_params(axis="y", which="major", labelsize=12)
    axs[1].spines["top"].set_visible(False)
    axs[1].spines["right"].set_visible(False)

    fig.supxlabel("Energy consumption increase (%)", fontsize=14)
    fig.suptitle(
        "Performance measures for increasing energy consumption", fontsize=16
    )

    plt.tight_layout()
    if SAVE_PLOT:
        plt.savefig(f"{RESULTS_DIRECTORY}{PLOT_NAME}.pdf")
        plt.close(fig)
    else:
        plt.show()
