'''
Docstring for remake.mercury
Mercury would receive a complicated dictionary like {index: [path, mtime], . . .}
Mercury has to take this and attach a third piece in each list as the 'message'. 
Mercury would request a 'default' query first. At this query, main would ask for a default message. 
Mercury would take the default and then ask for any specific changes under the 'custom' flag.
Custom flag would make main quickly ensure if the user needs any specific changes, then hand over the index and messages in a list to Mercury. 
Mercury compiles everything one last time and sends a updated flag to main, main confirms, and the loop starts again.
Mercury's job is done here.
'''