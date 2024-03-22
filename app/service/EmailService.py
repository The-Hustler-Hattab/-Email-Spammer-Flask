import smtplib
import threading
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Response, jsonify

from app.model.EmailCredsAlchemy import EmailCreds
from app.model.WirelessCarrierEmailToTextAlchemy import WirelessCarrierEmailText
from app.service.LLMService import LLMService

# Create a dictionary to store the email name and smtp connection
email_dict: dict = {}


class EmailService:

    @staticmethod
    def create_new_email(email: str, email_pass: str, email_host: str, port=587) -> tuple[Response, int]:
        """
        Create a new email in the db
        """
        try:
            # Check if the email credentials are valid
            if EmailService.check_smtp_connection(email, email_pass, email_host, port):
                try:
                    EmailCreds.create_email(email, email_pass, port, email_host)
                except Exception as e:
                    error = f"Error creating email: {e}"
                    print(error)
                    return jsonify({'msg': error}), 404
                return jsonify({'msg': 'Created email successfully'}), 200
        except Exception as e:
            error = f"Error connecting to email: {e}"
            print(error)
            return jsonify({'msg': error}), 404

    @staticmethod
    def check_smtp_connection(email: str, email_pass: str, email_host: str, port: int) -> bool:
        """
        Check SMTP connection.
        :param port:
        :param email: str
        :param email_pass: str
        :param email_host: str
        :return: bool
        """
        # Set up SMTP connection. check if the email credentials are valid
        with smtplib.SMTP(email_host, port) as smtp:
            smtp.starttls()
            smtp.login(email, email_pass)
            smtp.close()
        return True

    @staticmethod
    def connect_smtp(email_creds: EmailCreds) -> smtplib.SMTP:
        """
        Connect to SMTP
        """
        smtp = smtplib.SMTP(email_creds.email_host, email_creds.port)
        smtp.starttls()
        smtp.login(email_creds.email, email_creds.email_pass)
        EmailService.keep_alive_async(smtp, email_creds.email)
        return smtp

    @staticmethod
    def initialize_email_connections():
        """
        Initialize email connections
        """
        email_creds: list[EmailCreds] = EmailCreds.get_all()
        email = ''
        for cred in email_creds:
            try:
                if email_dict.get(cred.email) is not None:
                    print(f"Email smtp exists: {cred.email}")
                    continue
                email = cred.email
                smtp = EmailService.connect_smtp(cred)
                email_dict[cred.email] = smtp
            except Exception as e:
                print(f"Error initializing email connection for email: {email}. with error: {e}")

    @staticmethod
    def keep_alive_async(smtp: smtplib.SMTP, email: str):
        thread = threading.Thread(target=EmailService.send_noop, args=(smtp, email))
        thread.daemon = True  # Set the thread as a daemon, so it automatically stops when the main thread exits
        thread.start()

    @staticmethod
    def send_noop(smtp: smtplib.SMTP, email: str):
        """
        Send NOOP command every 3 minutes to keep the connection alive
        """
        while True:
            try:
                smtp.noop()
                print(f"NOOP command sent successfully for email '{email}'")
            except Exception as e:
                print(f"Error sending NOOP for email {email}, exception: '{e}'")
            time.sleep(300)  # Sleep for 5 minutes (300 seconds)

    @staticmethod
    def send_email(sender_email: str, receiver_email: str, subject: str, body: str, retry: bool = True,
                   email_sub_type: str = "plain", message_count: int = 1) -> tuple[Response, int]:
        """
        Send an email
        """
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, email_sub_type))

        try:
            smtp: smtplib.SMTP = email_dict.get(sender_email)
            if not smtp:
                email_cred: EmailCreds = EmailCreds.get_by_email(sender_email)
                if not email_cred:
                    return jsonify({'msg': f'Email credentials for {sender_email} not found.'}), 400
                else:
                    smtp = EmailService.connect_smtp(email_cred)
                    email_dict[sender_email] = smtp
            for i in range(message_count):
                smtp.sendmail(sender_email, receiver_email, message.as_string())
                print(f"Email sent successfully {i}")
            return jsonify({'msg': 'Sent email successfully'}), 200
        except Exception as e:
            print(f"Error sending email: {e}")
            if retry:
                print(f"Retrying to send email from {sender_email}")
                email_dict[sender_email] = EmailService.connect_smtp(EmailCreds.get_by_email(sender_email))

                # Retry to send the email
                return EmailService.send_email(sender_email, receiver_email, subject, body, False,
                                               message_count=message_count)
            return jsonify({'msg': f'Failed to Send Email due to {e}'}), 500

    @staticmethod
    def send_email_from_all(receiver_email: str, subject: str, body: str) -> tuple[Response, int]:
        """
        Send an email from all emails
        """
        if not email_dict:
            EmailService.initialize_email_connections()
        emails: list[str] = []
        for email in email_dict.keys():
            try:
                email_res = EmailService.send_email(email, receiver_email, subject, body)
                print(f"email_res: `{email_res}`")
                if email_res[1] == 200:
                    print(f"Email sent successfully from `{email}`")
                    emails.append(email)
            except Exception as e:
                print(f"Error sending email from `{email}`: `{e}`")

        return jsonify({'msg': f'emails sent successfully for these emails {emails}'}), 200

    @staticmethod
    def send_sms_to_phone(from_email: str, phone_number: str, subject: str, body: str, is_mms: bool = True,
                          message_count: int = 1) -> tuple[
        Response, int]:
        """
        Send an SMS to a phone
        """
        try:
            carrier_emails = WirelessCarrierEmailText.get_all_by_allow_multimedia(is_mms)
            if not carrier_emails:
                return jsonify({'msg': f'Carrier email for {carrier_emails} not found.'}), 400

            to_emails: list[str] = []
            for carrier_email in carrier_emails:
                to_email = f"{phone_number}{carrier_email.domain}"
                email_res = EmailService.send_email(from_email, to_email, subject, body,message_count=message_count)
                print(f"email_res: `{email_res}`")
                if email_res[1] == 200:
                    print(f"Email sent successfully to `{to_email}`")
                    to_emails.append(to_email)

            return jsonify({'msg': f'Sent SMS successfully to {to_emails}'}), 200

        except Exception as e:
            return jsonify({'msg': f'Failed to Send SMS due to {e}'}), 500

    @staticmethod
    def send_sms_from_all(receiver_email: str, subject: str, body: str, is_mime: bool = True, reword: bool = False,
                          message_count: int = 1) -> \
            tuple[
                Response, int]:
        """
        Send an email from all emails
        """
        if not email_dict:
            EmailService.initialize_email_connections()
        emails: list[str] = []
        for email in email_dict.keys():
            try:
                if reword:
                    body = f"Reword this: {body}"
                    body = LLMService.get_response(body)

                email_res = EmailService.send_sms_to_phone(email, receiver_email, subject, body, is_mime, message_count)
                print(f"email_res: `{email_res}`")
                if email_res[1] == 200:
                    print(f"Email sent successfully from `{email}`")
                    emails.append(email)
            except Exception as e:
                print(f"Error sending email from `{email}`: `{e}`")

        return jsonify({'msg': f'emails sent successfully for these emails {emails}'}), 200
