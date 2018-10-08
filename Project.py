import os
import Errors as err
import Settings as props
import FileHandler as fl
import JSONHandler as js

class Project:

    homeDIR=os.path.join(os.path.dirname(os.path.realpath(__file__)), "Projects")
    globalData=os.path.join(homeDIR, "metadata.json")

    def __init__(self):
        # Creating Home Directory
        if not os.path.exists(self.homeDIR):
            os.makedirs(self.homeDIR)
        # Creating MetaData File
        if not os.path.exists(self.globalData):
            fl.Write(self.globalData, "[]", True)

    def CreateProject(self, projectName, projectDescription):
        ProjectPath=os.path.join(self.homeDIR, projectName)
        # Creating Directory
        if fl.ValidatePath(ProjectPath, "Project", new=True)==False: return
        os.makedirs(ProjectPath)
        # Writing File
        fl.Write(os.path.join(ProjectPath, "metadata.json"), js.Dump(js.ProjectJSON(projectName, projectDescription)))
        return "Project '{0}' created successfully !".format(projectName)

    def ListProjects(self):
        return os.listdir(self.homeDIR)

    def OpenProject(self, projectName):
        ProjectPath=os.path.join(self.homeDIR, projectName)
        if fl.ValidatePath(os.path.join(self.homeDIR, projectName), "Project")==False: return
        jsonContent=js.Load(file.Read(os.path.join(ProjectPath, "metadata.json")))
        return jsonContent

    def GetProjectData(self, projectName, key):
        jsonContent=self.OpenProject(projectName)
        return jsonContent[key]