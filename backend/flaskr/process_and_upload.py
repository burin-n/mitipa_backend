from getPersonBoundingBox import VideoDetect
from process import Process
from dynamo import DynamoDB

import pickle


def process_and_upload(clientId, location, video):
    # videoDetect = VideoDetect()
    process = Process()
    dynamo = DynamoDB()
    # person_bbs = videoDetect.query_and_receive(video)
    # result = process.process_score(person_bbs)
    a = pickle.load(open("bbs4.p", "rb"))
    result = process.process_score(data=a)
    data = {
        "clientId": clientId,
        "location": location,
        "sitting_heatmap": result["sitting_heatmap"],
        "existence_heatmap": result["existence_heatmap"],
        "person_state": result["person_state"]
    }
    dynamo.upload(data)
    return "SUCCESSFUL OPERATION"


response = process_and_upload("buruay", "nonthaburuay", "video.mp4")
print(response)
