import csv
import json
import requests
from termcolor import colored

userDictionary = []
with open('SpeakersSheet.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    usersList = []
    headers = ["firstName", "lastName", "email", "password", "companyName", "title", "country", "isInvited", "isLinkedinAllowed", "eventId", "ticketId",
     "role", "profileImg"]
    for row in csv_reader:
        # print(row)
        if line_count != 0:
            # print(row)
            user = []
            profileImg = "D:/ENTERTAINMENT/_study_videos/WEB_DEV_MERN/Web_Development/_Internship_growthgear/automationScripts/avatar_placeholder.png"
            eventId = "605e03b1d6126847dc6e334d"
            email = row[4]
            password = ""
            role = "User"
            firstName = row[1]
            lastName = row[2]
            companyName = row[3]
            if row[3] == '?':
                companyName = ''
            title = ""
            country = "Singapore"
            isLinkedinAllowed = False
            isInvited = False
            # ticketId = "60424c9f1a905600345da05b"
            user_payload = [
                ("firstName", firstName),
                ("lastName", lastName),
                ("email", email),
                ("password", password),
                ("company", companyName),
                ("title", title),
                ("country", country),
                ("eventId", eventId),
                # ("ticketId", ticketId),
                ("role", role),
                ("occupationCategory", "NNI Staff"),
                ("occupationRole", 100)
            ]
            usersList.append(user_payload)
            # url = "https://api.engagepulse.me/api/user/signup"
            url = "http://localhost:5000/api/user/signup"
            files = {'profileImg': open('avatar_placeholder.png', 'rb')}
            response = requests.post(url, data=user_payload, files=files)
            print(user_payload)
            if response.status_code != 201:
                print(colored(response.text, 'red'))
                # break
            else:
                print(colored(response.text, 'green'))
                obj = json.loads(response.text)
                userDictionary.append({'name': row[0], 'speakerId': obj['userId'], 'email': email, 'password': password})
            # if line_count >= 2:
            #     break
        line_count += 1
    print(f'Processed {line_count} users.')
    print(userDictionary)

with open('registeredSpeakers.csv', mode='w', newline='') as csv_file:
    fieldnames = ['name', 'speakerId', 'email', 'password']
    file_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    file_writer.writeheader()
    for user in userDictionary:
        file_writer.writerow(user)

# D:/ENTERTAINMENT/_study_videos/WEB_DEV_MERN/Web_Development/_Internship_growthgear/automationScripts/avatar_placeholder.png

# POST https://dev-api.engagepulse.me/api/user/login/
# body = {email: "kritagya@growthgear.in", password: "thullu"}