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
SCENARIO_NAMES : list[str]
    A list with the scenario names that should be considered.
MEAN_RESPONSE_TIME_FILE : str
    The name of the file that contains the data set with the mean
    response times. If the script is run with multiple lambda values
    (i.e., arrival rates), note that the files should have a "Li" suffix,
    where "i" stands for the lambda rate "1/i". To facilitate reading multiple
    scenarios, the scenario name is automatically added by the script according
    to the order and value in ``SCENARIO_NAMES`` in a for-loop.
EMP_Q_FILE : str
    The name of the file that contains the data set with the 95% empirical
    quantile of the response times. If the script is run with multiple lambda
    values (i.e., arrival rates), note that the files should have a "Li" suffix,
    where "i" stands for the lambda rate "1/i". To facilitate reading multiple
    scenarios, the scenario name is automatically added by the script according
    to the order and value in ``SCENARIO_NAMES`` in a for-loop.
PLOT_NAME : str
    The name of the plot if it is saved.
RUN_PARAMETERS_FILE_NAME : str
    The name of the text file with the script parameters if ``SAVE_PLOT=True``.
LAMBDA_SCENARIOS_COUNTER : list[int] | None
    A list with the lambda values without "1/". Thus, if a lambda value of 1/4
    is used, provide "4". If it is ``None``, then a single lambda value
    (i.e., arrival rate) is used.
JITTER_SPREAD : float
    The spread of the jitter plot. A higher value means more spread.
SEED_VALUE : int
    The seed value.
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
SCENARIO_NAMES: list[str] = [
    "RB1",
    "RB2",
    "FB1",
    "RB1_RH1",
    "FB1_RH1",
    "RB1_FH1",
    "FB1_FH1",
    "Diesel",
]
MEAN_RESPONSE_TIME_FILE: str = "mean_response_times_all_runs_"
EMP_Q_FILE: str = "emp_quantile_response_times_all_runs_"

PLOT_NAME: str = "jitterplot_scenarios"
RUN_PARAMETERS_FILE_NAME: str = "run_parameters_jitterplot_scenarios"
##################################Parameters###################################
# counter for lambda scenarios file names
LAMBDA_SCENARIOS_COUNTER: list[int] | None = [4, 5, 6]
JITTER_SPREAD: float = 0.4
SEED_VALUE: int = 0
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
            f.write(f"MEAN_RESPONSE_TIME_FILE: {MEAN_RESPONSE_TIME_FILE}\n")
            f.write(f"EMP_Q_FILE: {EMP_Q_FILE}\n")
            f.write(f"PLOT_NAME: {PLOT_NAME}\n")
            f.write(f"RUN_PARAMETERS_FILE_NAME: {RUN_PARAMETERS_FILE_NAME}\n")
            f.write(f"LAMBDA_SCENARIOS_COUNTER: {LAMBDA_SCENARIOS_COUNTER}\n")
            f.write(f"JITTER_SPREAD: {JITTER_SPREAD}\n")
            f.write(f"SEED_VALUE: {SEED_VALUE}\n")
            f.write(f"SAVE_PLOT: {SAVE_PLOT}\n")
            f.close()
    ##################################Read data################################
    dfs_mean_response_times = []
    dfs_emp_q_response_times = []

    for scenario_name in SCENARIO_NAMES:
        df_mean_rt = []
        df_emp_q_rt = []

        if LAMBDA_SCENARIOS_COUNTER is None:
            df_mean_rt.append(
                pd.read_csv(
                    f"{DATA_DIRECTORY}"
                    f"{MEAN_RESPONSE_TIME_FILE}"
                    f"{scenario_name}.csv",
                    index_col=0,
                )
            )
            df_emp_q_rt.append(
                pd.read_csv(
                    f"{DATA_DIRECTORY}{EMP_Q_FILE}{scenario_name}.csv",
                    index_col=0,
                )
            )
        else:
            for lambda_value in LAMBDA_SCENARIOS_COUNTER:
                df_mean_rt.append(
                    pd.read_csv(
                        f"{DATA_DIRECTORY}"
                        f"{MEAN_RESPONSE_TIME_FILE}"
                        f"{scenario_name}_L"
                        f"{lambda_value}.csv",
                        index_col=0,
                    )
                )
                df_emp_q_rt.append(
                    pd.read_csv(
                        f"{DATA_DIRECTORY}"
                        f"{EMP_Q_FILE}"
                        f"{scenario_name}_L"
                        f"{lambda_value}.csv",
                        index_col=0,
                    )
                )

        df_mean_rt = np.concatenate(df_mean_rt).flatten()
        df_emp_q_rt = np.concatenate(df_emp_q_rt).flatten()

        dfs_mean_response_times.append(df_mean_rt)
        dfs_emp_q_response_times.append(df_emp_q_rt)
    ##################################Make plot################################
    NUM_SCENARIOS = len(SCENARIO_NAMES)
    NUM_RUNS: int = len(dfs_mean_response_times[0])
    rng = np.random.default_rng(SEED_VALUE)

    fig, axs = plt.subplots(1, 2, figsize=(12, 10), sharey=True)
    y_ints = np.arange(NUM_SCENARIOS)
    y_ints_rp = np.tile(y_ints, NUM_RUNS).reshape(NUM_RUNS, NUM_SCENARIOS)
    random_jitter = rng.uniform(
        -JITTER_SPREAD, JITTER_SPREAD, NUM_RUNS
    ).reshape(NUM_RUNS, 1)

    y_values = y_ints_rp + random_jitter

    for i in range(NUM_SCENARIOS):
        axs[0].scatter(
            dfs_mean_response_times[i],
            y_values[:, i],
            color="silver",
            alpha=0.2,
        )
        mean_rt = np.mean(dfs_mean_response_times[i])
        axs[0].vlines(
            mean_rt,
            y_ints[i] - JITTER_SPREAD,
            y_ints[i] + JITTER_SPREAD,
            color="tab:blue",
            linewidth=2,
            label="mean",
        )
        axs[0].text(
            mean_rt, y_ints[i] - JITTER_SPREAD, f"{mean_rt:.2f}", color="grey"
        )

        axs[1].scatter(
            dfs_emp_q_response_times[i],
            y_values[:, i],
            color="silver",
            alpha=0.2,
        )
        mean_qrt = np.mean(dfs_emp_q_response_times[i])
        axs[1].vlines(
            mean_qrt,
            y_ints[i] - JITTER_SPREAD,
            y_ints[i] + JITTER_SPREAD,
            color="tab:blue",
            linewidth=2,
            label="mean",
        )
        axs[1].text(
            mean_qrt,
            y_ints[i] - JITTER_SPREAD,
            f"{mean_qrt:.2f}",
            color="grey",
        )

    axs[0].set_title("Mean response time", fontsize=14)
    axs[0].set_yticks(np.arange(NUM_SCENARIOS), SCENARIO_NAMES, fontsize=14)
    axs[0].tick_params(axis="x", which="major", labelsize=12)
    axs[0].set_xlabel("Time (min)", fontsize=14)

    axs[1].set_title("95% emprical quantile response time", fontsize=14)
    axs[1].tick_params(axis="x", which="major", labelsize=12)
    axs[1].set_xlabel("Time (min)", fontsize=14)
    handles, labels = axs[1].get_legend_handles_labels()
    axs[1].legend([handles[0]], [labels[0]])

    fig.suptitle("Performance measures for the various scenarios", fontsize=16)

    plt.tight_layout()
    if SAVE_PLOT:
        plt.savefig(f"{RESULTS_DIRECTORY}{PLOT_NAME}.pdf")
        plt.close(fig)
    else:
        plt.show()
