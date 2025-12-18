so classes don't have their own scope, they are not isolated. Everything is inherited from the global scope.  
You can call methods of a class in its constructor  
Class variables are also called with self- so self in essence is the pointer to any instance. Remember that  
Path objects are recognized in filesystems so they can be used by methods like 'open'.  

This `*` forces keyword-only arguments.  

so in this:   
    ```
    def abort(*, user_msg: str, log_msg: str | None = None):  
    ...    
    ```  

This is illegal:  
    ```
    abort("Invalid path", "Regex failed")  
    ```

And this is legal:  
    ```
    abort(  
    user_msg="Invalid path",  
    log_msg="Path failed Windows regex validation"  
)  
    ```