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

#print(proj.CreateProject("Hello Universe","Test Project"))
#print(proj.GetProjectDescription("Hello Universe"))
#print(proj.OpenProject("Hello Universe"))
#print(temp.OpenTemplate("Hello Universe", "Azure"))
#print(proj.GetTemplateList("Hello Universe")
#print(proj.GetProjectVariables("Hello Universe"))
#print(temp.GetTemplateVariables("Hello Universe", "Azure"))
#print(temp.CreateTemplate("Hello Universe", "Azure", "Azure ARM template", 3))
#mod.CreateModule("Hello Universe", "Azure", "Storage", "VM Template", 4, "Data")
#var.CreateGlobalVariable("Path", "List")
#var.CreateProjectVariable("Hello Universe", "AppID", "String")
#var.CreateTemplateVariable("Hello Universe", "Azure", "App", "String")
#var.CreateModuleVariable("Hello Universe", "Azure", "Compute", "StorageAccount", "List", "User")