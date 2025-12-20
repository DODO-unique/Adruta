'''
Docstring for remake.turtle
we take the given paths, resolve it according to the target path so we have absolute paths and then we compare them with the files recursively. 
The picked files would be pried for their mtime, the mtime would be paired with the path.
Now, we send the a dictionary with indexed keys- the values would be lists of two like [path, mtime], with a query flag.
A query flag would prompt main.py to ask user if they want changes in the mtime.
If turtle receives changes, it changes the mtime and again returns a similar updated flag.
turtle's job is done here.

so:
1. GET the absolute path and the paths from git status
2. merge the two paths (in a loop)
3. use the merged paths to scan for mtime (in the same loop iteration)
4. create a dictionary with indexes as keys, and paths (relative) + mtime 
{
    index : {
        "path" : path,
        "mtime" : mtime
    }
}
5. GET the change index and new date.
6. parse date, spot the change index.
7. Replace change index, send back the new data again. 
8. 5 to 7 are repetable.

start by creating a Dock, establishing constraints like subprocess, logs, Pigeon 
'''

from pathlib import Path
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# local imports
from main import loggy, Pigeon, Conversations

main_Dock = Conversations.Dock
def outgoing(prepared_schematic):
    main_Dock(prepared_schematic)

squab = Pigeon(2)

schema = squab.create_communication_schema

def log(log: str) -> None:
    loggy("turtle", log)

class Soul:

    def __init__(self):
        pass

    def Dock(self, incoming: dict) -> None:
        log(f"Received {incoming['code']} from source {incoming['source']} at {incoming['meta']['timestamp']} by Turtle. OK: {incoming['ok']}")

        if incoming['code'] == 201:
            if incoming['ok']:
                # fetch git status and target path
                target_paths_dictionary = incoming['body']
                self.TARGET_PATH = target_paths_dictionary['target_path']
                self.PATHS = target_paths_dictionary['paths']
                # reinforce the above with pydantic later
                self.mtime_fetcher(self.TARGET_PATH, self.PATHS)
        
        if incoming['code'] == 202:
            if incoming['ok']:
                '''
                This should look like: 
                body = {
                'indices' : [],
                'new_time' : str,
                'mtimes' : dict,
                }'''


                body = incoming['body']

                indices = body['indices']
                new_time = body['new_time']
                mtimes = body['mtimes']

                self.change_mtime(indices, new_time, mtimes)


    def mtime_fetcher(self, target: str, paths: list) -> None:

        mtime_list = {}
        files_not_found = {}
        
        # first we make a loop that lasts till the paths are over
        for i, path in enumerate(paths, start=1):

            # merge target with relative path
            absolute_path = (Path(target) / path).resolve()

            try:           
                stat_object = os.stat(absolute_path)
            except OSError as e:
                files_not_found[i] = self.extract_os_error(e, path = path)
                continue

            last_modified_timestamp = stat_object.st_mtime


            utc_dt = datetime.fromtimestamp(last_modified_timestamp, tz=timezone.utc)
            ist_mtime = utc_dt.astimezone(ZoneInfo("Asia/Kolkata"))
            

            mtime_list[i] = {
                'path': path,
                'mtime': ist_mtime
            }
        


        if len(files_not_found.keys()) > 0:
            log("Found error in paths")
            err_content = files_not_found
            outgoing(schema(
                ok=False,
                code=952,
                target=0,
                err_content=err_content,
                fatal= True,
                err_logged=False
            ))
            log("sent error sources back to main")
            return
        
        outgoing(schema(code=904, target=0, body=mtime_list))
        log("fetched, packaged and dispatched modified time")

    def change_mtime(self, indices: list, new_time: str, mtimes: dict) -> None:
        
        if len(indices) > 0:    
            for index in indices:
                # WARNING: ADDING UNSANITIZED DATE HERE. MAIN HANDLES CORRECT INPUT OR OTHERWISE DICTATES CHANGES
                mtimes[index]['mtime'] = new_time
        else:
            # add error here
            pass

        outgoing(schema(code=905, target=0, body=mtimes))
        log(f"changed mtime at indices: {indices}")

    def extract_os_error(self, e: OSError, *, path=None) -> dict:
        return {
            "type": type(e).__name__,
            "path": path,
            "message": e.strerror,
            "errno": e.errno,
            "filename": e.filename,
        }
