import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js
from ProjectClass import Project

class Schema(Project):

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    schemaName=None
    schemaPath=None

    def __init__(self, projectName, schemaName):
        self.schemaName=schemaName
        super(Schema, self).__init__(projectName)
        self.schemaPath=os.path.join(self.projectPath, schemaName)

    def CreateSchema(self, schemaDescription, groupCount):
        try:
            if self.OpenSchema() is not None: 
                raise err.Conflict("A Schema with the name '{0}' already exists !".format(self.schemaName))
        except err.Conflict as ex:
            if "Unable to find a Project" in str(ex): return None
            if "already exists" in str(ex):
                raise err.Conflict("A Schema with the name '{0}' already exists !".format(self.schemaName))
                return None
        # Creating Directory & File
        try:
            os.makedirs(self.schemaPath)
            jsonContent=js.Load(fl.Read(self.metaDataFile))
            jsonContent["Schemas"].append(js.SchemaJSON(self.schemaName, schemaDescription, groupCount))
            fl.Write(self.metaDataFile, js.Dump(jsonContent), True)
            return "Schema '{0}' created successfully !".format(self.schemaName)
        except WindowsError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        except OSError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        if os.path.exists(self.schemaPath):
            os.removedirs(self.schemaPath)
        return None

    def OpenSchema(self):
        # Opening Schema
        schemas=self.GetSchemaList()
        schemaData=js.GetJSON(schemas, "SchemaName", self.schemaName)
        if schemaData==None:
            raise err.Conflict("Unable to find a Schema with the name '{0}'".format(self.schemaName))
            return None
        return js.Load(js.Dump(schemaData[0]))

    def GetSchemaDescription(self):
        jsonContent=self.OpenSchema()
        return jsonContent["SchemaDescription"]

    def GetModuleList(self):
        jsonContent=self.OpenSchema()
        return jsonContent["Modules"]

    def GetTemplateList(self):
        jsonContent=self.OpenSchema()
        return jsonContent["Templates"]

    def GetGroupCount(self):
        jsonContent=self.OpenSchema()
        return jsonContent["GroupCount"]

    def GetSchemaVariables(self):
        jsonContent=self.OpenSchema()
        return jsonContent["SchemaVariables"]

    def CreateSchemaVariable(self, variableName, variableDescription, variableType, variableMode, value=None):
        # Setting Value
        if variableMode != "Static":
            value = None
        jsonContent=js.Load(fl.Read(self.metaDataFile))
        for variable in self.GetSchemaVariables():
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Schema Variable with the name '{0}' already exists !".format(variableName))
                return None
        index=js.GetJSONIndex(jsonContent["Schemas"], "SchemaName", self.schemaName)
        jsonContent["Schemas"][int(index[0])]["SchemaVariables"].append(js.VariableJSON(variableName, variableDescription, variableType, variableMode, value))
        fl.Write(self.metaDataFile, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)