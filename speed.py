#! /usr/bin/python3

import speedtest
import os.path
from datetime import datetime

dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
csv_path = "/home/ace/speedtest_log.csv"
txt_path = "/home/ace/speedtest_log.txt"
if not os.path.exists(csv_path):
    with open(csv_path, "a") as my_file:
        my_file.write("Date;")
        my_file.write("Server;")
        my_file.write("Download;")
        my_file.write("Upload;")
        my_file.write("Ping")

try:
    st = speedtest.Speedtest()
    servername = st.get_best_server()
    download = str(round(st.download() / 1000000, 3))
    upload = str(round(st.upload() / 1000000, 3))
    ping = str(st.results.ping)

    with open(txt_path, "a") as my_file:
        my_file.write(dt + "\n")
        my_file.write(
            "Server " + servername["country"] + " (" + servername["host"] + ")\n"
        )
        my_file.write("Download Speed: ")
        my_file.write(download + " Mbit\n")
        my_file.write("Upload Speed: ")
        my_file.write(upload + " Mbit\n")
        my_file.write("Ping: ")
        my_file.write(ping + " ms\n")
        my_file.write("--------------------------------------------------" + "\n")

    with open(csv_path, "a") as my_file:
        my_file.write(dt + ";")
        my_file.write(servername["country"] + " (" + servername["host"] + ");")
        my_file.write(download + ";")
        my_file.write(upload + ";")
        my_file.write(ping + "\n")

except Exception as e:
    with open(txt_path, "a") as my_file:
        my_file.write(dt + "\n")
        my_file.write("Error: ", str(e))

    with open(csv_path, "a") as my_file:
        my_file.write(dt + ";")
        my_file.write(f"Error {str(e)};")
        my_file.write(0 + ";")
        my_file.write(0 + ";")
        my_file.write(0 + "\n")
