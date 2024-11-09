from time import sleep
import model
from app import app, socket
import smtplib
import imaplib
import socks
import socket
import time
from numpy.random import uniform
from dataclasses import dataclass
import hashlib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import random
import threading
import queue
import string
import re
import requests
import log_config

logger = log_config.setup_logging()


@dataclass
class ImapConfig:
    server: str
    port: int
    email: str
    password: str
    connect_timeout: int
    connect_attempts: int

    def line(self) -> str:
        return f"{self.server}:{self.port}:{self.email}:{self.password}"


@dataclass
class SMTPConfig:
    server: str
    port: int
    email: str
    password: str

    def line(self) -> str:
        return f"{self.server}:{self.port}:{self.email}:{self.password}"


def get_rand_string(n: int) -> str:
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(n)
    )


def try_int(n):
    try:
        return int(n)
    except:
        return None


def try_float(n):
    try:
        return float(n)
    except:
        return None


def validate_material(ar, c):
    res = set()
    for i in ar:
        if ar.count(i) >= c:
            res.add(i)
    return res


def connect_smtp(smtp, proxy):
    logger.info(f'Starting SMTP connection for {smtp.email} with proxy {proxy}')
    smtp_timeout = 45
    for attempt in range(3):
        if proxy:
            time.sleep(uniform(0.1, 10))
            socks.setdefaultproxy(
                socks.SOCKS5, proxy.split(":")[0], int(proxy.split(":")[1]), True
            )
            socket.socket = socks.socksocket
        server_connect = None

        try:
            if smtp.port == 587:
                server_connect = smtplib.SMTP(
                    smtp.server,
                    smtp.port,
                    local_hostname="[127.0.0.1]",
                    timeout=smtp_timeout,
                )
                server_connect.ehlo_or_helo_if_needed()
                server_connect.starttls()
            elif smtp.port == 465:
                server_connect = smtplib.SMTP_SSL(
                    smtp.server,
                    smtp.port,
                    local_hostname="[127.0.0.1]",
                    timeout=smtp_timeout,
                )
            else:
                server_connect = smtplib.SMTP(
                    smtp.server, local_hostname="[127.0.0.1]", timeout=smtp_timeout
                )
                server_connect.ehlo_or_helo_if_needed()
                try:
                    server_connect.starttls()
                except Exception:
                    pass
            server_connect.ehlo_or_helo_if_needed()
            server_connect.login(smtp.email, smtp.password)
            logger.info(f'Successfully connected to SMTP server {smtp.server} for {smtp.email}')
            return server_connect, proxy
        except Exception as ex:
            logger.error(f'Error connecting to SMTP server {smtp.server} for {smtp.email} with proxy {proxy}: {ex}')
            return None, ex
    logger.error(f'Failed to connect to SMTP server {smtp.server} for {smtp.email} after 3 attempts')
    return None, proxy


def connect_smtp_to_check(queue, socket_, smtp, proxy, timeout):
    s1 = smtp.email.replace(':', ' ')
    if proxy:
        s2 = proxy.replace(':', ' ')
    else:
        s2 = None

    logger.info(f'Starting SMTP check for {s1} with proxy {s2}')

    for attempt in range(3):
        if proxy:
            time.sleep(uniform(0.1, 10))
            socks.setdefaultproxy(
                socks.SOCKS5, proxy.split(":")[0], int(proxy.split(":")[1]), True
            )
            socket.socket = socks.socksocket
        server_connect = None

        try:
            if smtp.port == 587:
                server_connect = smtplib.SMTP(
                    smtp.server,
                    smtp.port,
                    local_hostname="[127.0.0.1]",
                    timeout=timeout,
                )
                server_connect.ehlo_or_helo_if_needed()
                server_connect.starttls()
            elif smtp.port == 465:
                server_connect = smtplib.SMTP_SSL(
                    smtp.server,
                    smtp.port,
                    local_hostname="[127.0.0.1]",
                    timeout=timeout,
                )
            else:
                server_connect = smtplib.SMTP(
                    smtp.server, local_hostname="[127.0.0.1]", timeout=timeout
                )
                server_connect.ehlo_or_helo_if_needed()
                try:
                    server_connect.starttls()
                except Exception:
                    pass
            server_connect.ehlo_or_helo_if_needed()
            server_connect.login(smtp.email, smtp.password)
            queue.put([server_connect, smtp])
            socket_.send(f'logs_check_smtps:console-debug:{s1}|{s2}|success')
            logger.info(f'Successfully connected to SMTP server {smtp.server} for {s1} with proxy {s2}')
            return server_connect, smtp
        except Exception as ex:
            logger.error(f'Error connecting to SMTP server {smtp.server} for {s1} with proxy {s2}: {ex}')
            s3 = ex
            socket_.send(f'logs_check_smtps:console-error:{s1}|{s2}|{s3}')
            queue.put([None, smtp])
            return None, smtp

    logger.error(f'Failed to connect to SMTP server {smtp.server} for {s1} after 3 attempts')
    socket_.send(f'logs_check_smtps:console-error:{s1}|{s2}|error')
    queue.put([None, smtp])
    return None, smtp


