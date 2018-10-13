import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js
from ProjectClass import Project

class Template:

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    proj = Project()

    def CreateTemplate(self, projectName, templateName, templateDescription, groupCount):
        # Checking Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        TempPath=os.path.join(ProjectPath, templateName)
        # Validating Path
        try:
            if self.OpenTemplate(projectName, templateName) is not None: 
                raise err.Conflict("A Template with the name '{0}' already exists !".format(templateName))
        except err.Conflict as ex:
            if "Unable to find a Project" in str(ex): return None
            if "already exists" in str(ex):
                raise err.Conflict("A Template with the name '{0}' already exists !".format(templateName))
                return None
        # Creating Directory & File
        try:
            os.makedirs(TempPath)
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

    def OpenTemplate(self, projectName, templateName):
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        TempPath=os.path.join(ProjectPath, templateName)
        # Opening Template
        templates=self.proj.GetTemplateList(projectName)
        templateData=js.GetJSON(templates, "TemplateName", templateName)
        if templateData==None:
            raise err.Conflict("Unable to find a Template with the name '{0}'".format(templateName))
            return None
        return js.Load(js.Dump(templateData[0]))

    def GetTemplateDescription(self, projectName, templateName):
        jsonContent=self.OpenTemplate(projectName, templateName)
        return jsonContent["TemplateDescription"]

    def GetModuleList(self, projectName, templateName):
        jsonContent=self.OpenTemplate(projectName, templateName)
        return jsonContent["Modules"]

    def GetTemplateGroupCount(self, projectName, templateName):
        jsonContent=self.OpenTemplate(projectName, templateName)
        return jsonContent["GroupCount"]

    def GetTemplateVariables(self, projectName, templateName):
        jsonContent=self.OpenTemplate(projectName, templateName)
        return jsonContent["TemplateVariables"]

    def CreateTemplateVariable(self, projectName, templateName, variableName, variableDescription, variableType):
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        jsonContent=js.Load(fl.Read(metaDataFile))
        for variable in self.GetTemplateVariables(projectName, templateName):
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Template Variable with the name '{0}' already exists !".format(variableName))
                return None
        index=js.GetJSONIndex(jsonContent["Templates"], "TemplateName", templateName)
        jsonContent["Templates"][int(index[0])]["TemplateVariables"].append(js.VariableJSON(variableName, variableDescription, variableType))
        fl.Write(metaDataFile, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)