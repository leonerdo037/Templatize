import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js
from SchemaClass import Schema

class Module(Schema):

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    moduleName=None
    modulePath=None

    #def __init__(self, projectName, schemaName, moduleName):
    #    self.moduleName=moduleName
    #    super(Module, self).__init__(projectName, schemaName)
    #    self.modulePath=os.path.join(self.schemaPath, moduleName)
    def __ValidateArgs(self):
        if self.moduleName==None:
            raise err.Conflict("Module arguments are missing !")
            return None

    @classmethod
    def InitModule(self, projectName=None, schemaName=None, moduleName=None):
        self.moduleName=moduleName
        super(Module, self).InitSchema(projectName, schemaName)
        self.modulePath=os.path.join(self.schemaPath, moduleName)

    def CreateModule(self, moduleDescription, group, data):
        self.__ValidateArgs()
        # Validating Path
        try:
            if self.OpenModule() is not None:
                raise err.Conflict("A Module with the name '{0}' already exists !".format(self.moduleName))
        except err.Conflict as ex:
            if "Unable to find a Project" in str(ex): return None
            if "Unable to find a Schema" in str(ex): return None
            if "already exists" in str(ex):
                raise err.Conflict("A Module with the name '{0}' already exists !".format(self.moduleName))
                return None
        # Checking Group Count
            groupCount=int(self.GetGroupCount())
            if group > groupCount: 
                raise err.Conflict("Group number '{0}' is greater than the allowed number of '{1}' !".format(group, groupCount))
                return None
        # Creating Directory & File
        try:
            jsonContent=js.Load(fl.Read(self.schemaMetaData))
            jsonContent["Modules"][self.moduleName]=js.ModuleJSON(self.moduleName, moduleDescription, group)
            fl.Write(self.schemaMetaData, js.Dump(jsonContent), True)
            fl.Write(self.modulePath, data, True)
            return "Module '{0}' created successfully !".format(self.moduleName)
        except WindowsError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        except OSError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        if os.path.exists(self.schemaPath):
            os.removedirs(self.schemaPath)
        return None

    def OpenModule(self):
        self.__ValidateArgs()
        # Opening Module
        modules=self.GetModuleList()
        if self.moduleName in modules:
            return js.Load(fl.Read(self.schemaMetaData))["Modules"][self.moduleName]
        else:
            raise err.Conflict("Unable to find a Module with the name '{0}'".format(self.moduleName))
            return None

    def GetModuleDescription(self):
        jsonContent=self.OpenModule()
        return jsonContent["ModuleDescription"]

    def GetModuleGroup(self):
        jsonContent=self.OpenModule()
        return jsonContent["Group"]

    def GetModuleVariables(self):
        jsonContent=self.OpenModule()
        return jsonContent["ModuleVariables"]

    def CreateModuleVariable(self, variableName, variableDescription, variableType, variableMode, value=None):
        self.__ValidateArgs()
        # Validating Variable Type
        if variableMode == "Internal":
            raise err.Conflict("A Variable with the mode '{0}' is not support by Modules !".format(variableMode))
            return None
        # Setting Value
        if variableMode != "Static":
            value = None
        jsonContent=self.OpenModule()
        # Validating Uniquness
        if variableName in jsonContent["ModuleVariables"]:
            raise err.Conflict("A Module Variable with the name '{0}' already exists !".format(variableName))
            return None
        else:
            jsonContent=self.OpenSchema()
            jsonContent["Modules"][self.moduleName]["ModuleVariables"][variableName]=(js.VariableJSON(variableName, variableDescription, variableType, variableMode, value))
            fl.Write(self.schemaMetaData, js.Dump(jsonContent), True)
            return "Variable '{0}' created successfully !".format(variableName)