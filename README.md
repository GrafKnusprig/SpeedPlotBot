# SpeedPlotBot

SpeedPlotBot is a tool for automating speedtests for your internet connection. It allows you to regularly monitor your internet speed and collect data for analysis. Additionally, there are plans to develop a Telegram bot that can send you information about your speed tests.

To use the Telegram bot functionality, you will need to add a `credentials.py` file to the project directory. In this file, define a variable named `token` and assign your Telegram bot token to it.

Please note that the Telegram bot feature is currently under development and may not be available in the initial release.

## Installation

To install SpeedPlotBot, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/SpeedPlotBot.git`
2. Navigate to the project directory: `cd SpeedPlotBot`
3. Install the required dependencies: `pip install -r requirements.txt`

## Usage

To run SpeedPlotBot, execute the following command:

```
python speed.py
```

This will start one speed test and create the speedtest_log.csv and speedtest_log.txt files.

## Setting up as a systemd timer on a Raspberry Pi

To set up SpeedPlotBot as a systemd timer on a Raspberry Pi, follow these steps:

1. Copy the `speedtest.service` and `speedtest.timer` files to the `/usr/lib/systemd/system` folder on your Raspberry Pi.
2. Change the /home/ace/speed.py to your actual location of the speed.py file.
3. Enable the timer by running the following command: `sudo systemctl enable speedtest.timer`
4. Start the timer by running the following command: `sudo systemctl start speedtest.timer`

This will schedule the `speed.py` script to run at regular intervals as specified in the `speedtest.timer` file.

## Plotting Speed Test Data

SpeedPlotBot also includes a Python script, `standalone-chart-plotter.py`, that allows you to plot the collected data from the `speedtest_log.csv` file. This script utilizes the `matplotlib` library to generate visualizations of your internet speed over time.

To plot the data, follow these steps:

1. Make sure you have the `matplotlib` library installed. If not, you can install it by running `pip install matplotlib`.
2. Run the `standalone-chart-plotter.py` script using the following command:

    ```
    python standalone-chart-plotter.py
    ```

    This will generate a line plot showing the variation of your internet speed over time.

Feel free to customize the `standalone-chart-plotter.py` script to suit your specific visualization needs.

## Command Line Parameters

The `standalone-chart-plotter.py` script accepts two command line parameters:

1. Specifies the path to the CSV file containing the speed test data. Example usage: `python standalone-chart-plotter.py /path/to/speedtest_log.csv`

2. `--last_n`: Specifies the number of last speed test results to be printed. Example usage: `python standalone-chart-plotter.py --last_n 10`

You can use these parameters to customize the behavior of the `standalone-chart-plotter.py` script and retrieve specific information from the speed test data.

Make sure to replace `/path/to/speedtest_log.csv` with the actual path to your `speedtest_log.csv` file.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.