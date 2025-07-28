import json
import boto3
import logging
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda function to invoke Claude Haiku via Bedrock
    
    Expected event structure:
    {
        "prompt": "Your question or prompt here",
        "max_tokens": 1000,  # optional, default 1000
        "temperature": 0.7   # optional, default 0.7
    }
    """
    
    try:
        # Initialize Bedrock client
        bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # Extract parameters from event
        prompt = event.get('prompt', '')
        max_tokens = event.get('max_tokens', 1000)
        temperature = event.get('temperature', 0.7)
        
        if not prompt:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Prompt is required'
                })
            }
        
        # Prepare the request body for Claude Haiku
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # Model ID for Claude Haiku
        model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        
        logger.info(f"Invoking Claude Haiku with prompt: {prompt[:100]}...")
        
        # Invoke the model
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body),
            contentType='application/json',
            accept='application/json'
        )
        
        # Parse the response
        response_body = json.loads(response['body'].read())
        
        # Extract the generated text
        generated_text = response_body['content'][0]['text']
        
        logger.info("Successfully generated response from Claude Haiku")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'response': generated_text,
                'usage': response_body.get('usage', {}),
                'model': model_id
            }, indent=2)
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS Client Error: {error_code} - {error_message}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'AWS Error: {error_code}',
                'message': error_message
            })
        }
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }


# CLI test function (for local testing)
def test_locally():
    """
    Function to test the Lambda locally before deployment
    """
    test_event = {
        "prompt": "Explain quantum computing in simple terms",
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    result = lambda_handler(test_event, None)
    print("Test Result:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    test_locally()
