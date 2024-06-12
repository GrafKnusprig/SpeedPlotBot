import subprocess


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
    # Run get-remote-file.py without arguments
    run_script("get-remote-file.py")

    # Run standalone-chart-plotter.py with arguments "./file" and "30"
    plotter_args = [
        "./speedtest_log.csv",
        "--last_n",
        f"{int(60/10*24)}",
        "--output_file",
        "./speedtest_plot.png",
    ]
    run_script("standalone-chart-plotter.py", plotter_args)
    run_script("calculate-deviation.py")