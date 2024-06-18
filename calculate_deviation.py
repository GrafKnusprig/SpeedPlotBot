import pandas as pd
import argparse
from datetime import datetime
import numpy as np


def calculate_bandwidth_percentage(file_path, column_name, fixed_value, last_n=None):
    # Read data from CSV file with semicolon separator
    df = pd.read_csv(file_path, sep=";")

    # Ensure the specified column exists in the dataframe
    if column_name not in df.columns:
        raise ValueError(f"The CSV file must contain a '{column_name}' column.")

    # If last_n is specified, consider only the last n values
    if last_n:
        df = df.tail(last_n)

    # Calculate the percentage of actual bandwidth delivered
    deviation_percentages = df[column_name] / fixed_value * 100

    # Calculate the mean percentage of actual bandwidth delivered
    mean_percentage = deviation_percentages.mean()

    return mean_percentage


def calculate_integral_bandwidth_percentage(
    file_path, column_name, fixed_value, last_n=None
):
    # Read data from CSV file with semicolon separator
    df = pd.read_csv(file_path, sep=";")

    # Ensure the necessary columns exist in the dataframe
    if column_name not in df.columns or "Date" not in df.columns:
        raise ValueError(
            f"The CSV file must contain '{column_name}' and 'Date' columns."
        )

    # Parse dates
    df["Date"] = pd.to_datetime(df["Date"])

    # If last_n is specified, consider only the last n values
    if last_n:
        df = df.tail(last_n)

    # Sort by Date
    df = df.sort_values(by="Date")

    # Calculate time differences in seconds
    time_diffs = df["Date"].diff().dt.total_seconds().iloc[1:]

    # Calculate the deviation percentages
    deviation_percentages = df[column_name].iloc[1:] / fixed_value * 100

    # Calculate the weighted average of the deviation percentages
    weighted_sum = np.sum(deviation_percentages * time_diffs)
    total_time = np.sum(time_diffs)

    if total_time == 0:
        raise ValueError(
            "Total time for integration is zero. Check the 'Date' column values for consistency."
        )

    average_percentage = weighted_sum / total_time

    return average_percentage


def main():
    parser = argparse.ArgumentParser(
        description="Calculate bandwidth percentage from speedtest log."
    )
    parser.add_argument(
        "--file_path",
        type=str,
        default="./speedtest_log.csv",
        help="Path to the CSV file.",
    )
    parser.add_argument(
        "--fixed_download_value",
        type=float,
        default=50.0,
        help="Fixed download value in Mbps.",
    )
    parser.add_argument(
        "--fixed_upload_value",
        type=float,
        default=20.0,
        help="Fixed upload value in Mbps.",
    )
    parser.add_argument(
        "--last_n",
        type=int,
        default=None,
        help="Number of last values to consider for calculation.",
    )
    parser.add_argument(
        "--integral", action="store_true", help="Use integral method for calculation."
    )

    args = parser.parse_args()

    download_column = "Download"
    upload_column = "Upload"

    if args.integral:
        mean_download_percentage = calculate_integral_bandwidth_percentage(
            args.file_path, download_column, args.fixed_download_value, args.last_n
        )
        mean_upload_percentage = calculate_integral_bandwidth_percentage(
            args.file_path, upload_column, args.fixed_upload_value, args.last_n
        )
    else:
        mean_download_percentage = calculate_bandwidth_percentage(
            args.file_path, download_column, args.fixed_download_value, args.last_n
        )
        mean_upload_percentage = calculate_bandwidth_percentage(
            args.file_path, upload_column, args.fixed_upload_value, args.last_n
        )

    print(
        f"On average, your provider delivers {mean_download_percentage:.2f}% of the promised {args.fixed_download_value} Mbps for download."
    )
    print(
        f"On average, your provider delivers {mean_upload_percentage:.2f}% of the promised {args.fixed_upload_value} Mbps for upload."
    )


if __name__ == "__main__":
    main()
