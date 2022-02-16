import os
import json 

def issue_sybmols():
    issue = []
    for name in os.listdir("data/"):
        f = open ("data/" + name, "r")
        data = json.loads(f.read())
        if 'r' in data.keys() and data['r'] == 'failed to get':
            issue.append(data['symbol'])
        f.close()
    f = open ("issue_symbols.txt", "w")
    for x in issue:
        f.write(x + '\n')
    f.close()

    return issue
    
  
# issue_sybmols()
