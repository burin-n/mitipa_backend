class Config:
    # database configuration
    host = "mitipa.cs1xewchsmfa.ap-northeast-1.rds.amazonaws.com"
    port = "3306"
    user = "mitipa"
    passwd = "nitipatjaidee"
    database = "innodb"
    topicArn = "arn:aws:sns:ap-northeast-1:665685927457:AmazonRekognition"
    queueUrl = "https://sqs.ap-northeast-1.amazonaws.com/665685927457/mitipa-rekognition-queue"
    # roleArn = "arn:aws:iam::665685927457:role/mitipa-rekognition-service-role"
    roleArn = "arn:aws:iam::665685927457:role/mitipa-role"
    videoBucket = "mitipa-video"
