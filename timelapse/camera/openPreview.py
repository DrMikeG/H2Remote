import subprocess

command = "libcamera-hello -t 0"

try:
    subprocess.run(command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Command execution failed with return code {e.returncode}")