import os
import logging
import Errors as err
from ProjectClass import Project
from SchemaClass import Schema
from ModuleClass import Module
from TemplateClass import Template

#project = Project("Hello Universe")

#print(project.CreateProject("Test Project"))
#print(project.CreateProjectVariable("TenantID", "Tenant ID of Azure", "String", "Static", "000-000-000"))

#schema = Schema("Hello Universe", "Azure")

#print(schema.CreateSchema("Azure ARM template", 3))
#print(schema.CreateSchemaVariable("Resource Group", "Resource group from Azure", "List", "Internal", "Dummy"))

#module = Module("Hello Universe", "Azure", "Storage")

#print(module.CreateModule("VM Template", 2, "Data"))
#print(module.CreateModuleVariable("Storage Size", "Size of the storage", "Number", "User"))

template = Template("Hello Universe", "Azure", "NewDeploy")

#print(template.CreateTemplate("Test deployment"))
#print(template.AddModules("Disk1", "Storage"))
print(template.GenerateVariables())