import json
import random
import re
import string

import mysql.connector

import config
import log_config
from utils import remove_duplicate_lines, process_smtp_line, get_imap_server_and_port

logger = log_config.setup_logging()


def login(name, password):
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM `users` WHERE name='{name}';")
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    else:
        if result[0][2] == password:
            letters = string.ascii_lowercase
            token = ''.join(random.choice(letters) for i in range(16))
            cursor.execute(f"DELETE FROM `tokens` WHERE user='{result[0][0]}';")
            connection.commit()
            cursor.execute(f'INSERT INTO `tokens` (user, token) VALUES (%s, %s);', (result[0][0], token))
            connection.commit()
            return token
        else:
            return False


def check_token(token):
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `tokens` WHERE token = %s;", (token,))
    result = cursor.fetchall()
    return len(result) > 0



def check_session_name(name):
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM `sessions` WHERE name='{name}';")
    result = cursor.fetchall()
    if len(result) > 0:
        return False
    return True


def add_session(name):
    if check_session_name(name):
        connection = mysql.connector.connect(
            host=config.DBhost,
            port=config.DBport,
            user=config.DBuser,
            password=config.DBpassword,
            database=config.DBdatabase
        )
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO `sessions` (name) VALUES (%s);', (name,))
        connection.commit()
        return 1
    else:
        return 'This name already exist!'


def del_session(name):
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM `sessions` WHERE name='{name}';")
    connection.commit()


def list_session():
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM `sessions`;')
    res = cursor.fetchall()
    result = []
    for i in res:
        result.append({'data': i[1]})
    return result


email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


