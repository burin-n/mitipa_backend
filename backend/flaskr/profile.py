import boto3
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--my-profile", dest = "myProfile", default = "default", help="My AWS Profile")

args = parser.parse_args()

myAWSSession = boto3.Session(profile_name=args.myProfile)

mySts = myAWSSession.client('sts').get_caller_identity()
myArn = mySts["Arn"]
myAccount = mySts["Account"]
myUser = myArn.split('/')[-1]

print("My profile user: {}".format(myUser))