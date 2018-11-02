import os
import logging
import Errors as err
from ProjectClass import Project
from SchemaClass import Schema
from ModuleClass import Module
from TemplateClass import Template

class Templatize(object):

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    __project=Project()
    __schema=Schema()
    __module=Module()
    __template=Template()

    # Properties

    @property
    def project(self):
        if self.__project is None:
            raise err.Conflict("Stage or Create the Project before use !")
            return None
        return self.__project

    @property
    def schema(self):
        self.project.Open()
        if self.__schema is None:
                raise err.Conflict("Stage or Create the Schema before use !")
                return None
        return self.__schema

    @property
    def module(self):
        self.schema.Open()
        if self.__module is None:
            raise err.Conflict("Stage or Create the Project before use !")
            return None
        return self.__module

    @property
    def template(self):
        self.schema.Open()
        if self.__template is None:
            raise err.Conflict("Stage or Create the Project before use !")
            return None
        return self.__template

    def __init__(self):
        # Initializaing Class Variables to None
        self.__project=None
        scema=None
        module=None
        template=None
        # Creating Home Directory
        if not os.path.exists(self.homeDIR):
            os.makedirs(self.homeDIR)

    def StageProject(self, Name):
        self.__project=Project()
        self.project.Init(Name)
        # Checking Project's Existence
        if not self.project.Exists():
            self.__project=None

    def CreateProject(self, Name, description):
        self.__project=Project()
        self.project.Init(Name)
        if self.project.Exists():
            self.__project=None
            raise err.Conflict("A Project with the name '{0}' already exists !".format(Name))
            return None
        else:
            return self.project.__Create(description)

    def StageSchema(self, schemaName):
        self.__project=Project()
        self.project.Init(Name)
        # Checking Schema's Existence
        if not self.project.Exists():
            self.__project=None

    def StageModule(self, moduleName):
        return super(Templatize, self).InitModule(self.project.projectName, self.schema.schemaName, moduleName)

    def StageTemplate(self, templateName):
        return super(Templatize, self).InitTemplate(self.project.projectName, self.schema.schemaName, templateName)

    def GetProjectList(self):
        return os.listdir(self.homeDIR)

# Creating Home Directory
#import shutil
#try:
#    shutil.rmtree(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects"))
#except:
#    pass

temp=Templatize()
#temp.CreateProject("Hello Universe", "Default Project")
temp.StageProject("Hello Universe")
print(temp.project.Open())
#temp.CreateProject("Default Project")
#temp.CreateProjectVariable("Path", "Path of the Project", "String", "Static", "/opt")

#temp.StageSchema("Hello Universe", "Azure-BPD")
#temp.CreateSchema("Azure Compute using BPD", 6)
#temp.CreateSchemaVariable("TenantID", "Azure Tenant ID", "String", "Runtime")

#temp.StageModule("Hello Universe", "Azure-BPD", "DataDisk")
#temp.CreateModule("Managed Datadisk", 3, "Data")
#temp.CreateModuleVariable("Disk Resource Name", "Name of the Disk", "String", "User")

#temp.StageTemplate("Hello Universe", "Azure-BPD", "New-Deployment")
#temp.CreateTemplate("Test Deployment")

#print(temp.project.OpenProject())
#print(temp.OpenSchema())
#print(temp.OpenModule())
#print(temp.OpenTemplate())