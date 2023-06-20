import boto3
import csv
import pandas as pd
from botocore.exceptions import ClientError

# AWS profiles for different environments
aws_profiles = ["ACCOUNTID"]

# Path for the log file
log_file_path = "C:/Users/$env:USERNAME/Desktop/iam_user_log.xlsx"

# List to store logs
log_data = []

def disable_iam_user(username, profile):
    session = boto3.Session(profile_name=profile)  # Use specific AWS profile
    iam_client = session.client('iam')

    log_entry = {"Username": username, "AWS Profile": profile, "Console Access Disabled": "No", "API Keys Disabled": "No", "Notes": ""}

    try:
        # Step 1: Delete login profile to disable console access
        try:
            iam_client.delete_login_profile(UserName=username)
            log_entry["Console Access Disabled"] = "Yes"
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                log_entry["Notes"] += "No console access. "
            else:
                log_entry["Notes"] += f"Error disabling console access: {e}. "

        # Step 2: List and disable all API keys
        access_keys = iam_client.list_access_keys(UserName=username)['AccessKeyMetadata']
        
        if not access_keys:
            log_entry["Notes"] += "No API keys found."
        else:
            all_keys_disabled = True
            for key in access_keys:
                key_id = key['AccessKeyId']
                key_status = key['Status']

                if key_status == 'Active':
                    all_keys_disabled = False
                    iam_client.update_access_key(UserName=username, AccessKeyId=key_id, Status='Inactive')
                    log_entry["API Keys Disabled"] = "Yes"
                    log_entry["Notes"] += f"API key {key_id} deactivated. "
            
            if all_keys_disabled:
                log_entry["Notes"] += "All API keys were already disabled."

    except ClientError as e:
        log_entry["Notes"] += f"Unexpected error: {e}"

    # Add log entry to list
    log_data.append(log_entry)

def process_csv(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            username = row[0].strip()
            if username:
                for profile in aws_profiles:  # Iterate through all AWS accounts
                    print(f"Processing user: {username} in {profile}")
                    disable_iam_user(username, profile)

    # Save log data to Excel with safe handling
    df = pd.DataFrame(log_data)
    try:
        with pd.ExcelWriter(log_file_path, mode='w', engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        print(f"\nLog saved to {log_file_path}")
    except PermissionError:
        print(f"⚠️ Permission denied: Close the Excel file before running the script.")
    except Exception as e:
        print(f"⚠️ Error writing to Excel: {e}")

# Example usage
if __name__ == "__main__":
    csv_file = "C:/Users/$env:USERNAME/Desktop/aws_users_deactivate.csv"  # Replace with actual CSV file path
    process_csv(csv_file)