def input_material(session, type, file, filename):
    print(f'Starting input of material for session {session}, type {type}, filename {filename}')

    logger.info(f'Starting input of material for session {session}, type {type}, filename {filename}')
    if type not in ['bases', 'proxies', 'domains', 'smtps', 'imaps', 'dummy', 'templates']:
        return 'Wrong type!'

    if type != 'domains':
        filename = '';

    errors = 0
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()

    if type == 'bases':
        for line in file.split('\n'):
            data = line.replace('\n', '').split('-')
            if len(data) == 3:
                cursor.execute(f'INSERT INTO `bases` (first, last, email, session) VALUES (%s, %s, %s, %s);',
                               (data[0], data[1], data[2], session))
                connection.commit()
            else:
                errors += 1

    elif type == 'proxies':
        for line in file.split('\n'):
            data = line.replace(' ', '').replace('\n', '').split(':')
            if len(data) == 2:
                cursor.execute(f'INSERT INTO `proxies` (ip, port, status, session) VALUES (%s, %s, %s, %s);',
                               (data[0], data[1], 'none', session))
                connection.commit()
            else:
                errors += 1

    elif type == 'domains':
        for line in file.split('\n'):
            data = line.replace(' ', '').replace('\n', '')
            if data == '':
                errors += 1
                continue
            cursor.execute(f'INSERT INTO `domains` (url, status, session, tempName) VALUES (%s, %s, %s, %s);',
                           (data, 'none', session, filename))
            connection.commit()

    elif type == 'smtps':
        unique_lines = remove_duplicate_lines(file)
        logger.info(f'Removed duplicate lines. Processing {len(unique_lines)} unique lines.')
        print(f"DEL DUBL:{len(unique_lines)}")

        for line in unique_lines:
            line = line.strip()

            result = process_smtp_line(line)
            if result is None:
                logger.error(f"Unable to process line format: {line}")
                print(f"Unable to process line format: {line}")
                errors += 1
                continue

            server, port, email, password = result

            if server and port and email and password:

                try:

                    cursor.execute(

                        'INSERT INTO `smtps` (server, port, email, password, status, session) VALUES (%s, %s, %s, %s, %s, %s);',

                        (server, port, email, password, 'none', session))

                    connection.commit()

                except Exception as e:

                    logger.error(f"Error inserting line: {line}. Error: {e}")

                    print(f"Error inserting line: {line}. Error: {e}")

                    errors += 1

            else:

                logger.error(f"Missing required data: {line}")

                print(f"Missing required data: {line}")

                errors += 1



    # elif type == 'smtps':
    #     for line in unique_lines:
    #         line = line.strip()
    #         data = line.split(':')
    #
    #         if len(data) < 4:
    #             logger.error(f"Invalid line format (too few parts): {line}")
    #             print(f"Invalid line format (too few parts): {line}")
    #             errors += 1
    #             continue
    #
    #         server = data[0]
    #         email = data[1]
    #         port = data[-1]
    #         password = ':'.join(data[2:-1])
    #
    #         if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    #             logger.error(f"Invalid email format: {email}")
    #             print(f"Invalid email format: {email}")
    #             errors += 1
    #             continue
    #
    #         if server and port and email and password:
    #             try:
    #                 cursor.execute(
    #                     'INSERT INTO `smtps` (server, port, email, password, status, session) VALUES (%s, %s, %s, %s, %s, %s);',
    #                     (server, port, email, password, 'none', session))
    #                 connection.commit()
    #             except Exception as e:
    #                 logger.error(f"Error inserting line: {line}. Error: {e}")
    #                 print(f"Error inserting line: {line}. Error: {e}")
    #                 errors += 1
    #         else:
    #             errors += 1

    # elif type == 'imaps':
    #     unique_lines = remove_duplicate_lines(file)
    #     logger.info(f'Removed duplicate lines. Processing {len(unique_lines)} unique lines.')
    #     print(f"DEL DUBL:{len(unique_lines)}")
    #     for line in unique_lines:
    #         line = line.strip()
    #         data = line.split(':')
    #
    #         if len(data) < 4:
    #             logger.error(f"Invalid line format (too few parts): {line}")
    #             print(f"Invalid line format (too few parts): {line}")
    #             errors += 1
    #             continue
    #
    #         server = data[0]
    #         email = data[1]
    #         port = data[-1]
    #         password = ':'.join(data[2:-1])
    #
    #         if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    #             logger.error(f"Invalid email format: {email}")
    #             print(f"Invalid email format: {email}")
    #             errors += 1
    #             continue
    #
    #         if server and port and email and password:
    #             try:
    #                 cursor.execute(
    #                     'INSERT INTO `imaps` (server, port, email, password, status, session) VALUES (%s, %s, %s, %s, %s, %s);',
    #                     (server, port, email, password, 'none', session))
    #                 connection.commit()
    #             except Exception as e:
    #                 logger.error(f"Error inserting line: {line}. Error: {e}")
    #                 print(f"Error inserting line: {line}. Error: {e}")
    #                 errors += 1
    #         else:
    #             errors += 1

    elif type == 'imaps':
        unique_lines = remove_duplicate_lines(file)
        logger.info(f'Removed duplicate lines. Processing {len(unique_lines)} unique lines.')
        print(f"DEL DUBL:{len(unique_lines)}")
        errors = 0

        for line in unique_lines:
            line = line.strip()
            data = line.split(':')

            if len(data) == 2:
                email = data[0]
                password = data[1]
                server, port = get_imap_server_and_port(email)
            elif len(data) >= 4:
                server = data[0]
                email = data[1]
                port = data[-1]
                password = ':'.join(data[2:-1])
            else:
                logger.error(f"Invalid line format (too few parts): {line}")
                print(f"Invalid line format (too few parts): {line}")
                errors += 1
                continue

            if not re.match(email_regex, email):
                logger.error(f"Invalid email format: {email}")
                print(f"Invalid email format: {email}")
                errors += 1
                continue

            # Check if the server and port are provided
            if not server or not port:
                logger.error(f"Missing server or port for email: {email}")
                print(f"Missing server or port for email: {email}")
                errors += 1
                continue

            try:
                # Insert into the database
                cursor.execute(
                    'INSERT INTO `imaps` (server, port, email, password, status, session) VALUES (%s, %s, %s, %s, %s, %s);',
                    (server, port, email, password, 'none', session)
                )
                connection.commit()
            except Exception as e:
                logger.error(f"Error inserting line: {line}. Error: {e}")
                print(f"Error inserting line: {line}. Error: {e}")
                errors += 1

    elif type == 'dummy':
        if 'name' in file.keys() and 'template' in file.keys() and 'froms' in file.keys() and 'link' in file.keys() and 'sentence' in file.keys() and 'subject' in file.keys():
            cursor.execute(
                f'INSERT INTO `dummy` (name, template, froms, link, sentence, subject, session) VALUES (%s, %s, %s, %s, %s, %s, %s);',
                (file['name'], file['template'], file['froms'], file['link'], file['sentence'], file['subject'],
                 session))
            connection.commit()
        else:
            return 'File attribute has wrong params!'

    elif type == 'templates':
        if all('name' in item and 'data' in item and 'htmlbodies' in item for item in file):
            for item in file:
                tmp_name = item['name']
                cursor.execute('SELECT COUNT(*) FROM `temp` WHERE tempName = %s AND session = %s;', (tmp_name, session))
                result = cursor.fetchone()
                if result[0] == 0:
                    cursor.execute(f'INSERT INTO `temp` (tempName, status, session) VALUES (%s, %s, %s);',
                                   (tmp_name, 'none', session))
                    connection.commit()

                tmp = item['data']
                data = {'template': '', 'froms': '', 'link': '', 'subject': ''}
                tmp = tmp.split('<br>')
                data['template'] = tmp[-1]
                tmp.pop(-1)
                state = ''
                for i in tmp:
                    i = i.replace('\n', '')
                    if i == '':
                        continue
                    elif i == 'Subjects:':
                        state = 'subject'
                        continue
                    elif i == 'From:':
                        state = 'froms'
                        continue
                    elif i == 'Link4 or Short:':
                        state = 'link'
                        continue
                    data[state] += f'{i}\n'
                temp_id = None
                cursor.execute('SELECT id FROM `temp` WHERE tempName = %s AND session = %s;', (tmp_name, session))
                result = cursor.fetchone()
                if result:
                    temp_id = result[0]

                cursor.execute(
                    f'INSERT INTO `templates` (maintmp, template, froms, subject, status, session, htmlbodies) VALUES (%s, %s, %s, %s, %s, %s, %s);',
                    (temp_id, data['template'], data['froms'][:-1], data['subject'][:-1], 'none', session,
                     item['htmlbodies']))
                connection.commit()
                template_id = cursor.lastrowid

                for line in data['link'].split('\n'):
                    url = line.strip().replace(' ', '').replace('\n', '')
                    if url and url.startswith('http'):
                        cursor.execute(
                            f'INSERT INTO `domains` (url, status, session, tempName, template_id) VALUES (%s, %s, %s, %s, %s);',
                            (url, 'none', session, item['name'], template_id))
                        connection.commit()
                    else:
                        errors += 1

        else:
            errors += 1
            logger.info(f"Errors encountered during template processing: {errors}")
        print("Errors: ", errors)
    if errors != 0:
        logger.warning(f'{errors} incorrectly formatted fields for session {session}, type {type}')
        return f'{errors} incorrectly formatted fields!'

    return 1


