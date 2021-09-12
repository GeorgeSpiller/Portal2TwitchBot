import queue
import threading
import time
from typing import final

import ConsoleCommands
import TwitchBot
from CmdExceptions import CommandNotRecognised

'''
    Needs to 
    -   Detect spam abuse for repeat commands
    -   Handel cooldown comand comtrols
    -   Remove/change toggle commands (as they do not work between saves)
    -   Remove error checking through reading terminal
    -   Make portal resizing work (delay sometimes doesnt work between save loads)
    -(?)Allow for parameters that run the same command multiple times?

'''

WorkQueue = queue.Queue()
TimeOutDict = {}


def newIncommingCommand(txn, cmdDict, cmdName, author, reset=False, parameterList=[]):
    newCommand = command(txn, cmdDict, cmdName, author, reset, parameterList)

    # handel timeout values before queuing command 
    check, timeLeft = handle_timeouts(newCommand)
    if check:
        WorkQueue.put(newCommand)
        workerThread = threading.Thread(target=worker, daemon=True)
        workerThread.start()
        # workerThread.join()
        return True, ""
    else:
        return False, f'{newCommand.name} command was used too soon! Please wait {int(timeLeft)} seconds before using it again.'


def handle_timeouts(command):
    # see if the command has been called previously
    currentTimestamp = time.time()
    if command.name not in TimeOutDict:
        # if not, add it to the list with its outTime = timeIn + waitTimeBetween, run cmd
        TimeOutDict[command.name] = command.time_in + command.waitTimeBetween
        return True, 0
    elif TimeOutDict[command.name] <= currentTimestamp:
        # if outTime < time.now(), remove from list, run cmd
        TimeOutDict.pop(command.name, None)
        return True, 0
    elif TimeOutDict[command.name] > currentTimestamp:
        # if outTime > time.now(), return false - message: cdm exec too soon (pass timeLeft = outTime - time.now())
        return False, TimeOutDict[command.name] - currentTimestamp
    else:
        ConsoleCommands.e_print("Time_Error", f"Bad times in handle_timeouts({command.name})\nCurrentTime: {currentTimestamp}, WaitTime: {command.waitTimeBetween}, outTime: {TimeOutDict[command.name]}, TimeOutDict: {TimeOutDict.items()}")
        return False, -0


def worker():
    while WorkQueue.not_empty:
        nextItem = WorkQueue.get()
        try:
            nextItem.execute()
        except CommandNotRecognised:
            ConsoleCommands.e_print("Command_Not_Executed", f"The command {CommandNotRecognised.command} could not be executed.")
        finally:
            WorkQueue.task_done()


class command:
    def __init__(self, txn, cmdDict, cmdName, author, reset, parameterList):
        self.txn = txn
        self.dict = cmdDict
        self.name = cmdName
        self.reset = reset
        self.author = author
        self.time_in = time.time()
        self.waitTimeBetween = ConsoleCommands.get_command_timeout(cmdName, cmdDict)
        self.toggleable = ConsoleCommands.command_is_toggleable(cmdName, cmdDict)
        if len(parameterList) > 0:
            params = parameterList
            params.insert(0, len(parameterList))
            self.parameters = params
        else:
            self.parameters = None

    def execute(self):
        
        if self.toggleable:
            ConsoleCommands.cmd_exec_toggle(self.txn, self.name, self.dict, reset=self.reset)
        elif self.parameters == None or (len(self.parameters) == 0):
            ConsoleCommands.cmd_exec_singleUse(self.txn, self.name, self.dict, reset=self.reset)
        else:
            ConsoleCommands.cmd_exec_withParam(self.txn, self.name, self.dict, self.parameters, reset=self.reset)


    def _debug_print(self):
        attrs = vars(self)
        print_message = ' ,\n '.join("%s: %s" % item for item in list(attrs.items())[2:])
        ConsoleCommands.e_print("Debug_Print_Command_Attributes", f"{print_message}")


if __name__== "__main__":
    txn, cmdDict = ConsoleCommands.setup()
    TwitchBot.run_bot(txn, cmdDict)



