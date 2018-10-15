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
    projectName=None
    schemaName=None
    ProjectPath=None
    metaDataFile=None
    schemaIndex=None
    moduleList=[]
    project = Project()
    schema = Schema()
    module = Module()

    def __init__(self, projectName, schemaName):
        self.projectName=projectName
        self.schemaName=schemaName
        self.ProjectPath=os.path.join(self.homeDIR, projectName)
        self.metaDataFile=os.path.join(self.ProjectPath, "metadata.json")
        self.moduleList=self.schema.GetModuleList(projectName, schemaName)
        jsonContent=js.Load(fl.Read(self.metaDataFile))
        self.schemaIndex=int(js.GetJSONIndex(jsonContent["Schemas"], "SchemaName", schemaName)[0])

    def CreateTemplate(self, templateName, templateDescription):
        # Validating Templates
        try:
            if self.OpenTemplate(templateName) is not None:
                raise err.Conflict("A Template with the name '{0}' already exists !".format(templateName))
                return None
        except err.Conflict as ex:
            if "Unable to find a Project" in str(ex): return None
            if "Unable to find a Schema" in str(ex): return None
            if "already exists" in str(ex):
                raise err.Conflict("A Template with the name '{0}' already exists !".format(templateName))
                return None
        # Creating Template
        jsonContent=js.Load(fl.Read(self.metaDataFile))
        jsonContent["Schemas"][self.schemaIndex]["Templates"].append(js.TemplateJSON(templateName, templateDescription))
        fl.Write(self.metaDataFile, js.Dump(jsonContent), True)
        return "Template '{0}' created successfully !".format(templateName)

    def OpenTemplate(self, templateName):
        # Opening Template
        templateData=self.schema.GetTemplateList(self.projectName, self.schemaName)
        if js.GetJSON(templateData, "TemplateName", templateName)==None:
            raise err.Conflict("Unable to find a Template with the name '{0}'".format(templateName))
            return None
        return js.Load(js.Dump(templateData[0]))

    def GetTemplateModules(self, templateName):
        jsonContent=self.OpenTemplate(templateName)
        return jsonContent["Modules"]

    def AddModules(self, templateName, moduleKey, moduleName, ):
        # Validating Module Key
        if js.GetJSON(self.GetTemplateModules(templateName), "ModuleKey", moduleKey):
            raise err.Conflict("A Module with the key '{0}' already exists !".format(moduleKey))
            return None
        # Adding Modules to Template
        jsonContent=js.Load(fl.Read(self.metaDataFile))
        index=js.GetJSONIndex(jsonContent["Schemas"][self.schemaIndex]["Templates"], "TemplateName", templateName)
        jsonContent["Schemas"][self.schemaIndex]["Templates"][int(index[0])]["Modules"].append(js.TemplateModuleJSON(moduleKey, moduleName))
        fl.Write(self.metaDataFile, js.Dump(jsonContent), True)
        return "Module '{0}' added successfully !".format(moduleName)
        