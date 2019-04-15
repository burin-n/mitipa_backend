#
#  Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
#
#  http://aws.amazon.com/apache2.0/
#
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
from config import Config as config


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class DynamoDB:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(config.dynamoDB_name)

    def upload(self, data):
        response = self.table.put_item(
            Item={
                "clientId": data["clientId"],
                "location": data["location"],
                "score": data["score"]
            })
        print("PutItem succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))


# db = DynamoDB()
# data = {"clientId": "burinrinrin", "location": "teenee", "score": 10}
# db.upload(data)
