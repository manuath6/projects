import boto3
import os
from getpass import getpass

# Prompt the user for AWS credentials and log group name
aws_access_key_id = input("Enter your AWS Access Key ID: ")
aws_secret_access_key = getpass("Enter your AWS Secret Access Key: ")
region_name = input("Enter your AWS Region: ")
log_group_name = input("Enter your Log Group Name: ")

# Initialize a session using Amazon CloudWatch
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Initialize CloudWatch Logs client
logs_client = session.client('logs')

# Get all log streams from the log group
log_streams_response = logs_client.describe_log_streams(
    logGroupName=log_group_name,
    orderBy='LastEventTime',
    descending=True
)
log_streams = log_streams_response['logStreams']

# Check if log streams are fetched
if not log_streams:
    print("No log streams found in the log group.")
else:
    print(f"Found {len(log_streams)} log streams.")

# Function to get log events
def get_log_events(log_group_name, log_stream_name):
    log_events = []
    next_token = None

    while True:
        if next_token:
            response = logs_client.get_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                nextToken=next_token,
                startFromHead=True
            )
        else:
            response = logs_client.get_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                startFromHead=True
            )

        log_events.extend(response['events'])
        next_token = response['nextForwardToken']

        if not response['events'] or next_token == response['nextForwardToken']:
            break

    return log_events

# Directory to save log files
output_dir = os.path.join('cloudwatch_logs', log_group_name.strip('/').replace('/', '_'))
print(f"Creating directory: {output_dir}")
os.makedirs(output_dir, exist_ok=True)

# Check if directory is created
if os.path.isdir(output_dir):
    print(f"Directory {output_dir} created successfully.")
else:
    print(f"Failed to create directory {output_dir}.")

# Loop through each log stream and get the log events
for log_stream in log_streams:
    log_stream_name = log_stream['logStreamName']
    print(f"Fetching logs from stream: {log_stream_name}")
    events = get_log_events(log_group_name, log_stream_name)
    
    # Save the events to a file named after the log stream
    file_path = os.path.join(output_dir, f"{log_stream_name}.txt")
    print(f"Saving logs to file: {file_path}")
    with open(file_path, 'w', encoding='utf-8') as f:
        for event in events:
            f.write(f"{event['timestamp']} {event['message']}\n")

    # Verify if the file is created
    if os.path.isfile(file_path):
        print(f"File {file_path} created successfully.")
    else:
        print(f"Failed to create file {file_path}.")
