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
# Subject = "JUNE 2026 B2 EXAM REGISTRATION-GOETHE-ZENTRUM"

email_accounts = [
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'alanjosephputhoor369@gmail.com', 'password': 'yfcr ohig cmxu dsgj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'zardra958@gmail.com', 'password': 'klje pjya wrtp vrlm', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'stephenashly2@gmail.com', 'password': 'sqoa reld bsfc uepa', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'kvv77720@gmail.com', 'password': 'zgfk rela gwkt xsok', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sanilsanusha105@gmail.com', 'password': 'tyux bcjk wcbc gfsv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleenajacob492@gmail.com', 'password': 'lmve sufn ejto oicn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annamolthomas2255@gmail.com', 'password': 'hjso injo oilg thdo', 'to': to, 'subject': Subject},
]

data_list = [
    ('Alan Joseph', 'Idukki', '8139803837', 'Sprechen', 'alanjosephputhoor369@gmail.com'),
    ('Ardra Meenakumary Suseelan Pillai', 'Kollam', '9995224065', 'Sprechen', 'zardra958@gmail.com'),
    ('Ashly Stephen', 'Idukki', '6235727198', 'Sprechen', 'stephenashly2@gmail.com'),
    ('Vishnu Vijayan', 'Ernakulam', '8848992156', 'Schreiben, Sprechen', 'kvv77720@gmail.com'),
    ('Sanusha Sanil', 'Pathanamthitta', '8089057148', 'Hören, Schreiben', 'sanilsanusha105@gmail.com'),
    ('Aleena Jacob', 'Ernakulam', '7025421591', 'Schreiben', 'aleenajacob492@gmail.com'),
    ('ANNAMOL AT', 'Alappuzha', '9645747862', 'Lesen', 'annamolthomas2255@gmail.com'),
]


def generate_email_body(full_name, current_district, contact_number, exam_modules, email_id):
    return f"""
    <html>
    <body>
        <table border=1 style="border-collapse: collapse; width: 100%;">
            <tr>
                <th>Full Name</th>
                <th>Current Residing Address</th>
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
    schedule_time = "22:18:10"
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