def del_material(id, type):
    if type not in ['bases', 'proxies', 'domains', 'smtps', 'imaps', 'dummy', 'templates']:
        return 'Wrong type!'
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM `{type}` WHERE id='{id}';")
    connection.commit()


def del_material_str(string, type, item, id):
    if type not in ['templates', 'dummy']:
        return 'Wrong type!'
    if type == 'templates':
        if item not in ['froms', 'subject']:
            return 'Wrong item!'
    if type == 'dummy':
        if item not in ['froms', 'link', 'sentence', 'subject']:
            return 'Wrong item!'
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    cursor.execute(f"SELECT {item} FROM {type} WHERE id='{id}';")
    result = cursor.fetchall()
    if len(result) > 0:
        result = result[0][0]
        result = result.replace(f"{string}\n", '')
    cursor.execute(f"UPDATE {type} SET {item}='{result}' WHERE id={id};")
    connection.commit()


def reset_all():
    logger.info('Starting reset of all tables')
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM bases;")
        cursor.execute("DELETE FROM proxies;")
        cursor.execute("DELETE FROM domains;")
        cursor.execute("DELETE FROM smtps;")
        cursor.execute("DELETE FROM imaps;")
        cursor.execute("DELETE FROM dummy;")
        cursor.execute("DELETE FROM templates;")
        connection.commit()
        logger.info('Successfully reset all tables')
        return 1
    except mysql.connector.Error as err:
        logger.error(f"Error resetting tables: {err}")
        print(f"Error: {err}")
        return str(err)
    finally:
        cursor.close()
        connection.close()


