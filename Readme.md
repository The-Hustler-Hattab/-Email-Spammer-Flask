# Email Spammer Flask Application

## Overview

The Email Spammer Flask Application is a simple API tool developed using Flask. This application allows users to send multiple emails to different recipients simultaneously. It can be used for testing purposes, educational demonstrations, or any scenario where bulk email sending is required.

## Features

1. **User Authentication:** The application supports user authentication through OAuth to ensure that only authorized users can access and utilize the email spamming functionality.

2. **Email Configuration:** Users can configure the email settings such as SMTP server, port, sender email address, and authentication credentials.

3. **Email Content:** Users can compose the email subject and body using a simple text editor provided by the application.

4. **Preview:** Before sending the emails, users can preview how the email will appear to the recipients.

5. **Spamming:** Once all configurations are set, users can initiate the email spamming process. The application sends emails to all recipients in the list using the specified email settings.

6. **Status Tracking:** Users can track the status of each email sent, including whether it was successfully delivered or if any errors occurred.

## Installation

1. Clone the repository from GitHub: [GitHub Repository Link](https://github.com/The-Hustler-Hattab/-Email-Spammer-Flask).

2. Navigate to the project directory.

3. Create a virtual environment:
    ```
    $ python3 -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
        ```
        $ venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```
        $ source venv/bin/activate
        ```

5. Install the required dependencies:
    ```
    $ pip install -r requirements.txt
    ```

6. Run the application:
    ```
    $ gunicorn -w 4 -b 0.0.0.0:5000 main:app
    ```

## Usage

1. **User Authentication:**
    - Access the application through a web browser.
    - Log in using your credentials.

2. **Email/SMS Configuration:**
    - Navigate to the create email endpoint.
    - Configure the SMTP server details, port, sender email address, and authentication credentials.

3. **Email/SMS Content:**
    - Navigate to the send email endpoint.
    - Enter the email subject and body.

4. **Preview:**
    - Review the email content to ensure it appears as intended.

5. **Spamming:**
    - Navigate to the spam page.
    - Click the "Send" button to initiate the email spamming process.

6. **Status Tracking:**
    - Monitor the status of each email sent on the status page.

## Technologies Used

- **Flask:** Python micro web framework used for building the web application.
- **Mysql:** Relational database used for storing Email credentials and email carriers.
- **SMTP:** Simple Mail Transfer Protocol used for sending emails.

