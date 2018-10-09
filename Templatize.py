import os
import logging
import Errors as err
from Project import Project
from Template import Template
from Module import Module
from Variable import Variable

proj = Project()
temp = Template()
mod = Module()
var = Variable()

#proj.CreateProject("Hello Universe","Test Project")
#temp.CreateTemplate("Hello Universe", "Azure", "Azure ARM template", 3)
#mod.CreateModule("Hello Universe", "Azure", "Storage", "VM Template", 4, "Data")
#var.CreateGlobalVariable("Path", "List")
#var.CreateProjectVariable("Hello Universe", "AppID", "String")
#var.CreateTemplateVariable("Hello Universe", "Azure", "App", "String")
var.CreateModuleVariable("Hello Universe", "Azure", "Compute", "StorageAccount", "List", "User")