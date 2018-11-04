import json
import Errors as err
from collections import OrderedDict

acceptedTypes=["Boolean" ,"String", "Number", "List", "Dictionary"]
acceptedModes=["Static", "Internal", "Runtime", "User"]

def CheckDataType(data, givenType):
    if givenType == "String":
        if type(data) is not str:
            return None
    elif givenType == "Number":
        if type(data) is not int:
            return None
    elif givenType == "List":
        if type(data) is not list:
            return None
    elif givenType == "Dictionary":
        if type(data) is not dict:
            return None
    elif givenType == "Boolean":
        if type(data) is not bool:
            return None
    return True

def Dump(data):
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

def Load(data):
    return json.loads(data, object_pairs_hook=OrderedDict)

def ProjectJSON(projectName, projectDescription, asJSON=False):
    output={
            'ProjectName': projectName,
            'ProjectDescription': projectDescription,
            'Schemas': [],
            'ProjectVariables': {}
           }
    if asJSON: return Dump(output)
    else: return output

def SchemaJSON(schemaName, schemaDescription, groupCount, asJSON=False):
    output={
            'SchemaName': schemaName,
            'SchemaDescription': schemaDescription,
            'GroupCount': groupCount,
            'Modules': {},
            'Templates': [],
            'SchemaVariables': {}
           }
    if asJSON: return Dump(output)
    else: return output

def ModuleJSON(moduleName, moduleDescription, group, asJSON=False):
    output={
            'ModuleName': moduleName,
            'ModuleDescription': moduleDescription,            
            'Group': group,
            'ModuleVariables': {}
           }
    if asJSON: return Dump(output)
    else: return output

def VariableJSON(variableName, variableDescription, variableType, variableMode, value=None, asJSON=False):
    if variableType not in acceptedTypes:
        raise err.Conflict("Unsupported variable type !")
        return None
    if variableMode not in acceptedModes:
        raise err.Conflict("Unsupported variable mode !")
        return None
    # Check if Mode is Static
    if variableMode == "Static":
        if CheckDataType(value, variableType)==None:
            raise err.Conflict("The value '{0}' is not of the type '{1}' !".format(value, variableType))
            return None
    else:
        # Non-Static Variables
        if variableType == "List":
            value=[]
        elif variableType == "Dictionary":
            value={}
        else:
            value=None
    output={
            'VariableName': variableName,
            'VariableDescription': variableDescription,            
            'VariableType': variableType,
            'VariableMode': variableMode,
            'Value': value
           }
    if asJSON: return Dump(output)
    else: return output

def TemplateJSON(templateName, templateDescription, asJSON=False):
    output={
            'TemplateName': templateName,
            'TemplateDescription': templateDescription,
            'Modules': {},
            'Variables': {}
           }
    if asJSON: return Dump(output)
    else: return output

def TemplateModuleJSON(moduleKey, moduleName, asJSON=False):
    output={
            'key': moduleKey,
            'Name': moduleName,
            'Variables': {}
           }
    if asJSON: return Dump(output)
    else: return output