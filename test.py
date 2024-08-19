import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv
import os

load_dotenv()

def lambda_handler(event, context):
    question = event.get("question", "")
    knowledge_base_id = event.get("knowledge_base_id", "")

    if not question:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Question parameter is required"})
        }

    if not knowledge_base_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Knowledge base ID is required"})
        }

    try:
        # Here, you would typically query your knowledge base
        # For the sake of example, let's assume we have a function get_ic_test_answer
        answer = get_ic_test_answer(question, knowledge_base_id)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"answer": answer})
        }
    except (BotoCoreError, ClientError) as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Unexpected error: {str(e)}"})
        }

def get_ic_test_answer(question, knowledge_base_id):
    # Implement your logic to retrieve answer from the knowledge base using the ID
    # For now, returning a dummy response
    return {
        "retrievalResults": [
            {"content": {"text": f"This is a sample response from knowledge base {knowledge_base_id}."}}
        ]
    }

# Simulate Lambda event
event = {
    "question": "Tell me about the facilities in IC",
    "knowledge_base_id": "sample_kb_id"
}

# Simulate Lambda context
context = {}

# Invoke the Lambda function locally
response = lambda_handler(event, context)
print(json.dumps(response, indent=4))


import os
from dotenv import load_dotenv

load_dotenv()

region_name = os.getenv('REGION_NAME')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
knowledge_base_id = os.getenv('Knowledge_Base_ID')

# Print environment variables to verify they are loaded correctly
print(f"Region: {region_name}")
print(f"Access Key ID: {aws_access_key_id}")
print(f"Secret Access Key: {aws_secret_access_key}")
print(f"Knowledge Base ID: {knowledge_base_id}")


