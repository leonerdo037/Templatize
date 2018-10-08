import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js

class Template:

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")

    def CreateTemplate(self, projectName, templateName, templateDescription, groupCount):
        # Checking Project Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        if fl.ValidatePath(ProjectPath, "Project", new=False)==False: return
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        # Checking Template Path
        TempPath=os.path.join(ProjectPath, templateName)
        if fl.ValidatePath(TempPath, "Template", new=True)==False: return
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
        # Checking Project Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        if fl.ValidatePath(ProjectPath, "Project", new=False)==False: return
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        # Checking Template Path
        TempPath=os.path.join(ProjectPath, templateName)
        if fl.ValidatePath(TempPath, "Template", new=False)==False: return
        # Return Data
        jsonContent=js.Load(fl.Read(os.path.join(ProjectPath, "metadata.json")))
        for template in jsonContent["Templates"]:
            if template["TemplateName"]==templateName:
                return template

    def GetTemplateData(self, projectName, templateName, key):
        jsonContent=self.OpenTemplate(projectName, templateName)
        return jsonContent[key]