import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js
from SchemaClass import Schema
from ModuleClass import Module

class Template(Schema):

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    templateMetaData=None
    templateName=None

    #def __init__(self, projectName, schemaName, templateName):
    #    self.templateName=templateName
    #    super(Template, self).__init__(projectName, schemaName)
    #    self.moduleList=self.GetModuleList()
    #    jsonContent=js.Load(fl.Read(self.projectMetaData))
    #    self.schemaIndex=int(js.GetJSONIndex(jsonContent["Schemas"], "SchemaName", schemaName)[0])
    def ValidateArgs(self):
        if self.moduleName==None:
            raise err.Conflict("Template arguments are missing !")
            return None

    @classmethod
    def InitTemplate(self, projectName=None, schemaName=None, templateName=None):
        self.templateName=templateName
        super(Template, self).InitSchema(projectName, schemaName)
        self.templateMetaData=os.path.join(self.schemaPath, self.templateName + ".json")

    def CreateTemplate(self, templateDescription):
        self.ValidateArgs()
        # Validating Templates
        try:
            if self.OpenTemplate() is not None:
                raise err.Conflict("A Template with the name '{0}' already exists !".format(self.templateName))
                return None
        except err.Conflict as ex:
            if "Unable to find a Project" in str(ex): return None
            if "Unable to find a Schema" in str(ex): return None
            if "already exists" in str(ex):
                raise err.Conflict("A Template with the name '{0}' already exists !".format(self.templateName))
                return None
        # Creating Template
        try:
            jsonContent=js.Load(fl.Read(self.schemaMetaData))
            jsonContent["Templates"].append(self.templateName)
            fl.Write(self.schemaMetaData, js.Dump(jsonContent), True)
            fl.Write(self.templateMetaData, "", True)
            return "Template '{0}' created successfully !".format(self.templateName)
        except WindowsError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        except OSError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        if os.path.exists(self.templateMetaData):
            os.remove(self.templateMetaData)
        return None

    def OpenTemplate(self):
        self.ValidateArgs()
        # Opening Template
        templates=self.GetTemplateList()
        if self.templateName in templates:
            return fl.Read(self.templateMetaData)
        else:
            raise err.Conflict("Unable to find a Template with the name '{0}'".format(self.templateName))
            return None

    def GetTemplateModules(self):
        jsonContent=self.OpenTemplate()
        return jsonContent["Modules"]

    def AddModules(self, moduleKey, moduleName):
        self.ValidateArgs()
        # Validating Module Key
        if js.GetJSON(self.GetTemplateModules(), "ModuleKey", moduleKey):
            raise err.Conflict("A Module with the key '{0}' already exists !".format(moduleKey))
            return None
        # Adding Modules to Template
        jsonContent=js.Load(fl.Read(self.projectMetaData))
        index=js.GetJSONIndex(jsonContent["Schemas"][self.schemaIndex]["Templates"], "TemplateName", self.templateName)
        jsonContent["Schemas"][self.schemaIndex]["Templates"][int(index[0])]["Modules"].append(js.TemplateModuleJSON(moduleKey, moduleName))
        fl.Write(self.projectMetaData, js.Dump(jsonContent), True)
        return "Module '{0}' added successfully !".format(moduleName)

    def GenerateVariables(self):
        self.ValidateArgs()
        output=[]
        output.append(self.GetProjectVariables())
        output.append(self.GetSchemaVariables())
        for tModule in self.GetTemplateModules():
            tModule=js.Load(js.Dump(tModule))
            module=Module(self.projectName, self.schemaName, tModule["ModuleName"])
            output.append(module.GetModuleVariables())
        fl.Write(os.path.join(self.schemaPath, self.templateName + ".json"), js.Dump(output), True)