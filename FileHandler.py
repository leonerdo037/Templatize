import os
import Errors as err

def Write(filePath, data, rewrite=False):
    file=open(filePath,"w+")
    if rewrite:
        file.seek(0)
        file.write(data)
        file.truncate()
    else:
        file.write(data)
    file.close()

def Read(filePath):
    file=open(filePath,"r+")
    output=file.read()
    file.close()
    return output