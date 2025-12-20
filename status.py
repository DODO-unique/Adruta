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
from main import loggy, Pigeon

# local file code = 1 (status)
squab = Pigeon(1)

schema = squab.create_communication_schema

def log(log: str) -> None:
    loggy("status", log)


class Soul:

    def __init__(self):
        pass

    def Dock(self, incoming: dict):
        log(f"Received {incoming['code']} from source {incoming['source']} at {incoming['meta']['timestamp']} by Status. OK: {incoming['ok']}")
        if incoming['code'] == 101:
            if incoming['ok']:
                path_dictionary = incoming['body']
                self.TARGET_PATH = path_dictionary['target_path']
                self.fetch_git_Status()
        
        if incoming['code'] == 102:
            if incoming['ok']:
                self.fetch_git_Status(details=True)
            
        if incoming['code'] == 103:
            if incoming['ok']:
                self.fetch_git_Status(paths=True)
    

    def fetch_git_Status(self, details: bool = False, paths: bool = False) -> str:
            check_status = subprocess.run(
                ["git", "status", "-s"],
                cwd=self.TARGET_PATH,
                capture_output=True,
                text=True
            )
            log("requesting git status...")
            # in case of any errors raised:
            if check_status.returncode:
                err_code = check_status.returncode
                err_msg = check_status.stderr
                schema(ok=False, code=951, target=0, err_msg=err_msg, err_code=err_code, err_logged=False, fatal=True)
                log("Failed to fetch git status")

            
            else:
                self.GIT_STATUS = check_status.stdout
                log("Success: Captured git status")
                packaged_git_status = {"git_status": self.GIT_STATUS}
                schema(code=901, target=0, body=packaged_git_status)
            
            if details:
                git_status_code_with_description_and_paths = self.description(self.GIT_STATUS)
                schema(code=902, target=0, body=git_status_code_with_description_and_paths)
                log("Fetched and dispatched detailed git status")
            
            if paths:
                paths_list = {
                "paths" : self.path_list(self.GIT_STATUS)
                }
                schema(code=903, target=0, body=paths_list)
                log("Fetched and dispatched list of paths")
    
    def description(self, snip: str) -> dict:

        # First, I split the given into lines
        lines = snip.split("\n")


        # took a sample corpus that we will compare our lines data against

        git_status_combinations_list = {' M': {'description': 'Modified in Working Tree (unstaged)', 'paths': []}, 'M ': {'description': 'Modified in Index (staged)', 'paths': []}, 'MM': {'description': 'Modified in Index (staged) AND modified again in Working Tree (unstaged)', 'paths': []}, ' A': {'description': 'Added in Working Tree (unstaged - very uncommon, usually A is seen)', 'paths': []}, 'A ': {'description': 'Added to Index (staged)', 'paths': []}, ' D': {'description': 'Deleted in Working Tree (unstaged)', 'paths': []}, 'D ': {'description': 'Deleted from Index (staged)', 'paths': []}, ' R': {'description': 'Renamed in Working Tree (unstaged)', 'paths': []}, 'R ': {'description': 'Renamed and Staged', 'paths': []}, ' C': {'description': 'Copied in Working Tree (unstaged)', 'paths': []}, 'C ': {'description': 'Copied and Staged', 'paths': []}, 'UU': {'description': 'Unmerged (Unresolved Conflict - Both Modified)', 'paths': []}, 'AU': {'description': 'Unmerged (Added by us, Updated by them)', 'paths': []}, 'UA': {'description': 'Unmerged (Updated by us, Added by them)', 'paths': []}, 'UD': {'description': 'Unmerged (Updated by us, Deleted by them)', 'paths': []}, 'DU': {'description': 'Unmerged (Deleted by us, Updated by them)', 'paths': []}, 'AA': {'description': 'Unmerged (Both Added)', 'paths': []}, 'DD': {'description': 'Unmerged (Both Deleted)', 'paths': []}, '??': {'description': 'Untracked File (Not in Git yet)', 'paths': []}, '!!': {'description': 'Ignored File (Visible with --ignored)', 'paths': []}, 'T ': {'description': 'File Type Changed (Staged)', 'paths': []}, ' T': {'description': 'File Type Changed (Unstaged)', 'paths': []}, 'CC': {'description': 'Copied and Staged AND copied again in Working Tree', 'paths': []}, 'RR': {'description': 'Renamed and Staged AND renamed again in Working Tree', 'paths': []}, '  ': {'description': 'Unmodified (Clean)', 'paths': []}
    }
        

        # Iterating over every line element. The goal is to make a dictionary. I can use a comprehension but I need to keep redability intact.
        for line in lines:

            # filter new lines:
            if not line.strip():
                continue

            # split line by space, very incovienient now that I think about it since git has spaces even in the symbols... so we have to skip two, then split the lines.
            # sp_line = line.split(" ")

            # improvised statement:
            status_code = line[:2]
            path = line[3:].strip()


            # This is important. I am checking if our data is in the corpus, if it is in then we are adding it to the corpus' list.
            if status_code in git_status_combinations_list:
                git_status_combinations_list[status_code]['paths'].append(path)

        filtered_git_status_list = {
            key : value
            for key, value 
            in git_status_combinations_list.items()
            if len(value['paths']) > 0
        }

        return filtered_git_status_list
    
    def path_list(self, snip: str) -> list:
        
        lines = snip.split("\n")
        paths = []

        for line in lines:
            
            if not line.strip():
                continue

            path = line[3:].strip()

            paths.append(path)
            
        return paths