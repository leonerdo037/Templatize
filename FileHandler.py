import os
import Errors as err

def ValidatePath(path, pathType, new=False):
    baseName=os.path.basename(path)
    if os.path.exists(path):
        # Found
        if new:
            raise err.Conflict("A {0} with the name '{1}' already exists !".format(pathType, baseName))
            return False
        else:
            return True
    else:
        # Not Found
        if new:
            return True
        else:
            raise err.Conflict("There are no {0} with the name '{1}'".format(pathType, baseName))
            return False

def ValidateProject(path, new=False):
    return ValidatePath(path, "Project", new)

def ValidateSchema(projectPath, schemaPath, new=False):
    ValidateProject(projectPath, False)
    return ValidatePath(schemaPath, "Schema", new)

def ValidateModule(projectPath, schemPath, modulePath, new=False):
    ValidateSchema(projectPath, schemPath, False)
    return ValidatePath(modulePath, "Module", new)

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