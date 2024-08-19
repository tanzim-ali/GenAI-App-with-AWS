from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import JSONResponse
import boto3
import json
import os
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow only your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lambda_client = boto3.client(
    'lambda',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def get_context(question: str, knowledge_base_id: str, conversation_history: str):
    try:
        # Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName='retrievedata',  # Replace with your actual Lambda function name
            InvocationType='RequestResponse',
            Payload=json.dumps({
                "question": question,
                "knowledge_base_id": knowledge_base_id,
                "conversation_history": conversation_history
            })
        )

        # Read the Lambda function's response stream and parse it
        response_payload = response['Payload'].read()
        response_payload_dict = json.loads(response_payload)
        
        if 'body' not in response_payload_dict:
            raise ValueError("No 'body' in Lambda response")
        
        body = json.loads(response_payload_dict['body'])
        
        if 'answer' not in body:
            raise ValueError("No 'answer' in Lambda response body")
        
        return {"response": body['answer']}
    
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat_with_knowledge_base")
def chat_with_knowledge_base(query: str = Query(...), knowledge_base_id: str = Query(...), body: dict = Body(...)): 
    conversation_history = body.get('conversation_history', '')
    context = get_context(query, knowledge_base_id, conversation_history)
    return JSONResponse(content=context, status_code=200)
