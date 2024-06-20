#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script creates a plot of the mean and 95% confidence interval of two
performance measures (the mean and 95% empirical quantile function)
cumulatively for each run.

Parameters
----------
DATA_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the input data is located.
RESULTS_DIRECTORY : str
    The folder, relative to the ``ROOT_DIRECTORY`` (automatically determined),
    where the output files should be saved.
MEAN_RESPONSE_TIME_FILE_1 : str
    The name of the file that contains the first data set with the mean
    response times.
MEAN_RESPONSE_TIME_FILE_2 : str
    The name of the file that contains the second data set with the mean
    response times.
MEAN_RESPONSE_TIME_FILE_3 : str
    The name of the file that contains the third data set with the mean
    response times.
EMP_QUANTILE_FILE_1 : str
    The name of the file that contains the first data set with the 95%
    empirical quantiles of the response times.
EMP_QUANTILE_FILE_2 : str
    The name of the file that contains the second data set with the 95%
    empirical quantiles of the response times.
EMP_QUANTILE_FILE_3 : str
    The name of the file that contains the third data set with the 95%
    empirical quantiles of the response times.
NUM_RUNS : int
    The number of runs that should be plotted.
SAVE_PLOT : bool
    Whether the plot should be saved or not.
PLOT_NAME : str
    The name of the plot if it is saved.
RUN_PARAMETERS_FILE_NAME : str
    The name of the text file with the script parameters if ``SAVE_PLOT=True``.