def connect_imap_to_check(queue, socket_, imap, proxy):
    s1 = imap.email.replace(':', ' ')
    if proxy:
        s2 = proxy.replace(':', ' ')
    else:
        s2 = None

    logger.info(f'Starting IMAP check for {s1} with proxy {s2}')
    socket.setdefaulttimeout(int(imap.connect_timeout))
    for _ in range(int(imap.connect_attempts)):
        try:
            server_connect = imaplib.IMAP4_SSL(imap.server, imap.port)
            server_connect.login(imap.email, imap.password)
            queue.put([server_connect, imap])
            socket_.send(f'logs_check_imaps:console-debug:{s1}|{s2}|success')
            logger.info(f'Successfully connected to IMAP server {imap.server} for {s1} with proxy {s2}')
            return server_connect
        except Exception as e:
            logger.error(f'Error connecting to IMAP server {imap.server} for {s1} with proxy {s2}: {e}')
            s3 = e
    logger.error(f'Failed to connect to IMAP server {imap.server} for {s1} after {imap.connect_attempts} attempts')
    socket_.send(f'logs_check_imaps:console-error:{s1}|{s2}|{s3}')
    queue.put([None, imap])
    print("Exceeded maximum connection attempts IMAP")
    return None


def test_proxy(queue, socket_, proxy):
    if proxy:
        s1 = proxy.replace(':', ' ')
    else:
        s1 = None

    logger.info(f'Starting proxy test for {s1}')
    try:
        proxy_host, proxy_port = proxy.split(':')
        socks.setdefaultproxy(socks.SOCKS5, proxy_host, int(proxy_port), True)
        socks.wrapmodule(smtplib)

        socket.socket = socks.socksocket

        with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as server:
            server.ehlo()
            socket_.send(f'logs_check_proxy:console-debug:{s1}|success')
            queue.put([True, proxy])
            logger.info(f'Proxy {s1} is working successfully')
            return True
    except Exception as e:
        logger.error(f'Error testing proxy {s1}: {e}')
        s2 = e
        socket_.send(f'logs_check_proxy:console-error:{s1}|{s2}')
        queue.put([False, proxy])
        return False
    finally:
        socks.setdefaultproxy()
        logger.info(f'Finished proxy test for {s1}')


def test_domain(queue, socket_, url):
    s1 = url
    try:
        requests.get(url, timeout=20)
    except Exception as ex:
        logger.error(f'Error testing domain {s1}: {ex}')
        socket_.send(f'logs_check_domain:console-error:{s1}|{ex}')
        queue.put([False, url])
        return False
    logger.info(f'Finished domain test for {s1}')
    socket_.send(f'logs_check_domain:console-debug:{s1}')
    queue.put([True, url])
    return True


def get_hash(plaintext: str) -> str:
    if not plaintext:
        print("Error: Empty string passed to get_hash()")
        return ""

    return hashlib.md5(plaintext.encode("utf-8")).hexdigest()


def prepare_email(data):
    def __put_controls(s: str, _body: str, _smtp: str, _proxy: str) -> str:
        return (
            s.replace("%%BODYID%%", str(get_hash(_body)))
            .replace("%%SMTPID%%", str(get_hash(_smtp)))
            .replace("%%PROXYID%%", str(get_hash(_proxy)))
        )

    msg = MIMEMultipart("related")
    msg["From"] = formataddr((data["from"], data["smtp"].email)) if data["from"] else data["smtp"].email
    msg["To"] = data["base"]
    msg["Subject"] = Header(data["subject"], "utf-8")

    to_use_proxy_in_control_line = data["proxy"]

    msg.attach(
        MIMEText(
            __put_controls(
                data["template"],
                data["template_name"],
                data["smtp"].line(),
                to_use_proxy_in_control_line,
            ),
            "html",
        )
    )

    return msg


