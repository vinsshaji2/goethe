import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Email account details
to = 'exams.deutschzeit@gmail.com'
Subject = "Testmail"
# to = 'EXAMS.REGISTRATION@GOETHE-ZENTRUM.ORG'
# Subject = "APRIL 2026 B2 EXAM REGISTRATION-GOETHE-ZENTRUM"

email_accounts = [
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'renjudanasree@gmail.com', 'password': 'eifl qifz xhrb mypu', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bijudiya47@gmail.com', 'password': 'pcln ykxa vovk lqho', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annmariasiju121@gmail.com', 'password': 'ledd rrri xwqr zycc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'kasinaths467@gmail.com', 'password': 'iumu yvcr wdfn lzxy', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'adithyankuttu07@gmail.com', 'password': 'iume zlnh nisb fsoz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'milanjosephgoethe@gmail.com', 'password': 'sgbb dhvv cqxo fzoa', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'leyashyjan006@gmail.com', 'password': 'kgci nvga tgzo ztik', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ciyonadonyciyona@gmail.com', 'password': 'tklk sffv dbtk poja', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nehabiju008@gmail.com', 'password': 'lawr mdtr jmwm nqyf', 'to': to, 'subject': Subject},


]

data_list = [
    ('Renju Jayachandren', 'Pathanamthitta', '8078419052', 'Sprechen', 'renjudanasree@gmail.com'),
    ('Diya Biju', 'Kottayam', '9778206044', 'Sprechen', 'bijudiya47@gmail.com'),
    ('Annmariya Siju', 'Idukki', '8075645378', 'Sprechen', 'annmariasiju121@gmail.com'),
    ('Kasinath Sreekumar', 'Kottayam', '8606855122', 'Schreiben, Sprechen', 'kasinaths467@gmail.com'),
    ('Adhithyan Sudheesh', 'Ernakulam', '9544278198', 'Schreiben, Sprechen', 'adithyankuttu07@gmail.com'),
    ('Milan Joseph', 'Idukki', '9447657113', 'Schreiben, Sprechen', 'milanjosephgoethe@gmail.com'),
    ('Leya Shyjan', 'Ernakulam', '9961591048', 'Lesen, Hören, Schreiben, Sprechen', 'leyashyjan006@gmail.com'),
    ('Ciyona Dony', 'Idukki', '7012635510', 'Hören, Sprechen', 'ciyonadonyciyona@gmail.com'),
    ('Neha Biju', 'Wayanad', '9605746139', 'Lesen, Hören', 'nehabiju008@gmail.com'),
]


def generate_email_body(full_name, current_district, contact_number, exam_modules, email_id):
    return f"""
    <html>
    <body>
        <table border=1 style="border-collapse: collapse; width: 100%;">
            <tr>
                <th>Full Name</th>
                <th>Current Residing District</th>
                <th>Personal Contact Number</th>
                <th>Exam Modules</th>
                <th>Registered E-mail ID used in our Website</th>
            </tr>
            <tr>
                <td>{full_name}</td>
                <td>{current_district}</td>
                <td>{contact_number}</td>
                <td>{exam_modules}</td>
                <td>{email_id}</td>
            </tr>
        </table>
    </body>
    </html>
    """


def send_email(account, full_name, current_district, contact_number, exam_modules, email_id):
    msg = MIMEMultipart()
    msg['From'] = account['username']
    msg['To'] = account['to']
    msg['Subject'] = account['subject']

    body = generate_email_body(full_name, current_district, contact_number, exam_modules, email_id)
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(account['smtp_server'], account['port'])
        server.starttls()
        server.login(account['username'], account['password'])
        server.sendmail(account['username'], account['to'], msg.as_string())
        server.quit()
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"✅ [{timestamp}] Email sent from {account['username']} to {account['to']}")
        return True
    except Exception as e:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"❌ [{timestamp}] Failed from {account['username']}: {e}")
        return False


def send_all_emails():
    """Send all emails in parallel - MAXIMUM SPEED"""
    start_time = time.time()
    results = []

    # Use max_workers equal to number of emails for true parallelism
    with ThreadPoolExecutor(max_workers=len(email_accounts)) as executor:
        # Submit ALL tasks at once (no waiting)
        futures = [
            executor.submit(send_email, account, *data)
            for account, data in zip(email_accounts, data_list)
        ]

        # Collect results as they complete
        for future in as_completed(futures):
            results.append(future.result())

    elapsed = time.time() - start_time
    print(f"\n⚡ All {len(results)} emails sent in {elapsed:.2f} seconds")
    print(f"📊 Success rate: {sum(results)}/{len(results)}")
    return all(results)


if __name__ == "__main__":
    schedule_time = "20:26:10"
    print(f"⏰ Scheduled to send emails at {schedule_time} to:- {to} and Subject:- {Subject}\n")

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == schedule_time:
            print(f"🚀 Starting parallel email blast at {current_time}...\n")
            success = send_all_emails()

            if not success:
                print("\n⚠️ Some emails failed. Retrying in 10 seconds...")
                time.sleep(10)
                # send_all_emails()

            # Wait 61 seconds to avoid sending multiple times in same minute
            time.sleep(61)

        time.sleep(0.5)