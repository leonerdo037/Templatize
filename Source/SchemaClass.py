import os
import shutil
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js

class Schema(object):

    Name=None
    Path=None
    MetaDataFile=None
    ProjectMetaData=None

    def Init(self, name, projectPath):
        self.Name=name
        self.Path=os.path.join(projectPath, name)
        self.ProjectMetaData=os.path.join(projectPath, "metadata.json")
        self.MetaDataFile=os.path.join(self.Path, "metadata.json")

    def Exists(self):
        if os.path.exists(self.Path):
            return True
        else:
            return False

    def _Create(self, description, groupCount):
        # Creating Directory & File
        try:
            os.makedirs(self.Path)
            jsonContent=js.Load(fl.Read(self.ProjectMetaData))
            jsonContent["Schemas"].append(self.Name)
            fl.Write(self.ProjectMetaData, js.Dump(jsonContent), True)
            # Creating Schema Metadata
            jsonContent=js.SchemaJSON(self.Name, description, groupCount)
            fl.Write(self.MetaDataFile, js.Dump(jsonContent), True)
            return "Schema '{0}' created successfully !".format(self.Name)
        except WindowsError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        except OSError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        if os.path.exists(self.Path):
            os.removedirs(self.Path)

    def CreateVariable(self, variableName, variableDescription, variableType, variableMode, value=None):
        # Setting Value
        if variableMode != "Static":
            value = None
        jsonContent=js.Load(self.Open())
        # Validating Uniquness
        if variableName in jsonContent["SchemaVariables"]:
            raise err.Conflict("A Schema Variable with the name '{0}' already exists !".format(variableName))
            return None
        else:
            jsonContent["SchemaVariables"][variableName]=(js.VariableJSON(variableName, variableDescription, variableType, variableMode, value))
            fl.Write(self.MetaDataFile, js.Dump(jsonContent), True)
            return "Variable '{0}' created successfully !".format(variableName)

    def Open(self):
        return fl.Read(self.MetaDataFile)

    def GetDescription(self):
        jsonContent=js.Load(self.Open())
        return jsonContent["SchemaDescription"]

    def GetModuleList(self):
        jsonContent=js.Load(self.Open())
        return jsonContent["Modules"]

    def GetTemplateList(self):
        jsonContent=js.Load(self.Open())
        return jsonContent["Templates"]

    def GetGroupCount(self):
        jsonContent=js.Load(self.Open())
        return jsonContent["GroupCount"]

    def GetVariables(self):
        jsonContent=js.Load(self.Open())
        return jsonContent["SchemaVariables"]

    def Delete(self):
        jsonContent=js.Load(fl.Read(self.ProjectMetaData))
        jsonContent["Schemas"].remove(self.Name)
        fl.Write(self.ProjectMetaData, js.Dump(jsonContent), True)
        shutil.rmtree(self.Path)