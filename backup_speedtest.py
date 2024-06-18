import os
import shutil
from datetime import datetime


def backup_speedtest_log(file_path="./speedtest_log.csv", backup_dir="./backups"):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Please check the path and try again.")
        return

    # Create the backups directory if it does not exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Get the current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create the backup filename
    base_filename = os.path.basename(file_path)
    backup_filename = f"{current_time}_{base_filename}"

    # Create the full backup file path
    backup_file_path = os.path.join(backup_dir, backup_filename)

    # Copy the file
    shutil.copy(file_path, backup_file_path)

    print(f"Backup created: {backup_file_path}")


if __name__ == "__main__":
    backup_speedtest_log()
