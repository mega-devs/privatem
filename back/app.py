from flask import Flask, request, jsonify, send_file
import requests
import utils
import model
import config
import datetime
import init
from flask_cors import CORS
from flask_socketio import SocketIO, send
import mailer
from io import BytesIO
import json
from flasgger import Swagger
import log_config
import os

init.init()
app = Flask(__name__)
CORS(app)
socket = SocketIO(app, cors_allowed_origins='*')
swagger = Swagger(app)
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
log_file_path = os.path.join(log_dir, 'app.log')
# Настройка логирования
logger = log_config.setup_logging()
app.logger = logger


# for getting server time
@app.route('/server_time')
def get_server_time():
    server_time = datetime.datetime.now().isoformat()
    return jsonify({'server_time': server_time})


@app.route('/api/login', methods=['POST'])
def login():
    """
    User login
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - password
          properties:
            name:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            token:
              type: string
      400:
        description: Wrong parameters
      401:
        description: User not found or password is incorrect
    """
    data = request.get_json()
    if utils.validate(data, ['name', 'password']):
        token = model.login(data['name'], data['password'])
        if token:
            app.logger.info(f'User {data["name"]} logged in successfully.')
            return {'token': token}
        else:
            app.logger.warning(f'Login failed for user {data["name"]}.')
            return {'error': 'user not found or password is incorrect'}, 401
    else:
        app.logger.error('Login failed due to wrong parameters.')
        return {'error': 'wrong params'}, 400


@app.route('/api/check/token', methods=['POST'])
def check_token():
    """
    Check token validity
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
          properties:
            token:
              type: string
    responses:
      200:
        description: Token is valid
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token']):
        if model.check_token(data['token']):
            app.logger.info(f'Token validation successful for token: {data["token"]}')
            return {'data': 'success'}
        else:
            app.logger.warning(f'Token validation failed for token: {data["token"]}')
            return {'error': 'wrong token'}, 401
    else:
        app.logger.error('Token validation failed due to wrong parameters.')
        return {'error': 'wrong params'}, 400


@app.route('/api/session/add', methods=['POST'])
def add_session():
    """
    Add a new session
    ---
    tags:
      - Session
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - name
          properties:
            token:
              type: string
            name:
              type: string
    responses:
      200:
        description: Session added successfully
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'name']):
        if model.check_token(data['token']):
            res = model.add_session(data['name'])
            with open('settings.json') as f:
                settings = json.load(f)

            model.create_settings(data['name'], settings)
            if res == 1:
                app.logger.info(f'Session {data["name"]} added successfully.')
                return {'data': 'success'}
            else:
                app.logger.error(f'Error adding session {data["name"]}: {res}')
                return {'data': 'error', 'error': res}
        else:
            app.logger.warning(f'Invalid token while adding session {data["name"]}.')
            return {'error': 'wrong token'}, 401
    else:
        app.logger.error('Failed to add session due to wrong parameters.')
        return {'error': 'wrong params'}, 400


@app.route('/api/update/settings_from_json', methods=['POST'])
def update_settings_from_json():
    """
    Update settings from JSON data
    ---
    tags:
      - Settings
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - session
            - json_data
          properties:
            session:
              type: string
            json_data:
              type: object
    responses:
      200:
        description: Settings updated successfully
        schema:
          type: object
          properties:
            status:
              type: string
      400:
        description: Missing parameters
    """
    data = request.get_json()
    if 'session' in data and 'json_data' in data:
        session = data['session']
        json_data = data['json_data']

        for key, value in json_data.items():
            model.update_setting(session, key, value)
        app.logger.info(f'Settings updated successfully for session {session}.')
        return {'status': 'success'}
    else:
        app.logger.error('Failed to update settings due to missing parameters.')
        return {'error': 'missing parameters'}, 400


