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

    def __init__(self, projectName, schemaName, moduleName):
        self.moduleName=moduleName
        super(Module, self).__init__(projectName, schemaName)
        self.modulePath=os.path.join(self.schemaPath, moduleName)

    def CreateModule(self, moduleDescription, group, data):
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
            jsonContent=js.Load(fl.Read(self.metaDataFile))
            index=js.GetJSONIndex(jsonContent["Schemas"], "SchemaName", self.schemaName)
            jsonContent["Schemas"][int(index[0])]["Modules"].append(js.ModuleJSON(self.moduleName, moduleDescription, group))
            fl.Write(self.metaDataFile, js.Dump(jsonContent), True)
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
        # Opening Module
        modules=self.GetModuleList()
        moduleData=js.GetJSON(modules, "ModuleName", self.moduleName)
        if moduleData==None:
            raise err.Conflict("Unable to find a Module with the name '{0}'".format(self.moduleName))
            return None
        return js.Load(js.Dump(moduleData[0]))

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
        # Validating Variable Type
        if variableMode == "Internal":
            raise err.Conflict("A Variable with the mode '{0}' is not support by Modules !".format(variableMode))
            return None
        # Setting Value
        if variableMode != "Static":
            value = None
        jsonContent=js.Load(fl.Read(self.metaDataFile))
        for variable in self.GetModuleVariables():
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Module Variable with the name '{0}' already exists !".format(variableName))
                return None
        schemaData=js.GetJSON(jsonContent["Schemas"], "SchemaName", self.schemaName)[0]
        schemaIndex=js.GetJSONIndex(jsonContent["Schemas"], "SchemaName", self.schemaName)
        index=js.GetJSONIndex(schemaData["Modules"], "ModuleName", self.moduleName)
        jsonContent["Schemas"][int(schemaIndex[0])]["Modules"][int(index[0])]["ModuleVariables"].append(js.VariableJSON(variableName, variableDescription, variableType, variableMode, value))
        fl.Write(self.metaDataFile, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)