import os
import logging
import Errors as err
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

    def StageProject(self, projectName):
        return super(Templatize, self).InitProject(projectName)

    def StageSchema(self, projectName, schemaName):
        return super(Templatize, self).InitSchema(projectName, schemaName)

    def StageModule(self, projectName, schemaName, moduleName):
        return super(Templatize, self).InitModule(projectName, schemaName, moduleName)

    def StageTemplate(self, projectName, schemaName, templateName):
        return super(Templatize, self).InitTemplate(projectName, schemaName, templateName)

    def GetProjectList(self):
        return os.listdir(self.homeDIR)

# Creating Home Directory
import shutil
try:
    shutil.rmtree(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects"))
except:
    pass

temp=Templatize()
temp.StageProject("Hello Universe")
temp.CreateProject("Default Project")
temp.CreateProjectVariable("Path", "Path of the Project", "String", "Static", "/opt")

temp.StageSchema("Hello Universe", "Azure-BPD")
temp.CreateSchema("Azure Compute using BPD", 6)
temp.CreateSchemaVariable("TenantID", "Azure Tenant ID", "String", "Runtime")

temp.StageModule("Hello Universe", "Azure-BPD", "DataDisk")
temp.CreateModule("Managed Datadisk", 3, "Data")
temp.CreateModuleVariable("Disk Resource Name", "Name of the Disk", "String", "User")

temp.InitTemplate("Hello Universe", "Azure-BPD", "New-Deployment")
temp.CreateTemplate("Test Deployment")

print(temp.OpenProject())
print(temp.OpenSchema())
print(temp.OpenModule())
print(temp.OpenTemplate())