def reset_status(type, status):
    logger.info(f'Starting reset status:{status} for {type}')
    if type not in ['proxies', 'domains', 'smtps', 'imaps', 'templates']:
        return 'Wrong type!'
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    try:
        cursor.execute(f"UPDATE {type} SET status='none';")
        connection.commit()
        logger.info(f'Successfully reset status {type}')
        return 1
    except mysql.connector.Error as err:
        logger.error(f"Error resetting status: {err}")
        print(f"Error: {err}")
        return str(err)
    finally:
        cursor.close()
        connection.close()


def getTbl(type, session):
    logger.info(f'Starting getTbl for session {session}, type {type}')

    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()

    try:
        if type not in ['bases', 'proxies', 'domains', 'smtps', 'imaps', 'dummy', 'templates']:
            logger.error(f'Invalid type {type} for session {session}')
            return 'Wrong type!'

        if type == 'bases':
            cursor.execute(f"SELECT * FROM `bases` WHERE session = '{session}';")
            res = cursor.fetchall()
            result = [{'id': i[0], 'name': i[1], 'status': i[3]} for i in res]
            logger.info(f'Fetched {len(result)} bases for session {session}')
        elif type == 'proxies':
            cursor.execute(f"SELECT * FROM `proxies` WHERE session = '{session}';")
            res = cursor.fetchall()
            result = [{'id': i[0], 'ip': i[1], 'port': i[2], 'status': i[3]} for i in res]
            logger.info(f'Fetched {len(result)} proxies for session {session}')
        elif type == 'domains':
            cursor.execute(f"""
                SELECT 
                    MIN(id) as id, 
                    SUBSTRING_INDEX(SUBSTRING_INDEX(url, '/', 3), '/', -1) as domain,
                    MIN(url) as url, 
                    MIN(status) as status 
                FROM domains 
                WHERE session = '{session}' 
                GROUP BY domain;
            """)
            res = cursor.fetchall()
            result = [{'id': i[0], 'url': i[1], 'status': i[3]} for i in res]
            logger.info(f'Fetched {len(result)} domains for session {session}')
        elif type == 'smtps':
            cursor.execute(f"SELECT * FROM `smtps` WHERE session = '{session}';")
            res = cursor.fetchall()
            result = [{'id': i[0], 'server': i[1], 'port': i[2], 'email': i[3], 'password': i[4], 'status': i[5]} for i
                      in res]
            logger.info(f'Fetched {len(result)} smtps for session {session}')
        elif type == 'imaps':
            cursor.execute(f"SELECT * FROM `imaps` WHERE session = '{session}';")
            res = cursor.fetchall()
            result = [{'id': i[0], 'server': i[1], 'port': i[2], 'email': i[3], 'password': i[4], 'status': i[5]} for i
                      in res]
            logger.info(f'Fetched {len(result)} imaps for session {session}')
        elif type == 'dummy':
            cursor.execute(f"SELECT * FROM `dummy` WHERE session = '{session}';")
            res = cursor.fetchall()
            result = [{'id': i[0], 'name': i[1]} for i in res]
            logger.info(f'Fetched {len(result)} dummy entries for session {session}')
        elif type == 'templates':
            cursor.execute(f"SELECT * FROM `temp` WHERE session = '{session}';")
            res = cursor.fetchall()
            result = [{'id': i[0], 'name': i[1], 'status': i[3], 'bodyName': i[-1]} for i in res]
            logger.info(f'Fetched {len(result)} templates for session {session}')
        return result
    except mysql.connector.Error as err:
        logger.error(f"Error fetching {type} for session {session}: {err}")
        return []
    finally:
        cursor.close()
        connection.close()


