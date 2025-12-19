import pyperclip
def inpy(incoming):
    new_dict = {}
    for key, value in incoming.items():
        new_dict[key] = {"description" : f"{value[0]}", "paths" : []}
    
    pyperclip.copy(new_dict)
    return new_dict

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

print(inpy(git_status_combinations_list))
