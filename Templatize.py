import os
import logging
import Errors as err
from ProjectClass import Project
from SchemaClass import Schema
from ModuleClass import Module
from TemplateClass import Template

project = Project()
schema = Schema()
module = Module()


print(project.CreateProject("Hello Universe","Test Project"))
print(schema.CreateSchema("Hello Universe", "Azure", "Azure ARM template", 3))
print(module.CreateModule("Hello Universe", "Azure", "Storage", "VM Template", 2, "Data"))
print(project.CreateProjectVariable("Hello Universe" ,"TenantID", "Tenant ID of Azure", "String", "Static", "000-000-000"))
print(schema.CreateSchemaVariable("Hello Universe", "Azure", "Resource Group", "Resource group from Azure", "List", "Internal", "Dummy"))
print(module.CreateModuleVariable("Hello Universe", "Azure", "Storage", "Storage Size", "Size of the storage", "Number", "User"))

template = Template("Hello Universe", "Azure")

print(template.CreateTemplate("NewDeploy", "Test deployment"))
print(template.AddModules("NewDeploy", "Disk2", "Storage"))