import boto3
from app.models.prompt_record import PromptRecord
import logging

logger = logging.getLogger("promptiq")

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("PromptRecords")  # Replace with your actual table name if different

def save_prompt_record(record: PromptRecord):
    try:
        table.put_item(Item=record.dict())
        logger.info("Prompt record saved to DynamoDB")
    except Exception as e:
        logger.error(f"Failed to save prompt record: {str(e)}", exc_info=True)