def send(socket, data, delay):
    global c_test_mode_send_error
    global c_test_mode_send_valid
    time.sleep(delay)
    smtp_connection, data["proxy"] = connect_smtp(data["smtp"], data["proxy"])
    email = data['smtp'].email
    proxy = data['proxy']

    if not smtp_connection:
        s1 = email.replace(':', ' ')
        s2 = proxy.replace(':', ' ')
        socket.send(f'logs_send:console-error:{s1}|{s2}|no connection')
        return False

    email_message = prepare_email(data)

    try:
        smtp_connection.send_message(email_message)
        smtp_connection.quit()
    except Exception as ex:
        print(ex)
        s1 = email.replace(':', ' ')
        s2 = proxy.replace(':', ' ')
        s3 = ex
        socket.send(f'logs_send:console-error:{s1}|{s2}|{s3}')
        c_test_mode_send_error += 1
        return False

    s1 = email.replace(':', ' ')
    s2 = proxy.replace(':', ' ')
    socket.send(f'logs_send:console-debug:{s1}|{s2}|success')
    c_test_mode_send_valid += 1
    return True


def check_smtps(socket, session, smtp_id, proxy_id, timeout):
    logger.info(f'Starting SMTP check for session {session}, SMTP ID {smtp_id}, and Proxy ID {proxy_id}')

    if not try_float(timeout):
        timeout = 45
    else:
        timeout = try_float(timeout)
    material = model.get_material_to_check(smtp_id, 'smtps', session)
    proxy_list = model.get_material_to_check(proxy_id, 'proxies', session)

    print(f"Material: {material}")
    print(f"Proxy list: {proxy_list}")

    count = 0
    len_smtps = len(material)
    valid = []
    errors = []
    threads = []
    queue_ = queue.Queue()
    for i in material:
        proxy = random.choice(proxy_list)
        proxy = proxy[1] + ':' + proxy[2]
        smtp = SMTPConfig(i[1], i[2], i[3], i[4])
        threads.append(threading.Thread(target=connect_smtp_to_check, args=(queue_, socket, smtp, proxy, timeout)))
    logger.info(f'Starting {len(threads)} threads for SMTP checking')
    for i in threads:
        i.start()
    for i in threads:
        i.join()
        res = queue_.get()
        if res[0] != None:
            valid.append(res[1].email)
        else:
            errors.append(res[1].email)
        count += 1
        socket.send(f'progress_check_smtps:{len(valid)}:{len(errors)}:{int(count / len_smtps * 100)}')
    model.change_status(valid, 'smtps', 'checked')
    model.change_status(errors, 'smtps', 'dead')


def check_smtp(socket, session, smtp_id):
    timeout = 5
    if not try_float(timeout):
        timeout = 45
    else:
        timeout = try_float(timeout)
    material = model.get_material_to_check(smtp_id, 'smtps', session)
    proxy_list = model.get_material_to_check("checked", 'proxies', session)

    print(f"Material: {material}")
    print(f"Proxy list: {proxy_list}")

    count = 0
    len_smtps = len(material)
    len_proxy = len(proxy_list)
    if len_proxy == 0:
        return False
    valid = []
    errors = []
    threads = []
    queue_ = queue.Queue()
    for i in material:
        proxy = random.choice(proxy_list)
        proxy = proxy[1] + ':' + proxy[2]
        smtp = SMTPConfig(i[1], i[2], i[3], i[4])
        threads.append(threading.Thread(target=connect_smtp_to_check, args=(queue_, socket, smtp, proxy, timeout)))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
        res = queue_.get()
        if res[0] != None:
            valid.append(res[1].email)
        else:
            errors.append(res[1].email)
        count += 1
        socket.send(f'progress_check_smtps:{len(valid)}:{len(errors)}:{int(count / len_smtps * 100)}')
    model.change_status(valid, 'smtps', 'checked')
    model.change_status(errors, 'smtps', 'dead')


