import json
import os


# ALL_NAMES = ['Primary_Button', 'Secondary_Button', 'Primary_Label', 'Secondary_Label', 'Primary_Checkbox', 'Secondary_Checkbox',
#             'Primary_Radio', 'Secondary_Radio', 'Primary_TextInput', 'Secondary_TextInput', 'Primary_Dropdown', 'Secondary_Dropdown',
#             'Primary_Icon', 'Secondary_Icon', 'Primary_Shape', 'Secondary_Shape', 'Primary_Image', 'Secondary_Image']


# PARTICULAR_NAMES = ['Primary_Gallery', 'Secondary_Gallery'] 
# PARTICULAR_NAMES = [] 

DESIGN_VARIETIES = ["Primary","Secondary","Success","Warning"]


with open(os.path.join("./", "style.json"), "r") as file:
    ELEMENTS = json.load(file)


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
    # Load the JSON file
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
                # for subchild in child["Children"]:
                #     print(subchild["StyleName"])
                #     if(subchild["Template"]["Name"] == "image"):
                #         print("image")
                #     elif(subchild["Template"]["Name"] == "label"):
                #         if(subchild["StyleName"] == "subtitleLabelStyle"):
                #             design_type, _ , specific_properties, global_properties = getPropertiesFromName(design_type+"_Label")
                #             print(_)
                #             updateComponent(subchild, specific_properties, global_properties, design_type)
                #         elif(subchild["StyleName"] == "titleLabelStyle"):
                #             design_type, _ , specific_properties, global_properties = getPropertiesFromName(design_type+"_Label")
                #             print(_)
                #             updateComponent(subchild, specific_properties, global_properties, design_type)
                #     elif(subchild["Template"]["Name"] == "icon"):
                #         design_type, _ , specific_properties, global_properties = getPropertiesFromName(design_type+"_Icon")
                #         print(_)
                #         updateComponent(subchild, specific_properties, global_properties, design_type)
                #     elif(subchild["Template"]["Name"] == "rectangle"):
                #         design_type, _ , specific_properties, global_properties = getPropertiesFromName(design_type+"_Shape")
                #         print(_)
                #         updateComponent(subchild, specific_properties, global_properties, design_type)

                pass
            
            else:

                design_type, _ , specific_properties, global_properties = getPropertiesFromName(element_name)
                print(_)
                updateComponent(child, specific_properties, global_properties, design_type)

                
    # Write the modified JSON to a file
    with open(os.path.join("./", jsonFile), "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    updateJsonFile("3.json")