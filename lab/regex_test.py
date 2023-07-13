import re


cmd_regex = re.compile(f"^([?|!]\s)(.+)$", re.DEBUG | re.IGNORECASE)

c = cmd_regex.search("? helloworld asdssd maconha suja")

if c:
    print(c.groups())
    
    print(c.groups()[1].split(' '))
    
else:
    print("Sem Match")