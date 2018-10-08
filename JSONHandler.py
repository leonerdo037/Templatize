import json
import Errors as err

def ProjectJSON(projectName, projectDescription):
    return {
            'ProjectName': projectName,
            'ProjectDescription': projectDescription,
            'ProjectVariables': [],
            'Templates': []
           }

def TemplateJSON(templateName, templateDescription, groupCount):
    return {
            'TemplateName': templateName,
            'TemplateDescription': templateDescription,
            'TemplateVariables': [],
            'GroupCount': groupCount,
            'Modules': []
           }

def ModuleJSON(moduleName, moduleDescription, group):
    return {
            'ModuleName': moduleName,
            'ModuleDescription': moduleDescription,
            'ModuleVariables': [],
            'Group': group
           }

def VariableJSON(variableName, variableType, variableScope="System"):
    return {
            'VariableName': variableName,
            'VariableType': variableType,
            'VariableScope': variableScope
           }

def Dump(data):
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

def Load(data):
    return json.loads(data)