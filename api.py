import json
from fastapi import FastAPI,BackgroundTasks,Query,Body
from test import  test
from task_crawl_aimovig import crawl_aimovig
from task_crawl_baush_access import  crawl_baush_access
from task_crawl_izervay import  crawl_izervay
from task_crawl_benlysta import crawl_benlysta_copay

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

from helpers import insert_data


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


def data_mapping(user_data):
    data = {}
    data["first_name"]=user_data.get("firstName")
    data["address"]=user_data.get("address")
    data["zip_code"]=user_data.get("zipCode")
    data["dob"]=user_data.get("birthDate").get("month")+"/"+user_data.get("birthDate").get("day")+"/"+user_data.get("birthDate").get("year")
    data["second_name"]=user_data.get("lastName")
    data["gender"]=user_data.get("gender")
    data["city"]=user_data.get("city")
    data["phone_number"]=user_data.get("contactNumber")
    data["email"]=user_data.get("email")
    data["medicine"]=user_data.get("drugName")
    return data

def data_mapping_platoforms(user_data):
    data = {}
    submit_data = user_data[0].get("submit_data")
    data["first_name"]=submit_data.get("fid8").get("value")
    data["address"]=submit_data.get("fid11").get("value")
    data["zip_code"]=submit_data.get("fid14").get("value")
    data["dob"]=submit_data.get("fid10").get("value")
    data["second_name"]=submit_data.get("fid9").get("value")
    data["gender"]=submit_data.get("fid17").get("value")
    data["city"]=submit_data.get("fid12").get("value")
    data["phone_number"]=submit_data.get("fid18").get("value")
    data["email"]=submit_data.get("fid19").get("value")
    data["medicine"]=submit_data.get("fid21").get("value")
    return data

def data_mapping_platoforms_samacare(data):
    user_data = dict()
    submit_data = data[0].get("submit_data")
    for k,i in submit_data.items():
        if "Patient's First Name" == i.get("label"):
            user_data["first_name"] = i.get("value")
        if "Name of the Drug" == i.get("label"):
            user_data["medicine"] = i.get("value")
        if "Patient's Last Name" == i.get("label"):
            user_data["second_name"] = i.get("value")
        if "Date of Birth" == i.get("label"):
            dob = i.get("value")
            user_data["dob_day"] = str((dob.split("/")[0]))
            user_data["dob_month"] = str((dob.split("/")[1]))
            user_data["dob_year"] = str((dob.split("/")[2]))
            user_data["dob"] = user_data["dob_day"]+"/"+user_data["dob_month"]+"/"+user_data["dob_year"]
        if "Patient's Address" == i.get("label"):
            user_data["address"] = i.get("value")
        if "Patient's Gender" == i.get("label"):
            user_data["gender"] = i.get("value")
        if "City" == i.get("label"):
            user_data["city"] = i.get("value")
        if "State" == i.get("label"):
            user_data["state"] = i.get("value")
        if "ZIP" == i.get("label"):
            user_data["zip_code"] = i.get("value")
        if "Patient Email ID" == i.get("label"):
            user_data["email"] = i.get("value")
        if "Patient's Contact Number" == i.get("label"):
            user_data["phone_number"] = i.get("value")
        if "Medical Insurance Name" == i.get("label"):
            user_data["medical_insurance_name"] = i.get("value")
        if "Primary Insurance Member ID" == i.get("label"):
            user_data["medical_insurance_id"] = i.get("value")
        if "Physician's Email Address" == i.get("label"):
            user_data["provider_email"] = i.get("value")
    return user_data


def data_mapping_platoforms_benlysta(data):
    user_data=dict()
    submit_data=data[0].get("submit_data")
    for i in submit_data:
        if "Patient's First Name" == i.get("label"):
            user_data["first_name"]=i.get("value")

        if "Select the drug" == i.get("label"):
            user_data["medicine"]=i.get("value")
        
        if "Patient's Last Name" == i.get("label"):
            user_data["last_name"]=i.get("value")

        if "Date of Birth" == i.get("label"):
            dob=i.get("value")
            user_data["dob_day"]= str(int(dob.split("/")[0]))
            user_data["dob_month"]= str(int(dob.split("/")[1]))
            user_data["dob_year"]= str(int(dob.split("/")[2]))

        if "Patient's Address" == i.get("label"):
            user_data["address"]=i.get("value")

        if "City" == i.get("label"):
            user_data["city"]=i.get("value")

        if "State" == i.get("label"):
            user_data["state"]=i.get("value")

        if "ZIP" == i.get("label"):
            user_data["zip"]=i.get("value")

        if "Patient Email ID" == i.get("label"):
            user_data["email"]=i.get("value")

        if "Patient's contact number" == i.get("label"):
            user_data["phone_number"]=i.get("value")[-10:]

        if "Medical Insurance Name" == i.get("label"):
            user_data["medical_insurance_name"]=i.get("value")

        if "Primary Insurance Member ID" == i.get("label"):
            user_data["medical_insurance_id"]=i.get("value")

        if "Physician's Email Address" == i.get("label"):
            user_data["provider_email"]=i.get("value")
    return user_data

