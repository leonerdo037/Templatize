import os
import logging
import Errors as err
from ProjectClass import Project
from SchemaClass import Schema
from ModuleClass import Module
from TemplateClass import Template

class Templatize(Module, Template):

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")

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
proj=Project()
proj.InitProject("Hello Universe")
#proj.CreateProject("Test Project")
proj.CreateProjectVariable("Two", "Test Variable", "String", "Runtime", "Dummy")
#print(temp.InitModule("Hello Universe", "Azure", "Storage"))
#print(temp.GetModuleVariables())