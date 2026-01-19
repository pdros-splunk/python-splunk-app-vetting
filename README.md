# Splunk App Vetting Tool

A Python-based utility for submitting and monitoring Splunk applications through the Splunk AppInspect validation process. This tool automates the authentication, app submission, and validation status monitoring workflows.

## Overview

This tool streamlines the Splunk app vetting process by:
- Authenticating with Splunk Cloud using credentials
- Submitting app packages for validation through AppInspect
- Monitoring validation status and retrieving reports
- Supporting filtered validation (cloud-only or self-service)

## Prerequisites

- Python 3.6 or higher
- Valid Splunk username and password
- A Splunk Cloud account with AppInspect API access (Optional)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd python-splunk-app-vetting
```

2. Run env and install dependencies:
```bash
python -m venv .venv
source bin/activate
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with your Splunk credentials:
```bash
touch .env
```
```
USER=your_splunk_username
PASSWORD=your_splunk_password
```

## Usage

Run the vetting tool with the path to your app package:

```bash
python main.py --app-dir /path/to/your/app.tar.gz
```

### Optional Arguments

- `--cloud-only`: Run only cloud validation tests
  ```bash
  python main.py --app-dir /path/to/app.tar.gz --cloud-only true
  ```

- `--ssai-only`: Run only self-service (SSAI) validation tests
  ```bash
  python main.py --app-dir /path/to/app.tar.gz --ssai-only true
  ```

## Features

- **Automatic Authentication**: Handles basic auth with Splunk Cloud
- **App Submission**: Uploads app packages to AppInspect for validation
- **Status Monitoring**: Continuously polls validation status with user-friendly messages
- **Flexible Testing**: Filter validation tests by cloud or self-service categories
- **Error Handling**: Provides clear error messages for authentication and submission failures

## Project Structure

```
.
├── main.py           # Main application logic
├── const.py          # API endpoints and constants
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Dependencies

- `requests`: HTTP library for API calls
- `python-dotenv`: Environment variable management
- `certifi`: SSL certificate verification

See [requirements.txt](requirements.txt) for complete dependency list with versions.

## API Endpoints

This tool uses the following Splunk AppInspect API endpoints:

- **Login**: `https://api.splunk.com/2.0/rest/login/splunk`
- **Validation**: `https://appinspect.splunk.com/v1/app/validate`
- **Status**: `https://appinspect.splunk.com/v1/app/validate/status`
- **Report**: `https://appinspect.splunk.com/v1/app/report`

## Security

- Credentials are loaded from environment variables and should never be hardcoded
- Ensure your `.env` file is added to `.gitignore` to prevent credential exposure
- Use strong passwords for Splunk Cloud accounts

## Troubleshooting

**Authentication Failed**: Verify your username and password in the `.env` file

**App Submission Failed**: Ensure:
- The app package path is correct and accessible
- The file is a valid tar.gz archive
- Your Splunk account has AppInspect API permissions

**Validation Timeout**: The tool monitors status continuously; allow sufficient time for validation to complete
