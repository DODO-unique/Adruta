'''
Docstring for remake.main
This is runs the current flow and logs:
status - the git status checker
turtle - the path scanner and mtime editor
mercury - check and manage the messages
climax - the irreversal climax.

pancake - our universal name for a decorator

This and other Docstring documents are subject to revision during final documentation and are simply written as a guide while creation of this utility
This file will also deal with taking inputs, managing logs, passing metrics etc.
All functions and files will be called here and returned here, values will be passed here strategically. This is a centralised distributer and maintainer of the entire project.

flow:
Stage 1:
we start with a logger class. This class will specifically create a file and then use a method which everyone will paste notes to- automatically appending timestamps to the entry.

Take input path-> this is the path we will mainly work on. 
We will give two options: Take the cwd, or take a custom path. (not implemented yet)
I am thinking of creating a flag for the future and calling it the 'quick' flag- all the functions marked false won't run under the flag and this would make sure the script is carried out without much pauses. Not a priority

Stage 2:
Once the input path is passed to status. Status will send three things: Error flag, git status (a dictionary), and compared git guide.
We will take the error flag: if true, we pass control to the RepoUp util, if flase we sent take the git status (making sure it is passed successfully) and reflect it.
Once reflected we ask the user if they want detailes on it, want to commit it with custom dates and messages, or simply quit. 
If details are asked we will quickly paste the output with the guide prettily.

Stage 3:
Once we get the green light, we take the status dictionary, and the target path and pass it to turtle.

turtle passes an indexed dictionary with a list of two as its value containing [path, mtime] and three flags.
We have to arrange and reflect this in a pretty format (pretty format is a tabular format. We will see how many variations it gets, if it is too much we will assign that task to pancakes)
when sent with a query flag, we will ask the user for confirmation and if they need any change, then send the query back to turtle so it makes the changes (so we don't make main do the actual work and clutter it's purpose)
an updated flag means the data returned is updated, until user confirms that the data is right, main would keep sending whatever update queries are made back to turtle, who would keep sending the updated flag till the loop is escaped, by termination of the program or user's confirmation.
Turtle will also send a cache flag first of all with the mtime-path pairs- this will be cached for later check

Stage 4:
Once confirmed that the changes are right, we will go on to pass the final dictionary to pancakes who is meant to mercury.
First, we send the dictionary to mercury. 
Mercury would then request for with a default flag, which we have to reflect as a request for the default message.
Then we take the default message, send it back to Mercury
Mercury would then send us a query flag, where we will ask for changes- we have to ask for index and the message, then pass that list to Mercury
Mercury finally returns the updated dictionary which looks like this now: {index: [path, mtime, message], . . .} with a updated flag...
and updated flag means the same confirmation loop again. So we will make sure the confirmation loop into a reusable function 🐦‍🔥

Stage 5:
Anyway, once this is confirmed, we pass everything to climax which makes sure the final 'path's exist, compare some snapshots of the mtime taken by turtle and if git status is still running, then send final data and a confirmation flag (confirmation flag >>> query flag). This is final and irreversible. Once confirmation flag is returned with a positive response, climax punches it in.

important clarifications: 
1. Flags and expected behavior:
    Flags are analogous to internal APIs. The following is a fundamental list of flags
    Flags are not exactly boolean and can be enums, referring to a shared index of code, so for example 333 is a Cache flag. 
    a. Error flag: Reports Errors, main reflects 'check logs', or anything specific
    b. Query flag: Requests main to make a relevant query and return initial information
    c. Updated flag: starts an escapable loop, taking updated information, noting requests, sending the requests back
    d. Cache flag: snapshots for later confirmation
    e. Default flag: Unique to Mercury, asks for a default message
    d. Confirmation flag: highly logged, transparent and ultimate flag.
2. Pancake has to handle tabular representation of data- this is done sending it information while it sends a formatted, calculated tabular ASCII format for display.


'''

# All import statements:
import time
import sys
from datetime import datetime
from pathlib import Path
import re
from typing import NoReturn
import status

# log file path (absolute because of resolve)
LOG_FILE = Path(__file__).resolve().parent / "logs.txt"

