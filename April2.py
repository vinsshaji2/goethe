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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'staniyathomas43@gmail.com', 'password': 'meyq vkjc wjwv mdjc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjusandyave@gmail.com', 'password': 'oals vyvj cevo hyyo', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjuanjanabiju16@gmail.com', 'password': 'hbwh qvhc qffm mwdh', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'vaaswin735@gmail.com', 'password': 'jpjo dqtb ecoi nihj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ashnasuresh13122006@gmail.com', 'password': 'bmlw ofdn mheq dgpu', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anums742003@gmail.com', 'password': 'ehsc zwph bkwx nqfw', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'johnaagi3@gmail.com', 'password': 'zlvm vsde qlnk goxk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bijudiya47@gmail.com', 'password': 'rbvp mfjq iygc mwjn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'beenamathew680@gmail.com', 'password': 'uepi jwxt tbhz qtoa', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'leoarmy504@gmail.com', 'password': 'hkpx fgbw flvg soif', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'athulyareji03@gmail.com', 'password': 'paul uexr dzjw vvje', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'saniyasabu9544@gmail.com', 'password': 'mnyp aadb szsk jlyp', 'to': to, 'subject': Subject},
]

data_list = [
    ('Staniya Thomas', 'Idukki', '8547503947', 'Sprechen', 'staniyathomas43@gmail.com'),
    ('Anju Kunnummal Sandyav', 'Ernakulam', '8589958119', 'Sprechen', 'anjusandyave@gmail.com'),
    ('Anjana Biju', 'Alappuzha', '8589073201', 'Sprechen', 'anjuanjanabiju16@gmail.com'),
    ('Aswin Vattakuzhiyil Anil', 'Ernakulam', '9074146309', 'Schreiben, Sprechen', 'vaaswin735@gmail.com'),
    ('Ashna Suresh', 'Ernakulam', '6235428751', 'Schreiben, Sprechen', 'ashnasuresh13122006@gmail.com'),
    ('Anu Muthedathu Sali', 'Ernakulam', '6282829972', 'Lesen,Hören,Schreiben,Sprechen', 'anums742003@gmail.com'),
    ('Aagi John', 'Idukki', '9188348965', 'Schreiben', 'johnaagi3@gmail.com'),
    ('Diya Biju', 'Kottayam', '9778206044', 'Schreiben', 'bijudiya47@gmail.com'),
    ('Beena Mathew', 'Pathanamthitta', '9142378926', 'Lesen', 'beenamathew680@gmail.com'),
    ('Kripa Johnbosco', 'Alappuzha', '7012580670', 'Schreiben', 'leoarmy504@gmail.com'),
    ('Athulya Reji', 'Idukki', '7012704991', 'Lesen, Hören, Schreiben, Sprechen', 'athulyareji03@gmail.com'),
    ('Saniya Sabu', 'Kottayam', '9995765408', 'Schreiben', 'saniyasabu9544@gmail.com')
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
    schedule_time = "23:25:10"
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