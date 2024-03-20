from typing import Tuple, Dict

from flask import jsonify, Response, request

from app import app
from app.model.EmailCredsAlchemy import EmailCreds
from app.model.WirelessCarrierEmailToTextAlchemy import WirelessCarrierEmailText
from app.service.EmailService import EmailService


@app.route('/health', methods=['GET'])
def health() -> Tuple[Dict[str, str], int]:
    """
    Health Check Endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: OK if the service is healthy.
    """
    return {'status': 'OK',
            'msg': 'API is up'}, 200


@app.route('/initialize-email-connections', methods=['GET'])
def initialize_email_connections() -> tuple[Response, int]:
    """
    Initialize email connections
    ---
    tags:
      - Email
    responses:
      200:
        description: OK if email connections are initialized successfully.
      500:
        description: Internal server error if failed to initialize email connections.
    """
    try:
        EmailService.initialize_email_connections()
        return jsonify({'msg': 'Email connections initialized successfully'}), 200

    except Exception as e:
        error = f'Error initializing email connections: {e}'
        print(error)
        return jsonify({'msg': error}), 500


@app.route('/get-emails', methods=['GET'])
def get_all_emails() -> tuple[Response, int]:
    """
    Get All Emails inside the db.
    ---
    tags:
      - Email
    responses:
      200:
        description: OK if emails retrieved.
    """
    email_creds = EmailCreds.get_all()

    email_creds_dicts = [cred.as_dict() for cred in email_creds]
    return jsonify({'emails': email_creds_dicts, 'msg': 'retrieved emails successfully'}), 200


@app.route('/get-email-carriers', methods=['GET'])
def get_email_carriers() -> tuple[Response, int]:
    """
    Get All Emails carriers inside the db.
    ---
    tags:
      - Email Carriers
    responses:
      200:
        description: OK if emails carriers retrieved.
    """
    email_carriers = WirelessCarrierEmailText.get_all()

    email_carriers_dict = [cred.as_dict() for cred in email_carriers]
    return jsonify({'email_carriers': email_carriers_dict, 'msg': 'retrieved email carriers successfully'}), 200


@app.route('/create-email', methods=['POST'])
def create_email() -> tuple[Response, int]:
    """
    Create a new email in the db
    ---
    tags:
      - Email
    parameters:
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            email:
              type: string
            email_pass:
              type: string
            email_host:
              type: string
            port:
              type: integer

    responses:
      200:
        description: OK if email is created.
      400:
        description: Bad request if email is not created.
    """
    # Extract data from JSON request body and ensure required fields are present
    request_data = request.json
    # print(request_data)
    email = request_data.get('email')
    email_host = request_data.get('email_host')
    email_pass = request_data.get('email_pass')
    email_port = request_data.get('email_port')
    # print(email_host)
    if not email_port:
        email_port = 587

    # # Check if all required fields are provided
    if not email_port or not email or not email_pass or not email_host:
        return jsonify({'error': 'Missing required fields'}), 400

    return EmailService.create_new_email(email, email_pass, email_host, email_port)


@app.route('/create-wireless-carrier-email', methods=['POST'])
def create_wireless_carrier_email() -> tuple[Response, int]:
    """
    Create a new record in the wireless_carrier_email_text table
    ---
    tags:
      - Email Carriers
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            wireless_carrier:
              type: string
            domain:
              type: string
            allow_multimedia:
              type: boolean

    responses:
      200:
        description: OK if record is created.
      400:
        description: Bad request if record is not created.
    """
    # Extract data from JSON request body and ensure required fields are present
    request_data = request.json
    wireless_carrier = request_data.get('wireless_carrier')
    domain = request_data.get('domain')
    allow_multimedia = request_data.get('allow_multimedia')

    # Check if all required fields are provided
    if not wireless_carrier or not domain or allow_multimedia is None:
        return jsonify({'error': 'Missing required fields'}), 400

    # Call the create method of WirelessCarrierEmailText class
    try:
        WirelessCarrierEmailText.create(wireless_carrier, domain, allow_multimedia)
        return jsonify({'message': 'Record created successfully'}), 200
    except Exception as e:
        error = f'Error creating new record: {e}'
        print(error)

        return jsonify({'error': error}), 400


