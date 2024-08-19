import os
import boto3
import json

# Initialize the Bedrock clients
boto3_session = boto3.session.Session()
bedrock_runtime_client = boto3_session.client('bedrock-runtime')
bedrock_agent_client = boto3_session.client('bedrock-agent-runtime')

# Set the model ID for Titan Text G1 - Premier
model_id = "amazon.titan-text-premier-v1:0"

def retrieve_information(input_text, knowledge_base_id):
    print("Retrieving information for:", input_text, "from knowledge base:", knowledge_base_id)
    response = bedrock_agent_client.retrieve(
        knowledgeBaseId=knowledge_base_id,
        retrievalQuery={
            'text': input_text
        },
        retrievalConfiguration={
            'vectorSearchConfiguration': {
                'numberOfResults': 100
            }
        }
    )
    print("Retrieve response:", response)  # Debugging line
    return response

def generate_answer(input_text, retrieved_information, conversation_history):
    print("Generating answer for:", input_text, "using model:", model_id)
    response = bedrock_runtime_client.invoke_model(
        modelId=model_id,
        contentType='application/json',
        accept='application/json',
        body=json.dumps({
            "inputText": conversation_history + "\n" + input_text + " " + retrieved_information,
            "textGenerationConfig": {
                "temperature": 0.7,
                "topP": 0.9,
                "maxTokenCount": 512
            }
        })
    )
    print("Generate response:", response)  # Debugging line
    return response

def lambda_handler(event, context):
    if 'question' not in event or 'knowledge_base_id' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Question and knowledge_base_id parameters are required'})
        }

    question = event['question']
    knowledge_base_id = event['knowledge_base_id']
    conversation_history = event.get('conversation_history', '')

    try:
        # Step 1: Retrieve information from the knowledge base
        retrieval_response = retrieve_information(question, knowledge_base_id)
        retrieved_text = retrieval_response['retrievalResults'][0]['content']['text']
        
        print("Retrieved text:", retrieved_text)  # Debugging line
        
        # Step 2: Generate answer using the retrieved information
        bedrock_response = generate_answer(question, retrieved_text, conversation_history)
        
        # Extracting the relevant part of the response
        response_body = bedrock_response['body'].read().decode('utf-8')
        print("Response body:", response_body)  # Debugging line
        response_data = json.loads(response_body)
        
        # Extract the generated text
        answer = response_data.get('results', [])[0].get('outputText', 'No relevant answer found')
        
        # Logging the answer for debugging purposes
        print("Answer retrieved:", answer)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'answer': answer})
        }
    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
