import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js
from ProjectClass import Project

class Schema(Project):

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    schemaMetaData=None
    schemaName=None
    schemaPath=None

    #def __init__(self, projectName, schemaName):
    #    self.schemaName=schemaName
    #    super(Schema, self).__init__(projectName)
    #    self.schemaPath=os.path.join(self.projectPath, schemaName)

    def __ValidateArgs(self):
        if self.schemaName==None:
            raise err.Conflict("Schema arguments are missing !")
            return None

    @classmethod
    def InitSchema(self, projectName=None, schemaName=None):
        self.schemaName=schemaName
        super(Schema, self).InitProject(projectName)
        self.schemaPath=os.path.join(self.projectPath, schemaName)
        self.schemaMetaData=os.path.join(self.schemaPath, "metadata.json")

    def CreateSchema(self, schemaDescription, groupCount):
        self.__ValidateArgs()
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
            jsonContent=js.Load(fl.Read(self.projectMetaData))
            jsonContent["Schemas"].append(self.schemaName)
            fl.Write(self.projectMetaData, js.Dump(jsonContent), True)
            # Creating Schema Metadata
            jsonContent=js.SchemaJSON(self.schemaName, schemaDescription, groupCount)
            fl.Write(self.schemaMetaData, js.Dump(jsonContent), True)
            return "Schema '{0}' created successfully !".format(self.schemaName)
        except WindowsError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        except OSError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        if os.path.exists(self.schemaPath):
            os.removedirs(self.schemaPath)
        return None

    def OpenSchema(self):
        self.__ValidateArgs()
        schemas=self.GetSchemaList()
        # Opening Schema
        if self.schemaName in schemas:
            return js.Load(fl.Read(self.schemaMetaData))
        else:
            raise err.Conflict("Unable to find a Schema with the name '{0}'".format(self.schemaName))
            return None            

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
        self.__ValidateArgs()
        # Setting Value
        if variableMode != "Static":
            value = None
        jsonContent=self.OpenSchema()
        # Validating Uniquness
        if variableName in jsonContent["SchemaVariables"]:
            raise err.Conflict("A Schema Variable with the name '{0}' already exists !".format(variableName))
            return None
        else:
            jsonContent["SchemaVariables"][variableName]=(js.VariableJSON(variableName, variableDescription, variableType, variableMode, value))
            fl.Write(self.schemaMetaData, js.Dump(jsonContent), True)
            return "Variable '{0}' created successfully !".format(variableName)