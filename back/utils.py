import re


def validate(data, params):
    flag = True
    for param in params:
        if param not in data:
            flag = False
            break
    return flag


def remove_duplicate_lines(file_content):
    lines = file_content.split('\n')
    unique_lines = list(dict.fromkeys(lines))
    return unique_lines


def process_smtp_format_1(smtp_input):
    try:
        server, port, email, password = smtp_input.split(':', 3)

        if not validate_email(email):
            return None

        return server, port, email, password
    except Exception:
        return None


def process_smtp_format_2(smtp_input):
    try:
        server, email, parts = smtp_input.split(':', 2)
        password, port = parts.rsplit(':', 1)

        if not validate_email(email):
            return None

        return server, port, email, password
    except Exception:
        return None


def process_smtp_format_3(smtp_input):
    try:

        server, port, email, password = smtp_input.split(',', 3)

        if not validate_email(email):
            return None

        return server, port, email, password
    except Exception:
        return None


def process_smtp_format_4(smtp_input):
    try:
        part1, email, password = smtp_input.split(',', 2)
        server, port = part1.split(':', 1)
        port_digits = ''.join(filter(str.isdigit, port))

        if not validate_email(email):
            return None

        return server, port_digits, email, password
    except Exception:
        return None


def process_smtp_format_5(smtp_input):
    try:
        key_value_pairs = smtp_input.split('  ', 6)
        data = {}
        for pair in key_value_pairs:
            key, value = pair.split(':', 1)
            data[key.strip()] = value.strip()

        email = data['EMail']
        server = data['SMTP Server']
        port = data['Port']
        password = data['Password']

        if not validate_email(email):
            return None

        return server, port, email, password
    except Exception:
        return None


def auto_detect_smtp_format(smtp_input):
    parts = re.split(r'[:,]', smtp_input)

    if len(parts) < 4:
        return None

    server = parts[0]
    email = next((p for p in parts if validate_email(p)), None)
    port = next((p for p in parts if p.isdigit()), None)

    password_candidates = [p for p in parts if p not in (server, email, port)]

    if not email or not port or not password_candidates:
        return None

    password = ','.join(password_candidates)
    return server, port, email, password


def process_smtp_line(smtp_input):
    processors = [
        process_smtp_format_1,
        process_smtp_format_2,
        process_smtp_format_3,
        process_smtp_format_4,
        process_smtp_format_5
    ]

    for processor in processors:
        result = processor(smtp_input)
        if result:
            return result

    return auto_detect_smtp_format(smtp_input)


def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def get_imap_server_and_port(email):

    domain = email.split('@')[-1].lower()

    imap_servers = {
        'outlook.com': ('outlook.office365.com', 993),
        'gmail.com': ('imap.gmail.com', 993),
        'yahoo.com': ('imap.mail.yahoo.com', 993),
    }
    if domain in imap_servers:
        return imap_servers[domain]
    else:
        return None, None