@app.get("/health")
def health():
    return {"status": "OK"}

@app.get("/test-data-push")
def test_push():
    try:
        test.apply_async(args=[],queue='test',routing_key='copay_crawler.test')
        return {"status": True}
    except Exception as EX:
        return {"status":False,"exception":str(EX)}

@app.get("/crawl_aimovig")
def call_crawl_aimovig(email_to: str = Query(..., description="Email To send Attachment")):
    try:
        crawl_aimovig.apply_async(args=[email_to],queue='crawl_aimovig',routing_key='copay_crawler.crawl_aimovig')
        return {"status": True,"message":"Job Scheduled !"}
    except Exception as EX:
        return {"status":False,"exception":str(EX)}

@app.get("/crawl_baush_access")
def call_crawl_baush_access(email_to: str = Query(..., description="Email To send Attachment")):
    try:
        crawl_baush_access.apply_async(args=[email_to],queue='crawl_baush_access',routing_key='copay_crawler.crawl_baush_access')
        return {"status": True,"message":"Job Scheduled !"}
    except Exception as EX:
        return {"status":False,"exception":str(EX)}


@app.post("/crawl_foundation")
def crawl_foundation(user_data: dict = Body(..., description="User data in JSON format")):
    s3_url = [
    "https://foundational-crawler-downloads.s3.ap-south-1.amazonaws.com/grant_card.png",
    "https://foundational-crawler-downloads.s3.ap-south-1.amazonaws.com/grand_card_2.jpeg"
    ]
    import random
    return {"status": True,"s3_url":random.choice(s3_url)}


@app.post("/webhook_samacare")
async def crawl_copay_webhook_samacare(request: Request):
    user_data = await request.json()
    try:
        # Process user_data as needed
        #with open("data_1.json","w") as f:
        #    f.write(json.dumps(user_data,indent=4))
        user = data_mapping_platoforms_samacare(user_data)
        with open("data_1.json","w") as f:
            f.write(json.dumps(user,indent=4))
        medicine = user.get("medicine")
        if medicine.lower() == "aimovig":
            crawl_aimovig.apply_async(args=[user], queue='crawl_aimovig', routing_key='copay_crawler.crawl_aimovig')
        elif medicine.lower() == "besivance" or medicine.lower() == "lotemax":
            crawl_baush_access.apply_async(args=[user], queue='crawl_baush_access',
                                           routing_key='copay_crawler.crawl_baush_access')
        elif medicine.lower() == 'izervay':
            crawl_izervay.apply_async(args=[user], queue='crawl_izervay',
                                      routing_key='copay_crawler.crawl_izervay')
        else:
            return {"status": True, "message": "Job not Scheduled Ivalid Medicine !", "data": user}

        #insert_data("copay_card_form", user_data)
        return {"status": True, "message": "Job Scheduled !", "data": user_data}
    except Exception as EX:
        return {"status": False, "exception": str(EX), "data": user_data}


@app.post("/crawl_copay")
def crawl_copay(user_data: dict = Body(..., description="User data in JSON format")):
    try:
        # Process user_data as needed
        user = data_mapping(user_data)
        medicine = user.get("medicine")
        if medicine.lower()=="aimovig":
            crawl_aimovig.apply_async(args=[user], queue='crawl_aimovig', routing_key='copay_crawler.crawl_aimovig')
        elif medicine.lower()=="besivance" or medicine.lower()=="lotemax":
            crawl_baush_access.apply_async(args=[user], queue='crawl_baush_access',
                                           routing_key='copay_crawler.crawl_baush_access')
        elif medicine.lower()=='izervay':
            crawl_izervay.apply_async(args=[user], queue='crawl_izervay',
                                           routing_key='copay_crawler.crawl_izervay')
        else:
            return {"status": True, "message": "Job not Scheduled Ivalid Medicine !", "data": user}

        insert_data("copay_card_form",user_data)
        return {"status": True, "message": "Job Scheduled !", "data": user_data}
    except Exception as EX:
        return {"status": False, "exception": str(EX),"data":user_data}


@app.post("/webhook_benlysta")
async def crawl_benlysta(request: Request):
    user = await request.json()
    #user_data  = data_mapping_platoforms_benlysta(user)
    with open("data.json","w") as f:
        f.write(json.dumps(user,indent=4))
    try:
        # Process user_data as needed
        user = data_mapping_platoforms_benlysta(user)
        #with open("data.json","w") as f:
         #   f.write(json.dumps(user,indent=4))
        if user.get("medicine") == 'Benlysta':
            crawl_benlysta_copay.apply_async(args=[user], queue='crawl_benlysta', routing_key='copay_crawler.crawl_benylsta')
            return {"status": True, "message": "Job Scheduled !", "data": user}
        else:
            return {"status": True, "message": "Medicine Request not in List !", "data": user}
    except Exception as EX:
        return {"status": False, "exception": str(EX), "data": user}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