def getTblSub(id, type, item):
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    if type not in ['templates', 'dummy', 'bases']:
        return 'Wrong type!'
    if type == 'templates':
        if item not in ['template', 'froms', 'subject', '*']:
            return 'Wrong item!'
        else:
            cursor.execute(f"SELECT {item} FROM `{type}` WHERE maintmp='{id}';")
    if type == 'dummy':
        if item not in ['template', 'froms', 'link', 'sentence', 'subject', '*']:
            return 'Wrong item!'
        else:
            cursor.execute(f"SELECT {item} FROM `{type}` WHERE maintmp='{id}';")
    if type == 'bases':
        if item not in ['*']:
            return 'Wrong item!'
        else:
            cursor.execute(f"SELECT {item} FROM `{type}` WHERE base_id='{id}';")
    result = cursor.fetchall()
    return result


def get_material_to_check(id, type, session):
    logger.info(f'Starting get_material_to_check for session {session}, type {type}, id {id}')
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    try:
        if id == 'all':
            cursor.execute(f"SELECT * FROM {type} WHERE session='{session}';")
            logger.info(f'Fetched all records for session {session}, type {type}')
            return cursor.fetchall()
        elif id == 'inbox':
            query = f"SELECT * FROM {type} WHERE session = %s AND status = %s;"
            cursor.execute(query, (session, 'inbox'))
            return cursor.fetchall()
        elif id == 'junk':
            query = f"SELECT * FROM {type} WHERE session = %s AND status = %s;"
            cursor.execute(query, (session, 'junk'))
            return cursor.fetchall()
        elif id == 'dead':
            query = f"SELECT * FROM {type} WHERE session = %s AND status = %s;"
            cursor.execute(query, (session, 'dead'))
            return cursor.fetchall()
        elif id == 'none':
            query = f"SELECT * FROM {type} WHERE session = %s AND status = %s;"
            cursor.execute(query, (session, 'none'))
            return cursor.fetchall()
        elif id == 'checked':
            query = f"SELECT * FROM {type} WHERE session = %s AND status = %s;"
            cursor.execute(query, (session, 'checked'))
            return cursor.fetchall()
        else:
            res = []
            if isinstance(id, str):
                try:
                    id = int(id)
                except ValueError:
                    pass
            if isinstance(id, int):
                cursor.execute(f"SELECT * FROM {type} WHERE id='{id}' AND session='{session}';")
                row = cursor.fetchone()
                if row:
                    res.append(row)
                logger.info(f'Fetched record for session {session}, type {type}, id {id}')
            else:
                for i in id:
                    cursor.execute(f"SELECT * FROM {type} WHERE id='{i}' AND session='{session}';")
                    row = cursor.fetchone()
                    if row:
                        res.append(row)
            return res
    except mysql.connector.Error as err:
        logger.error(f"Error fetching material to check for session {session}, type {type}, id {id}: {err}")
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()
        connection.close()


def del_log(session, type):
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    query = "DELETE FROM `logs` WHERE `type` = %s AND `session` = %s;"
    cursor.execute(query, (type, session))
    connection.commit()
    cursor.close()
    connection.close()


def change_status(ar, type, status):
    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    if type == 'smtps':
        for i in ar:
            cursor.execute(f"UPDATE smtps SET status='{status}' WHERE email='{i}';")
            connection.commit()
    elif type == 'imaps':
        for i in ar:
            cursor.execute(f"UPDATE imaps SET status='{status}' WHERE email='{i}';")
            connection.commit()
    elif type == 'proxies':
        for i in ar:
            cursor.execute(f"UPDATE proxies SET status='{status}' WHERE ip='{i}';")
            connection.commit()
    elif type == 'domains':
        for i in ar:
            cursor.execute(f"UPDATE domains SET status='{status}' WHERE url='{i}';")
            connection.commit()


def change_password(user_id, current_password, new_password):
    try:
        connection = mysql.connector.connect(
            host=config.DBhost,
            port=config.DBport,
            user=config.DBuser,
            password=config.DBpassword,
            database=config.DBdatabase
        )
        cursor = connection.cursor()

        cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            return "User not found"

        current_stored_password = result[0]

        if current_password != current_stored_password:
            return "Incorrect password"

        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, user_id))
        connection.commit()

        return "Password changed successfully"
    except mysql.connector.Error as err:
        return f"Database error: {err}"
    finally:
        cursor.close()
        connection.close()


