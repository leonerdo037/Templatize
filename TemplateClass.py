import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js
from ProjectClass import Project
from SchemaClass import Schema
from ModuleClass import Module

class Template:

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    templateName=None
    schemaIndex=None
    moduleList=[]
    schema = None

    def __init__(self, projectName, schemaName, templateName):
        self.templateName=templateName
        self.schema=Schema(projectName, schemaName)
        self.moduleList=self.schema.GetModuleList()
        jsonContent=js.Load(fl.Read(self.schema.project.metaDataFile))
        self.schemaIndex=int(js.GetJSONIndex(jsonContent["Schemas"], "SchemaName", schemaName)[0])

    def CreateTemplate(self, templateDescription):
        # Validating Templates
        try:
            if self.Open() is not None:
                raise err.Conflict("A Template with the name '{0}' already exists !".format(self.templateName))
                return None
        except err.Conflict as ex:
            if "Unable to find a Project" in str(ex): return None
            if "Unable to find a Schema" in str(ex): return None
            if "already exists" in str(ex):
                raise err.Conflict("A Template with the name '{0}' already exists !".format(self.templateName))
                return None
        # Creating Template
        jsonContent=js.Load(fl.Read(self.schema.project.metaDataFile))
        jsonContent["Schemas"][self.schemaIndex]["Templates"].append(js.TemplateJSON(self.templateName, templateDescription))
        fl.Write(self.schema.project.metaDataFile, js.Dump(jsonContent), True)
        return "Template '{0}' created successfully !".format(self.templateName)

    def Open(self):
        # Opening Template
        templateData=self.schema.GetTemplateList()
        if js.GetJSON(templateData, "TemplateName", self.templateName)==None:
            raise err.Conflict("Unable to find a Template with the name '{0}'".format(self.templateName))
            return None
        return js.Load(js.Dump(templateData[0]))

    def GetModules(self):
        jsonContent=self.Open()
        return jsonContent["Modules"]

    def AddModules(self, moduleKey, moduleName, ):
        # Validating Module Key
        if js.GetJSON(self.GetModules(), "ModuleKey", moduleKey):
            raise err.Conflict("A Module with the key '{0}' already exists !".format(moduleKey))
            return None
        # Adding Modules to Template
        jsonContent=js.Load(fl.Read(self.schema.project.metaDataFile))
        index=js.GetJSONIndex(jsonContent["Schemas"][self.schemaIndex]["Templates"], "TemplateName", self.templateName)
        jsonContent["Schemas"][self.schemaIndex]["Templates"][int(index[0])]["Modules"].append(js.TemplateModuleJSON(moduleKey, moduleName))
        fl.Write(self.schema.project.metaDataFile, js.Dump(jsonContent), True)
        return "Module '{0}' added successfully !".format(moduleName)
        