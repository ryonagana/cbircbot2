import re

if __name__ == "__main__":
    
    try:
        text = re.compile(r"^([?|!])[\s](.+[aA-zZ0-9])[\s](.+[aA-zZ0-9])$", re.IGNORECASE | re.UNICODE)
        match = text.match("?                           modulo                   comando").groups()
        
        sufixo = match[0].lstrip()
        modulo = match[1].lstrip()
        comando = match[2].lstrip()
        
        print(match[1].strip(),len(match[1].strip()))
        print(match[2].strip(),len(match[2].strip()))
        print(match[0].strip(),len(match[0].strip()))
        
        
        
    except Exception as e:
        print(e)