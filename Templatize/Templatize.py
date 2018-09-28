import os
import wpf
import logging
import Class_Error as err
from Class_Project import Project

from System.Windows import Application, Window

class MyWindow(Window):

    # Creating Logger
    logPath=os.path.join(os.path.dirname(os.path.realpath(__file__)), "templatize.log")
    logging.basicConfig(filename=logPath, format='%(levelname)s: %(asctime)s - %(message)s', datefmt="%d-%m-%Y %H:%M:%S", level=logging.INFO)
    proj=Project()
    projList=[]

    def SwapWorkArea():
        pass

    def __init__(self):
        wpf.LoadComponent(self, 'Templatize.xaml')
                
    def Window_Loaded(self, sender, e):
        # Loading Projects
        try:
            self.projList = self.proj.ListProject()
            for p in self.projList:
                self.LB_List.Items.Add(p)
        except Exception as error:
            logging.error(str(error))
      
    def B_Create_Click(self, sender, e):
        try:
            logging.info(self.proj.CreateProject(self.TB_Name.Text,self.TB_Description.Text))
        except err.Conflict as error:
            logging.error(error.value)
        except Exception as error:
            logging.error(str(error))
    
    def Button_Click(self, sender, e):
        try:
            logging.info(self.proj.CreateProject(self.TB_Name.Text,self.TB_Description.Text))
        except Exception as error:
            logging.error(str(error))
    
if __name__ == '__main__':
    Application().Run(MyWindow())