def check_imaps(socket, session, imap_id, proxy_id, timeout):
    timeout = 5
    if not try_float(timeout):
        timeout = 45
    else:
        timeout = try_float(timeout)
    material = model.get_material_to_check(imap_id, 'imaps', session)
    proxy_list = model.get_material_to_check(proxy_id, 'proxies', session)

    print(f"Material: {material}")
    print(f"Proxy list: {proxy_list}")

    count = 0
    len_smtps = len(material)
    len_proxy = len(proxy_list)
    if len_proxy == 0:
        return False
    valid = []
    errors = []
    threads = []
    queue_ = queue.Queue()
    for i in material:
        proxy = random.choice(proxy_list)
        proxy = proxy[1] + ':' + proxy[2]
        imap = ImapConfig(i[1], i[2], i[3], i[4], timeout, timeout)
        threads.append(threading.Thread(target=connect_imap_to_check, args=(queue_, socket, imap, proxy)))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
        res = queue_.get()
        if res[0] != None:
            valid.append(res[1].email)
        else:
            errors.append(res[1].email)
        count += 1
        socket.send(f'progress_check_imaps:{len(valid)}:{len(errors)}:{int(count / len_smtps * 100)}')
    model.change_status(valid, 'imaps', 'checked')
    model.change_status(errors, 'imaps', 'dead')
    return True


def check_imap(socket, session, imap_id):
    timeout = 5
    if not try_float(timeout):
        timeout = 45
    else:
        timeout = try_float(timeout)
    material = model.get_material_to_check(imap_id, 'imaps', session)
    proxy_list = model.get_material_to_check("checked", 'proxies', session)

    print(f"Material: {material}")
    print(f"Proxy list: {proxy_list}")

    count = 0
    len_smtps = len(material)
    len_proxy = len(proxy_list)
    if len_proxy == 0:
        return False
    valid = []
    errors = []
    threads = []
    queue_ = queue.Queue()
    for i in material:
        proxy = random.choice(proxy_list)
        proxy = proxy[1] + ':' + proxy[2]
        imap = ImapConfig(i[1], i[2], i[3], i[4], timeout, timeout)
        threads.append(threading.Thread(target=connect_imap_to_check, args=(queue_, socket, imap, proxy)))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
        res = queue_.get()
        if res[0] != None:
            valid.append(res[1].email)
        else:
            errors.append(res[1].email)
        count += 1
        socket.send(f'progress_check_imaps:{len(valid)}:{len(errors)}:{int(count / len_smtps * 100)}')
    model.change_status(valid, 'imaps', 'checked')
    model.change_status(errors, 'imaps', 'dead')
    return True


def check_proxy(socket, session, proxy_id):
    material = model.get_material_to_check(proxy_id, 'proxies', session)
    len_proxy = len(material)
    if len_proxy == 0:
        return False

    count = 0
    valid = []
    errors = []
    threads = []
    queue_ = queue.Queue()
    for i in material:
        proxy = i[1] + ':' + i[2]
        threads.append(threading.Thread(target=test_proxy, args=(queue_, socket, proxy)))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
        res = queue_.get()
        if res[0]:
            valid.append(res[1].split(':')[0])
        else:
            errors.append(res[1].split(':')[0])
        count += 1
        socket.send(f'progress_check_proxy:{len(valid)}:{len(errors)}:{int(count / len_proxy * 100)}')
    model.change_status(valid, 'proxies', 'checked')
    model.change_status(errors, 'proxies', 'dead')
    return True


def check_domain(socket, session, domain_id):
    material = model.get_material_to_check(domain_id, 'domains', session)
    count = 0
    len_domain = len(material)
    valid = []
    errors = []
    threads = []
    queue_ = queue.Queue()
    for i in material:
        domain = i[1]
        threads.append(threading.Thread(target=test_domain, args=(queue_, socket, domain)))
    for i in threads:
        i.start()
    for i in threads:
        i.join()
        res = queue_.get()
        if res[0]:
            valid.append(res[1])
        else:
            errors.append(res[1])
        count += 1
        socket.send(f'progress_check_domain:{len(valid)}:{len(errors)}:{int(count / len_domain * 100)}')
    model.change_status(valid, 'domains', 'checked')
    model.change_status(errors, 'domains', 'dead')


c_test_mode_send_valid = 0
c_test_mode_send_error = 0


