import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js
from ProjectClass import Project

class Schema:

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    project = Project()

    def CreateSchema(self, projectName, schemaName, schemaDescription, groupCount):
        # Checking Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        SchemaPath=os.path.join(ProjectPath, schemaName)
        # Validating Path
        try:
            if self.OpenSchema(projectName, schemaName) is not None: 
                raise err.Conflict("A Schema with the name '{0}' already exists !".format(schemaName))
        except err.Conflict as ex:
            if "Unable to find a Project" in str(ex): return None
            if "already exists" in str(ex):
                raise err.Conflict("A Schema with the name '{0}' already exists !".format(schemaName))
                return None
        # Creating Directory & File
        try:
            os.makedirs(SchemaPath)
            jsonContent=js.Load(fl.Read(metaDataFile))
            jsonContent["Schemas"].append(js.SchemaJSON(schemaName, schemaDescription, groupCount))
            fl.Write(metaDataFile, js.Dump(jsonContent), True)
            return "Schema '{0}' created successfully !".format(schemaName)
        except WindowsError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        except OSError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        if os.path.exists(SchemaPath):
            os.removedirs(SchemaPath)
        return None

    def OpenSchema(self, projectName, schemaName):
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        SchemaPath=os.path.join(ProjectPath, schemaName)
        # Opening Schema
        schemas=self.project.GetSchemaList(projectName)
        schemaData=js.GetJSON(schemas, "SchemaName", schemaName)
        if schemaData==None:
            raise err.Conflict("Unable to find a Schema with the name '{0}'".format(schemaName))
            return None
        return js.Load(js.Dump(schemaData[0]))

    def GetSchemaDescription(self, projectName, schemaName):
        jsonContent=self.OpenSchema(projectName, schemaName)
        return jsonContent["SchemaDescription"]

    def GetModuleList(self, projectName, schemaName):
        jsonContent=self.OpenSchema(projectName, schemaName)
        return jsonContent["Modules"]

    def GetSchemaGroupCount(self, projectName, schemaName):
        jsonContent=self.OpenSchema(projectName, schemaName)
        return jsonContent["GroupCount"]

    def GetSchemaVariables(self, projectName, schemaName):
        jsonContent=self.OpenSchema(projectName, schemaName)
        return jsonContent["SchemaVariables"]

    def CreateSchemaVariable(self, projectName, schemaName, variableName, variableDescription, variableType):
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        jsonContent=js.Load(fl.Read(metaDataFile))
        for variable in self.GetSchemaVariables(projectName, schemaName):
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Schema Variable with the name '{0}' already exists !".format(variableName))
                return None
        index=js.GetJSONIndex(jsonContent["Schemas"], "SchemaName", schemaName)
        jsonContent["Schemas"][int(index[0])]["SchemaVariables"].append(js.VariableJSON(variableName, variableDescription, variableType))
        fl.Write(metaDataFile, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)