__author__ = 'karthik'

import requests, csv, urllib, time

__ROOM_NAME__ = "" # Enter Hipchat Room
__AUTH_TOKEN__ = " " # Enter Auth_Token


class API_CONSTANTS:

    BASE_URL = "https://api.hipchat.com/"
    VERSION = "v2/"

    #URL Constants
    ROOM_STRING = "room/"
    MEMBERS_STRING = "member"

    #query params
    AUTH_TOKEN_STRING = "auth_token"


class Room :
    def __init__(self, room_name):
        self.room_name = urllib.quote(room_name,safe="%/:=&?~#+!$,;'@()*[]")

    def getRoomDetails(self):
        requestString = API_CONSTANTS.BASE_URL+API_CONSTANTS.VERSION+API_CONSTANTS.ROOM_STRING+self.room_name+"/"+API_CONSTANTS.MEMBERS_STRING+"?"+API_CONSTANTS.AUTH_TOKEN_STRING+"="+__AUTH_TOKEN__
        response = requests.get(requestString)
        if response.status_code == 200:
            self.details = response.json()
            return
        self.details =None

    def getAllEmails(self):
        items = self.details["items"]
        emails = []
        for user in items:
            self = user["links"]["self"]
            if self:
                response = requests.get(self+"?"+API_CONSTANTS.AUTH_TOKEN_STRING+"="+__AUTH_TOKEN__)
                if response.status_code == 200:
                    response = response.json()
                    if response["email"]:
                        emails.append(response["email"])
        return emails


if __name__ == '__main__':
    tigers_room = Room(__ROOM_NAME__)
    tigers_room.getRoomDetails()
    emails = tigers_room.getAllEmails()

    fileName  = "emails_"+ str(int(time.time()))+".csv"
    resultFile = open(fileName,'wb')
    writer = csv.writer(resultFile,dialect='excel')
    writer.writerow(emails)


