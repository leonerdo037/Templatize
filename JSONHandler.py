import json
import Errors as err
from collections import OrderedDict

acceptedTypes=["String", "Number", "List", "Dictionary"]
acceptedModes=["System", "User"]

def Dump(data):
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

def Load(data):
    return json.loads(data)#, object_pairs_hook=OrderedDict

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

def VariableJSON(variableName, variableDescription, variableType, variableMode="System", asJSON=False):
    if variableType not in acceptedTypes:
        raise err.Conflict("Unsupported variable type !")
        return None
    if variableMode not in acceptedModes:
        raise err.Conflict("Unsupported variable mode !")
        return None
    output={
            'VariableName': variableName,
            'VariableDescription': variableDescription,
            'VariableType': variableType,
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
    result=[value for (value,key) in enumerate(jsonArray) if key[searchKey]==searchValue]
    # Validating existance of data
    if len(result)==0:
        return None
    return result