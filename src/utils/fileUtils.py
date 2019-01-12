# Utilities for file mangement

# @Vendors
import json

# @Constants
from src.constants.constants import constants

# Loads a json file as dict
def loadJSONFile(pathFromRoot):
    with open(pathFromRoot) as f:
        parsedDict = json.loads(f.read())
    f.close()
    return parsedDict

# @Paths
paths = loadJSONFile('paths.json')

# Parses path and gets path from path file
def getPath(element):
    pathComponents = element.split(constants['PATH_SEPARATOR'])
    if len(pathComponents) == 2 :
        pathFromRoot = paths[pathComponents[0]][pathComponents[1]]
        return pathFromRoot
    return None

# Loads a dictionary from a json file
def loadDictFromJSONFile(document):
    pathFromRoot = getPath(document)
    if pathFromRoot is not None:
        return loadJSONFile(pathFromRoot)
    return {}