"""

import os
import scipy
import datetime
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
MEAN_RESPONSE_TIME_FILE_1: str = "mean_response_times_all_runs_Diesel_24_ambu"
MEAN_RESPONSE_TIME_FILE_2: str = "mean_response_times_all_runs_Diesel_22_ambu"
MEAN_RESPONSE_TIME_FILE_3: str = "mean_response_times_all_runs_Diesel_20_ambu"

EMP_QUANTILE_FILE_1: str = (
    "emp_quantile_response_times_all_runs_Diesel_24_ambu"
)
EMP_QUANTILE_FILE_2: str = (
    "emp_quantile_response_times_all_runs_Diesel_22_ambu"
)
EMP_QUANTILE_FILE_3: str = (
    "emp_quantile_response_times_all_runs_Diesel_20_ambu"
)
#################################Parameters####################################
NUM_RUNS: int = 10000
SAVE_PLOT: bool = False
PLOT_NAME: str = f"advancing_performance_measures_plot_{NUM_RUNS}"
RUN_PARAMETERS_FILE_NAME: str = f"run_parameters_{PLOT_NAME}"
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
            f.write(
                f"MEAN_RESPONSE_TIME_FILE_1: {MEAN_RESPONSE_TIME_FILE_1}\n"
            )
            f.write(
                f"MEAN_RESPONSE_TIME_FILE_2: {MEAN_RESPONSE_TIME_FILE_2}\n"
            )
            f.write(
                f"MEAN_RESPONSE_TIME_FILE_3: {MEAN_RESPONSE_TIME_FILE_3}\n"
            )
            f.write(f"EMP_QUANTILE_FILE_1: {EMP_QUANTILE_FILE_1}\n")
            f.write(f"EMP_QUANTILE_FILE_2: {EMP_QUANTILE_FILE_2}\n")
            f.write(f"EMP_QUANTILE_FILE_3: {EMP_QUANTILE_FILE_3}\n")
            f.write(f"NUM_RUNS: {NUM_RUNS}\n")
            f.write(f"SAVE_PLOT: {SAVE_PLOT}\n")
            f.write(f"PLOT_NAME: {PLOT_NAME}\n")
            f.write(f"RUN_PARAMETERS_FILE_NAME: {RUN_PARAMETERS_FILE_NAME}\n")
            f.close()
    ##################################Read data################################
    start_time = datetime.datetime.now()

    df_1 = pd.read_csv(
        f"{DATA_DIRECTORY}{MEAN_RESPONSE_TIME_FILE_1}.csv", index_col=0
    )
    df_2 = pd.read_csv(
        f"{DATA_DIRECTORY}{MEAN_RESPONSE_TIME_FILE_2}.csv", index_col=0
    )
    df_3 = pd.read_csv(
        f"{DATA_DIRECTORY}{MEAN_RESPONSE_TIME_FILE_3}.csv", index_col=0
    )

    df_4 = pd.read_csv(
        f"{DATA_DIRECTORY}{EMP_QUANTILE_FILE_1}.csv", index_col=0
    )
    df_5 = pd.read_csv(
        f"{DATA_DIRECTORY}{EMP_QUANTILE_FILE_2}.csv", index_col=0
    )
    df_6 = pd.read_csv(
        f"{DATA_DIRECTORY}{EMP_QUANTILE_FILE_3}.csv", index_col=0
    )

    mean_response_times_1 = df_1.iloc[:, 0].values
    mean_response_times_2 = df_2.iloc[:, 0].values
    mean_response_times_3 = df_3.iloc[:, 0].values
    emp_quantile_response_times_1 = df_4.iloc[:, 0].values
    emp_quantile_response_times_2 = df_5.iloc[:, 0].values
    emp_quantile_response_times_3 = df_6.iloc[:, 0].values
    #################################Initialize################################
    am_mean_response_times_1 = np.full((NUM_RUNS - 1), np.nan)
    am_mean_response_times_2 = np.full((NUM_RUNS - 1), np.nan)
    am_mean_response_times_3 = np.full((NUM_RUNS - 1), np.nan)
    astd_mean_response_times_1 = np.full((NUM_RUNS - 1), np.nan)
    astd_mean_response_times_2 = np.full((NUM_RUNS - 1), np.nan)
    astd_mean_response_times_3 = np.full((NUM_RUNS - 1), np.nan)
    aerror_mean_response_times_1 = np.full((NUM_RUNS - 1), np.nan)
    aerror_mean_response_times_2 = np.full((NUM_RUNS - 1), np.nan)
    aerror_mean_response_times_3 = np.full((NUM_RUNS - 1), np.nan)

    am_emp_quantile_response_times_1 = np.full((NUM_RUNS - 1), np.nan)
    am_emp_quantile_response_times_2 = np.full((NUM_RUNS - 1), np.nan)
    am_emp_quantile_response_times_3 = np.full((NUM_RUNS - 1), np.nan)
    astd_emp_quantile_response_times_1 = np.full((NUM_RUNS - 1), np.nan)
    astd_emp_quantile_response_times_2 = np.full((NUM_RUNS - 1), np.nan)
    astd_emp_quantile_response_times_3 = np.full((NUM_RUNS - 1), np.nan)
    aerror_emp_quantile_response_times_1 = np.full((NUM_RUNS - 1), np.nan)
    aerror_emp_quantile_response_times_2 = np.full((NUM_RUNS - 1), np.nan)
    aerror_emp_quantile_response_times_3 = np.full((NUM_RUNS - 1), np.nan)
    #######################Calculate performance measures######################
    for i in range(2, NUM_RUNS + 1):
        am_mean_response_times_1[i - 2] = np.mean(mean_response_times_1[:i])
        am_mean_response_times_2[i - 2] = np.mean(mean_response_times_2[:i])
        am_mean_response_times_3[i - 2] = np.mean(mean_response_times_3[:i])
        astd_mean_response_times_1[i - 2] = np.std(
            mean_response_times_1[:i], ddof=1
        )
        astd_mean_response_times_2[i - 2] = np.std(
            mean_response_times_2[:i], ddof=1
        )
        astd_mean_response_times_3[i - 2] = np.std(
            mean_response_times_3[:i], ddof=1
        )
        aerror_mean_response_times_1[i - 2] = scipy.stats.t.ppf(
            0.975, i - 1
        ) * (astd_mean_response_times_1[i - 2] / np.sqrt(i))
        aerror_mean_response_times_2[i - 2] = scipy.stats.t.ppf(
            0.975, i - 1
        ) * (astd_mean_response_times_2[i - 2] / np.sqrt(i))
        aerror_mean_response_times_3[i - 2] = scipy.stats.t.ppf(
            0.975, i - 1
        ) * (astd_mean_response_times_3[i - 2] / np.sqrt(i))

    for i in range(2, NUM_RUNS + 1):
        am_emp_quantile_response_times_1[i - 2] = np.mean(
            emp_quantile_response_times_1[:i]
        )
        am_emp_quantile_response_times_2[i - 2] = np.mean(
            emp_quantile_response_times_2[:i]
        )
        am_emp_quantile_response_times_3[i - 2] = np.mean(
            emp_quantile_response_times_3[:i]
        )
        astd_emp_quantile_response_times_1[i - 2] = np.std(
            emp_quantile_response_times_1[:i], ddof=1
        )
        astd_emp_quantile_response_times_2[i - 2] = np.std(
            emp_quantile_response_times_2[:i], ddof=1
        )
        astd_emp_quantile_response_times_3[i - 2] = np.std(
            emp_quantile_response_times_3[:i], ddof=1
        )
        aerror_emp_quantile_response_times_1[i - 2] = scipy.stats.t.ppf(
            0.975, i - 1
        ) * (astd_emp_quantile_response_times_1[i - 2] / np.sqrt(i))
        aerror_emp_quantile_response_times_2[i - 2] = scipy.stats.t.ppf(
            0.975, i - 1
        ) * (astd_emp_quantile_response_times_2[i - 2] / np.sqrt(i))
        aerror_emp_quantile_response_times_3[i - 2] = scipy.stats.t.ppf(
            0.975, i - 1
        ) * (astd_emp_quantile_response_times_3[i - 2] / np.sqrt(i))

    x = np.arange(2, NUM_RUNS + 1)
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    axs[0].plot(
        x, am_mean_response_times_1, label="24 ambulances", color="#1b9e77"
    )
    axs[0].plot(
        x,
        am_mean_response_times_1 - aerror_mean_response_times_1,
        linestyle="dashed",
        color="#1b9e77",
        alpha=0.1,
    )
    axs[0].plot(
        x,
        am_mean_response_times_1 + aerror_mean_response_times_1,
        linestyle="dashed",
        color="#1b9e77",
        alpha=0.1,
    )
    axs[0].fill_between(
        x,
        am_mean_response_times_1 - aerror_mean_response_times_1,
        am_mean_response_times_1 + aerror_mean_response_times_1,
        color="#1b9e77",
        alpha=0.1,
    )

    axs[0].plot(
        x, am_mean_response_times_2, label="22 ambulances", color="#d95f02"
    )
    axs[0].plot(
        x,
        am_mean_response_times_2 - aerror_mean_response_times_2,
        linestyle="dashed",
        color="#d95f02",
        alpha=0.1,
    )
    axs[0].plot(
        x,
        am_mean_response_times_2 + aerror_mean_response_times_2,
        linestyle="dashed",
        color="#d95f02",
        alpha=0.1,
    )
    axs[0].fill_between(
        x,
        am_mean_response_times_2 - aerror_mean_response_times_2,
        am_mean_response_times_2 + aerror_mean_response_times_2,
        color="#d95f02",
        alpha=0.1,
    )

    axs[0].plot(
        x, am_mean_response_times_3, label="20 ambulances", color="#7570b3"
    )
    axs[0].plot(
        x,
        am_mean_response_times_3 - aerror_mean_response_times_3,
        linestyle="dashed",
        color="#7570b3",
        alpha=0.1,
    )
    axs[0].plot(
        x,
        am_mean_response_times_3 + aerror_mean_response_times_3,
        linestyle="dashed",
        color="#7570b3",
        alpha=0.1,
    )
    axs[0].fill_between(
        x,
        am_mean_response_times_3 - aerror_mean_response_times_3,
        am_mean_response_times_3 + aerror_mean_response_times_3,
        color="#7570b3",
        alpha=0.1,
    )

    axs[0].set_title("Mean response time", fontsize=14)
    axs[0].set_xlabel(r"Run $n$", fontsize=12)
    axs[0].set_ylabel("Time (min)", fontsize=12)
    axs[0].set_ylim(5.5, 8.5)
    axs[0].text(1000, 7.7, "20 ambulances", color="#7570b3")
    axs[0].text(1000, 7.15, "22 ambulances", color="#d95f02")
    axs[0].text(1000, 6.55, "24 ambulances", color="#1b9e77")
    axs[0].spines["top"].set_visible(False)
    axs[0].spines["right"].set_visible(False)

    axs[1].plot(
        x,
        am_emp_quantile_response_times_1,
        label="24 ambulances",
        color="#1b9e77",
    )
    axs[1].plot(
        x,
        am_emp_quantile_response_times_1
        - aerror_emp_quantile_response_times_1,
        linestyle="dashed",
        color="#1b9e77",
        alpha=0.1,
    )
    axs[1].plot(
        x,
        am_emp_quantile_response_times_1
        + aerror_emp_quantile_response_times_1,
        linestyle="dashed",
        color="#1b9e77",
        alpha=0.1,
    )
    axs[1].fill_between(
        x,
        am_emp_quantile_response_times_1
        - aerror_emp_quantile_response_times_1,
        am_emp_quantile_response_times_1
        + aerror_emp_quantile_response_times_1,
        color="#1b9e77",
        alpha=0.1,
    )

    axs[1].plot(
        x,
        am_emp_quantile_response_times_2,
        label="22 ambulances",
        color="#d95f02",
    )
    axs[1].plot(
        x,
        am_emp_quantile_response_times_2
        - aerror_emp_quantile_response_times_2,
        linestyle="dashed",
        color="#d95f02",
        alpha=0.1,
    )
    axs[1].plot(
        x,
        am_emp_quantile_response_times_2
        + aerror_emp_quantile_response_times_2,
        linestyle="dashed",
        color="#d95f02",
        alpha=0.1,
    )
    axs[1].fill_between(
        x,
        am_emp_quantile_response_times_2
        - aerror_emp_quantile_response_times_2,
        am_emp_quantile_response_times_2
        + aerror_emp_quantile_response_times_2,
        color="#d95f02",
        alpha=0.1,
    )

    axs[1].plot(
        x,
        am_emp_quantile_response_times_3,
        label="20 ambulances",
        color="#7570b3",
    )
    axs[1].plot(
        x,
        am_emp_quantile_response_times_3
        - aerror_emp_quantile_response_times_3,
        linestyle="dashed",
        color="#7570b3",
        alpha=0.1,
    )
    axs[1].plot(
        x,
        am_emp_quantile_response_times_3
        + aerror_emp_quantile_response_times_3,
        linestyle="dashed",
        color="#7570b3",
        alpha=0.1,
    )
    axs[1].fill_between(
        x,
        am_emp_quantile_response_times_3
        - aerror_emp_quantile_response_times_3,
        am_emp_quantile_response_times_3
        + aerror_emp_quantile_response_times_3,
        color="#7570b3",
        alpha=0.1,
    )

    axs[1].set_title("95% empirical quantile response time", fontsize=14)
    axs[1].set_xlabel(r"Run $n$", fontsize=12)
    axs[1].set_ylim(10, 17)
    axs[1].spines["top"].set_visible(False)
    axs[1].spines["right"].set_visible(False)

    plt.suptitle("Cumulative means with 95% confidence intervals", fontsize=16)
    if SAVE_PLOT:
        plt.savefig(f"{RESULTS_DIRECTORY}{PLOT_NAME}.pdf", bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()

    print(f"The running time was: {datetime.datetime.now() - start_time}")
