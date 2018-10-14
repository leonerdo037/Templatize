import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js

class Project:

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    globalDataFile=os.path.join(homeDIR, "metadata.json")

    def __init__(self):
        # Creating Home Directory
        if not os.path.exists(self.homeDIR):
            os.makedirs(self.homeDIR)
        # Creating MetaData File
        if not os.path.exists(self.globalDataFile):
            fl.Write(self.globalDataFile, js.GlobalJSON(asJSON=True), True)

    def CreateProject(self, projectName, projectDescription):
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        # Creating Directory & File
        try:
            os.makedirs(ProjectPath)
            fl.Write(metaDataFile, js.ProjectJSON(projectName, projectDescription, asJSON=True))
            return "Project '{0}' created successfully !".format(projectName)
        except WindowsError:
            raise err.Conflict("A Project with the name '{0}' already exists !".format(projectName))
        except OSError:
            raise err.Conflict("A Project with the name '{0}' already exists !".format(projectName))
        return None

    def GetProjectList(self):
        return os.listdir(self.homeDIR)

    def GetGlobalVariables(self):
        jsonContent=js.Load(fl.Read(self.globalDataFile))
        return jsonContent["GlobalVariables"]

    def CreateGlobalVariable(self, variableName, variableDescription, variableType, value):
        jsonContent=js.Load(fl.Read(self.globalDataFile))
        for variable in jsonContent["GlobalVariables"]:
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Global Variable with the name '{0}' already exists !".format(variableName))
                return None
        jsonContent["GlobalVariables"].append(js.VariableJSON(variableName, variableDescription, variableType, value, "Static"))
        fl.Write(self.globalDataFile, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)

    def OpenProject(self, projectName):
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        # Opening Project
        try:
            projectData=fl.Read(metaDataFile)
            return js.Load(projectData)
        except IOError:
            raise err.Conflict("Unable to find a Project with the name '{0}'".format(projectName))
        return None

    def GetProjectDescription(self, projectName):
        jsonContent=self.OpenProject(projectName)
        return jsonContent["ProjectDescription"]

    def GetProjectVariables(self, projectName):
        jsonContent=self.OpenProject(projectName)
        return jsonContent["ProjectVariables"]

    def GetTemplateList(self, projectName):
        jsonContent=self.OpenProject(projectName)
        return jsonContent["Templates"]

    def CreateProjectVariable(self, projectName, variableName, variableDescription, variableType, value):
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        jsonContent=js.Load(fl.Read(metaDataFile))
        for variable in jsonContent["ProjectVariables"]:
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Project Variable with the name '{0}' already exists !".format(variableName))
                return None
        jsonContent["ProjectVariables"].append(js.VariableJSON(variableName, variableDescription, variableType, value, "Static"))
        fl.Write(metaDataFile, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)