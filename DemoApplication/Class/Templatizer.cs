using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DemoApplication.Class
{
    public class Templatizer
    {
        // Python Variables
        private ScriptEngine pythonEngine;
        private ScriptScope pythonScope;
        private ScriptSource pythonSource;
        private CompiledCode pythonCode;
        private object pythonClass;
        private string prePath = @"F:\Infra\037\# Projects\Templatize\Templatize\";
        private string dir = @"C:\Program Files\IronPython 2.7\Lib";

        public Templatizer()
        {
            // Setting up IronPython
            pythonEngine = Python.CreateEngine();
            pythonScope = pythonEngine.CreateScope();
            ICollection<string> paths = pythonEngine.GetSearchPaths();

            if (!String.IsNullOrWhiteSpace(dir))
            {
                paths.Add(prePath);
                paths.Add(dir);
            }
            else
            {
                paths.Add(Environment.CurrentDirectory);
            }
            pythonEngine.SetSearchPaths(paths);
        }

        public string CreateProject(string projectName, string projectDescription)
        {
            try
            {
                pythonSource = pythonEngine.CreateScriptSourceFromFile(prePath + "Class_Project.py");
                pythonCode = pythonSource.Compile();
                pythonCode.Execute(pythonScope);
                pythonClass = pythonEngine.Operations.Invoke(pythonScope.GetVariable("Project"));
                object[] args = { projectName, projectDescription };
                var result = pythonEngine.Operations.InvokeMember(pythonClass, "CreateProject", args);
                return result;
            }
            catch (Exception ex)
            {
                ExceptionOperations except = pythonEngine.GetService<ExceptionOperations>();
                return except.FormatException(ex);
            }
        }

        public string CreateTemplate(string projectName, string templateName, string templateDescription, int sectionCount)
        {
            try
            {
                pythonSource = pythonEngine.CreateScriptSourceFromFile(prePath + "Class_Project.py");
                pythonCode = pythonSource.Compile();
                pythonCode.Execute(pythonScope);
                pythonClass = pythonEngine.Operations.Invoke(pythonScope.GetVariable("Project"));
                object[] args = { projectName, templateName, templateDescription, sectionCount };
                var result = pythonEngine.Operations.InvokeMember(pythonClass, "CreateTemplate", args);
                return result;
            }
            catch (Exception ex)
            {
                ExceptionOperations except = pythonEngine.GetService<ExceptionOperations>();
                return except.FormatException(ex);
            }
        }

        public string CreateModule(string projectName, string templateName, string moduleName, string moduleDescription, int section, string data)
        {
            try
            {
                pythonSource = pythonEngine.CreateScriptSourceFromFile(prePath + "Class_Project.py");
                pythonCode = pythonSource.Compile();
                pythonCode.Execute(pythonScope);
                pythonClass = pythonEngine.Operations.Invoke(pythonScope.GetVariable("Project"));
                object[] args = { projectName, templateName, moduleName, moduleDescription, section, data };
                var result = pythonEngine.Operations.InvokeMember(pythonClass, "CreateModule", args);
                return result;
            }
            catch (Exception ex)
            {
                ExceptionOperations except = pythonEngine.GetService<ExceptionOperations>();
                return except.FormatException(ex);
            }
        }
    }
}