def get_material_to_mailing(id, type, session):
    logger.info(f'Starting get_material_to_mailing for session {session}, type {type}, id {id}')

    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()
    try:
        if type == 'domains':
            if id in ['inbox', 'junk', 'dead', 'none', 'checked']:
                cursor.execute(f"SELECT * FROM {type} WHERE status='{id}' AND session='{session}';")
                result = cursor.fetchall()
                domains = []
                for i in result:
                    url = i[1].replace('https://', '').replace('http://', '')
                    logger.debug(f'Processed domain URL: {url}')
                    domains.append(url)
                logger.info(
                    f'Fetched and processed {len(domains)} domains for session {session}, type {type}, status {id}')
                return domains
            elif id == 'all':
                cursor.execute(f"SELECT * FROM {type} WHERE session='{session}';")
                result = cursor.fetchall()
                logger.info(f'Fetched all domains for session {session}, type {type}')
                return result
            else:
                res = []
                for i in id:
                    cursor.execute(f"SELECT * FROM {type} WHERE id='{i}' AND session='{session}';")
                    res.append(cursor.fetchall()[0])
                logger.info(f'Fetched specific domains for session {session}, type {type}, ids {id}')
                return res
        else:
            if id in ['inbox', 'junk', 'dead', 'none', 'checked']:
                cursor.execute(f"SELECT * FROM {type} WHERE status='{id}' AND session='{session}';")
                result = cursor.fetchall()
                logger.info(f'Fetched {type} for session {session}, status {id}')
                return result
            elif id == 'all':
                cursor.execute(f"SELECT * FROM {type} WHERE session='{session}';")
                result = cursor.fetchall()
                logger.info(f'Fetched all {type} for session {session}')
                return result
            else:
                res = []
                for i in id:
                    cursor.execute(f"SELECT * FROM {type} WHERE id='{i}' AND session='{session}';")
                    res.append(cursor.fetchall()[0])
                logger.info(f'Fetched specific {type} for session {session}, ids {id}')
                return res
    except mysql.connector.Error as err:
        logger.error(f"Error fetching material to mailing for session {session}, type {type}, id {id}: {err}")
        return None
    finally:
        cursor.close()
        connection.close()


def update_material_status(material_type, material_id, new_status, session):
    logger.info(
        f'Starting update_material_status for session {session}, material_type {material_type}, material_id {material_id}, new_status {new_status}')

    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()

    try:
        if material_type == 'domains':
            cursor.execute(f"SELECT url FROM domains WHERE id='{material_id}' AND session='{session}';")
            domain = cursor.fetchone()[0]
            base_domain = '.'.join(domain.split('.')[-2:])

            cursor.execute(
                f"UPDATE domains SET status='{new_status}' WHERE url LIKE '%{base_domain}' AND session='{session}';")
            logger.info(f'Updated status for base domain {base_domain} in session {session} to {new_status}')
        else:
            cursor.execute(
                f"UPDATE {material_type} SET status='{new_status}' WHERE id='{material_id}' AND session='{session}';")
            logger.info(f'Updated status for {material_type} id {material_id} in session {session} to {new_status}')

        connection.commit()
    except mysql.connector.Error as err:
        logger.error(
            f"Error updating material status for session {session}, material_type {material_type}, material_id {material_id}: {err}")
    finally:
        cursor.close()
        connection.close()


def add_log(type, session, logtext, status):
    logger.info(f'Starting add_log for session {session}, type {type}')
    try:
        connection = mysql.connector.connect(
            host=config.DBhost,
            port=config.DBport,
            user=config.DBuser,
            password=config.DBpassword,
            database=config.DBdatabase
        )
        cursor = connection.cursor()
        query = "INSERT INTO logs (type, session, TEXT, status) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (type, session, logtext, status))
        connection.commit()
        logger.info(f'Log added for session {session}, type {type}')
    except mysql.connector.Error as err:
        logger.error(f"Error adding log for session {session}, type {type}: {err}")
    finally:
        cursor.close()
        connection.close()


