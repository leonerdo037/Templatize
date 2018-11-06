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
    MetaDataFile=None
    
    def Init(self, name):
        self.Name=name
        self.Path=os.path.join(self.homeDIR, name)
        self.MetaDataFile=os.path.join(self.Path, "metadata.json")
        self.MetaData=self.Open() # Updating MetaData

    def Exists(self):
        if os.path.exists(self.Path):
            return True
        else:
            return False

    def _Create(self, description):
        # Creating Directory & File
        os.makedirs(self.Path)
        fl.Write(self.MetaDataFile, js.ProjectJSON(self.Name, description, asJSON=True))
        self.MetaData=self.Open() # Updating MetaData
        return "Project '{0}' created successfully !".format(self.Name)

    def CreateVariable(self, variableName, variableDescription, variableType, variableMode, value=None):
        # Validating Variable Type
        if variableMode != "Static" and variableMode != "Runtime":
            raise err.Conflict("A Variable with the mode '{0}' is not support by Projects !".format(variableMode))
            return None
        # Setting Value
        if variableMode != "Static":
            value = None
        jsonContent=js.Load(self.MetaData)
        # Validating Uniquness
        if variableName in jsonContent["ProjectVariables"]:
            raise err.Conflict("A Project Variable with the name '{0}' already exists !".format(variableName))
            return None
        else:
            jsonContent["ProjectVariables"][variableName]=(js.VariableJSON(variableName, variableDescription, variableType, variableMode, value))
            fl.Write(self.MetaDataFile, js.Dump(jsonContent), True)
            self.MetaData=jsonContent # Updating MetaData
            return "Variable '{0}' created successfully !".format(variableName) 

    def Open(self):
        # Opening Project
        projectData=fl.Read(self.MetaDataFile)
        return projectData

    def GetDescription(self):
        jsonContent=js.Load(self.MetaData)
        return jsonContent["ProjectDescription"]

    def GetVariables(self):
        jsonContent=js.Load(self.MetaData)
        return jsonContent["ProjectVariables"]

    def GetSchemaList(self):
        jsonContent=js.Load(self.MetaData)
        return jsonContent["Schemas"]
                