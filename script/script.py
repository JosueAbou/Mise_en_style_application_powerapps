from optparse import OptionParser
import json
import os


class MissingParameterError(Exception):
    def __init__(self, message):
        self.message = message  


DESIGN_VARIETIES = ["Primary","Secondary","Success","Warning"]


def getPropertiesFromName(elmt_name): 
    design_type, element_type = elmt_name.split("_")
    properties_to_update = ELEMENTS["Elements"][element_type]
    specific_properties = ELEMENTS["Design_Variations"][design_type][elmt_name]
    global_properties = [i for i in properties_to_update if i not in specific_properties]
    
    return design_type, element_type, specific_properties, global_properties 


def updateComponent(chld, spc_properties,glb_properties, dsg_type):
    for rule in chld["Rules"]:
        if(rule["Property"] in spc_properties):
            print("spec : ",rule["Property"])
            rule["InvariantScript"] = spc_properties[rule["Property"]]
        elif(rule["Property"] in glb_properties):
            print("global : ",rule["Property"])
            rule["InvariantScript"] = ELEMENTS["Design_Variations"][dsg_type][rule["Property"]]


def updateJsonFile(jsonFile):
    with open(os.path.join("./", jsonFile), "r") as file:
        data = json.load(file)

    if(str(data["TopParent"]["Name"]).startswith("Primary")):
        for rule in data["TopParent"]["Rules"]:
            if(rule["Property"] == "Fill"):
                rule["InvariantScript"] = "RGBA(243, 249, 253, 1)" 

    for child in data["TopParent"]["Children"]:

        element_name = child["Name"]

        if(element_name.startswith("Primary") or element_name.startswith("Secondary") or element_name.startswith("Success") or element_name.startswith("Warning")):

            print(element_name)

            design_type, element_type, __ = element_name.split("_")

            element_name = design_type+"_"+element_type
 
            if(element_type == "Gallery"):
                # We haven't yet defined the style for galleries
                # Feel free to contribute 
                pass
            
            else:

                design_type, _ , specific_properties, global_properties = getPropertiesFromName(element_name)
                print(_)
                updateComponent(child, specific_properties, global_properties, design_type)

                
    with open(os.path.join("./", jsonFile), "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-a','--app_file',dest = 'app_file', help='the name of the json file to update')
    parser.add_option('-s','--style_file',dest = 'style_file', help='the name of the json file containing the style to apply')
    (options,args) = parser.parse_args()

    if (options.app_file and options.style_file):
        # load the style
        with open(os.path.join("./", options.style_file), "r") as file:
            ELEMENTS = json.load(file)
        # Do the modifications
        updateJsonFile(options.app_file)
    else:
        raise MissingParameterError("Please make sure you are calling the program with the right parameters")
