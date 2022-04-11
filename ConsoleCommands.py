import json
from time import sleep

import TelnetSetup
from colors import bcolors

SLEEP = 0.02

def e_print(e_type, e_message):
    """Print a formatted title and error message"""

    # calculate spacing
    divider_num = int(max(len(e_type), max([len(x) for x in e_message.split("\n")]))) + 14
    spaceTitleBuff = " " * ((divider_num // 2) - len(f"-----[ {e_type} ]----") // 2)
    dividerBuff = "-" * divider_num

    print(f"{bcolors.WARNING}{dividerBuff}{bcolors.ENDC}")
    print(f"{bcolors.WARNING}{spaceTitleBuff}-----[ {e_type} ]----{bcolors.ENDC}")
    print(f"{bcolors.WARNING}" + "\t {}".format("\n\t ".join(e_message.strip().split('\n'))) + f"{bcolors.ENDC}")
    print(f"{bcolors.WARNING}{dividerBuff}{bcolors.ENDC}")



def cmd_run_with_sleep(txn, cmdString, sleepLen=SLEEP):
    """Sleep for SLEEP number of seconds, then execute a command string through TelnetSetup.run_and_log"""

    sleep(sleepLen)
    TelnetSetup.run_and_log(txn, cmdString)


def gen_command_list(verbose=False):
    """Read and return json file containing command data"""

    data = json.load(open('C.json'))
    exec_cmd = [execStr for execStr in data["commands"] if type(execStr) == str]
    dict_cmd_attr = [cmdDict for cmdDict in data["commands"] if type(cmdDict) != str]
    exec_dict = dict(zip(exec_cmd, dict_cmd_attr))

    titleText = f"Loaded Command Dict (Verbose = {bcolors.OKBLUE}True{bcolors.ENDC}):\n" if verbose else f"Loaded Command Dict:\n"
    print(f"{titleText}{bcolors.DARKGRAY} Full: {exec_dict.items()}{bcolors.ENDC}") if verbose else print(f"{titleText}{bcolors.DARKGRAY} Keys: {exec_dict.keys()}{bcolors.ENDC}")
    return exec_dict


def command_is_toggleable(cmdString, cmdDict):
    """Returns True if the cmdString is labled as toggleable in the cmdDict"""

    attr = cmdDict[cmdString]
    return True if attr["toggleable"] else False


def get_command_timeout(cmdString, cmdDict):
    """Returns the cmdString's timout value in the cmdDict"""

    attr = cmdDict[cmdString]
    return attr["timeout"] 


def cmd_exec_toggle(txn, command, commandDict, reset=False):
    """Format all commands that are flagged as Toggleable"""

    attr = commandDict[command]
    if not attr["toggleable"]:
        e_print("cmdIsNotToggleable", f"Attempted to call cmd_exec_toggle() on {command} where toggleable: {bcolors.OKBLUE}False{bcolors.ENDC}")

    if reset:
        cmd_exec_string = attr["default_reset"]
    else:
        # flip toggle value
        if type(attr["currToggleValue"]) == int:
            attr["currToggleValue"] = 1 if attr["currToggleValue"] == 0 else 0
            cmd_exec_string = "{} {}".format(command, attr["currToggleValue"])
        else:
            attr["currToggleValue"] = command if attr["currToggleValue"] == attr["default_reset"] else attr["default_reset"]
            cmd_exec_string = "{}".format(attr["currToggleValue"])
    
    # run command string
    
    cmd_run_with_sleep(txn, cmd_exec_string)
    
    

def cmd_exec_singleUse(txn, command, commandDict, reset=False):
    """Format all commands that are single use"""

    attr = commandDict[command]
    cmd_exec_string = attr["default_reset"] if reset else command

    # run command string
    cmd_run_with_sleep(txn, cmd_exec_string)


def cmd_exec_withParam(txn, command, commandDict, customParameters, reset=False):
    """Format all commands that require parameters"""

    attr = commandDict[command]
    # sanity check customParameters, format: [x, arg1, arg2, ..., argx]
    if not reset:
        if (len(customParameters) != customParameters[0]+1):
            e_print("cmd_exec_withParam - customParameters", f"Requires {customParameters[0]+1} args, args: {customParameters}\n\t {bcolors.OKCYAN}Format: [x, arg1, arg2, ..., argx]{bcolors.ENDC}")
        else:
            cmd_exec_string = command + " " + " ".join([str(customParameters[i]) for i in range(1, len(customParameters))])
    else:
        cmd_exec_string = attr['default_reset']

    # run command string
    cmd_run_with_sleep(txn, cmd_exec_string)


def cmd_exec_multiple(txn, command, commandDict, numberOfExecutions , reset=False):
    """Format all commands that run multiple times"""

    attr = commandDict[command]
    try:
        execNum = int(numberOfExecutions)
        # sanity check customParameters, format: [x, arg1, arg2, ..., argx]
        if not reset:
            if (execNum not in range(10)):
                e_print("cmd_exec_multiple - numberOfExecutions",
                        f"Requires 1 args, args: {numberOfExecutions}\n\t {bcolors.OKCYAN}Format: [x, arg1]{bcolors.ENDC}")
            else:
                cmd_exec_string = command
        else:
            cmd_exec_string = attr['default_reset']
        # run command string
        for _ in range(execNum):
            print(execNum)
            # cmd_run_with_sleep(txn, cmd_exec_string)

    except ValueError:
        cmd_exec_string = attr['default_reset']
        cmd_run_with_sleep(txn, cmd_exec_string)


def setup():
    """Return the TellNet obj from TelnetSetup, and return the command dictionary"""

    print(chr(27) + "[2J")
    txn = TelnetSetup.connect_telnet()
    commands = gen_command_list(verbose=True)

    TelnetSetup.run(txn, "echo --------------------")
    TelnetSetup.run(txn, "say [PYTHON] connected!")
    TelnetSetup.run(txn, "echo --------------------")
    TelnetSetup.run(txn, "sv_cheats 1")
    TelnetSetup.run(txn, "exec resetStreamCommands")

    return([txn, commands])


if __name__== "__main__":
    txn, commands = setup()

    input(">>")
    sleep(1)

    for i in range(10):
        cmd_exec_singleUse(txn, 'ent_create_portal_companion_cube', commands)
    cmd_exec_toggle(txn, 'thirdperson', commands)
    cmd_exec_toggle(txn, 'thirdperson', commands)
    cmd_exec_toggle(txn, 'sv_portal_placement_never_fail', commands)
    cmd_exec_toggle(txn, 'sv_portal_placement_never_fail', commands)
    
    cmd_exec_withParam(txn, 'portals_resizeall', commands,  [2, 66, 110])
    cmd_exec_withParam(txn, 'portals_resizeall', commands, [2, 0, 0], reset=True)

    cmd_exec_singleUse(txn, 'shake', commands)
    cmd_exec_singleUse(txn, 'ent_fire prop_portal fizzle', commands)
    cmd_exec_singleUse(txn, 'ent_create_portal_companion_cube', commands)
    cmd_exec_singleUse(txn, 'ent_create_paint_bomb_portal', commands)
    cmd_exec_singleUse(txn, 'ent_create_paint_bomb_jump', commands)
    cmd_exec_singleUse(txn, 'ent_create_paint_bomb_speed', commands)
    cmd_exec_singleUse(txn, 'npc_create npc_portal_turret_floor', commands)
    cmd_exec_singleUse(txn, 'ent_create npc_personality_core', commands)
    cmd_exec_singleUse(txn, 'fire_rocket_projectile', commands)
    cmd_exec_singleUse(txn, 'give prop_testchamber_door', commands)
    cmd_exec_singleUse(txn, 'ent_create prop_dynamic', commands)

