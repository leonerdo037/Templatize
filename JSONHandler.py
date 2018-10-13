import json
import Errors as err

def Dump(data):
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

def Load(data):
    return json.loads(data)

def GlobalJSON(asJSON=False):
    output={
            'GlobalVariables': []
           }
    if asJSON: return Dump(output)
    else: return output

def ProjectJSON(projectName, projectDescription, asJSON=False):
    output={
            'ProjectName': projectName,
            'ProjectDescription': projectDescription,
            'ProjectVariables': [],
            'Templates': []
           }
    if asJSON: return Dump(output)
    else: return output

def TemplateJSON(templateName, templateDescription, groupCount, asJSON=False):
    output={
            'TemplateName': templateName,
            'TemplateDescription': templateDescription,
            'TemplateVariables': [],
            'GroupCount': groupCount,
            'Modules': []
           }
    if asJSON: return Dump(output)
    else: return output

def ModuleJSON(moduleName, moduleDescription, group, asJSON=False):
    output={
            'ModuleName': moduleName,
            'ModuleDescription': moduleDescription,
            'ModuleVariables': [],
            'Group': group
           }
    if asJSON: return Dump(output)
    else: return output

def VariableJSON(variableName, variableType, variableScope, variableMode="System", asJSON=False):
    output={
            'VariableName': variableName,
            'VariableType': variableType,
            'VariableScope': variableScope,
            'VariableMode': variableMode
           }
    if asJSON: return Dump(output)
    else: return output

def GetJSON(jsonArray, searchKey, searchValue):
    result=[i for i in jsonArray if i[searchKey]==searchValue]
    # Validating existance of data
    if len(result)==0:
        return None
    return result

def GetJSONIndex(jsonArray, searchKey, searchValue):
    result=[i for i in enumerate(jsonArray) if i[searchKey]==searchValue]
    # Validating existance of data
    if len(result)==0:
        return None
    return result