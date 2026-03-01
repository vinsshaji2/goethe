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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aswathypa287@gmail.com', 'password': 'gfwv gwrg qywa wnrv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'paruzzz1230@gmail.com', 'password': 'xwds vubd fybx hrpe', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'vyshnavimadhu90@gmail.com', 'password': 'hgsp bwoz byxx ljzc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sunithasreelekshmi550@gmail.com', 'password': 'sfea qsgd fyps myxh', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bhagya1142007@gmail.com', 'password': 'wngq rcvi hqmy uopl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'alfiyans385@gmail.com', 'password': 'ejfa zsee qqyk xdor', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sandrasajeevan547@gmail.com', 'password': 'hpqr idvz yxer lonn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'niranjanbose36@gmail.com', 'password': 'faox ekkz ausf xjie', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ameen122605@gmail.com', 'password': 'yjmw wovj tmpa kkcb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'samithaparasad1992@gmail.com', 'password': 'ielk ulym fgip btiy', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aswathimp003@gmail.com', 'password': 'ccly vjzx mgyp ynnb', 'to': to, 'subject': Subject},

]

data_list = [
    ('Aswathy  Puthenveedu Anilkumar', 'Malappuram', '6238402207', 'Sprechen', 'aswathypa287@gmail.com'),
    ('Ettiyedath Madathil Ajikumar Gowrinanda', 'Ernakulam', '9847715466', 'Sprechen', 'paruzzz1230@gmail.com'),
    ('Vyshnavi Madhu', 'Kottayam', '7994120926', 'Sprechen', 'vyshnavimadhu90@gmail.com'),
    ('Sreelekshmi Sunitha', 'Kollam', '9746871109', 'Sprechen', 'sunithasreelekshmi550@gmail.com'),
    ('Bhagyalakshmi Babu', 'Kottayam', '9400420150', 'Schreiben, Sprechen', 'bhagya1142007@gmail.com'),
    ('Alfiya Noushad Sabeena', 'Kollam', '7902824969', 'Schreiben, Sprechen', 'alfiyans385@gmail.com'),
    ('Sandra Sajeevan', 'Ernakulam', '8281013292', 'Lesen,Hören,Schreiben,Sprechen', 'sandrasajeevan547@gmail.com'),
    ('Niranjan Bose', 'Thrissur', '6235131489', 'Schreiben', 'niranjanbose36@gmail.com'),
    ('Al Ameen Nissarudeen', 'Kollam', '9526948087', 'Schreiben', 'ameen122605@gmail.com'),
    ('Samitha Vazhekattil Saji', 'Thrissur', '6235551984', 'Lesen, Hören ', 'samithaparasad1992@gmail.com'),
    ('Aswathi Manoj', 'Idukki', '7559924532', 'Lesen', 'aswathimp003@gmail.com'),


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
    schedule_time = "23:09:00"
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