class Logger:
    '''
    Docstring for Logger
    This is a shared instance. One for each run. Good luck.
    '''
    def __init__(self):
        try: 
            with open(LOG_FILE, 'x') as logs:
                logs.write(f'{datetime.now().isoformat()} -> Created logs\n')

        except FileExistsError:
            # noisy but would help when debugging for the grand flow:
            self.entry("Attempted adding a new log file. Caught under explicit file creation")

    def entry(self, log: str):
        
        # open the file
        with open(LOG_FILE, 'a') as logs:
            logs.write(f'{datetime.now().isoformat()} -> {log}\n')

# This instance is shared, so all the files can add their logs.
Hebu = Logger()



# ------------ This entire section is subject to revision during documentation ----------


# suggestion, try storing it as logs when importing elsewhere. Like `logs = Hebu.entry`, then going logs("Heyo!"). Wait, let me add that here itself:
'''logs = Hebu.entry'''
# now, simply `from main import logs` or better:
def log(log: str) -> None:
    Hebu.entry(log=log)
# same thing, but no one dies during debugging.


# ------------------ The section ends here ------------------


def abort(*, user_msg: str, log_msg: str | None = None, code: int = 1) -> NoReturn:
    '''
    Docstring for abort
    
    :param user_msg: Message reflected back at user. High-level reason for aborting.
    :type user_msg: str
    :param log_msg: Logged event. Low-level detail for aborting. If not passed, uses user_msg as log
    :type log_msg: str | None
    :param code: Aborting code; default = 1.
    :type code: int
    :return: No Return.
    :rtype: NoReturn
    '''
    if log_msg:
        log(log_msg)
    else:
        log(user_msg)
    
    print(user_msg, file=sys.stderr)
    #  (oh, imagine some feral raccoon sent a code 0 as an argument! Let me patch that LMAO).
    code = code if code != 0 else 1
    sys.exit(code)



# Taking the first input path:
unsanitized_path = input("Enter the file path (absolute path): ")
windows_path_regex = re.compile(r'^[a-zA-Z]:[\\/](?:[^\\/]*[\\/])*[^\\/]*$')

r'''
REGEX BREAKDOWN:
[] -> ensures any one single letter is used. Forces the path to be absolute
: -> compulsory
\ or / -> so C:\ or C:/
(?: ) -> this is a group where non-slash character are supposed to be followed by a slashes. Where the non-slash can be zero or more (*)
* outside the group shows that the group can repeat for zero or more times
and the last bit shows that non-slash characters must be at end- so it does not end with a slash. Again, non-slash characters can be zero or more.
'''

if windows_path_regex.match(unsanitized_path):
    TARGET_PATH = unsanitized_path
else:
    abort(
        user_msg="error in input path",
        log_msg="Given path did not match relevant regex. Aborting..."
        )


# a communication schema generator: Pigeon

class Pigeon:

    def __init__(self, local):
        self.local = local

    def create_communication_schema(
        self, 
        *, 
        code: int,  
        target: int, 
        body: dict = None, 
        err_msg: str = None, 
        source: int = None, 
        err_content: dict = None, 
        err_logged: bool = True, 
        fatal: bool = False, 
        ok: bool = True
        
    ):

        if source is None:
            source = self.local
        
        if ok:
            return {
                "ok" : True,
                "code" : code,
                "source" : source,
                "target" : target,
                "body" : body,
                "error" : None,
                "meta" : {
                    "timestamp" : datetime.now().isoformat()
                },
                "version" : "Pigeon_v1"
            }
        else:
            return {
                "ok" : False,
                "code" : code,
                "source" : source,
                "target" : target,
                "body" : body,
                "error" : {
                    "message" : err_msg,
                    "content" : err_content,
                    "error_logged" : err_logged,
                    "fatal" : fatal
                },
                "meta" : {
                    "timestamp" : datetime.now().isoformat()
                },
                "version" : "Pigeon_v1"
            }




# sending initiation code to status.
squab = Pigeon(0)

main = squab.create_communication_schema

status.Dock(main(code=111, target=1, body={"target_path": TARGET_PATH}))