def get_logs(type, session):
    logger.info(f'Starting get_logs for session {session}, type {type}')
    logs = []
    try:
        connection = mysql.connector.connect(
            host=config.DBhost,
            port=config.DBport,
            user=config.DBuser,
            password=config.DBpassword,
            database=config.DBdatabase
        )
        cursor = connection.cursor(dictionary=True)
        query = "SELECT created_at,TEXT,status FROM logs WHERE session = %s AND type = %s ORDER BY id ASC"
        cursor.execute(query, (session, type,))
        logs = cursor.fetchall()
        logger.info(f'Fetched {len(logs)} logs for session {session}, type {type}')
    except mysql.connector.Error as err:
        logger.error(f"Error fetching logs for session {session}, type {type}: {err}")
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()
    return logs


def get_counts(session):
    logger.info(f'Starting get_counts for session {session}')
    counts = {
        'count': 0,
        'valid': 0,  # Инициализируем valid
        'dead': 0,
        'inbox': 0,
        'junk': 0,
        'templates': 0,
        'allDomains': 0, # for all domains 
        'urlDomains': 0, # for unique domains
        'imgDomains': 0,
        'socks': 0
    }
    try:
        connection = mysql.connector.connect(
            host=config.DBhost,
            port=config.DBport,
            user=config.DBuser,
            password=config.DBpassword,
            database=config.DBdatabase
        )
        cursor = connection.cursor()

        # Общий подсчет SMTP
        query = f"SELECT COUNT(*) as count FROM smtps WHERE session = %s"
        cursor.execute(query, (session,))
        result = cursor.fetchone()
        if result:
            counts['count'] = result[0]

        # Подсчет dead SMTP
        query = f"SELECT COUNT(*) as count FROM smtps WHERE session = %s AND status = 'dead'"
        cursor.execute(query, (session,))
        result = cursor.fetchone()
        if result:
            counts['dead'] = result[0]

        # Подсчет inbox SMTP
        query = f"SELECT COUNT(*) as count FROM smtps WHERE session = %s AND status = 'inbox'"
        cursor.execute(query, (session,))
        result = cursor.fetchone()
        if result:
            counts['inbox'] = result[0]

        # Подсчет junk SMTP
        query = f"SELECT COUNT(*) as count FROM smtps WHERE session = %s AND status = 'junk'"
        cursor.execute(query, (session,))
        result = cursor.fetchone()
        if result:
            counts['junk'] = result[0]

        # Подсчет checked (valid) SMTP
        query = f"SELECT COUNT(*) as count FROM smtps WHERE session = %s AND status = 'checked'"
        cursor.execute(query, (session,))
        result = cursor.fetchone()
        if result:
            counts['valid'] = result[0]  # Добавлен подсчет для checked

        # Подсчет шаблонов
        query = f"SELECT COUNT(*) as count FROM templates WHERE session = %s"
        cursor.execute(query, (session,))
        result = cursor.fetchone()
        if result:
            counts['templates'] = result[0]

        # Подсчет доменов
        query = f"SELECT COUNT(*) as count FROM domains WHERE session = %s"
        cursor.execute(query, (session,))
        result = cursor.fetchone()
        if result:
            counts['domains'] = result[0]

        # Подсчет прокси
        query = f"SELECT COUNT(*) as count FROM proxies WHERE session = %s"
        cursor.execute(query, (session,))
        result = cursor.fetchone()
        if result:
            counts['socks'] = result[0]

        # Counting all URL Domains
        query = f"SELECT COUNT(*) as count FROM domains WHERE session = %s;"
        cursor.execute(query, (session,))
        result = cursor.fetchone()
        if result:
            counts['allDomains'] = result[0]  # Count of all domains


        query = f"""
            SELECT COUNT(DISTINCT SUBSTRING_INDEX(url, '.', 1)) AS count 
            FROM domains 
            WHERE session = %s;
        """
        cursor.execute(query, (session,))
        result = cursor.fetchone()
        if result:
            counts['urlDomains'] = result[0]  # Count of main domains

        # Counting IMG Domains
        query = f"SELECT COUNT(*) as count FROM domains WHERE session = %s AND (url LIKE '%.jpg' OR url LIKE '%.jpeg' OR url LIKE '%.png' OR url LIKE '%.gif' OR url LIKE '%.bmp' OR url LIKE '%.tiff');"
        cursor.execute(query, (session,))
        result = cursor.fetchone()
        if result:
            counts['imgDomains'] = result[0]  # Count of image domains

        logger.info(f'Counts for session {session}: {counts}')
    except mysql.connector.Error as err:
        logger.error(f"Error getting counts for session {session}: {err}")
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return counts


