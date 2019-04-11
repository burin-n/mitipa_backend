import boto3
from utils import eprint


class S3:
    def __init__(self):
        pass

    def list_buckets(self, user="s3"):
        # boto3.setup_default_session(profile_name=user)
        s3 = boto3.client("s3")
        response = s3.list_buckets()
        buckets = [bucket["Name"] for bucket in response["Buckets"]]
        print("Bucket List: %s" % buckets)
        return buckets

    def upload_to_bucket(self,
                         filePath,
                         fileName,
                         user="s3-mitipa",
                         bucket_name="mitipa-video"):
        # boto3.setup_default_session(profile_name=user)
        s3 = boto3.client("s3")
        try:
            s3.upload_file(filePath, bucket_name, fileName)
        except:
            eprint("s3_upload_error")

    def list_items_in_bucket(self, bucket_name, user="s3-mitipa"):
        # boto3.setup_default_session(profile_name=user)
        s3 = boto3.client("s3")
        keys = []
        resp = s3.list_objects_v2(Bucket=bucket_name)
        for obj in resp["Contents"]:
            keys.append(obj["Key"])
        return keys


s3 = S3()
# s3.upload_to_bucket(
#     "/Users/chanokthornuerpairojkit/Desktop/classvids/classvid2/videos/20190218_143733.mp4",
#     "video",
#     user="s3",
#     bucket_name="kukukukay")
# print(s3.list_buckets(user="s3"))
print(s3.list_items_in_bucket("kukukukay", user="s3"))
