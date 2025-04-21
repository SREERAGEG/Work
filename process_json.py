import json

# Open and read the JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

def data_mapping_platoforms_benlysta(data):
    user_data=dict()
    submit_data=data[0].get("submit_data")
    for i in submit_data:
        if "Patient's First Name" == i.get("label"):
            user_data["First_name"]=i.get("value")
        
        if "Patient's Last Name" == i.get("label"):
            user_data["Last_name"]=i.get("value")

        if "Policy Holder " == i.get("label"):
            user_data["DOB"]=i.get("value")

        if "Patient's Address" == i.get("label"):
            user_data["Address"]=i.get("value")

        if "City" == i.get("label"):
            user_data["City"]=i.get("value")

        if "State" == i.get("label"):
            user_data["State"]=i.get("value")

        if "ZIP" == i.get("label"):
            user_data["ZIP"]=i.get("value")

        if "Patient Email ID" == i.get("label"):
            user_data["Email"]=i.get("value")

        if "Patient's contact number" == i.get("label"):
            user_data["Contact_number"]=i.get("value")

        if "Medical Insurance Name" == i.get("label"):
            user_data["Medical_Insurance_Name"]=i.get("value")

        if "Primary Insurance Member ID" == i.get("label"):
            user_data["Primary_Insurance_Member_ID"]=i.get("value")
    return user_data
# print(data_mapping_platoforms_benlysta(data))
with open("processed_json.json", "w") as file:
    json.dump(data_mapping_platoforms_benlysta(data), file)