# def get_counts(session):
#     logger.info(f'Starting get_counts for session {session}')
#     counts = {
#         'count': 0,
#         'valid': 0,
#         'dead': 0,
#         'inbox': 0,
#         'junk': 0,
#         'templates': 0,
#         'domains': 0,
#         'socks': 0
#     }
#     try:
#         connection = mysql.connector.connect(
#             host=config.DBhost,
#             port=config.DBport,
#             user=config.DBuser,
#             password=config.DBpassword,
#             database=config.DBdatabase
#         )
#         cursor = connection.cursor()
#         query = f"SELECT COUNT(*) as count FROM smtps WHERE session = %s"
#         cursor.execute(query, (session,))
#         result = cursor.fetchone()
#         if result:
#             counts['count'] = result[0]
#         query = f"SELECT COUNT(*) as count FROM smtps WHERE session = %s AND status = 'dead'"
#         cursor.execute(query, (session,))
#         result = cursor.fetchone()
#         if result:
#             counts['dead'] = result[0]
#         query = f"SELECT COUNT(*) as count FROM smtps WHERE session = %s AND status = 'inbox'"
#         cursor.execute(query, (session,))
#         result = cursor.fetchone()
#         if result:
#             counts['inbox'] = result[0]
#         query = f"SELECT COUNT(*) as count FROM smtps WHERE session = %s AND status = 'junk'"
#         cursor.execute(query, (session,))
#         result = cursor.fetchone()
#         if result:
#             counts['junk'] = result[0]
#         query = f"SELECT COUNT(*) as count FROM templates WHERE session = %s"
#         cursor.execute(query, (session,))
#
#         if result:
#             counts['templates'] = result[0]
#         query = f"SELECT COUNT(*) as count FROM domains WHERE session = %s"
#         cursor.execute(query, (session,))
#         result = cursor.fetchone()
#         if result:
#             counts['domains'] = result[0]
#         query = f"SELECT COUNT(*) as count FROM proxies WHERE session = %s"
#         cursor.execute(query, (session,))
#         result = cursor.fetchone()
#         if result:
#             counts['socks'] = result[0]
#         logger.info(f'Counts for session {session}: {counts}')
#     except mysql.connector.Error as err:
#         logger.error(f"Error getting counts for session {session}: {err}")
#         print(f"Error: {err}")
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()
#     return counts


def create_settings(session, settings):
    logger.info(f'Starting create_settings for session {session}')

    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()

    try:
        for key in settings.keys():
            cursor.execute(
                "INSERT INTO settings (session, type, data) VALUES (%s, %s, NULL) ON DUPLICATE KEY UPDATE data = NULL;",
                (session, key))
        connection.commit()
        logger.info(f'Settings created/updated for session {session}')
    except mysql.connector.Error as err:
        logger.error(f"Error creating settings for session {session}: {err}")
    finally:
        cursor.close()
        connection.close()


def update_setting(session, setting_type, data):
    logger.info(f'Starting update_setting for session {session}, setting_type {setting_type}')

    connection = mysql.connector.connect(
        host=config.DBhost,
        port=config.DBport,
        user=config.DBuser,
        password=config.DBpassword,
        database=config.DBdatabase
    )
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE settings SET data = %s WHERE session = %s AND type = %s;",
                       (json.dumps(data) if isinstance(data, (list, dict)) else str(data), session, setting_type))
        connection.commit()
        logger.info(f'Setting updated for session {session}, setting_type {setting_type}')
    except mysql.connector.Error as err:
        logger.error(f"Error updating setting for session {session}, setting_type {setting_type}: {err}")
    finally:
        cursor.close()
        connection.close()
