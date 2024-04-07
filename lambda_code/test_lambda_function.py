import sys
from boto3 import resource, client
from unittest import TestCase
import os
from moto import mock_aws
import json


sys.path.append('lambda_function.py')
from lambda_code.lambda_function import dyn_get_item,dyn_update_item, get_update_table_item, JSONEncoder, LambdaDynamoDBClass

# use moto for aws resource mock
@mock_aws
class TestViewCount(TestCase):
        
    def setUp(self):
        
        self.test_ddb_table_name = "unit_test_ddb"
        os.environ["DYNAMODB_TABLE_NAME"] = self.test_ddb_table_name
        dynamodb = resource("dynamodb", region_name="eu-central-1")
        dynamodb.create_table(
            TableName = self.test_ddb_table_name,
            KeySchema = [{"AttributeName": "Id", "KeyType": "HASH"}],
            AttributeDefinitions = [{"AttributeName": "Id", "AttributeType":"S"}],
            BillingMode = "PAY_PER_REQUEST"
        )
        
        mocked_dynamo_resource = {
            "resource": resource("dynamodb"),
            "table_name": self.test_ddb_table_name,
            "access_control_origin": "test.example.com"
            }
        self.mocked_dynamodb_class = LambdaDynamoDBClass(mocked_dynamo_resource)
        dynamodb_table = self.mocked_dynamodb_class.table
        dynamodb_table.put_item(
            Item = {
                "Id": "count",
                "Counts":{"pageviews": 0, "visits":0}
            }
        )

        
    def tearDown(self):
        dynamodb_resource = client("dynamodb", region_name ="eu-central-1")
        dynamodb_resource.delete_table(TableName = self.test_ddb_table_name)      
    
    def test_get_item(self):
        # check if data bas item is successfully returned
        items = dyn_get_item(self.mocked_dynamodb_class)
        count_json = json.dumps(items['Counts'], cls=JSONEncoder)
        self.assertEqual(count_json, json.dumps({"pageviews": 0, "visits":0}))
        
    def test_update_item(self):
        # check successfull data update     
        items = dyn_get_item(self.mocked_dynamodb_class)
        old_item = items['Counts']
        new_pageview = old_item['pageviews'] + 1
        new_visit = old_item['visits'] + 1
        
        updated_item = dyn_update_item(self.mocked_dynamodb_class, new_visit, new_pageview)
        res = updated_item["ResponseMetadata"]["HTTPStatusCode"]
        self.assertEqual(res, 200)
        
    def test_get_update_item(self):
        # check successfully handler response sent to request origin
        session_type = 'visit-pageview'
        res = get_update_table_item(self.mocked_dynamodb_class, session_type)
        self.assertEqual(res['statusCode'], 200)
        self.assertEqual(res['body'], json.dumps({'pageviews': 1, 'visits': 1}))
        
