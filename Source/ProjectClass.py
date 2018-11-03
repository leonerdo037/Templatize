import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js

class Project(object):

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    Name=None
    Path=None
    MetaData=None
    
    def Init(self, name):
        self.Name=name
        self.Path=os.path.join(self.homeDIR, name)
        self.MetaData=os.path.join(self.Path, "metadata.json")

    def Exists(self):
        if os.path.exists(self.Path):
            return True
        else:
            return False

    def _Create(self, description):
        # Creating Directory & File
        os.makedirs(self.Path)
        fl.Write(self.MetaData, js.ProjectJSON(self.Name, description, asJSON=True))
        return "Project '{0}' created successfully !".format(self.Name)

    def Open(self):
        # Opening Project
        projectData=fl.Read(self.MetaData)
        return js.Load(projectData)

    def GetDescription(self):
        jsonContent=self.Open()
        return jsonContent["ProjectDescription"]

    def GetVariables(self):
        jsonContent=self.Open()
        return jsonContent["ProjectVariables"]

    def GetSchemaList(self):
        jsonContent=self.Open()
        return jsonContent["Schemas"]

    def CreateVariable(self, variableName, variableDescription, variableType, variableMode, value=None):
        # Validating Variable Type
        if variableMode != "Static" and variableMode != "Runtime":
            raise err.Conflict("A Variable with the mode '{0}' is not support by Projects !".format(variableMode))
            return None
        # Setting Value
        if variableMode != "Static":
            value = None
        jsonContent=self.Open()
        # Validating Uniquness
        if variableName in jsonContent["ProjectVariables"]:
            raise err.Conflict("A Project Variable with the name '{0}' already exists !".format(variableName))
            return None
        else:
            jsonContent["ProjectVariables"][variableName]=(js.VariableJSON(variableName, variableDescription, variableType, variableMode, value))
            fl.Write(self.MetaData, js.Dump(jsonContent), True)
            return "Variable '{0}' created successfully !".format(variableName)         
                