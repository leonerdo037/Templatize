import os
import logging
import Class_Error as err
from Class_Project import Project

class Templatize:
    proj = Project()
    #proj.CreateModule("Hello Universe", "Test2", "King", "Testing Man", 4, "Dummy Data entered !")
    print(proj.GetModuleData("Hello Universe", "Test2", "King", "Section"))