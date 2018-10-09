import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js
from Project import Project
from Template import Template
from Module import Module
from Variable import Variable

class Variable:
    
    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    globalData=os.path.join(homeDIR, "metadata.json")
    proj=Project()
    temp=Template()
    mod=Module()

    def CreateGlobalVariable(self, variableName, variableType):
        jsonContent=js.Load(fl.Read(self.globalData))
        for variable in jsonContent:
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Variable with the name '{0}' already exists !".format(variableName))
                return None
        jsonContent.append(js.VariableJSON(variableName, variableType, "Global"))
        fl.Write(self.globalData, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)

    def CreateProjectVariable(self, projectName, variableName, variableType):
        # Checking Project Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        # Checking If Variable Exist
        for variable in self.proj.GetProjectData(projectName, "ProjectVariables"):
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Variable with the name '{0}' already exists !".format(variableName))
                return None
        # Creating Variable
        jsonContent["ProjectVariables"].append(js.VariableJSON(variableName, variableType, "Project"))
        fl.Write(metaDataFile, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)

    def CreateTemplateVariable(self, projectName, templateName, variableName, variableType):
        # Checking Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        TempPath=os.path.join(ProjectPath, templateName)
        # Checking If Variable Exist
        jsonContent=js.Load(fl.Read(metaDataFile))
        for variable in self.temp.GetTemplateData(projectName, templateName, "TemplateVariables"):
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Variable with the name '{0}' already exists !".format(variableName))
                return None
        # Creating Variable
        jsonContent["Templates"][i]["TemplateVariables"].append(js.VariableJSON(variableName, variableType, "Template"))
        fl.Write(metaDataFile, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)

    def CreateModuleVariable(self, projectName, templateName, moduleName, variableName, variableType, variableMode):
        # Checking Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        TempPath=os.path.join(ProjectPath, templateName)
        ModulePath=os.path.join(TempPath, moduleName)
        if fl.ValidateModule(ProjectPath, TempPath, ModulePath, new=False)==False: return
        # Creating Variable
        jsonContent=js.Load(fl.Read(metaDataFile))
        for templates in jsonContent["Templates"]:
            # Iterating Over The Templates
            if templates["TemplateName"]==templateName:
                # Iterating Over The Modules
                for module in templates:
                    if module["ModuleName"]==moduleName:
                        jsonContent.append(js.VariableJSON(variableName, variableType, "Module", variableMode))
                        fl.Write(metaDataFile, js.Dump(jsonContent), True)
                        return "Variable '{0}' created successfully !".format(variableName)