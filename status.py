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
from main import log, Pigeon

# local file code = 1 (status)
squab = Pigeon(1)

schema = squab.create_communication_schema


def make_global():
    pass

def Dock(incoming: dict):
    log(f"Received {incoming['code']} from source {incoming['source']} at {incoming['meta']['timestamp']} by Status. OK: {incoming['ok']}")

    if incoming['ok']:
        path_dictionary = incoming['body']
        TARGET_PATH = path_dictionary['target_path']
        make_global(TARGET_PATH)

    

def fetch_git_Status() -> str:
        check_status = subprocess.run(
            ["git", "status", "-s"],
            cwd=path,
            capture_output=True,
            text=True
        )
        # print(check_status.returncode)
        if check_status.returncode:
            

        else:
            git_status = check_status.stdout

            # debug essential!!
            print("This is the git status: \n", git_status)

            # imported comments >>
            # Send the git status to next function. In OOPs we can just make it an attribute? Also, I don't understand why I added the fetch_path flag in the first place there.
            # parseStatus(git_status, fetch_path=True)

            # I will return the git status, and navigate through these class methods with an external main() function

            return git_status
        
    
    def parseStatus(self, snip: str, fetch_details= False) -> list:

        # First, I split the given into lines
        lines = snip.split("\n")


        # took a sample corpus that we will compare our lines data against

        git_status_combinations_list = {
        # 1. Staged and Unstaged Changes (Tracked Files)
        # The most common statuses
        ' M': ['Modified in Working Tree (unstaged)'],
        'M ': ['Modified in Index (staged)'],
        'MM': ['Modified in Index (staged) AND modified again in Working Tree (unstaged)'],
        ' A': ['Added in Working Tree (unstaged - very uncommon, usually A is seen)'],
        'A ': ['Added to Index (staged)'],
        ' D': ['Deleted in Working Tree (unstaged)'],
        'D ': ['Deleted from Index (staged)'],
        ' R': ['Renamed in Working Tree (unstaged)'],
        'R ': ['Renamed and Staged'],
        ' C': ['Copied in Working Tree (unstaged)'],
        'C ': ['Copied and Staged'],
        
        # 2. Unmerged Files (Conflicts) - X and Y are both 'U', 'A', or 'D'
        'UU': ['Unmerged (Unresolved Conflict - Both Modified)'],
        'AU': ['Unmerged (Added by us, Updated by them)'],
        'UA': ['Unmerged (Updated by us, Added by them)'],
        'UD': ['Unmerged (Updated by us, Deleted by them)'],
        'DU': ['Unmerged (Deleted by us, Updated by them)'],
        'AA': ['Unmerged (Both Added)'],
        'DD': ['Unmerged (Both Deleted)'],
        
        # 3. Other Statuses (Untracked and Ignored)
        '??': ['Untracked File (Not in Git yet)'],
        '!!': ['Ignored File (Visible with --ignored)'],
        
        # 4. Special/Less Common States
        'T ': ['File Type Changed (Staged)'], 
        ' T': ['File Type Changed (Unstaged)'],
        'CC': ['Copied and Staged AND copied again in Working Tree'],
        'RR': ['Renamed and Staged AND renamed again in Working Tree'],
        
        # 5. Clean/Unmodified
        '  ': ['Unmodified (Clean)'] # Only seen if a file is explicitly listed
    }
        

        # Iterating over every line element. The goal is to make a dictionary. I can use a comprehension but I need to keep redability intact.
        for line in lines:

            # split line by space, very incovienient now that I think about it since git has spaces even in the symbols... so we have to skip two, then split the lines.
            # sp_line = line.split(" ")

            # improvised statement:
            first_part = line[:2]
            second_part = line[2:]


            # This is important. I am checking if our data is in the corpus, if it is in then we are adding it to the corpus' list.
            if first_part in git_status_combinations_list:
                git_status_combinations_list[first_part].append(second_part)

            # First we filter the corpus to make a fresh, filtered dictionary
            dict_with_valid_paths = {key: value for key, value in git_status_combinations_list.items() if len(value) < 1}

            # we grab the paths from the dictionary- this is what we want. By default. I could've directly returned it, but for neatness I won't
            paths = [path[1] for path in dict_with_valid_paths.values()]

            # I will return these paths to main. If fetch_details flag is applied, I will send the list of list instead
            if fetch_details:
                return [path for path in dict_with_valid_paths.values()] 
            
            return paths