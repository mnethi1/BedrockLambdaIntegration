# Basic invocation
aws lambda invoke \
  --function-name your-lambda-function-name \
  --payload '{"prompt": "What is machine learning?"}' \
  response.json && cat response.json

# With custom parameters
aws lambda invoke \
  --function-name your-lambda-function-name \
  --payload '{"prompt": "Explain Python decorators", "max_tokens": 800, "temperature": 0.5}' \
  response.json && cat response.json
