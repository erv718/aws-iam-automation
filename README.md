# AWS IAM Automation

When employees left the company, their AWS IAM accounts needed to be disabled across multiple AWS accounts. Console access had to be revoked, API keys deactivated, and everything logged. Doing this manually in the AWS console for each account was slow and easy to miss.

## What These Scripts Do

- **Offboard-IAMUsers.py** - Bulk offboards IAM users across multiple AWS accounts. Reads a list of usernames, iterates through configured AWS profiles, disables console access, deactivates all API keys, and logs the results to an Excel report.
- **Disable-IAMUser.py** - Single-user version for quick one-off disables.
- **Disable-IAMUser-v2.py** - Updated version with improved error handling and multi-profile support.

## Usage

```python
# Bulk offboard users across all configured AWS accounts
python Offboard-IAMUsers.py

# Disable a single IAM user
python Disable-IAMUser-v2.py
```

Update the `aws_profiles` list in each script with your AWS CLI profile names before running.

## Requirements

- Python 3.x
- `boto3` and `pandas` packages
- AWS CLI configured with named profiles for each account
- IAM permissions: `iam:DeleteLoginProfile`, `iam:ListAccessKeys`, `iam:UpdateAccessKey`

## Blog Post

[Bulk Offboarding IAM Users Across Multiple AWS Accounts with Python](https://blog.soarsystems.cc/aws-iam-automation)
