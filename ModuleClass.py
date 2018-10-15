import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js
from ProjectClass import Project
from SchemaClass import Schema

class Module:

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    schema=Schema()

    def CreateModule(self, projectName, schemaName, moduleName, moduleDescription, group, data):
        # Checking Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        SchemaPath=os.path.join(ProjectPath, schemaName)
        ModulePath=os.path.join(SchemaPath, moduleName)
        # Validating Path
        try:
            if self.OpenModule(projectName, schemaName, moduleName) is not None: 
                raise err.Conflict("A Module with the name '{0}' already exists !".format(moduleName))
        except err.Conflict as ex:
            if "Unable to find a Project" in str(ex): return None
            if "Unable to find a Schema" in str(ex): return None
            if "already exists" in str(ex):
                raise err.Conflict("A Module with the name '{0}' already exists !".format(moduleName))
                return None
        # Checking Group Count
            groupCount=int(self.schema.GetSchemaGroupCount(projectName, schemaName))
            if group > groupCount: 
                raise err.Conflict("Group number '{0}' is greater than the allowed number of '{1}' !".format(group, groupCount))
                return None
        # Creating Directory & File
        try:
            jsonContent=js.Load(fl.Read(metaDataFile))
            index=js.GetJSONIndex(jsonContent["Schemas"], "SchemaName", schemaName)
            jsonContent["Schemas"][int(index[0])]["Modules"].append(js.ModuleJSON(moduleName, moduleDescription, group))
            fl.Write(metaDataFile, js.Dump(jsonContent), True)
            fl.Write(ModulePath, data, True)
            return "Module '{0}' created successfully !".format(moduleName)
        except WindowsError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        except OSError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        if os.path.exists(SchemaPath):
            os.removedirs(SchemaPath)
        return None

    def OpenModule(self, projectName, schemaName, moduleName):
        # Checking Project Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        SchemaPath=os.path.join(ProjectPath, schemaName)
        ModulePath=os.path.join(SchemaPath, moduleName)
        # Opening Module
        modules=self.schema.GetModuleList(projectName, schemaName)
        moduleData=js.GetJSON(modules, "ModuleName", moduleName)
        if moduleData==None:
            raise err.Conflict("Unable to find a Module with the name '{0}'".format(moduleName))
            return None
        return js.Load(js.Dump(moduleData[0]))

    def GetModuleDescription(self, projectName, schemaName, moduleName):
        jsonContent=self.OpenModule(projectName, schemaName, moduleName)
        return jsonContent["ModuleDescription"]

    def GetModuleGroup(self, projectName, schemaName, moduleName):
        jsonContent=self.OpenModule(projectName, schemaName, moduleName)
        return jsonContent["Group"]

    def GetModuleVariables(self, projectName, schemaName, moduleName):
        jsonContent=self.OpenModule(projectName, schemaName, moduleName)
        return jsonContent["ModuleVariables"]

    def CreateModuleVariable(self, projectName, schemaName, moduleName, variableName, variableDescription, variableType, variableMode, value=None):
        # Validating Variable Type
        if variableMode == "Internal":
            raise err.Conflict("A Variable with the mode '{0}' is not support by Modules !".format(variableMode))
            return None
        # Setting Value
        if variableMode != "Static":
            value = None
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        jsonContent=js.Load(fl.Read(metaDataFile))
        for variable in self.GetModuleVariables(projectName, schemaName, moduleName):
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Module Variable with the name '{0}' already exists !".format(variableName))
                return None
        schemaData=js.GetJSON(jsonContent["Schemas"], "SchemaName", schemaName)[0]
        schemaIndex=js.GetJSONIndex(jsonContent["Schemas"], "SchemaName", schemaName)
        index=js.GetJSONIndex(schemaData["Modules"], "ModuleName", moduleName)
        jsonContent["Schemas"][int(schemaIndex[0])]["Modules"][int(index[0])]["ModuleVariables"].append(js.VariableJSON(variableName, variableDescription, variableType, variableMode, value))
        fl.Write(metaDataFile, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)