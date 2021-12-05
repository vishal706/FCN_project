import subprocess

## result: Random behavior
def simulating_different_segment_sizes():
    for segment_size in range(100, 10000, 100):
        cmd = f"python3 RUDPClient.py -i 10.0.0.2 -f \"1.5MB.mp4\" -p 101 -s {segment_size}"
        print(f"{segment_size}:\n")
        print(f"{cmd}\n")
        returned_output = subprocess.check_output(cmd, shell=True)
        print(returned_output)
        print("------------------------------------------------------------------------------------")
    return None


def simulating_different_segment_sizes_multiple_hosts():
    return None


simulating_different_segment_sizes()
