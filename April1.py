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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annmariasiju121@gmail.com', 'password': 'lrha pcwb vsmt kktn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'poppychippy20@gmail.com', 'password': 'hmxv svdu vano ifrd', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sruthisruthizz012@gmail.com', 'password': 'brse odpy wqjx xhar', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'athirarenjith3459@gmail.com', 'password': 'eapi fmst khzq yhev', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'saniyathomas6282@gmail.com', 'password': 'xcej rsuh nwxe caod', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ebinmathew318@gmail.com', 'password': 'ckui rddi rdem fcwz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleenatherese2002@gmail.com', 'password': 'wsui gnva pfga giuk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'dvndu3@gmail.com', 'password': 'wkbt ztps kisa twtm', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'd9884304@gmail.com', 'password': 'lvjw qzdk xgac jqoe', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleetj95@gmail.com', 'password': 'tpkr rsuc bdpj napp', 'to': to, 'subject': Subject},

]

data_list = [
    ('Ann Mariya Siju', 'Idukki', '8075645378', 'Sprechen', 'annmariasiju121@gmail.com'),
    ('Gowri Krishna', 'Alappuzha', '7736995021', 'Sprechen', 'poppychippy20@gmail.com'),
    ('Sruthykrishna Shaji', 'Kottayam', '7736738342', 'Sprechen', 'sruthisruthizz012@gmail.com'),
    ('Athira Renjith', 'Trivandrum', '7591903459', 'Sprechen', 'athirarenjith3459@gmail.com'),
    ('Saniya Thomas', 'Kollam', '6282553475', 'Schreiben, Sprechen', 'saniyathomas6282@gmail.com'),
    ('Ebin Mathew', 'Kannur', '9961030442', 'Schreiben, Sprechen', 'ebinmathew318@gmail.com'),
    ('Aleena Therese Mathew', 'Kottayam', '9446041251', 'Lesen,Hören,Schreiben,Sprechen', 'aleenatherese2002@gmail.com'),
    ('Deveendu Poothamveettil Thambi', 'Thrissur', '6238166159', 'Lesen,Schreiben', 'dvndu3@gmail.com'),
    ('Dona Doly Johnson', 'Kollam', '9037663274', 'Schreiben', 'd9884304@gmail.com'),
    ('Aleena Thengarackal Joseph', 'Idukki', '94002 98121', 'Schreiben', 'aleetj95@gmail.com'),

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
    schedule_time = "23:02:00"
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