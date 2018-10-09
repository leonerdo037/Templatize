import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js

class Module:

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")

    def CreateModule(self, projectName, templateName, moduleName, moduleDescription, group, data):
        # Checking Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        TempPath=os.path.join(ProjectPath, templateName)
        ModulePath=os.path.join(TempPath, moduleName)
        if fl.ValidateModule(ProjectPath, TempPath, ModulePath, new=True)==False: return
        # Fetching metadata
        jsonContent=js.Load(fl.Read(metaDataFile))
        for temp in jsonContent["Templates"]:
            if temp["TemplateName"]==templateName:
                # Validating Count
                if temp["GroupCount"] >= group:
                    temp["Modules"].append(js.ModuleJSON(moduleName, moduleDescription, group))
                else:
                    raise err.Conflict("Group should be lesser than or equal to {0} !".format(temp["GroupCount"]))
                # Create Module
                fl.Write(ModulePath, data)
                # Updating Metadata
                fl.Write(metaDataFile, js.Dump(jsonContent), True)
                return "Module '{0}' created successfully !".format(moduleName)

    def ListModules(self, projectName, templateName, moduleName):
        ProjectPath=os.path.join(self.homeDIR, projectName)
        TempPath=os.path.join(ProjectPath, templateName)
        return os.listdir(TempPath)

    def OpenModule(self, projectName, templateName, moduleName):
        # Checking Project Path
        ProjectPath=os.path.join(self.homeDIR, projectName)
        metaDataFile=os.path.join(ProjectPath, "metadata.json")
        TempPath=os.path.join(ProjectPath, templateName)
        ModulePath=os.path.join(TempPath, moduleName)
        if fl.ValidateModule(ProjectPath, TempPath, ModulePath, new=False)==False: return
        # Return Data
        jsonContent=js.Load(fl.Read(metaDataFile))
        for templates in jsonContent["Templates"]:
            # Iterating Over The Templates
            if templates["TemplateName"]==templateName:
                # Iterating Over The Modules
                for module in templates:
                    if module["ModuleName"]==moduleName:
                        return module

    def GetModuleData(self, projectName, templateName, moduleName, key):
        jsonContent=self.OpenModule(projectName, templateName, moduleName)
        return jsonContent[key]