@app.route('/api/session/del', methods=['POST'])
def del_session():
    """
    Delete a session
    ---
    tags:
      - Session
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - name
          properties:
            token:
              type: string
            name:
              type: string
    responses:
      200:
        description: Session deleted successfully
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'name']):
        if model.check_token(data['token']):
            model.del_session(data['name'])
            app.logger.info(f'Session {data["name"]} deleted successfully.')
            return {'data': 'success'}
        else:
            app.logger.warning(f'Invalid token while deleting session {data["name"]}.')
            return {'error': 'wrong token'}, 401
    else:
        app.logger.error('Failed to delete session due to wrong parameters.')
        return {'error': 'wrong params'}, 400


@app.route('/api/session/list', methods=['GET'])
def list_session():
    """
    List all sessions
    ---
    tags:
      - Session
    responses:
      200:
        description: List of sessions
        schema:
          type: array
          items:
            type: object
    """
    return model.list_session()


@app.route('/api/input/material', methods=['POST'])
def input_material():
    """
    Input material into session
    ---
    tags:
      - Material
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - session
            - type
            - file
          properties:
            token:
              type: string
            session:
              type: string
            type:
              type: string
            file:
              type: string
            fileName:
              type: string
              required: false
    responses:
      200:
        description: Material input successful
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'session', 'type', 'file']):
        if model.check_token(data['token']):
            if utils.validate(data, ['fileName']):
                res = model.input_material(data['session'], data['type'], data['file'], data['fileName'])
            else:
                data['fileName'] = ''
                res = model.input_material(data['session'], data['type'], data['file'], data['fileName'])

            if res == 1:
                app.logger.info(f'Material input successful for session {data["session"]} with type {data["type"]}.')
                return {'data': 'success'}
            else:
                app.logger.error(
                    f'Error inputting material for session {data["session"]} with type {data["type"]}: {res}')
                return {'data': 'error', 'error': res}
        else:
            app.logger.warning(
                f'Invalid token while inputting material for session {data["session"]} with type {data["type"]}.')
            return {'error': 'wrong token'}, 401
    else:
        app.logger.error('Failed to input material due to wrong parameters.')
        return {'error': 'wrong params'}, 400


@app.route('/api/get/list/<type>/<session>', methods=['GET'])
def get_list(type, session):
    """
    Get list of items in a session
    ---
    tags:
      - Material
    parameters:
      - in: path
        name: type
        required: true
        type: string
      - in: path
        name: session
        required: true
        type: string
    responses:
      200:
        description: List of items
        schema:
          type: array
          items:
            type: object
    """
    return model.getTbl(type, session)


@app.route('/api/get/materials/<id>/<type>/<item>', methods=['GET'])
def get_materials(id, type, item):
    """
    Get materials of a specific item
    ---
    tags:
      - Material
    parameters:
      - in: path
        name: id
        required: true
        type: string
      - in: path
        name: type
        required: true
        type: string
      - in: path
        name: item
        required: true
        type: string
    responses:
      200:
        description: Materials of the item
        schema:
          type: object
    """
    return model.getTblSub(id, type, item)


@app.route('/api/input/log/<type>/<session>', methods=['POST'])
def input_log(type, session):
    """
    Input log for a session
    ---
    tags:
      - Log
    parameters:
      - in: path
        name: type
        required: true
        type: string
      - in: path
        name: session
        required: true
        type: string
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - logtext
            - status
          properties:
            token:
              type: string
            logtext:
              type: string
            status:
              type: string
    responses:
      200:
        description: Log input successful
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'logtext', 'status']):
        if model.check_token(data['token']):
            model.add_log(type, session, data['logtext'], data['status'])
            return {'data': 'success'}
        else:
            return {'error': 'wrong token'}, 401
    else:
        return {'error': 'wrong params'}, 400


@app.route('/api/logs/<type>/<session>', methods=['GET'])
def fetch_logs(type, session):
    """
    Fetch logs of a session
    ---
    tags:
      - Log
    parameters:
      - in: path
        name: type
        required: true
        type: string
      - in: path
        name: session
        required: true
        type: string
    responses:
      200:
        description: List of logs
        schema:
          type: array
          items:
            type: object
    """
    logs = model.get_logs(type, session)
    return {'data': logs}


@app.route('/api/count/<session>', methods=['GET'])
def fetch_counts(session):
    """
    Fetch count of items in a session
    ---
    tags:
      - Material
    parameters:
      - in: path
        name: session
        required: true
        type: string
    responses:
      200:
        description: Count of items
        schema:
          type: object
          properties:
            count:
              type: integer
    """
    count = model.get_counts(session)
    return {'count': count}


@app.route('/api/del/material', methods=['POST'])
def del_material():
    """
    Delete material from a session
    ---
    tags:
      - Material
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - id
            - type
          properties:
            token:
              type: string
            id:
              type: string
            type:
              type: string
    responses:
      200:
        description: Material deleted successfully
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'id', 'type']):
        if model.check_token(data['token']):
            model.del_material(data['id'], data['type'])
            app.logger.info(f'Material with ID {data["id"]} and type {data["type"]} deleted successfully.')
            return {'data': 'success'}
        else:
            app.logger.warning(f'Invalid token while deleting material with ID {data["id"]} and type {data["type"]}.')
            return {'error': 'wrong token'}, 401
    else:
        app.logger.error('Failed to delete material due to wrong parameters.')
        return {'error': 'wrong params'}, 400


