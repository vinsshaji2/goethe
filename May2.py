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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'vaaswin735@gmail.com', 'password': 'uvjb xfea hist oicg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bijichacko722018@gmail.com', 'password': 'ydll htcn vlpj asia', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'Karolinajijo9c@gmail.com', 'password': 'pzkv rdug colw mvrk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'niru59765@gmail.com', 'password': 'svaq ijmf fugn ejoc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ayswaryathomas23@gmail.com', 'password': 'hkwf vowh qtwg mbzx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'linimathai2010@gmail.com', 'password': 'qbze euwb fqcz thgl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'shruthyvmartin@gmail.com', 'password': 'gqhy gjhp phnj csyy', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'xaviersaniya5@gmail.com', 'password': 'dvzc nmlu etmc nase', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anandhuayyappan62@gmail.com', 'password': 'soto eckl iiod ndfs', 'to': to, 'subject': Subject},

]

data_list = [
    ('Aswin vattakuzhiyil anil', 'Ernakulam', '9074802303', 'Sprechen', 'vaaswin735@gmail.com'),
    ('Biji Chacko Kunnethara', 'Pathanamthitta', '7510902772', 'Sprechen', 'bijichacko722018@gmail.com'),
    ('Karolina Jijo', 'Ernakulam', '8943690446', 'Sprechen', 'Karolinajijo9c@gmail.com'),
    ('Niranjana Thambilot', 'Kannur', '9744267857', 'Schreiben, Sprechen', 'niru59765@gmail.com'),
    ('Ayswarya Thomas', 'Kozhikode', '9526872741', 'Schreiben, Sprechen', 'ayswaryathomas23@gmail.com'),
    ('Lini Mathai', 'Pathanamthitta', '7025755231', 'Schreiben, Sprechen', 'linimathai2010@gmail.com'),
    ('Shruthy Veluthamannumkal Martin', 'Alappuzha', '9605175576', 'Lesen, Hören, Schreiben, Sprechen', 'shruthyvmartin@gmail.com'),
    ('Saniya Xavier Xavier Alphonsa', 'Thiruvananthapuram', '8848478137', 'Hören,Schreiben', 'xaviersaniya5@gmail.com'),
    ('Anandhu Ayyappan', 'Ernakulam', '6282692768', 'Schreiben', 'anandhuayyappan62@gmail.com'),


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
    schedule_time = "20:22:10"
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