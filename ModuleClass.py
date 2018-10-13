import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js
from ProjectClass import Project
from TemplateClass import Template

class Module:

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    proj=Project()
    temp=Template()

    def CreateModule(self, projectName, templateName, moduleName, moduleDescription, group, data):
        # Checking Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        TempPath=os.path.join(ProjectPath, templateName)
        ModulePath=os.path.join(TempPath, moduleName)
        # Validating Path
        try:
            if self.OpenModule(projectName, templateName, moduleName) is not None: 
                raise err.Conflict("A Module with the name '{0}' already exists !".format(moduleName))
        except err.Conflict as ex:
            if "Unable to find a Project" in str(ex): return None
            if "Unable to find a Template" in str(ex): return None
            if "already exists" in str(ex):
                raise err.Conflict("A Module with the name '{0}' already exists !".format(moduleName))
                return None
        # Creating Directory & File
        try:
            os.makedirs(ModulePath)
            jsonContent=js.Load(fl.Read(metaDataFile))
            jsonContent["Templates"].append(js.TemplateJSON(templateName, templateDescription, groupCount))
            fl.Write(metaDataFile, js.Dump(jsonContent), True)
            return "Template '{0}' created successfully !".format(templateName)
        except WindowsError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        except OSError:
            raise err.Conflict("There are errors in the metadata file. Synchronize the data to fix them !")
        if os.path.exists(TempPath):
            os.removedirs(TempPath)
        return None

    def OpenModule(self, projectName, templateName, moduleName):
        # Checking Project Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        TempPath=os.path.join(ProjectPath, templateName)
        ModulePath=os.path.join(TempPath, moduleName)
        # Opening Module
        modules=self.temp.GetModuleList(projectName, templateName)
        moduleData=js.GetJSON(modules, "ModuleName", moduleName)
        if moduleData==None:
            raise err.Conflict("Unable to find a Module with the name '{0}'".format(moduleName))
            return None
        return js.Load(js.Dump(moduleData[0]))

    def GetModuleVariables(self, projectName, templateName, moduleName):
        jsonContent=self.OpenModule(projectName, templateName, moduleName)
        return jsonContent["ModuleVariables"]