@app.route('/api/del/material/str', methods=['POST'])
def del_material_str():
    """
    Delete material from a session by string
    ---
    tags:
      - Material
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - string
            - type
            - item
            - id
          properties:
            token:
              type: string
            string:
              type: string
            type:
              type: string
            item:
              type: string
            id:
              type: string
    responses:
      200:
        description: Material deleted successfully
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'string', 'type', 'item', 'id']):
        if model.check_token(data['token']):
            model.del_material_str(data['string'], data['type'], data['item'], data['id'])
            app.logger.info(
                f'Material with string {data["string"]}, type {data["type"]}, item {data["item"]}, and ID {data["id"]} deleted successfully.')
            return {'data': 'success'}
        else:
            app.logger.warning(
                f'Invalid token while deleting material with string {data["string"]}, type {data["type"]}, item {data["item"]}, and ID {data["id"]}.')
            return {'error': 'wrong token'}, 401
    else:
        app.logger.error('Failed to delete material due to wrong parameters.')
        return {'error': 'wrong params'}, 400


@app.route('/api/reset', methods=['POST'])
def reset():
    """
    Reset all settings
    ---
    tags:
      - Settings
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
          properties:
            token:
              type: string
    responses:
      200:
        description: Settings reset successfully
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token']):
        if model.check_token(data['token']):
            res = model.reset_all()
            if res == 1:
                return {'data': 'success'}
            else:
                return {'data': 'error', 'error': res}
        else:
            return {'error': 'wrong token'}, 401
    else:
        return {'error': 'wrong params'}, 400


@app.route('/api/reset/status', methods=['POST'])
def reset_status():
    """
    Reset status of a specific type
    ---
    tags:
      - Settings
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - type
            - status
          properties:
            token:
              type: string
            type:
              type: string
            status:
              type: string
    responses:
      200:
        description: Status reset successfully
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'type', 'status']):
        if model.check_token(data['token']):
            res = model.reset_status(data['type'], data['status'])
            if res == 1:
                return {'data': 'success'}
            else:
                return {'data': 'error', 'error': res}
        else:
            return {'error': 'wrong token'}, 401
    else:
        return {'error': 'wrong params'}, 400


@app.route('/api/check/smtp', methods=['POST'])
def check_smtp():
    """
    Check SMTP configuration
    ---
    tags:
      - SMTP
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - session
            - smtp_id
            - proxy_id
            - timeout
          properties:
            token:
              type: string
            session:
              type: string
            smtp_id:
              type: string
            proxy_id:
              type: string
            timeout:
              type: integer
    responses:
      200:
        description: SMTP check successful
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'session', 'smtp_id', 'proxy_id', 'timeout']):
        if model.check_token(data['token']):
            mailer.check_smtps(socket, data['session'], data['smtp_id'], data['proxy_id'], data['timeout'])
            return {'data': 'success'}
        else:
            return {'error': 'wrong token'}, 401
    else:
        return {'error': 'wrong params'}, 400


