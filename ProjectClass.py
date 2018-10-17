import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js

class Project(object):

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    projectName=None
    projectPath=None
    metaDataFile=None

    #def __init__(self, projectName):
    #    self.projectName=projectName
    #    self.projectPath=os.path.join(self.homeDIR, projectName)
    #    self.metaDataFile=os.path.join(self.projectPath, "metadata.json")

    def ValidateArgs(self):
        if self.projectName==None:
            raise err.Conflict("Project arguments are missing !")
            return None

    @classmethod
    def InitProject(self, projectName=None):
        self.projectName=projectName
        self.projectPath=os.path.join(self.homeDIR, projectName)
        self.metaDataFile=os.path.join(self.projectPath, "metadata.json")

    def CreateProject(self, projectDescription):
        self.ValidateArgs()
        # Creating Directory & File
        try:
            os.makedirs(self.projectPath)
            fl.Write(self.metaDataFile, js.ProjectJSON(self.projectName, projectDescription, asJSON=True))
            return "Project '{0}' created successfully !".format(self.projectName)
        except WindowsError or OSError:
            raise err.Conflict("A Project with the name '{0}' already exists !".format(self.projectName))
        return None


    def OpenProject(self):
        self.ValidateArgs()
        # Opening Project
        try:
            projectData=fl.Read(self.metaDataFile)
            return js.Load(projectData)
        except IOError:
            raise err.Conflict("Unable to find a Project with the name '{0}'".format(self.projectName))
        return None

    def GetProjectDescription(self):
        jsonContent=self.OpenProject()
        return jsonContent["ProjectDescription"]

    def GetProjectVariables(self):
        jsonContent=self.OpenProject()
        return jsonContent["ProjectVariables"]

    def GetSchemaList(self):
        jsonContent=self.OpenProject()
        return jsonContent["Schemas"]

    def CreateProjectVariable(self, variableName, variableDescription, variableType, variableMode, value=None):
        self.ValidateArgs()
        # Validating Variable Type
        if variableMode != "Static" and variableMode != "Runtime":
            raise err.Conflict("A Variable with the mode '{0}' is not support by Projects !".format(variableMode))
            return None
        # Setting Value
        if variableMode != "Static":
            value = None
        jsonContent=js.Load(fl.Read(self.metaDataFile))
        for variable in jsonContent["ProjectVariables"]:
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Project Variable with the name '{0}' already exists !".format(variableName))
                return None
        jsonContent["ProjectVariables"].append(js.VariableJSON(variableName, variableDescription, variableType, variableMode, value))
        fl.Write(self.metaDataFile, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)