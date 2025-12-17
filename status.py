'''
Docstring for remake.status
This file will take a path- absolute, of the target itself.
It must be a directory.
For example home/user/data/target/
(I hate windows path. POSIX rules)

we will run this as cwd in subprocess and run command: git status -s 
This gives us a short summary of the files.
If the we get errorcode 128 from git, that would mean repo does not exist and we will retun the error flag, rest would be empty.
If the we get errorcode 0, we will move on and return the git status.

We will take the git status, convert it into a dictionary and also create a second dictionary that will replace the paths with discription of the status codes.

So we will return three things: Error flag, git status (a dictionary), and compared git guide.
At each step we will make sure we are recording everything in a log file.
'''
from main import log

def Dock(incoming: dict):
    log(f"Received {incoming['code']} from source {incoming['source']} at {incoming['meta']['timestamp']} by Status. OK: {incoming['ok']}")

    if incoming['ok']:
        path_dictionary = incoming['body']
        TARGET_PATH = path_dictionary['target_path']
    

