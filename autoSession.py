import csv
import json
import requests
from termcolor import colored

speakerDictionary = {}

monthMap = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}

def getDateString(date, time):
    day = '0' + date[0]
    month = monthMap[date[4:7]]
    year = date[8: 12]
    hours = time[0:2]
    minutes = time[2:4]
    seconds = '00'
    res = year + '-' + month + '-' + day + 'T' + hours + ':' + minutes + ':' + seconds
    return res

def getSpeakerObject(name):
    return speakerDictionary[name]

def populateSpeakerDictionary():
    with open('registeredSpeakers.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                speakerDictionary[row[0]] = {
                    "name": row[0],
                    "speakerId": row[1]
                }
            line_count += 1

def stringToArray(str):
    return str.split(' | ')
# {
#     "audiId":"606ee01f7332f623587e1962", //Object Id of the audi
#     "startTime":"2021-03-24T17:06:44.603Z", // Start time of the session
#     "endTime":"2021-04-27T17:06:44.603Z", // end time of the session
#     "sessionName":"Introduction to Placement in Google", // Name time of the session
#     "speakers":[
#         {
#             "speakerId":"604f922bcb2916a72cf533f8", // ObjectId of the speaker
#             "name":"Zachary Hamilton" //Name of the speaker
#         }
#     ]
# }

def replaceIfNotThere(str):
    if str == '?': return ''
    return str

populateSpeakerDictionary()
url = 'http://localhost:5000/api/user/session/create'
with open('sessions_sheet.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    total_successful = 0
    total_failed = 0
    total_skipped = 0
    successful = []
    failed = []
    skipped = []
    for row in csv_reader:
        if line_count != 0:
            body = {}
            body['audiId'] = '6075d99785e0694bf4683220'
            body['startTime'] = getDateString(row[2], row[3][0:4])
            body['endTime'] = getDateString(row[2], row[3][7:11])
            body['sessionName'] = row[4]
            body['sessionType'] = row[0]
            body['topic'] = row[1]
            body['companyName'] = replaceIfNotThere(row[8])
            body['speakers'] = []
            body['sessionSpace'] = replaceIfNotThere(row[6])
            if row[7] != '?':
                speakers = stringToArray(row[7])
                for speaker in speakers:
                    try:
                        body['speakers'].append(speakerDictionary[speaker])
                    except:
                        continue
            if row[7] != '?':
                response = requests.post(url, json=body, headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Il9pZCI6IjYwNmVkZGI5NzMzMmY2MjM1ODdlMTk2MCIsInJvbGUiOiJPcmdhbml6ZXIiLCJldmVudElkIjoiNjA2YzllYzc2NmYwYTg2YmIwYTdkYjgzIn0sImlhdCI6MTYxNzg3OTA1Mn0.NFWnunm-uD7fJFTMyjMhDutfUp0nY63EoX3Ij_u7iPs"})
                print(response.text)
                if response.status_code == 200:
                    total_successful += 1
                    successful.append(line_count)
                    print(colored(json.dumps(body, indent=4), 'green'))
                else:
                    total_failed += 1
                    failed.append(line_count)
                    print(colored(print(json.dumps(body, indent=4)), 'red'))
            else:
                total_skipped += 1
            # if line_count >= 1:
            #     break
        line_count += 1

    print(colored('successfully created: ' + str(total_successful), 'green'))
    print(colored('failed to create: ' + str(total_failed), 'red'))
    print(colored('skipped to create: ' + str(total_skipped), 'yellow'))
# print(speakerDictionary)
# print(getDateString('6th May 2021', '0855'))
# print(getSpeakerObject('Lim Kah Leong'))
