import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js
from ProjectClass import Project
from SchemaClass import Schema

class Module:

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    moduleName=None
    modulePath=None
    schema=None

    def __init__(self, projectName, schemaName, moduleName):
        self.moduleName=moduleName
        self.schema=Schema(projectName, schemaName)
        self.modulePath=os.path.join(self.schema.schemaPath, moduleName)

    def CreateModule(self, moduleDescription, group, data):
        # Validating Path
        try:
            if self.Open() is not None: 
                raise err.Conflict("A Module with the name '{0}' already exists !".format(self.moduleName))
        except err.Conflict as ex:
            if "Unable to find a Project" in str(ex): return None
            if "Unable to find a Schema" in str(ex): return None
            if "already exists" in str(ex):
                raise err.Conflict("A Module with the name '{0}' already exists !".format(self.moduleName))
                return None
        # Checking Group Count
            groupCount=int(self.schema.GetGroupCount())
            if group > groupCount: 
                raise err.Conflict("Group number '{0}' is greater than the allowed number of '{1}' !".format(group, groupCount))
                return None
        # Creating Directory & File
        try:
            jsonContent=js.Load(fl.Read(self.schema.project.metaDataFile))
            index=js.GetJSONIndex(jsonContent["Schemas"], "SchemaName", self.schema.schemaName)
            jsonContent["Schemas"][int(index[0])]["Modules"].append(js.ModuleJSON(self.moduleName, moduleDescription, group))
            fl.Write(self.schema.project.metaDataFile, js.Dump(jsonContent), True)
            fl.Write(self.modulePath, data, True)
            return "Module '{0}' created successfully !".format(self.moduleName)
        except WindowsError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        except OSError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        if os.path.exists(self.schema.schemaPath):
            os.removedirs(self.schema.schemaPath)
        return None

    def Open(self):
        # Opening Module
        modules=self.schema.GetModuleList()
        moduleData=js.GetJSON(modules, "ModuleName", self.moduleName)
        if moduleData==None:
            raise err.Conflict("Unable to find a Module with the name '{0}'".format(self.moduleName))
            return None
        return js.Load(js.Dump(moduleData[0]))

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
        jsonContent=js.Load(fl.Read(self.schema.project.metaDataFile))
        for variable in self.GetVariables():
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Module Variable with the name '{0}' already exists !".format(variableName))
                return None
        schemaData=js.GetJSON(jsonContent["Schemas"], "SchemaName", self.schema.schemaName)[0]
        schemaIndex=js.GetJSONIndex(jsonContent["Schemas"], "SchemaName", self.schema.schemaName)
        index=js.GetJSONIndex(schemaData["Modules"], "ModuleName", self.moduleName)
        jsonContent["Schemas"][int(schemaIndex[0])]["Modules"][int(index[0])]["ModuleVariables"].append(js.VariableJSON(variableName, variableDescription, variableType, variableMode, value))
        fl.Write(self.schema.project.metaDataFile, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)