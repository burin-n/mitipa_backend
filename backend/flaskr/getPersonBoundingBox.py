#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import json
import sys
from config import Config as config
import pickle


class VideoDetect:
    jobId = ''
    rek = boto3.client('rekognition')
    queueUrl = config.queueUrl
    roleArn = config.roleArn
    topicArn = config.topicArn
    bucket = "kukukukay"

    # video = "video.mp4"

    def query_and_receive(self, video):
        self.video = video
        response = self.query_rekognition()
        return response

    def query_rekognition(self):

        jobFound = False
        sqs = boto3.client('sqs')

        #=====================================
        response = self.rek.start_person_tracking(
            Video={'S3Object': {
                'Bucket': self.bucket,
                'Name': self.video
            }},
            NotificationChannel={
                'RoleArn': self.roleArn,
                'SNSTopicArn': self.topicArn
            })
        #=====================================
        print('Start Job Id: ' + response['JobId'])
        dotLine = 0
        while jobFound == False:
            sqsResponse = sqs.receive_message(QueueUrl=self.queueUrl,
                                              MessageAttributeNames=['ALL'],
                                              MaxNumberOfMessages=10)

            if sqsResponse:

                if 'Messages' not in sqsResponse:
                    if dotLine < 20:
                        print('.', end='')
                        dotLine = dotLine + 1
                    else:
                        print()
                        dotLine = 0
                    sys.stdout.flush()
                    continue

                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    rekMessage = json.loads(notification['Message'])
                    print(rekMessage['JobId'])
                    print(rekMessage['Status'])
                    if str(rekMessage['JobId']) == response['JobId']:
                        print('Matching Job Found:' + rekMessage['JobId'])
                        jobFound = True
                        #=============================================
                        response = self.GetResultsPersons(rekMessage['JobId'])
                        #=============================================

                        sqs.delete_message(
                            QueueUrl=self.queueUrl,
                            ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" + str(rekMessage['JobId']) +
                              ' : ' + str(response['JobId']))
                    # Delete the unknown message. Consider sending to dead letter queue
                    sqs.delete_message(QueueUrl=self.queueUrl,
                                       ReceiptHandle=message['ReceiptHandle'])

        return response

    def GetResultsPersons(self, jobId):
        maxResults = 1000
        paginationToken = ''
        finished = False
        persons_bbs = {}

        while finished == False:
            response = self.rek.get_person_tracking(JobId=jobId,
                                                    MaxResults=maxResults,
                                                    NextToken=paginationToken)

            # print(response['VideoMetadata']['Codec'])
            # print(str(response['VideoMetadata']['DurationMillis']))
            # print(response['VideoMetadata']['Format'])
            # print(response['VideoMetadata']['FrameRate'])

            for personDetection in response['Persons']:
                person_index = personDetection['Person']['Index']
                if 'BoundingBox' not in personDetection['Person']:
                    continue
                person_bb = personDetection['Person']['BoundingBox']
                # print(person_bb)
                person_timestamp = personDetection['Timestamp']
                if person_index not in persons_bbs:
                    persons_bbs[person_index] = {}
                persons_bbs[person_index][person_timestamp] = person_bb

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True
                pickle.dump(persons_bbs, open("bbs4.p", "wb"))
                return persons_bbs


if __name__ == "__main__":

    analyzer = VideoDetect()
    analyzer.query_and_receive("305_1.mp4")
    # analyzer.main()
    # analyzer.GetResultsPersons(
    #     # jobId="a60a8e87ad9f4efbeff7987d826e42a6fcedf82f3a9d6edd8d4c010ee23dd7c2"
    # )
