#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import json
import sys
from config import Config as config


class VideoDetect:
    jobId = ''
    rek = boto3.client('rekognition')
    queueUrl = config.queueUrl
    roleArn = config.roleArn
    topicArn = config.topicArn
    bucket = "kukukukay"
    video = "video.mp4"

    def main(self):

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
                        self.GetResultsPersons(rekMessage['JobId'])
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

        print('done')

    def GetResultsLabels(self, jobId):
        maxResults = 10
        paginationToken = ''
        finished = False

        while finished == False:
            response = self.rek.get_label_detection(JobId=jobId,
                                                    MaxResults=maxResults,
                                                    NextToken=paginationToken,
                                                    SortBy='TIMESTAMP')

            print(response['VideoMetadata']['Codec'])
            print(str(response['VideoMetadata']['DurationMillis']))
            print(response['VideoMetadata']['Format'])
            print(response['VideoMetadata']['FrameRate'])

            for labelDetection in response['Labels']:
                label = labelDetection['Label']

                print("Timestamp: " + str(labelDetection['Timestamp']))
                print("   Label: " + label['Name'])
                print("   Confidence: " + str(label['Confidence']))
                print("   Instances:")
                for instance in label['Instances']:
                    print("      Confidence: " + str(instance['Confidence']))
                    print("      Bounding box")
                    print("        Top: " +
                          str(instance['BoundingBox']['Top']))
                    print("        Left: " +
                          str(instance['BoundingBox']['Left']))
                    print("        Width: " +
                          str(instance['BoundingBox']['Width']))
                    print("        Height: " +
                          str(instance['BoundingBox']['Height']))
                    print()
                print()
                print("   Parents:")
                for parent in label['Parents']:
                    print("      " + parent['Name'])
                print()

                if 'NextToken' in response:
                    paginationToken = response['NextToken']
                else:
                    finished = True

    def GetResultsPersons(self, jobId):
        maxResults = 10
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
                print(person_bb)
                person_timestamp = personDetection['Timestamp']
                if person_index not in persons_bbs:
                    persons_bbs[person_index] = {}
                persons_bbs[person_index][person_timestamp] = person_bb
                # print('Index: ' + str(personDetection['Person']['Index']))
                # print('Timestamp: ' + str(personDetection['Timestamp']))
                # print()

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True
                print(persons_bbs)


if __name__ == "__main__":

    analyzer = VideoDetect()
    # analyzer.main()
    analyzer.GetResultsPersons(
        jobId="a60a8e87ad9f4efbeff7987d826e42a6fcedf82f3a9d6edd8d4c010ee23dd7c2"
    )
