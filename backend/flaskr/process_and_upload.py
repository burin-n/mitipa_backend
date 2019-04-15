from getPersonBoundingBox import VideoDetect
from process import Process
from dynamo import DynamoDB


def process_and_upload(clientId, location, video):
    videoDetect = VideoDetect()
    process = Process()
    dynamo = DynamoDB()
    person_bbs = videoDetect.query_and_receive(video)
    score = process.easy_loop_leave_count(person_bbs)
    data = {"clientId": clientId, "location": location, "score": score}
    dynamo.upload(data)
    return "SUCCESSFUL OPERATION"


response = process_and_upload("buruay", "silom", "video.mp4")
print(response)
