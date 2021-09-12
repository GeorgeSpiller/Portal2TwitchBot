import sys
import telnetlib
import psutil
import signal
from time import sleep
from os import path
from colors import bcolors
from CmdExceptions import CommandNotRecognised

# Config
tn_host = "127.0.0.1"
tn_port = "2121"
cfg_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Portal 2\\portal2\\cfg"

def signal_handler(signal, frame):
    """Exit"""
    print(f"{bcolors.FAIL}\nquitting...{bcolors.ENDC}")
    sys.exit(0)


def processExists(processName):
    """List PIDs of processes matching processName"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == processName.lower():
            return True
    return False


def run(txn, command):
    """Runs commands on the portal2 console through telnet server"""
    cmd_s = command + "\n"
    txn.write(cmd_s.encode('utf-8'))
    sleep(0.05)
    #console_ret = txn.read_eager().decode("utf-8")
    #if f"Unknown command: {cmd_s}" in console_ret:
        #raise CommandNotRecognised(command, f"Command resulted in Unknown command message in the console: {console_ret}.")


def run_and_log(tnx, command):
    """Runs commands on the portal2 console through telnet server and prints message to portal2 console and terminal"""
    log_msg = "say [PY]: {}".format(command)
    run(tnx, log_msg)
    run(tnx, command)
    print(f"[Command executed]: {bcolors.OKCYAN}{command}{bcolors.ENDC}")


signal.signal(signal.SIGINT, signal_handler)


def connect_telnet():
    """Set up telnet server. Make sure portal2 is running before trying to connect"""

    # wait for portal2 to be running
    if not processExists("portal2.exe"):
        print(f"{bcolors.WARNING}Waiting for portal2 to start...{bcolors.ENDC}")
        while not processExists("portal2.exe"):
            sleep(0.25)
        sleep(10)

    # Initialize portal2 telnet connection
    print(f"Trying {bcolors.OKBLUE}{tn_host}:{tn_port}{bcolors.ENDC}...")
    try:
        tn = telnetlib.Telnet(tn_host, tn_port)
    except ConnectionRefusedError:
        # Retry in 10 seconds
        sleep(10)
        pass
    try:
        tn = telnetlib.Telnet(tn_host, tn_port)
    except ConnectionRefusedError:
        print(f"{bcolors.FAIL}Connection refused. Make sure you have the following launch option set:{bcolors.ENDC}")
        print(f"{bcolors.WARNING}\t-netconport {str(tn_port)}{bcolors.ENDC}")
        sys.exit(1)
    
    print("Successfully Connected")
    return tn


if __name__== "__main__":
    txn = connect_telnet()
    while True:
        usr_cmd = input("Enter Command >>")
        run_and_log(txn, usr_cmd)