@app.route('/api/proxy', methods=['GET'])
def proxy():
    """
    Proxy a URL request
    ---
    tags:
      - Proxy
    parameters:
      - in: query
        name: url
        required: true
        type: string
    responses:
      200:
        description: Proxy request successful
        schema:
          type: file
      400:
        description: No URL provided
      500:
        description: Proxy request failed
    """
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        return send_file(BytesIO(response.content), download_name='templates.zip', as_attachment=True)
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/check/smtpp', methods=['POST'])
def check_smtpp():
    """
    Check single SMTP configuration
    ---
    tags:
      - SMTP
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - session
            - smtp_id
          properties:
            token:
              type: string
            session:
              type: string
            smtp_id:
              type: string
    responses:
      200:
        description: SMTP check successful
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'session', 'smtp_id']):
        if model.check_token(data['token']):
            mailer.check_smtp(socket, data['session'], data['smtp_id'])
            return {'data': 'success'}
        else:
            return {'error': 'wrong token'}, 401
    else:
        return {'error': 'wrong params'}, 400


@app.route('/api/del/log', methods=['POST'])
def del_log():
    """
    Delete log from a session
    ---
    tags:
      - Log
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - session
            - type
          properties:
            token:
              type: string
            session:
              type: string
            type:
              type: string
    responses:
      200:
        description: Log deleted successfully
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
      500:
        description: Internal server error
    """
    data = request.get_json()
    print("Received data:", data)  # Debugging statement

    if not utils.validate(data, ['token', 'session', 'type']):
        print("Validation failed")  # Debugging statement
        return {'error': 'wrong params'}, 400

    if not model.check_token(data['token']):
        print("Invalid token")  # Debugging statement
        return {'error': 'wrong token'}, 401

    try:
        model.del_log(data['session'], data['type'])
        return {'data': 'success'}
    except Exception as e:
        print("Error occurred:", str(e))
        return {'error': str(e)}, 500


@app.route('/api/check/imap', methods=['POST'])
def check_imap():
    """
    Check IMAP configuration
    ---
    tags:
      - IMAP
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - session
            - imap_id
            - proxy_id
            - timeout
          properties:
            token:
              type: string
            session:
              type: string
            imap_id:
              type: string
            proxy_id:
              type: string
            timeout:
              type: integer
    responses:
      200:
        description: IMAP check successful
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'session', 'imap_id', 'proxy_id', 'timeout']):
        if model.check_token(data['token']):
            mailer.check_imaps(socket, data['session'], data['imap_id'], data['proxy_id'], data['timeout'])
            return {'data': 'success'}
        else:
            return {'error': 'wrong token'}, 401
    else:
        return {'error': 'wrong params'}, 400


@app.route('/api/check/imapp', methods=['POST'])
def check_imapp():
    """
    Check single IMAP configuration
    ---
    tags:
      - IMAP
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - session
            - imap_id
          properties:
            token:
              type: string
            session:
              type: string
            imap_id:
              type: string
    responses:
      200:
        description: IMAP check successful
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'session', 'imap_id']):
        if model.check_token(data['token']):
            mailer.check_imap(socket, data['session'], data['imap_id'])
            return {'data': 'success'}
        else:
            return {'error': 'wrong token'}, 401
    else:
        return {'error': 'wrong params'}, 400


@app.route('/api/check/proxy', methods=['POST'])
def check_proxy():
    """
    Check proxy configuration
    ---
    tags:
      - Proxy
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - socket
            - session
            - proxy_id
          properties:
            token:
              type: string
            socket:
              type: string
            session:
              type: string
            proxy_id:
              type: string
    responses:
      200:
        description: Proxy check successful
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'socket', 'session', 'proxy_id']):
        if model.check_token(data['token']):
            result = mailer.check_proxy(socket, data['session'], data['proxy_id'])
            if result:
                return {'data': 'success'}
            else:
                return {'error': 'no proxies to check'}, 400
        else:
            return {'error': 'wrong token'}, 401
    else:
        return {'error': 'wrong params'}, 400