def test_mode(socket, session, sending_limit, threads_number, timeout, delay, emails_per_session, emails_to_validate,
              emails_per_material, smtp_form, proxy_form, imap_form, domain_form, template_form, to_check):
    return 1
    sent_emails_count = 0

    global c_test_mode_send_valid
    global c_test_mode_send_error

    if not try_int(sending_limit):
        sending_limit = 200
    else:
        sending_limit = try_int(sending_limit)
    if not try_int(threads_number):
        threads_number = 5
    else:
        threads_number = try_int(threads_number)
    if not try_float(timeout):
        timeout = 45
    else:
        timeout = try_float(timeout)
    if not try_float(delay):
        delay = 0.3
    else:
        delay = try_float(delay)
    if not try_int(emails_per_session):
        emails_per_session = 3
    else:
        emails_per_session = try_int(emails_per_session)
    if not try_int(emails_to_validate):
        emails_to_validate = 3
    else:
        emails_to_validate = try_int(emails_to_validate)
    if not try_int(emails_per_material):
        emails_per_material = 5
    else:
        emails_per_material = try_int(emails_per_material)

    template_list = model.get_material_to_mailing(template_form['id'], 'templates', session)
    proxy_list = model.get_material_to_mailing(proxy_form, 'proxies', session)
    smtp_list = model.get_material_to_mailing(smtp_form, 'smtps', session)
    imap = model.get_material_to_mailing(imap_form, 'imaps', session)[0]
    domain_list = model.get_material_to_mailing(domain_form, 'domains', session)

    smtps = []
    for i in smtp_list:
        smtps.append(SMTPConfig(i[1], i[2], i[3], i[4]))
    proxies = []
    for i in proxy_list:
        i = i[1] + ':' + i[2]
        proxies.append(i)
    imap = ImapConfig(imap[1], imap[2], imap[3], imap[4], timeout, timeout)
    old_control = "<!-- PSB %%PROXYID%% %%SMTPID%% %%BODYID%% PSB -->"
    templates = []
    for template in template_list:
        domain = random.choice(domain_list)
        link = domain[1]
        subject = template[4]
        froms = template[3]
        html = template[2]
        html = re.sub(r"</body>", f"{old_control}\n</body>", html)
        html = html.replace("%%RANDSTRING%%", get_rand_string(16)).replace("%%FROM%%", froms).replace("%%URL%%",
                                                                                                      link).replace(
            "%%SUBJECT%%", subject)
        templates.append({'template': html, 'from': froms, 'link': link, 'subject': subject})

    threads = []

    if to_check == 'proxy':
        c = 0
        for _ in range(int(emails_per_material)):
            for proxy in proxies:
                c += 1
                delay = delay * c
                template = random.choice(templates)
                data = {'smtp': random.choice(smtps), 'template': template['template'], 'link': template['link'],
                        "proxy": proxy, "base": base_form, 'template_name': dummy_form, 'subject': template['subject'],
                        'from': template['from']}
                threads.append(threading.Thread(target=send, args=(socket, data, delay)))

    elif to_check == 'smtp':
        c = 0
        for _ in range(int(emails_per_material)):
            for smtp in smtps:
                proxy = random.choice(proxies)
                c += 1
                delay = delay * c
                template = random.choice(templates)
                data = {'smtp': smtp, 'template': template['template'], 'link': template['link'], "proxy": proxy,
                        "base": base_form, 'template_name': dummy_form, 'subject': template['subject'],
                        'from': template['from']}
                threads.append(threading.Thread(target=send, args=(socket, data, delay)))

    elif to_check == 'templates':
        c = 0
        for _ in range(int(emails_per_material)):
            for template in templates:
                proxy = random.choice(proxies)
                smtp = random.choice(smtps)
                c += 1
                delay = delay * c
                data = {'smtp': smtp, 'template': template['template'], 'link': template['link'], "proxy": proxy,
                        "base": base_form, 'template_name': dummy_form, 'subject': template['subject'],
                        'from': template['from']}
                threads.append(threading.Thread(target=send, args=(socket, data, delay)))

    elif to_check == 'domains':
        c = 0
        for _ in range(int(emails_per_material)):
            for domain in domain_list:
                c += 1
                delay = delay * c
                template = random.choice(templates)
                data = {'smtp': random.choice(smtps), 'template': template['template'], 'link': domain[1],
                        "proxy": random.choice(proxies),
                        "base": base_form, 'template_name': dummy_form, 'subject': template['subject'],
                        'from': template['from']}
                threads.append(threading.Thread(target=send, args=(socket, data, delay)))

    c_test_mode_send_valid = 0
    c_test_mode_send_error = 0
    for t in threads:
        t.start()
        sent_emails_count += 1
        if sent_emails_count >= sending_limit:
            socket.send('pause_test_mode')
    while any(t.is_alive() for t in threads):
        socket.send(
            f'progress_test_mode_send:{c_test_mode_send_valid}:{c_test_mode_send_error}:{int(((c_test_mode_send_error + c_test_mode_send_valid) / len(threads)) * 100)}')
        sleep(1)

    socket.send(f'progress_test_mode_finish')

    mail = imaplib.IMAP4_SSL(imap.host)
    mail.login(imap.user, imap.password)
    mail.select("inbox")

    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()

    successful_sends = {'smtp': []}

    for email_id in reversed(email_ids):
        result, data = mail.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        from_email = msg['From']

        for smtp in smtps:
            if smtp.user in from_email:
                successful_sends['smtp'].append(smtp)
                mail.store(email_id, '+FLAGS', '\\Deleted')

        if to_check == 'domains':
            for domain in domain_list:
                if domain[1] in from_email:
                    successful_sends['domains'].append(domain[1])
                    mail.store(email_id, '+FLAGS', '\\Deleted')

    mail.expunge()
    mail.logout()

    for smtp in successful_sends['smtp']:
        if len(successful_sends['smtp']) >= emails_to_validate:
            model.update_material_status('smtp', smtp, 'INBOX', session)
        else:
            model.update_material_status('smtp', smtp, 'JUNK', session)

    if to_check == 'domains':
        domain_count = {domain: 0 for domain in domain_list}
        for success_domain in successful_sends['domains']:
            for domain in domain_list:
                domain_root = '.'.join(domain[1].split('.')[-2:])
                if success_domain.endswith(domain_root):
                    domain_count[domain] += 1

        for domain, count in domain_count.items():
            if count >= emails_to_validate:
                model.update_material_status('domains', domain[0], 'INBOX', session)
            else:
                model.update_material_status('domains', domain[0], 'JUNK', session)

    elif to_check == 'proxy':
        proxy_count = {proxy: 0 for proxy in proxies}
        for success_proxy in successful_sends['smtp']:
            for proxy in proxies:
                if success_proxy['proxy'] == proxy:
                    proxy_count[proxy] += 1

        for proxy, count in proxy_count.items():
            if count >= emails_to_validate:
                model.update_material_status('proxy', proxy, 'INBOX', session)
            else:
                model.update_material_status('proxy', proxy, 'JUNK', session)

    elif to_check == 'templates':
        template_count = {template['template']: 0 for template in templates}
        for success_template in successful_sends['smtp']:
            for template in templates:
                if success_template['template'] == template['template']:
                    template_count[template['template']] += 1

        for template, count in template_count.items():
            if count >= emails_to_validate:
                # Assuming template_id is used to identify templates in the database
                model.update_material_status('templates', template['template_id'], 'INBOX', session)
            else:
                model.update_material_status('templates', template['template_id'], 'JUNK', session)


