import json
def get_processed_json():
    try:
        with open("./processed_json.json","r") as file:
        # Sample json format : {"First_name": "Aevy", "Last_name": "Jackson", "Address": "A803", "City": "Dover", "State": "Delaware", "ZIP": "19901", "Contact_number": "+1 6193248725", "Email": "anoj.viswanathan@gmail.com", "Medical_Insurance_Name": "Aetna", "Primary_Insurance_Member_ID": "5676532q"}
            return json.load(file)
    except:
        print("Load json file failed")

# print(get_processed_json()["Contact_number"].split()[-1])
processed_json=get_processed_json()
full_name=processed_json["First_name"]+ (f" {processed_json["Last_name"]}" if len(processed_json["Last_name"]) else "")
print(full_name)
