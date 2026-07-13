import paramiko
from dataclasses import dataclass


@dataclass
class CoreIOSSHClient:
    hostname: str
    username: str
    password: str

    def connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        self.ssh.connect(
            hostname=self.hostname,
            username=self.username,
            password=self.password,
            timeout=10
        )

        print("SSH connected")

    def run_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)

        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            print("ERROR:")
            print(error)

        return output


if __name__ == "__main__":

    client = CoreIOSSHClient(
        hostname="192.168.80.3",
        username="spot",
        key_filename = "/home/scrobotics/.ssh/id_spot",
        timeout = 10
    )

    client.connect()

    print(client.run_command("hostname"))

    print(client.run_command("docker ps"))