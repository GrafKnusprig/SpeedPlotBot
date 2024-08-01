import subprocess
import argparse


def run_script(script_name, args=[]):
    try:
        result = subprocess.run(
            [".\.venv\Scripts\python.exe", script_name] + args,
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        print(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_name}: {e.stderr}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sync data from Raspberry and plot it."
    )
    parser.add_argument("-n", "--no_sync", action="store_true")

    args = parser.parse_args()

    if not args.no_sync:
        # Run get-remote-file.py without arguments
        run_script("get_remote_file.py")
        run_script("backup_speedtest.py")

    # Run the mighty plotter
    plotter_args = [
        "./speedtest_log.csv",
        "--last_duration",
        "1d",
        "--output_file",
        "./speedtest_plot.png",
        "--modern",
        # "--integral",
        "--fixed_download_value",
        "50.0",
        "--fixed_upload_value",
        "20.0",
    ]
    run_script("mighty_plotter.py", plotter_args)

    # # Run standalone-chart-plotter.py with arguments "./file" and "30"
    # plotter_args = [
    #     "./speedtest_log.csv",
    #     "--last_n",
    #     f"{int(60/10*24*4)}",
    #     "--output_file",
    #     "./speedtest_plot.png",
    #     "--modern",  # Modern plot style
    # ]
    # run_script("standalone-chart-plotter.py", plotter_args)

    # deviation_args = [
    #     "--file_path",
    #     "./speedtest_log.csv",
    #     "--fixed_download_value",
    #     "50.0",
    #     "--fixed_upload_value",
    #     "20.0",
    #     "--last_n",
    #     f"{int(60/10*24*4)}",
    #     "--integral",
    # ]
    # run_script("calculate-deviation.py", deviation_args)
