import os
import logging
import Errors as err
from ProjectClass import Project
from TemplateClass import Template
from ModuleClass import Module
from VariableClass import Variable

proj = Project()
temp = Template()
mod = Module()
var = Variable()

print(proj.CreateProject("Hello Universe","Test Project"))
print(temp.CreateTemplate("Hello Universe", "Azure", "Azure ARM template", 3))
print(mod.CreateModule("Hello Universe", "Azure", "Storage", "VM Template", 2, "Data"))
print(proj.CreateGlobalVariable("Header", "Company name", "String", "Tata Consultancy Services"))
print(proj.CreateProjectVariable("Hello Universe" ,"TenantID", "Tenant ID of Azure", "String", "000-000-000-000"))
print(temp.CreateTemplateVariable("Hello Universe", "Azure", "Resource Group", "Resource group from Azure", "List"))
print(mod.CreateModuleVariable("Hello Universe", "Azure", "Storage", "Storage Size", "Size of the storage", "Number", "User"))