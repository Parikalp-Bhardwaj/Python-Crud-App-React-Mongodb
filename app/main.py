import re
from flask import Flask,request,jsonify,Response
from bson.objectid import ObjectId
import json

import pymongo


app = Flask(__name__)

try:

    mongo = pymongo.MongoClient(
    host="localhost",
    port=27017,
    serverSelectionTimeoutMS=1000)
    db = mongo.flask2
    mongo.server_info()

except:
    print("Not connected mongodb")







@app.route("/users",methods=["GET","POST"])
def getpost():
    if request.method == "GET":
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(response=json.dumps(data),
                status=200,
                mimetype="application/json")



    elif request.method == "POST":

        try:

            id = db.users.insert_one({
                "name":request.json["name"],
                "email":request.json["email"],
                "contact":request.json["contact"],
                "address":request.json["address"]
                })
            return Response(
                response=json.dumps({"message":"user created","id":f"{id.inserted_id}"}),
                status=200,
                mimetype="application/json")

        except Exception as err:
            return Response(
                response=json.dumps({"Message":f"{err}"}),
                status=400
            )



#Get By Id
@app.route("/users/<id>",methods=["GET"])
def getById(id):
    try:
        dbResponse = db.users.find_one({"_id":ObjectId(id)}),
        return Response(response=json.dumps({"data":f"{dbResponse}"}),status=200,mimetype="application/json")

    except Exception as err:
        print("***********",err)
        return Response(
            response=json.dumps(
                {"message":"Something went wrong","err":f"{err}"}),
                status=500,
                mimetype="application/json"
            )   

    

#Updated One

@app.route("/users/<id>",methods=["PATCH"])
def updateOne(id):
    try:
        dbResponse = db.users.update_one({"_id":ObjectId(id)},{"$set":{"name":request.json["name"]}})

        if dbResponse.modified_count == 1:
            return Response(
                    response=json.dumps(
                        {"message":"user updated"}),
                        status=200,
                        mimetype="application/json"
                )


        return Response(
            response=json.dumps(
                {"message":"nothing to be updated"}),
                status=200,
                mimetype="application/json"
            )   


    except Exception as err:
        print(f"*************{err}**********")
        return Response(response=json.dumps(
                {"message":"sorry cannot update anything"}),
                status=500,
                mimetype="application/json")   
            


#Updated Many
@app.route("/users/<id>",methods=["PUT"])
def updateMany(id):
    try:
        dbResponse = db.users.update_many({"_id":ObjectId(id)},{"$set":{"name":request.json["name"],
        "email":request.json["email"],"contact":request.json["contact"],"address":request.json["address"]}})

        if dbResponse.modified_count == 1:
            return Response(response=json.dumps({"messgae":"successfilly update"}),status=200,mimetype="application/json")
    
        return Response(
            response=json.dumps(
                {"message":"nothing to be updated"}),
                status=200,
                mimetype="application/json"
            )   

    except:
        return Response(response=json.dumps({"messgae":"inValid update"}),status=500,mimetype="application/json")


#Delete One
@app.route("/users/<id>",methods=["DELETE"])
def deleteInfo(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(
                response=json.dumps({"message":"user deleted","id":f"{id}"}),
                status=200,
                mimetype="application/user")

    except Exception as err:
        return Response(response=json.dumps(
            {"message":"sorry cannot delete user"}),
            status=500,
            mimetype="application/json")





app.run(debug=True)
