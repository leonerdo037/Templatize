import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js

class Schema(object):

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    MetaData=None
    Name=None
    Path=None

    def Init(self, Name, projectPath):
        self.Name=Name
        self.Path=os.path.join(projectPath, Name)
        self.MetaData=os.path.join(self.Path, "metadata.json")

    def __Create(self, schemaDescription, groupCount):
        try:
            if self.Open() is not None: 
                raise err.Conflict("A Schema with the name '{0}' already exists !".format(self.Name))
        except err.Conflict as ex:
            if "Unable to find a Project" in str(ex): return None
            if "already exists" in str(ex):
                raise err.Conflict("A Schema with the name '{0}' already exists !".format(self.Name))
                return None
        # Creating Directory & File
        try:
            os.makedirs(self.Path)
            jsonContent=js.Load(fl.Read(self.projectMetaData))
            jsonContent["Schemas"].append(self.Name)
            fl.Write(self.projectMetaData, js.Dump(jsonContent), True)
            # Creating Schema Metadata
            jsonContent=js.SchemaJSON(self.Name, schemaDescription, groupCount)
            fl.Write(self.MetaData, js.Dump(jsonContent), True)
            return "Schema '{0}' created successfully !".format(self.Name)
        except WindowsError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        except OSError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        if os.path.exists(self.Path):
            os.removedirs(self.Path)
        return None

    def Open(self):
        schemas=self.GetSchemaList()
        # Opening Schema
        if self.Name in schemas:
            return js.Load(fl.Read(self.MetaData))
        else:
            raise err.Conflict("Unable to find a Schema with the name '{0}'".format(self.Name))
            return None            

    def GetDescription(self):
        jsonContent=self.Open()
        return jsonContent["SchemaDescription"]

    def GetModuleList(self):
        jsonContent=self.Open()
        return jsonContent["Modules"]

    def GetTemplateList(self):
        jsonContent=self.Open()
        return jsonContent["Templates"]

    def GetGroupCount(self):
        jsonContent=self.Open()
        return jsonContent["GroupCount"]

    def GetVariables(self):
        jsonContent=self.Open()
        return jsonContent["SchemaVariables"]

    def CreateVariable(self, variableName, variableDescription, variableType, variableMode, value=None):
        # Setting Value
        if variableMode != "Static":
            value = None
        jsonContent=self.Open()
        # Validating Uniquness
        if variableName in jsonContent["SchemaVariables"]:
            raise err.Conflict("A Schema Variable with the name '{0}' already exists !".format(variableName))
            return None
        else:
            jsonContent["SchemaVariables"][variableName]=(js.VariableJSON(variableName, variableDescription, variableType, variableMode, value))
            fl.Write(self.MetaData, js.Dump(jsonContent), True)
            return "Variable '{0}' created successfully !".format(variableName)