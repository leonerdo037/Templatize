import os
import json
import Errors as err

class Settings:
    #Manages the settings of the framework

    envDIR=os.path.dirname(os.path.realpath(__file__))
    homeDIR=os.path.join(envDIR, "Projects")
    settingsFilePath=os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings.json")

    def __init__(self):
        settingsFile=open(self.settingsFilePath, "w+")
        pass

    def SetEnvironmentPath(self, envPath):
        if os.path.exists(envPath):
            self.envDIR=envPath
        else:
            raise err.Conflict("The path '{0}' not found !".format(envPath))
        os.makedirs(ProjectPath)
        metaFile=open(os.path.join(ProjectPath, ".metadata"),"w+")
        metaFile.write(json.dumps({'ProjectName': projectName, 'ProjectDescription': projectDescription,'Schemas':[]}, sort_keys=True, indent=4, separators=(',', ': ')))
        metaFile.close()
        self.curProject=ProjectPath
        return "Project '{0}' created successfully !".format(projectName)