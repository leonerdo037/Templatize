import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js

class Module(object):

    Name=None
    Path=None
    SchemaMetaData=None

    def Init(self, name, schemaPath):
        self.Name=name
        self.Path=os.path.join(schemaPath, name)
        self.SchemaMetaData=os.path.join(schemaPath, "metadata.json")

    def Exists(self):
        try:
            self.Open()
            return True
        except:
            return False

    def _Create(self, description, group, groupCount, data):
        # Checking Group Count
        if group > groupCount:
            raise err.Conflict("Group number '{0}' is greater than the allowed number of '{1}' !".format(group, groupCount))
            return None
        # Creating Directory & File
        try:
            jsonContent=js.Load(fl.Read(self.SchemaMetaData))
            jsonContent["Modules"][self.Name]=js.ModuleJSON(self.Name, description, group)
            fl.Write(self.SchemaMetaData, js.Dump(jsonContent), True)
            fl.Write(self.Path, data, True)
            return "Module '{0}' created successfully !".format(self.Name)
        except WindowsError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        except OSError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        if os.path.exists(self.schemaPath):
            os.removedirs(self.schemaPath)
        return None

    def Open(self):
        # Opening Module
        return js.Load(fl.Read(self.SchemaMetaData))["Modules"][self.Name]

    def GetDescription(self):
        jsonContent=self.Open()
        return jsonContent["ModuleDescription"]

    def GetGroup(self):
        jsonContent=self.Open()
        return jsonContent["Group"]

    def GetVariables(self):
        jsonContent=self.Open()
        return jsonContent["ModuleVariables"]

    def CreateVariable(self, variableName, variableDescription, variableType, variableMode, value=None):
        # Validating Variable Type
        if variableMode == "Internal":
            raise err.Conflict("A Variable with the mode '{0}' is not support by Modules !".format(variableMode))
            return None
        # Setting Value
        if variableMode != "Static":
            value = None
        jsonContent=self.Open()
        # Validating Uniquness
        if variableName in jsonContent["ModuleVariables"]:
            raise err.Conflict("A Module Variable with the name '{0}' already exists !".format(variableName))
            return None
        else:
            jsonContent=js.Load(fl.Read(self.SchemaMetaData))
            jsonContent["Modules"][self.Name]["ModuleVariables"][variableName]=(js.VariableJSON(variableName, variableDescription, variableType, variableMode, value))
            fl.Write(self.SchemaMetaData, js.Dump(jsonContent), True)
            return "Variable '{0}' created successfully !".format(variableName)