@app.route('/api/check/domain', methods=['POST'])
def check_domain():
    """
    Check domain configuration
    ---
    tags:
      - Domain
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - socket
            - session
            - domain_id
          properties:
            token:
              type: string
            socket:
              type: string
            session:
              type: string
            domain_id:
              type: string
    responses:
      200:
        description: Domain check successful
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Wrong parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    if utils.validate(data, ['token', 'socket', 'session', 'domain_id']):
        if model.check_token(data['token']):
            mailer.check_domain(socket, data['session'], data['domain_id'])
            return {'data': 'success'}
        else:
            return {'error': 'wrong token'}, 401
    else:
        return {'error': 'wrong params'}, 400


@app.route('/api/start/sendx', methods=['POST'])
def check_sendx():
    """
    Start sendx process
    ---
    tags:
      - Process
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - socket
            - session
            - sending_limit
            - threads_number
            - timeout
            - delay
            - emails_per_session
            - emails_to_validate
            - emails_per_material
            - smtp_form
            - proxy_form
            - bases_form
            - domain_form
            - template_form
          properties:
            token:
              type: string
            socket:
              type: string
            session:
              type: string
            sending_limit:
              type: integer
            threads_number:
              type: integer
            timeout:
              type: integer
            delay:
              type: integer
            emails_per_session:
              type: integer
            emails_to_validate:
              type: integer
            emails_per_material:
              type: integer
            smtp_form:
              type: string
            proxy_form:
              type: string
            bases_form:
              type: string
            domain_form:
              type: string
            template_form:
              type: string
    responses:
      200:
        description: Sendx process started successfully
        schema:
          type: object
          properties:
            data:
              type: string
      400:
        description: Missing parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    required_params = [
        'token', 'socket', 'session', 'sending_limit', 'threads_number', 'timeout', 'delay',
        'emails_per_session', 'emails_to_validate', 'emails_per_material', 'smtp_form',
        'proxy_form', 'bases_form', 'domain_form', 'template_form',
    ]
    if utils.validate(data, required_params):
        if model.check_token(data['token']):
            socket = data['socket']
            session = data['session']
            sending_limit = data['sending_limit']
            threads_number = data['threads_number']
            timeout = data['timeout']
            delay = data['delay']
            emails_per_session = data['emails_per_session']
            emails_to_validate = data['emails_to_validate']
            emails_per_material = data['emails_per_material']
            smtp_form = data['smtp_form']
            proxy_form = data['proxy_form']
            bases_form = data['imap_form']
            domain_form = data['domain_form']
            template_form = data['template_form']

            mailer.func_sendx(
                socket, session, sending_limit, threads_number, timeout, delay, emails_per_session,
                emails_to_validate, emails_per_material, smtp_form, proxy_form,
                domain_form, template_form, bases_form
            )

            return {'data': 'success'}
        else:
            return {'error': 'wrong token'}, 401

    return {'error': 'missing parameters'}, 400


