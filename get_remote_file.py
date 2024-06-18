import paramiko
from credentials import raspberrypw
from scp import SCPClient


def create_ssh_client(server, user, password, port=22):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port=port, username=user, password=password)
    return client


def get_file_via_scp(remote_path, local_path, server, user, password, port=22):
    ssh_client = create_ssh_client(server, user, password, port)
    scp = SCPClient(ssh_client.get_transport())
    scp.get(remote_path, local_path)
    scp.close()
    ssh_client.close()


if __name__ == "__main__":
    server = "192.168.0.20"
    user = "ace"
    password = raspberrypw  # Replace with the actual password
    port = 22  # Specify the port here

    try:
        get_file_via_scp(
            "/home/ace/speedtest_log.csv",
            "./speedtest_log.csv",
            server,
            user,
            password,
            port,
        )
        print(f"File downloaded to ./speedtest_log.csv")
        get_file_via_scp(
            "/home/ace/speedtest_log.txt",
            "./speedtest_log.txt",
            server,
            user,
            password,
            port,
        )
        print(f"File downloaded to ./speedtest_log.txt")
    except Exception as e:
        print(f"An error occurred: {e}")
