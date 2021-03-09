import csv
import requests
from termcolor import colored

with open('RegList.csv') as csv_file:
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
            eventId = "60424ae16bd9d2557e6543bb"
            email = row[7]
            password = "hiv21mar"
            role = "User"
            firstName = row[2]
            lastName = row[3]
            companyName = row[5]
            title = row[4]
            country = row[6]
            isLinkedinAllowed = False
            isInvited = False
            ticketId = "60424c9f1a905600345da05b"
            user_payload = [
                ("firstName", firstName),
                ("lastName", lastName),
                ("email", email),
                ("password", password),
                ("company", companyName),
                ("title", title),
                ("country", country),
                ("eventId", eventId),
                ("ticketId", ticketId),
                ("role", role)
            ]
            usersList.append(user_payload)
            url = "https://api.engagepulse.me/api/user/signup"
            files = {'profileImg': open('avatar_placeholder.png', 'rb')}
            response = requests.post(url, data=user_payload, files=files)
            if response.status_code != 201:
                print(colored(response.text, 'red'))
                # break
            else:
                print(colored(response.text, 'green'))
            # if line_count >= 5:
            #     break
        line_count += 1
    print(f'Processed {line_count} users.')

# D:/ENTERTAINMENT/_study_videos/WEB_DEV_MERN/Web_Development/_Internship_growthgear/automationScripts/avatar_placeholder.png