@app.route('/delete-wireless-carrier-email/<int:id>', methods=['DELETE'])
def delete_wireless_carrier_email(id: int) -> tuple[Response, int]:
    """
    Delete a record from the wireless_carrier_email_text table by ID
    ---
    tags:
      - Email Carriers
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID of the record to delete

    responses:
      200:
        description: OK if record is deleted.
      400:
        description: Bad request if record is not found or deletion fails.
    """
    try:
        # Call the delete_by_id method of WirelessCarrierEmailText class
        WirelessCarrierEmailText.delete_by_id(id)
        return jsonify({'message': 'Record deleted successfully'}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        error = f'Error deleting record: {e}'
        print(error)
        return jsonify({'error': error}), 400


@app.route('/send-email', methods=['POST'])
def send_email() -> tuple[Response, int]:
    """
    Create a new email in the db
    ---
    tags:
      - Email
    parameters:
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            email:
              type: string
            to_email:
              type: string
            email_subject:
              type: string
            email_body:
              type: string
            message_count:
              type: integer


    responses:
      200:
        description: OK if email is sent.
      400:
        description: Bad request if email is not sent.
    """
    # Extract data from JSON request body and ensure required fields are present
    request_data = request.json
    email = request_data.get('email')
    to_email = request_data.get('to_email')
    email_subject = request_data.get('email_subject')
    email_body = request_data.get('email_body')
    message_count = request_data.get('message_count')
    # # Check if all required fields are provided
    if not email_body or not email or not to_email:
        return jsonify({'error': 'Missing required fields'}), 400
    return EmailService.send_email(email, to_email, email_subject, email_body, message_count=message_count)


@app.route('/send-email-from-all', methods=['POST'])
def send_email_from_all() -> tuple[Response, int]:
    """
    Create a new email in the db
    ---
    tags:
      - Email
    parameters:
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            to_email:
              type: string
            email_subject:
              type: string
            email_body:
              type: string

    responses:
      200:
        description: OK if email is sent.
      400:
        description: Bad request if email is not sent.
    """
    # Extract data from JSON request body and ensure required fields are present
    request_data = request.json
    to_email = request_data.get('to_email')
    email_subject = request_data.get('email_subject')
    email_body = request_data.get('email_body')

    # # Check if all required fields are provided
    if not email_body or not to_email:
        return jsonify({'error': 'Missing required fields'}), 400

    return EmailService.send_email_from_all(to_email, email_subject, email_body)


@app.route('/send-sms', methods=['POST'])
def send_sms_to_phone() -> tuple[Response, int]:
    """
    Send an SMS to a phone
    ---
    tags:
      - Email
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            from_email:
              type: string
            phone_number:
              type: string
            subject:
              type: string
            body:
              type: string
            is_mms:
              type: boolean
            message_count:
              type: integer

    responses:
      200:
        description: OK if SMS is sent successfully.
      400:
        description: Bad request if carrier emails not found.
      500:
        description: Internal server error if failed to send SMS.
    """
    # Extract data from JSON request body
    request_data = request.json
    from_email = request_data.get('from_email')
    phone_number = request_data.get('phone_number')
    subject = request_data.get('subject')
    body = request_data.get('body')
    is_mms = request_data.get('is_mms')
    message_count = request_data.get('message_count')

    # Check if all required fields are provided
    if not from_email or not phone_number or not subject or not body or is_mms is None:
        return jsonify({'msg': 'Missing required fields'}), 400

    return EmailService.send_sms_to_phone(from_email, phone_number, subject, body, is_mms, message_count)


@app.route('/send_sms_from_all', methods=['POST'])
def send_sms_from_all() -> tuple[Response, int]:
    """
    Create a new email in the db
    ---
    tags:
      - Email
    parameters:
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            phone_number:
              type: string
            email_subject:
              type: string
            email_body:
              type: string
            is_mime:
              type: boolean
            reword:
              type: boolean
            message_count:
              type: integer

    responses:
      200:
        description: OK if email is sent.
      400:
        description: Bad request if email is not sent.
    """
    # Extract data from JSON request body and ensure required fields are present
    request_data = request.json
    phone_number = request_data.get('phone_number')
    email_subject = request_data.get('email_subject')
    email_body = request_data.get('email_body')
    is_mime = request_data.get('is_mime')
    reword = request_data.get('reword')
    message_count: int = request_data.get('message_count')
    # # Check if all required fields are provided
    if not email_body or not phone_number:
        return jsonify({'error': 'Missing required fields'}), 400

    return EmailService.send_sms_from_all(phone_number, email_subject, email_body, is_mime, reword, message_count)
