from django.shortcuts import render
import requests, json, re
from django.http import HttpRequest, HttpResponse
# Create your views here.
from ConnectAlmMainApp.models import *
from django.db.models import Q

def artifact_list(sig):
    "List of all artifact IDs for a user"

    artifactsList = []
    users = User.objects.get(signum = sig)

    for artifact in Artifact.objects.filter(user_id=users):
        artifactsList.append(artifact)

    return artifactsList

def get_user(sig):
    if User.objects.filter(signum=sig):
        return "User exists"
    else:
        return "User does not exist"



def add_user(sig, userName):

    newUser = User(Name = userName, signum=sig)
    newUser.save()

def delete_artifcat(artifactId, sig):
    Artifact.artifact_id = artifactId
    users = User.objects.get(signum = sig)
    Artifact.objects.filter(artifact_id = artifactId, user_id = users).delete()

def insert_artifcat(artifactId, sig, newValue, newSatus):
    users = User.objects.get(signum = sig)
    if Artifact.objects.filter(artifact_id = artifactId, user_id = users).exists():
        print("Artifact Exists Already")
    else :
        newArtifact = Artifact(artifact_id = artifactId, user_id = users, status = newSatus, value = newValue, type= "")
        newArtifact.save()


def update_artifact(artifactID, newStatus):
     Artifact.objects.filter(artifact_id = artifactID).update(status = newStatus)

#This function takes a user name and password then produces a token from openAlm
def get_security_token(openAlmUser, openAlmPassword):

    status = True
    msg = None
    openAlmTokenUrl = "https://openalm.lmera.ericsson.se/api/v1/tokens"
    data = json.dumps({"username": openAlmUser, "password": openAlmPassword})
    r = requests.post(openAlmTokenUrl, data, auth=(openAlmUser, openAlmPassword))

    userId = 0
    token = ""
    strippedResponse = r.text.strip()

    for line in strippedResponse.splitlines():
        match = re.search('user_id', line)
        if match:
            uncleanId = line.split(':')[1].strip()
            userId = re.sub("[^0-9]", "", uncleanId)

        match = re.search('"token"', line)
        if match:
            uncleanToken = line.split(':')[1].strip()
            securityToken = re.sub("[^0-9a-zA-Z]", "", uncleanToken)

    if not securityToken:
        msg = "\nCould not obtain security token."
        status = False
    else:
        status=True

    return (status, msg, securityToken, userId)

#This function takes the artifact Id and returns the id, description and status of this particular one
def openAlmArtifact(artifactid) :
    status, msg, securityToken, userId = get_security_token("ecsdpdev", "t4eTecrazeNAwru4")
    url = "https://openalm.lmera.ericsson.se/api/v1/artifacts/"+str(artifactid)
    openAlmRequest = {"X-Auth-UserId":userId, "X-Auth-Token":securityToken}
    request = requests.get(url, headers=openAlmRequest)

    artifactId = 0
    processId = False
    value = "No Value"
    processValue = False
    status = "No Status"
    processStatus = False

    strippedResponse = request.text.strip()

    for line in strippedResponse.splitlines():
        match = re.search('"id"', line)
        if match and processId==False:
            uncleanId = line.split(':')[1].strip()
            artifactId = re.sub("[^0-9]", "", uncleanId)
            processId=True

        match = re.search('"value"', line)
        if match and processValue==False:
            value = line.split(':')[1].strip()
            processValue=True

        match = re.search('105348', line)
        if match and processStatus==False:
            status = "Not Started"
            processStatus=True

        match = re.search('105349', line)
        if match and processStatus==False:
            status = "In Progress"
            processStatus=True

        match = re.search('105350', line)
        if match and processStatus==False:
            status = "Done"
            processStatus=True

    return (artifactId, value, status)

def connect(request, input):
    input = input.upper()
    result = get_user(input)
    if(result == "User does not exist"):
        add_user(input, "")

    return addCORSHeaders(HttpResponse(json.dumps({}), content_type="application/json"))

def follow(request, input):
    sig,id=input.split("QQQQQ") # yeah thats right! 5 Qs!
    sig = sig.upper()
    artifactId, value, status = openAlmArtifact(id)
    if(artifactId==0):
        return HttpResponse("Artifact not found", content_type="application/json")
    insert_artifcat(artifactId, sig, value, status)
    return addCORSHeaders(HttpResponse(json.dumps({}), content_type="application/json"))

def unfollow(request, input):
    sig,id=input.split("QQQQQ") # yeah thats right! 5 Qs!
    sig = sig.upper()
    delete_artifcat(id, sig)
    return addCORSHeaders(HttpResponse(json.dumps({}), content_type="application/json"))

def poll(request, sig):
    sig = sig.upper()
    artifactList = []
    resultDictionary = {}
    if(get_user(sig)=="User exists"):
        for artifact in artifact_list(sig):
            artifactId, value, status = openAlmArtifact(artifact.artifact_id)
            if(status!=artifact.status):
                value = "The "+ artifact.value+" changed from "+artifact.status+" to "+status
                resultDictionary[artifactId] = value
                update_artifact(artifactId, status)
        return addCORSHeaders(HttpResponse(json.dumps(resultDictionary), content_type="application/json"))
    else:
        return addCORSHeaders(HttpResponse(json.dumps({}), content_type="application/json"))

def addCORSHeaders(theHttpResponse):
    if theHttpResponse and isinstance(theHttpResponse, HttpResponse):
        theHttpResponse['Access-Control-Allow-Origin'] = '*'
        theHttpResponse['Access-Control-Max-Age'] = '120'
        theHttpResponse['Access-Control-Allow-Credentials'] = 'true'
        theHttpResponse['Access-Control-Allow-Methods'] = 'HEAD, GET, OPTIONS, POST, DELETE'
        theHttpResponse['Access-Control-Allow-Headers'] = 'origin, content-type, accept, x-requested-with'
    return theHttpResponse



















