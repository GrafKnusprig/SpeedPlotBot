import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse
import os
from datetime import datetime, timedelta
import numpy as np
from modern_plot import setup_modern_plot
import re


def calculate_bandwidth_percentage(df, column_name, fixed_value):
    if column_name not in df.columns:
        raise ValueError(f"The dataframe must contain a '{column_name}' column.")
    deviation_percentages = df[column_name] / fixed_value * 100
    mean_percentage = deviation_percentages.mean()
    mean_absolute = df[column_name].mean()
    return mean_percentage, mean_absolute


def calculate_integral_bandwidth_percentage(df, column_name, fixed_value):
    if column_name not in df.columns or "Date" not in df.columns:
        raise ValueError(
            f"The dataframe must contain '{column_name}' and 'Date' columns."
        )
    df = df.sort_values(by="Date")
    time_diffs = df["Date"].diff().dt.total_seconds().iloc[1:]
    deviation_percentages = df[column_name].iloc[1:] / fixed_value * 100
    weighted_sum = np.sum(deviation_percentages * time_diffs)
    weighted_sum_absolute = np.sum(df[column_name].iloc[1:] * time_diffs)
    total_time = np.sum(time_diffs)
    if total_time == 0:
        raise ValueError(
            "Total time for integration is zero. Check the 'Date' column values for consistency."
        )
    average_percentage = weighted_sum / total_time
    average_absolute = weighted_sum_absolute / total_time
    return average_percentage, average_absolute


def parse_duration(duration_str):
    match = re.match(
        r"((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?", duration_str
    )
    if not match:
        raise ValueError("Invalid duration format. Use format like '1d12h30m'.")
    parts = match.groupdict()
    duration = timedelta(
        days=int(parts["days"]) if parts["days"] else 0,
        hours=int(parts["hours"]) if parts["hours"] else 0,
        minutes=int(parts["minutes"]) if parts["minutes"] else 0,
    )
    return duration


def plot_data_from_csv(
    file_path,
    last_n=None,
    last_duration=None,
    modern=False,
    output_file=None,
    integral=False,
    fixed_download_value=50.0,
    fixed_upload_value=20.0,
):
    try:
        data = pd.read_csv(file_path, sep=";", parse_dates=["Date"])
    except FileNotFoundError:
        print("File not found. Please check the path and try again.")
        return
    if last_n is not None:
        data = data.tail(last_n)
    if last_duration is not None:
        duration = parse_duration(last_duration)
        cutoff_time = data["Date"].max() - duration
        data = data[data["Date"] >= cutoff_time]
    if modern:
        setup_modern_plot()
    marker = "o"
    color_download = "r"
    color_upload = "b"
    color_hline = "#000000"
    alpha_hline = 1
    if modern:
        marker = ""
        color_download = "#9400d3"
        color_upload = "#3fd300"
        color_hline = "#FFFFFF"
        alpha_hline = 0.3
    plt.figure(figsize=(10, 6))
    plt.plot(
        data["Date"],
        data["Download"],
        marker=marker,
        label="Download Speed (Mbps)",
        color=color_download,
    )
    plt.plot(
        data["Date"],
        data["Upload"],
        marker=marker,
        label="Upload Speed (Mbps)",
        color=color_upload,
    )
    y_min = min(data["Download"].min(), data["Upload"].min())
    y_max = max(data["Download"].max(), data["Upload"].max())
    y_range = range(int(y_min // 10) * 10, int(y_max // 10) * 10 + 20, 10)
    for y in y_range:
        plt.axhline(y=y, color=color_hline, linestyle=":", alpha=alpha_hline)
    plt.title("Network Performance Over Time")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%y %H:%M"))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()
    if integral:
        mean_download_percentage, mean_download_absolute = (
            calculate_integral_bandwidth_percentage(
                data, "Download", fixed_download_value
            )
        )
        mean_upload_percentage, mean_upload_absolute = (
            calculate_integral_bandwidth_percentage(data, "Upload", fixed_upload_value)
        )
    else:
        mean_download_percentage, mean_download_absolute = (
            calculate_bandwidth_percentage(data, "Download", fixed_download_value)
        )
        mean_upload_percentage, mean_upload_absolute = calculate_bandwidth_percentage(
            data, "Upload", fixed_upload_value
        )
    deviation_text = (
        f"Avg Download: {mean_download_percentage:.2f}% ({mean_download_absolute:.2f} Mbps) of {fixed_download_value} Mbps\n"
        f"Avg Upload: {mean_upload_percentage:.2f}% ({mean_upload_absolute:.2f} Mbps) of {fixed_upload_value} Mbps"
    )
    plt.annotate(
        deviation_text,
        xy=(-0.1, 1.1),
        xycoords="axes fraction",
        fontsize=10,
        ha="left",
        va="top",
        bbox=dict(facecolor="white", alpha=0.045, pad=5),
    )
    plt.tight_layout()
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Plot data from a CSV file and calculate deviation."
    )
    parser.add_argument("csv_file", nargs="?", help="Path to the CSV file")
    parser.add_argument(
        "-n", "--last_n", type=int, help="Number of last data points to plot"
    )
    parser.add_argument(
        "-d",
        "--last_duration",
        type=str,
        help="Duration of the last data points to plot (e.g., '1d12h30m')",
    )
    parser.add_argument("-o", "--output_file", help="Path to save the plot image")
    parser.add_argument("-m", "--modern", action="store_true")
    parser.add_argument(
        "-i",
        "--integral",
        action="store_true",
        help="Use integral method for calculation",
    )
    parser.add_argument(
        "-fd",
        "--fixed_download_value",
        type=float,
        default=50.0,
        help="Fixed download value in Mbps",
    )
    parser.add_argument(
        "-fu",
        "--fixed_upload_value",
        type=float,
        default=20.0,
        help="Fixed upload value in Mbps",
    )

    args = parser.parse_args()

    if args.csv_file:
        file_path = args.csv_file
    else:
        file_path = input("Please enter the path to the CSV file: ")

    plot_data_from_csv(
        file_path,
        args.last_n,
        args.last_duration,
        args.modern,
        args.output_file,
        args.integral,
        args.fixed_download_value,
        args.fixed_upload_value,
    )


if __name__ == "__main__":
    main()
