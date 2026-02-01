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
# Subject = "MARCH 2026 B2 EXAM REGISTRATION-GOETHE-ZENTRUM"

email_accounts = [
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anandhuayyappan62@gmail.com', 'password': 'amys rvtq jttj bdaf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'staniyathomas43@gmail.com',
     'password': 'uoie nqqf ubmq dlwg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'shanijoseph5197@gmail.com',
     'password': 'crwq sbfx lxal cyyp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nidhishasudhesh@gmail.com',
     'password': 'xpog epqw kbrl rsgd', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sumithomas956@gmail.com', 'password': 'dbcc zmay ruho bqtd',
     'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'mariyamable006@gmail.com',
     'password': 'orxg klzy foik umcg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleenaelizabethbabu261@gmail.com',
     'password': 'fyyy czbs hggx jwng', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'kasinaths467@gmail.com', 'password': 'vksq pdre tuht glkp',
     'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'josephmereena20@gmail.com',
     'password': 'xdou wxsw aufj encl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'krishnabindhunegil@gmail.com',
     'password': 'uxfk xgim hovn pclq', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'samueljohnson7592@gmail.com',
     'password': 'iuqm onhv eihy movs', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleenajacob492@gmail.com',
     'password': 'ivil cxbb ybue emst', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'lintamariyaantony123@gmail.com',
     'password': 'oubk zcqr oehr aplk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'clintthomasde@gmail.com', 'password': 'ndwt khpq hwgh muol',
     'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleeshaelzamathew@gmail.com',
     'password': 'glqq esvb cvan zmgq', 'to': to, 'subject': Subject},

]

data_list = [
    ('Anandhu Ayyappan', 'Ernakulam', '6282692768', 'Sprechen', 'anandhuayyappan62@gmail.com'),
    ('Staniya Thomas', 'Idukki', '8547503947', 'Sprechen', 'staniyathomas43@gmail.com'),
    ('Shani Joseph', 'Trivandrum', '7909103191', 'Sprechen', 'shanijoseph5197@gmail.com'),
    ('Nidhisha Sudhesh', 'Thrissur', '8129665658', 'Sprechen', 'nidhishasudhesh@gmail.com'),
    ('Sumi Thomas', 'Kottayam', '9072787693', 'Schreiben, Sprechen', 'sumithomas956@gmail.com'),
    ('Mariya Mable', 'Ernakulam', '6238858167', 'Schreiben, Sprechen', 'mariyamable006@gmail.com'),
    ('Aleena Elizabeth Babu', 'Kottayam', '7034689320', 'Schreiben, Sprechen', 'aleenaelizabethbabu261@gmail.com'),
    ('Kasinath Sreekumar', 'Kottayam', '8606855122', 'Schreiben, Sprechen', 'kasinaths467@gmail.com'),
    ('Mereena Joseph', 'Ernakulam', '7558919926', 'Lesen,Hören,Schreiben,Sprechen', 'josephmereena20@gmail.com'),
    ('Krishna Bindhu Negil', 'Kollam', '8590408807', 'Lesen, Sprechen', 'krishnabindhunegil@gmail.com'),
    ('Samuel Johnson', 'Kollam', '7592075219', 'Schreiben', 'samueljohnson7592@gmail.com'),
    ('Aleena Jacob', 'Ernakulam', '7025421591', 'Lesen, Hören', 'aleenajacob492@gmail.com'),
    ('Linta Mariya Antony', 'Idukki', '8590572656', 'Lesen, Hören', 'lintamariyaantony123@gmail.com'),
    ('Clint Thomas', 'Idukki', '9061536086', 'Lesen, Hören', 'clintthomasde@gmail.com'),
    ('Aleesha Mathew', 'Idukki', '8590507542', 'Schreiben', 'aleeshaelzamathew@gmail.com')
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
    schedule_time = "23:17:10"
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