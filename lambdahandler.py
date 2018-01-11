import json
import boto3

bucketName = "myserverlesrpa"
filename = "tssdata.json"
s3 = boto3.client("s3")
def getTheJsonFile():
    objData =s3.get_object(Bucket=bucketName,Key=filename)
    return objData["Body"].read().decode()

def loadJsonData(theFileStr):
    return json.loads(theFileStr)

def saveDataToFile(theData):
    prevData = loadJsonData(getTheJsonFile())
    es = prevData["data"]
    es.append(json.loads(theData))
    fullData = json.dumps(prevData)
    s3.put_object(Body=fullData.encode(), Bucket=bucketName, Key=filename)
    return "1"


def lambda_handler(event, context):
    # TODO implement
    resp= {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": "No_Data"}
    datasz = loadJsonData(getTheJsonFile())
    # rs = ""
    # for key, val in datasz.items():
    #     rs += key+" "
    if event["httpMethod"] == "GET":
        resp =  {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"data":datasz["data"]})}
    elif event["httpMethod"] == "POST":
        resp =  {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(saveDataToFile(event["body"]))}

    return resp
