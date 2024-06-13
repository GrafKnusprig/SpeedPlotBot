import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse
import os
from modern_plot import setup_modern_plot


def plot_data_from_csv(file_path, last_n=None, modern=False, output_file=None):
    # Read the CSV file
    try:
        data = pd.read_csv(file_path, sep=";", parse_dates=["Date"])
    except FileNotFoundError:
        print("File not found. Please check the path and try again.")
        return

    # If last_n is specified, slice the dataframe to only the last n rows
    if last_n is not None:
        data = data.tail(last_n)

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

    # Plotting the data
    plt.figure(figsize=(10, 6))

    # Plot download speeds
    plt.plot(
        data["Date"],
        data["Download"],
        marker=marker,
        label="Download Speed (Mbps)",
        color=color_download,
    )

    # Plot upload speeds
    plt.plot(
        data["Date"],
        data["Upload"],
        marker=marker,
        label="Upload Speed (Mbps)",
        color=color_upload,
    )

    # plt.yscale("log")
    # Plot ping times
    # plt.plot(data["Date"], data["Ping"], marker="o", label="Ping (ms)", color="gray")

    plt.axhline(y=50, color=color_hline, linestyle=":", alpha=alpha_hline)
    plt.axhline(y=40, color=color_hline, linestyle=":", alpha=alpha_hline)
    plt.axhline(y=30, color=color_hline, linestyle=":", alpha=alpha_hline)
    plt.axhline(y=20, color=color_hline, linestyle=":", alpha=alpha_hline)
    plt.axhline(y=10, color=color_hline, linestyle=":", alpha=alpha_hline)
    # plt.axhline(y=15, color="b", linestyle=":", label="15")

    plt.title("Network Performance Over Time")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()

    # Format the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%y %H:%M"))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.gcf().autofmt_xdate()  # Rotate date labels

    plt.tight_layout()

    # Save the plot to a file if specified
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="Plot data from a CSV file.")
    parser.add_argument("csv_file", nargs="?", help="Path to the CSV file")
    parser.add_argument(
        "-n", "--last_n", type=int, help="Number of last data points to plot"
    )
    parser.add_argument("-o", "--output_file", help="Path to save the plot image")
    parser.add_argument(
        "-m",
        "--modern",
        action="store_true",
    )

    args = parser.parse_args()

    if args.csv_file:
        file_path = args.csv_file
    else:
        file_path = input("Please enter the path to the CSV file: ")

    plot_data_from_csv(file_path, args.last_n, args.modern, args.output_file)


if __name__ == "__main__":
    main()
