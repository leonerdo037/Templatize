import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js

class Template(object):

    Name=None
    MetaData=None
    SchemaMetaData=None
    ProjectVaraibles=None
    SchemaVariables=None

    def Init(self, name, schemaPath, projectVariables, schemaVariables):
        self.Name=name
        self.MetaData=os.path.join(schemaPath, name + ".json")
        self.SchemaMetaData=os.path.join(schemaPath, "metadata.json")
        self.ProjectVaraibles=projectVariables
        self.SchemaVariables=schemaVariables

    def Exists(self):
        if os.path.exists(self.MetaData):
            return True
        else:
            return False

    def _Create(self, description):
        # Creating Template
        try:
            jsonContent=js.Load(fl.Read(self.SchemaMetaData))
            jsonContent["Templates"].append(self.Name)
            fl.Write(self.SchemaMetaData, js.Dump(jsonContent), True)
            jsonContent=js.TemplateJSON(self.Name, description, True)
            fl.Write(self.MetaData, jsonContent, True)
            return "Template '{0}' created successfully !".format(self.Name)
        except WindowsError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        except OSError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        if os.path.exists(self.MetaData):
            os.remove(self.MetaData)
        return None

    def Open(self):
        return js.Load(fl.Read(self.MetaData))

    def GetTemplateModules(self):
        jsonContent=self.Open()
        print(jsonContent["Modules"])
        return jsonContent["Modules"]

    def GetTemplateVariables(self):
        jsonContent=self.Open()
        return jsonContent["Variables"]

    def AddModules(self, moduleKey, moduleName):
        # Validating Module Key
        if moduleKey in self.GetTemplateModules():
            raise err.Conflict("A Module with the key '{0}' already exists !".format(moduleKey))
            return None           
        # Adding Modules to Template
        jsonContent=self.Open()
        jsonContent["Modules"][moduleKey]=js.TemplateModuleJSON(moduleKey, moduleName)
        fl.Write(self.MetaData, js.Dump(jsonContent), True)
        return "Module '{0}' added successfully !".format(moduleName)

    def GenerateVariables(self):
        output=[]
        output.append(self.GetProjectVariables())
        output.append(self.GetSchemaVariables())
        for tModule in self.GetTemplateModules():
            tModule=js.Load(js.Dump(tModule))
            module=Module(self.projectName, self.schemaName, tModule["ModuleName"])
            output.append(module.GetModuleVariables())
        fl.Write(os.path.join(self.schemaPath, self.Name + ".json"), js.Dump(output), True)