def func_sendx(socket, session, sending_limit, threads_number, timeout, delay, emails_per_session, emails_to_validate,
               emails_per_material, smtp, proxy, bases, domain, template):
    sent_emails_count = 0

    global c_test_mode_send_valid
    global c_test_mode_send_error

    sending_limit = try_int(sending_limit) or 200
    threads_number = try_int(threads_number) or 5
    timeout = try_float(timeout) or 45
    delay = try_float(delay) or 0.3
    emails_per_session = try_int(emails_per_session) or 3
    emails_to_validate = try_int(emails_to_validate) or 3
    emails_per_material = try_int(emails_per_material) or 5

    template_list = model.get_material_to_mailing(template['id'], 'templates', session)
    proxy_list = model.get_material_to_mailing(proxy, 'proxies', session)
    smtp_list = model.get_material_to_mailing(smtp, 'smtps', session)
    domain_list = model.get_material_to_mailing(domain, 'domains', session)
    bases_list = model.get_material_to_mailing(bases, 'bases', session)

    smtps = [SMTPConfig(i[1], i[2], i[3], i[4]) for i in smtp_list]
    proxies = [f"{i[1]}:{i[2]}" for i in proxy_list]
    domains = domain_list

    templates = []
    for tmpl in template_list:
        chosen_domain = random.choice(domains)
        link = chosen_domain[1]
        subject = tmpl[4]
        froms = tmpl[3]
        html = tmpl[2]
        html = re.sub(r"</body>", f"<!-- PSB %%PROXYID%% %%SMTPID%% %%BODYID%% PSB -->\n</body>", html)
        html = html.replace("%%RANDSTRING%%", get_rand_string(16)).replace("%%FROM%%", froms).replace("%%URL%%",
                                                                                                      link).replace(
            "%%SUBJECT%%", subject)
        templates.append({'template': html, 'from': froms, 'link': link, 'subject': subject})

    threads = []
    c_test_mode_send_valid = 0
    c_test_mode_send_error = 0

    for base in bases_list:
        chosen_template = random.choice(templates)
        chosen_smtp = random.choice(smtps)
        chosen_proxy = random.choice(proxies)
        chosen_domain = random.choice(domains)

        t = threading.Thread(target=send,
                             args=(base, chosen_template, chosen_smtp, chosen_proxy, chosen_domain, timeout, delay))
        threads.append(t)

    for t in threads:
        t.start()
        sent_emails_count += 1
        if sent_emails_count >= sending_limit:
            socket.send('pause_test_mode')

    while any(t.is_alive() for t in threads):
        socket.send(
            f'progress_test_mode_send:{c_test_mode_send_valid}:{c_test_mode_send_error}:{int(((c_test_mode_send_error + c_test_mode_send_valid) / len(threads)) * 100)}')
        sleep(1)

    socket.send(f'progress_test_mode_finish')

    return sent_emails_count


