import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js

class Variable:
    
    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    globalData=os.path.join(homeDIR, "metadata.json")

    def CreateGlobalVariable(self, variableName):
        jsonContent=js.Load(fl.Read(self.globalData))
        for variable in jsonContent:
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Variable with the name '{0}' already exists !".format(variableName))
                return None
        jsonContent.append(js.VariableJSON(variableName, "Global"))
        fl.Write(self.globalData, js.Dump(jsonContent), True)
        return "Variable '{0}' created successfully !".format(variableName)

    def CreateProjectVariable(self, projectName, variableName):
        # Checking Project Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        if fl.ValidatePath(ProjectPath, "Project", new=False)==False: return
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        # Creating Variable
        jsonContent=js.Load(fl.Read(metaDataFile))
        for variable in jsonContent["ProjectVariables"]:
            if variable["VariableName"]==variableName:
                raise err.Conflict("A Variable with the name '{0}' already exists !".format(variableName))
                return None
            jsonContent.append(js.VariableJSON(variableName, "Project"))
            fl.Write(metaDataFile, js.Dump(jsonContent), True)
            return "Variable '{0}' created successfully !".format(variableName)

    def CreateTemplateVariable(self, projectName, templateName, variableName):
        # Checking Project Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        if fl.ValidatePath(ProjectPath, "Project", new=False)==False: return
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        # Checking Template Path
        TempPath=os.path.join(ProjectPath, templateName)
        if fl.ValidatePath(TempPath, "Template", new=False)==False: return
        # Creating Variable
        jsonContent=js.Load(fl.Read(metaDataFile))
        for template in jsonContent["Templates"]:
            if template["TemplateName"]==templateName:
                jsonContent.append(js.VariableJSON(variableName, "Project"))
                fl.Write(metaDataFile, js.Dump(jsonContent), True)
                return "Variable '{0}' created successfully !".format(variableName)