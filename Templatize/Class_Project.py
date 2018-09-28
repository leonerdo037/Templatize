import os
import json
import Class_Error as err

class Project:
    # Manages all project related activities
    # Variables
    projectDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    curProject=None

    def __init__(self):
        pass
        #if not os.path.exists(self.projectDIR):
        #    os.makedirs(self.projectDIR)

    def UpdateMetaData(data):
        pass

    def GetProjectData(projectName, key):
        ProjectPath=os.path.join(self.projectDIR, projectName)
        metadata=open(os.path.join(ProjectPath, ".metadata"),"r+")
        jsonContent=json.loads(metaFile.read())
        return jsonContent[key]

    def GetTemplateData(projectName, templateName, key):
        ProjectPath=os.path.join(self.projectDIR, projectName)
        TempPath=os.path.join(ProjectPath, templateName)
        metadata=open(os.path.join(TempPath, ".metadata"),"r+")
        jsonContent=json.loads(metaFile.read())
        return jsonContent[key]

    def GetModuleData(projectName, templateName, moduleName, key):
        ProjectPath=os.path.join(self.projectDIR, projectName)
        TempPath=os.path.join(ProjectPath, templateName)
        ModulePath=os.path.join(TempPath, moduleName)
        metadata=open(os.path.join(ModulePath, ".metadata"),"r+")
        jsonContent=json.loads(metaFile.read())
        return jsonContent[key]

    def CreateProject(self, projectName, projectDescription):
        ProjectPath=os.path.join(self.projectDIR, projectName)
        if os.path.exists(ProjectPath):
            raise err.Conflict("A Project with the same name already exists !")
        else:
            os.makedirs(ProjectPath)
            metadata=open(os.path.join(ProjectPath, ".metadata"),"w+")
            metaFile.write(json.dumps({'ProjectName': projectName, 'ProjectDescription': projectDescription,'Templates':[]}, sort_keys=True, indent=4, separators=(',', ': ')))
            metaFile.close()
            self.curProject=ProjectPath
            return "Project '{0}' created successfully !".format(projectName)

    def CreateTemplate(self, projectName, templateName, templateDescription, sectionCount):
        ProjectPath=os.path.join(self.projectDIR, projectName)
        TempPath=os.path.join(ProjectPath, templateName)
        if os.path.exists(ProjectPath):
            # Check if template exists
            if os.path.exists(TempPath):
                raise err.Conflict("A Template with the same name already exists !")
            # Create Template
            os.makedirs(os.path.join(ProjectPath, templateName))
            metadata=open(os.path.join(ProjectPath, ".metadata"),"r+")
            jsonContent=json.loads(metaFile.read())
            jsonContent["Templates"].append({'TemplateName': templateName, 'TemplateDescription': templateDescription, 'SectionCount': sectionCount, 'Modules':[]})
            metaFile.seek(0)
            metaFile.write(json.dumps(jsonContent, sort_keys=True, indent=4, separators=(',', ': ')))
            metaFile.truncate()
            metaFile.close()
        else:
            raise err.Conflict("There are no Project with the name '{0}'".format(projectName))

    def CreateModule(self, projectName, templateName, moduleName, moduleDescription, section, data):
        ProjectPath=os.path.join(self.projectDIR, projectName)
        TempPath=os.path.join(ProjectPath, templateName)
        ModulePath=os.path.join(TempPath, moduleName)
        # Fetching metadata
        metadata=open(os.path.join(ProjectPath, ".metadata"),"r+")
        jsonContent=json.loads(metaFile.read())
        for temp in jsonContent["Templates"]:
            if temp["TemplateName"]==templateName:
                # Validating Count
                print(temp["SectionCount"])
                print(section)
                if temp["SectionCount"] >= section:
                    temp["Modules"].append({'ModuleName': moduleName, 'Section': section})
                else:
                    raise err.Conflict("Section should be lesser than or equal to {0} !".format(temp["SectionCount"]))
        if os.path.exists(ProjectPath):
            # Check if template exists
            if os.path.exists(TempPath):
                # Check if module exists
                if os.path.exists(ModulePath):
                    raise err.Conflict("A Module with the same name already exists !")
                # Create Module
                moduleFile=open(ModulePath,"w+")
                moduleFile.write(data)
                moduleFile.close()
                # Updating Metadata
                metaFile.seek(0)
                metaFile.write(json.dumps(jsonContent, sort_keys=True, indent=4, separators=(',', ': ')))
                metaFile.truncate()
                metaFile.close()
            else:
                raise err.Conflict("There is no Template with the name '{0}'".format(templateName))
        else:
            raise err.Conflict("There is no Project with the name '{0}'".format(projectName))
        pass

    def ListProject(self):
        return os.listdir(self.projectDIR)

    def OpenProject(self, projectName):
        if not os.path.exists(os.path.join(self.projectDIR, projectName)):
            raise err.Conflict("Unable to find a project with that name !")
        else:
            pass