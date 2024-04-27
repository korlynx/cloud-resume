import json
from boto3 import resource
from botocore.exceptions import ClientError
from os import environ
from decimal import Decimal
import logging


_LAMBDA_DYNAMODB_RESOURCE = {
    "resource": resource('dynamodb'),
    "table_name": environ.get("DYNAMODB_TABLE_NAME", "NONE"),
    "access_control_origin": environ.get('ORIGIN_URL', 'NONE')
    }

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    global _LAMBDA_DYNAMODB_RESOURCE
    dynamodb_resource_class = LambdaDynamoDBClass(_LAMBDA_DYNAMODB_RESOURCE)
    session_type = event['queryStringParameters']['type']
    return get_update_table_item(dynamodb_resource_class, session_type)
        

class LambdaDynamoDBClass:
    def __init__(self, lambda_dynamodb_resource):
        self.access_origin = lambda_dynamodb_resource["access_control_origin"]
        self.resource = lambda_dynamodb_resource["resource"]
        self.table_name = lambda_dynamodb_resource["table_name"]
        self.table = self.resource.Table(self.table_name)

def dyn_get_item(dynamo_db_class):
    # get item from dynamodb table
    try:
        dynamodb_table_resource = dynamo_db_class.table
        dynamo_db_table_name = dynamo_db_class.table_name
        res = dynamodb_table_resource.get_item(Key={'Id': 'count'})
        logger.info("%s table items: %s", dynamo_db_table_name, res['Item'])
        
        return res['Item']
    except ClientError as err:
        logger.info(
            "Couldn't get item from table DyvnamoDB table named: %s. Here is why %s: %s",
            dynamo_db_table_name, err.response["Error"]["Code"], err.response["Error"]["Message"])
        return {"statusCode": err.response["Error"]["Code"], "body": err.response["Error"]["Message"]}
        

def dyn_update_item(dynamo_db_class, value_1, value_2):
    # update item in dynamodb table
    try:
        dynamodb_table_resource = dynamo_db_class.table
        dynamo_db_table_name = dynamo_db_class.table_name
        res = dynamodb_table_resource.update_item(
            Key={'Id': 'count'}, 
            UpdateExpression='set Counts.pageviews=:p, Counts.visits=:v',
            ExpressionAttributeValues={':v': value_1, ':p': value_2},
            ReturnValues='UPDATED_NEW'
        )
        logger.info("%s table item successfully updated. StatusCode: %s", dynamo_db_table_name, res["ResponseMetadata"]["HTTPStatusCode"])
        return res
    except ClientError as err:
        logger.info(
            "Couldn't update table: %s. Because of the following %s: %s",
            dynamo_db_table_name, err.response["Error"]["Code"], err.response["Error"]["Message"])
        return {"statusCode": err.response["Error"]["Code"], "body": err.response["Error"]["Message"]}

def get_update_table_item(dynamo_db_class, session_type):
    status_code = 200
    header =  {
                'Access-Control-Allow-Headers': 'application/json',
                'Access-Control-Allow-Origin': dynamo_db_class.access_origin,
                'Access-Control-Allow-Methods': 'GET'
            }
    body = json.dumps({'pageviews': 0, 'visits': 0})
    try:
        data_item = dyn_get_item(dynamo_db_class)
        data_item['Counts']['pageviews'] += 1
        
        if session_type == 'visit-pageview':
            data_item['Counts']['visits'] += 1
            
        # update data base with the new counts
        dyn_update_item(dynamo_db_class, data_item['Counts']['visits'], 
                        data_item['Counts']['pageviews'])
        new_item = dyn_get_item(dynamo_db_class)
        
        res = new_item['Counts']
        body = json.dumps(res, cls=JSONEncoder)
        
    except KeyError as index_err:
        status_code = 404
        logger.info("Not Found: %s", index_err)
    except Exception as other_error:
        status_code = 505
        logger.info("%s", other_error)
    finally:
        return {
            'statusCode': status_code,
            'headers': header,
            'body': body
        }
        
# convert Decimal to string
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)
