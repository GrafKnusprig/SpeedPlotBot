import pandas as pd

def calculate_bandwidth_percentage(file_path, column_name, fixed_value):
    # Read data from CSV file with semicolon separator
    df = pd.read_csv(file_path, sep=';')

    # Ensure the specified column exists in the dataframe
    if column_name not in df.columns:
        raise ValueError(f"The CSV file must contain a '{column_name}' column.")

    # Calculate the percentage of actual bandwidth delivered
    deviation_percentages = df[column_name] / fixed_value * 100

    # Calculate the mean percentage of actual bandwidth delivered
    mean_percentage = deviation_percentages.mean()

    return mean_percentage

def main():
    file_path = './speedtest_log.csv'  # Replace with the path to your CSV file
    download_column = 'Download'  # Replace with the download column name
    upload_column = 'Upload'  # Replace with the upload column name
    fixed_download_value = 50.0  # Mbps
    fixed_upload_value = 20.0  # Mbps

    mean_download_percentage = calculate_bandwidth_percentage(file_path, download_column, fixed_download_value)
    mean_upload_percentage = calculate_bandwidth_percentage(file_path, upload_column, fixed_upload_value)

    print(f"On average, your provider delivers {mean_download_percentage:.2f}% of the promised {fixed_download_value} Mbps for download.")
    print(f"On average, your provider delivers {mean_upload_percentage:.2f}% of the promised {fixed_upload_value} Mbps for upload.")

if __name__ == '__main__':
    main()
