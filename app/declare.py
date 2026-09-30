import re

class Declare:

    def __init__(self):
        self.vars = {}

    def print_var(self,NAME):
        if NAME in self.vars:
            print(f"declare -- {NAME}=\"{self.vars[NAME]}\"")
        else:
            print(f"declare: {NAME}: not found")
            
    def store_var(self, arg):
        NAME, VALUE = arg.split("=")
      
        if not bool(re.match(r"^[a-zA-Z0-9_]+$", NAME)) or NAME[0].isdigit():
            print(f"declare: `{arg}\': not a valid identifier")
            return
       
                
   
        self.vars[NAME] = VALUE
        