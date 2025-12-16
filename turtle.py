'''
Docstring for remake.turtle
we take the given paths, resolve it according to the target path so we have absolute paths and then we compare them with the files recursively. 
The picked files would be pried for their mtime, the mtime would be paired with the path.
Now, we send the a dictionary with indexed keys- the values would be lists of two like [path, mtime], with a query flag.
A query flag would prompt main.py to ask user if they want changes in the mtime.
If turtle receives changes, it changes the mtime and again returns a similar updated flag.
turtle's job is done here.
'''