@app.route('/api/start/test_mode', methods=['POST'])
def start_test_mode():
    """
    Start test mode
    ---
    tags:
      - Mailing
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - socket
            - session
            - sending_limit
            - threads_number
            - timeout
            - delay
            - emails_per_session
            - emails_to_validate
            - emails_per_material
            - smtp_form
            - proxy_form
            - imap_form
            - domain_form
            - template_form
            - to_check
          properties:
            token:
              type: string
            socket:
              type: string
            session:
              type: string
            sending_limit:
              type: integer
            threads_number:
              type: integer
            timeout:
              type: integer
            delay:
              type: integer
            emails_per_session:
              type: integer
            emails_to_validate:
              type: integer
            emails_per_material:
              type: integer
            smtp_form:
              type: string
            proxy_form:
              type: string
            imap_form:
              type: string
            domain_form:
              type: string
            template_form:
              type: string
            to_check:
              type: string
    responses:
      200:
        description: Success
      400:
        description: Missing parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    required_params = [
        'token', 'socket', 'session', 'sending_limit', 'threads_number', 'timeout', 'delay',
        'emails_per_session', 'emails_to_validate', 'emails_per_material', 'smtp_form',
        'proxy_form', 'imap_form', 'domain_form', 'template_form', 'to_check'
    ]

    if utils.validate(data, required_params):
        if model.check_token(data['token']):
            socket = data['socket']
            session = data['session']
            sending_limit = data['sending_limit']
            threads_number = data['threads_number']
            timeout = data['timeout']
            delay = data['delay']
            emails_per_session = data['emails_per_session']
            emails_to_validate = data['emails_to_validate']
            emails_per_material = data['emails_per_material']
            smtp_form = data['smtp_form']
            proxy_form = data['proxy_form']
            imap_form = data['imap_form']
            domain_form = data['domain_form']
            template_form = data['template_form']
            to_check = data['to_check']

            mailer.test_mode(
                socket, session, sending_limit, threads_number, timeout, delay, emails_per_session,
                emails_to_validate, emails_per_material, smtp_form, proxy_form, imap_form,
                domain_form, template_form, to_check
            )

            return {'data': 'success'}
        else:
            return {'error': 'wrong token'}, 401

    return {'error': 'missing parameters'}, 400


@app.route('/api/start/mailing', methods=['POST'])
def mailing():
    """
    Start mailing
    ---
    tags:
      - Mailing
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - token
            - socket
            - session
            - dummy_form
            - proxies_form
            - smtps_form
            - base_form
            - threads_form
            - delay_form
            - sending_limit
            - emails_per_check
            - count_of_material
            - timeout
          properties:
            token:
              type: string
            socket:
              type: string
            session:
              type: string
            dummy_form:
              type: string
            proxies_form:
              type: string
            smtps_form:
              type: string
            base_form:
              type: string
            threads_form:
              type: string
            delay_form:
              type: integer
            sending_limit:
              type: integer
            emails_per_check:
              type: integer
            count_of_material:
              type: integer
            timeout:
              type: integer
    responses:
      200:
        description: Success
      400:
        description: Missing parameters
      401:
        description: Wrong token
    """
    data = request.get_json()
    required_params = [
        'token', 'socket', 'session', 'dummy_form', 'proxies_form', 'smtps_form', 'base_form',
        'threads_form', 'delay_form', 'sending_limit', 'emails_per_check', 'count_of_material', 'timeout'
    ]

    if not all(param in data for param in required_params):
        return {'error': 'missing parameters'}, 400

    if model.check_token(data['token']):
        token = data['token']
        socket = data['socket']
        session = data['session']
        template = data['dummy_form']
        proxy = data['proxies_form']
        smtp = data['smtps_form']
        base = data['base_form']
        domain = data['domain_form']
        threads = data['threads_form'],
        delay = data['delay_form']
        sending_limit = data['sending_limit']
        emails_per_check = data['emails_per_check']
        count_of_material = data['count_of_material']
        timeout = data['timeout']
        if socket is None:
            return {'error': 'invalid socket'}, 400
        mailer.mailing_mode(socket, session, template, proxy, smtp, base, domain, threads, delay, sending_limit,
                            emails_per_check, count_of_material, timeout)

        return {'data': 'success'}
    else:
        return {'error': 'wrong token'}, 401

@app.route('/api/debug', methods=['GET'])
def get_debugs():
    """
    Get logs from app.log
    ---
    tags:
      - Logs
    responses:
      200:
        description: Logs retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              timestamp:
                type: string
              name:
                type: string
              level:
                type: string
              message:
                type: string
    """
    logs = []
    try:
        with open(log_file_path, 'r') as file:
            for line in file.readlines():
                parts = line.split(' - ')
                if len(parts) >= 4:
                    log_entry = {
                        'timestamp': parts[0],
                        'name': parts[1],
                        'level': parts[2],
                        'message': ' - '.join(parts[3:]).strip()
                    }
                    logs.append(log_entry)
        return {'logs': logs}, 200
    except Exception as e:
        logger.error(f"Error reading logs: {str(e)}")
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


@app.route('/change_user_password', methods=['POST'])
def change_password_route():
    data = request.get_json()
    if utils.validate(data, ['token', 'current_password', 'new_password']):
        if model.check_token(data['token']):
            user_id = get_user_id_from_token(data['token'])
            if user_id is None:
                return {'error': 'Invalid token'}, 401

            result = model.change_password(user_id, data['current_password'], data['new_password'])
            if isinstance(result, str) and result.startswith("Password changed"):
                return {'message': result}
            else:
                return {'error': result}, 400
        else:
            return {'error': 'Invalid token'}, 401
    else:
        return {'error': 'Missing parameters'}, 400


def get_user_id_from_token(token):
    connection = model.mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT user_id FROM tokens WHERE token = %s", (token,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except model.mysql.connector.Error as err:
        logger.error(f"Database error in get_user_id_from_token: {err}")
        return None
    finally:
        cursor.close()
        connection.close()
