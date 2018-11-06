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
            raise err.Conflict("Stage the Project before use !")
            return None
        return self.__project

    @property
    def schema(self):
        self.project.Path
        if self.__schema is None:
                raise err.Conflict("Stage the Schema before use !")
                return None
        return self.__schema

    @property
    def module(self):
        self.schema.Path
        if self.__module is None:
            raise err.Conflict("Stage the Module before use !")
            return None
        return self.__module

    @property
    def template(self):
        self.schema.Path
        if self.__template is None:
            raise err.Conflict("Stage the Template before use !")
            return None
        return self.__template

    def __init__(self):
        # Initializaing Class Variables to None
        self.__project=None
        self.__scema=None
        self.__module=None
        self.__template=None
        # Creating Home Directory
        if not os.path.exists(self.homeDIR):
            os.makedirs(self.homeDIR)

    def GetProjectList(self):
        return os.listdir(self.homeDIR)

    def StageProject(self, name):
        self.__project=Project()
        self.project.Init(name)
        # Checking Project's Existence
        if not self.project.Exists():
            self.__project=None
            raise err.Conflict("Create the Project before staging!")

    def StageSchema(self, name):
        self.__schema=Schema()
        self.schema.Init(name, self.project.Path)
        # Checking Schema's Existence
        if not self.schema.Exists() or name not in self.project.GetSchemaList():
            self.__schema=None
            raise err.Conflict("Create the Schema before staging!")

    def StageModule(self, name):
        self.__module=Module()
        self.module.Init(name, self.schema.Path)
        # Checking Module's Existence
        if not self.module.Exists() or name not in self.schema.GetModuleList():
            self.__module=None
            raise err.Conflict("Create the Module before staging!")

    def StageTemplate(self, name):
        self.__template=Template()
        self.template.Init(name, self.schema.Path, self.project.GetVariables(), self.schema.GetVariables())
        # Checking Module's Existence
        if not self.template.Exists() or name not in self.schema.GetTemplateList():
            self.__template=None
            raise err.Conflict("Create the Template before staging!")

    def CreateProject(self, name, description):
        self.__project=Project()
        self.project.Init(name)
        if self.project.Exists():
            self.__project=None
            raise err.Conflict("A Project with the name '{0}' already exists !".format(name))
        else:
            return self.project._Create(description)

    def CreateSchema(self, name, description, groupCount):
        self.__schema=Schema()
        self.schema.Init(name, self.project.Path)
        if self.schema.Exists():
            self.__schema=None
            raise err.Conflict("A Schema with the name '{0}' already exists !".format(name))
        else:
            return self.schema._Create(description, groupCount)

    def CreateModule(self, name, description, group, data):
        self.__module=Module()
        self.module.Init(name, self.schema.Path)
        if self.module.Exists():
            self.__module=None
            raise err.Conflict("A Module with the name '{0}' already exists !".format(name))
        else:
            return self.module._Create(description, group, self.schema.GetGroupCount(), data)

    def CreateTemplate(self, name, description):
        self.__template=Template()
        self.template.Init(name, self.schema.Path, self.project.GetVariables(), self.schema.GetVariables())
        if self.template.Exists():
            self.__template=None
            raise err.Conflict("A Template with the name '{0}' already exists !".format(name))
        else:
            return self.template._Create(description)

# import shutil
# try:
    # shutil.rmtree(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects"))
# except:
    # pass

# temp=Templatize()
# temp.CreateProject("Hello Universe", "Default Project")
# temp.CreateSchema("Azure-BPD", "Azure Templates for Blueprint Designer", 6)
# temp.CreateModule("Data Disk", "Azure Managed Disk", 5, "<Data HERE>")
# temp.CreateTemplate("NewTemplate", "Test Template based on Azure")

# temp.project.CreateVariable("Path", "Path of the target files", "String", "Runtime")
# temp.schema.CreateVariable("TenantID", "Azure Tenant GUID", "String", "Static", "0000-0000-0000")
# temp.module.CreateVariable("Disk Size", "Azure Data Disk Size", "Number", "User")

# print(temp.template.AddModules("One", "Disk Size"))

# temp.CreateProject("Hello World", "Test Project")
# temp.CreateProject("Hello Galaxy", "Test Project")
# temp.CreateProject("Hello Multiverse", "Test Project")
# temp.CreateProject("Hello Country", "Test Project")
# temp.CreateProject("Hello Solar System", "Test Project")
# temp.CreateProject("Hello State", "Test Project")
# temp.CreateProject("Hello Continent", "Test Project")
# temp.CreateProject("Hello City", "Test Project")
# temp.CreateProject("Hello Street", "Test Project")
# temp.CreateProject("Hello House", "Test Project")
# temp.CreateProject("Hello Room", "Test Project")
# temp.CreateProject("Hello Chair", "Test Project")