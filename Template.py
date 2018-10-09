import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js

class Template:

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")

    def CreateTemplate(self, projectName, templateName, templateDescription, groupCount):
        # Checking Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        TempPath=os.path.join(ProjectPath, templateName)
        if fl.ValidateTemplate(ProjectPath, TempPath, new=True)==False: return
        # Create Template
        os.makedirs(TempPath)
        jsonContent=js.Load(fl.Read(metaDataFile))
        jsonContent["Templates"].append(js.TemplateJSON(templateName, templateDescription, groupCount))
        fl.Write(metaDataFile, js.Dump(jsonContent), True)
        return "Template '{0}' created successfully !".format(templateName)

    def ListTempaltes(self, projectName):
        ProjectPath=os.path.join(self.homeDIR, projectName)
        return os.listdir(ProjectPath)

    def OpenTemplate(self, projectName, templateName):
        # Checking Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        TempPath=os.path.join(ProjectPath, templateName)
        if fl.ValidateTemplate(ProjectPath, TempPath, new=False)==False: return
        # Return Data
        jsonContent=js.Load(fl.Read(metaDataFile))
        for template in jsonContent["Templates"]:
            if template["TemplateName"]==templateName:
                return template

    def GetTemplateData(self, projectName, templateName, key):
        jsonContent=self.OpenTemplate(projectName, templateName)
        return jsonContent[key]