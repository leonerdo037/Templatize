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

#var.CreateProjectVariable("Dummy", "test2")
#proj.CreateProject("Dummy","Test Project")
#temp.CreateTemplate("Dummy", "testTemp", "FirstTest", 3)
#print(temp.OpenTemplate("Dummy", "testTemp"))
#print(temp.GetTemplateData("Dummy", "testTemp", "TemplateDescription"))
#proj.CreateModule("Hello Universe", "Test2", "King", "Testing Man", 4, "Dummy Data entered !")
#print(proj.GetModuleData("Hello Universe", "Test2", "King", "Section"))