def mailing_mode(socket, session, template, proxy, smtp, base, domain, threads, delay, sending_limit, emails_per_check,
                 count_of_material, timeout):
    sent_emails_count = 0

    global c_mailing_mode_send_valid
    global c_mailing_mode_send_error

    sending_limit = try_int(sending_limit) or 200
    threads = try_int(threads) or 5
    timeout = try_float(timeout) or 45
    delay = try_float(delay) or 0.3
    emails_per_check = try_int(emails_per_check) or 3
    count_of_material = try_int(count_of_material) or 3

    template_list = model.get_material_to_mailing(template, 'temp', session)
    proxy_list = model.get_material_to_mailing(proxy, 'proxies', session)
    smtp_list = model.get_material_to_mailing(smtp, 'smtps', session)
    domain_list = model.get_material_to_mailing(domain, 'domains', session)
    bases_list = model.get_material_to_mailing(base, 'bases', session)

    smtps = [SMTPConfig(i[1], i[2], i[3], i[4]) for i in smtp_list]
    proxies = [f"{i[1]}:{i[2]}" for i in proxy_list]
    domains = domain_list

    templates = []
    for tmpl in template_list:
        chosen_domain = random.choice(domains)
        link = chosen_domain[1]
        subject = tmpl[4]
        froms = tmpl[3]
        html = tmpl[2]
        html = re.sub(r"</body>", f"<!-- PSB %%PROXYID%% %%SMTPID%% %%BODYID%% PSB -->\n</body>", html)
        html = html.replace("%%RANDSTRING%%", get_rand_string(16)).replace("%%FROM%%", froms).replace("%%URL%%",
                                                                                                      link).replace(
            "%%SUBJECT%%", subject)
        templates.append({'template': html, 'from': froms, 'link': link, 'subject': subject})

    # threads = []
    c_mailing_mode_send_valid = 0
    c_mailing_mode_send_error = 0
    pause_event = threading.Event()

    def pause_handler():
        socket.on('pause_mailing_mode', lambda: pause_event.set())
        socket.on('resume_mailing_mode', lambda: pause_event.clear())

    threading.Thread(target=pause_handler).start()

    for base in bases_list:
        chosen_template = random.choice(templates)
        chosen_smtp = random.choice(smtps)
        chosen_proxy = random.choice(proxies)
        chosen_domain = random.choice(domains)

        t = threading.Thread(target=send, args=(
            base, socket, chosen_template, chosen_smtp, chosen_proxy, chosen_domain, timeout, delay))
        threads.append(t)

    for t in threads:
        t.start()
        if sent_emails_count >= sending_limit:
            socket.send('pause_mailing_mode')

    while any(t.is_alive() for t in threads):
        socket.send(
            f'progress_mailing_mode_send:{c_mailing_mode_send_valid}:{c_mailing_mode_send_error}:{int(((c_mailing_mode_send_error + c_mailing_mode_send_valid) / len(threads)) * 100)}')
        sleep(1)

    socket.send(f'progress_mailing_mode_finish')

    return sent_emails_count

