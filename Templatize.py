import os
import logging
import Errors as err
from ProjectClass import Project
from SchemaClass import Schema
from ModuleClass import Module
from TemplateClass import Template

class Templatize(Module, Template):

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    project=None
    schema=None
    module=None
    template=None

    def __init__(self):
        # Creating Home Directory
        if not os.path.exists(self.homeDIR):
            os.makedirs(self.homeDIR)

    def InitProject(self, projectName=None):
        return super(Templatize, self).InitProject(projectName)

    def InitSchema(self, projectName=None, schemaName=None):
        return super(Templatize, self).InitSchema(projectName, schemaName)

    def InitModule(self, projectName=None, schemaName=None, moduleName=None):
        return super(Templatize, self).InitModule(projectName, schemaName, moduleName)

    def InitTemplate(self, projectName=None, schemaName=None, templateName=None):
        return super(Templatize, self).InitTemplate(projectName, schemaName, templateName)

    def GetProjectList(self):
        return os.listdir(self.homeDIR)

temp=Templatize()
temp.InitProject("Hello Universe")
temp.InitSchema("Hello Universe", "Azure")
#temp.CreateSchema("Test Schema", 3)
temp.InitModule("Hello Universe", "Azure", "DiskTest")
#temp.CreateModule("Test Module", 3, "Data")
temp.CreateModuleVariable("Disk2","Test Variable", "Number", "Runtime")
#temp.CreateSchemaVariable("Disk2","Test Variable", "Number", "Internal")
#temp.CreateProject("Test Project")
#proj.CreateProject("Test Project")
#print(temp.InitModule("Hello Universe", "Azure", "Storage"))
#print(temp.GetModuleVariables())