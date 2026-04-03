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
# Subject = "MAY 2026 B2 EXAM REGISTRATION-GOETHE-ZENTRUM"

email_accounts = [
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'noblebaisy12@gmail.com', 'password': 'jpke qtup peyz moyr', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ashnasuresh13122006@gmail.com', 'password': 'kzkr kzkz xtgw moht', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjusandyave@gmail.com', 'password': 'zsyj bhlj nhdh dqqq', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'saniyaalice25@gmail.com', 'password': 'jguh ggse lyiz zvxa', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjuksks8@gmail.com', 'password': 'zkyq zmvh wnnz mbht', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sreyathekkethottyil123@gmail.com', 'password': 'mlas axpd xkki zzcf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bsblessy777@gmail.com', 'password': 'lcil grrv vzeq mdqx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'priyasunimon@gmail.com', 'password': 'fzxa mpzg dkra teud', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'athirarenjith3459@gmail.com', 'password': 'lopu mbms xfof ymtr', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'abhiramiviswanathan91@gmail.com', 'password': 'uxkq hcaj nsur iruf', 'to': to, 'subject': Subject},

]

data_list = [
    ('Noble Kalambal Baisy Joseph', 'Thrissur', '8714509388', 'Sprechen', 'noblebaisy12@gmail.com'),
    ('Ashna Suresh', 'Ernakulam', '6235428751', 'Sprechen', 'ashnasuresh13122006@gmail.com'),
    ('Anju Kunnummal Sandyav', 'Ernakulam', '8589958119', 'Sprechen', 'anjusandyave@gmail.com'),
    ('Saniya Sandeep', 'Kottayam', '9061834409', 'Schreiben, Sprechen', 'saniyaalice25@gmail.com'),
    ('Anju Kompenkeril Satheesh', 'Pathanamthitta', '8590815717', 'Schreiben, Sprechen', 'anjuksks8@gmail.com'),
    ('Sreya Elizabeth Sunil', 'Kottayam', '9778114621', 'Schreiben, Sprechen', 'sreyathekkethottyil123@gmail.com'),
    ('Blessy Bernit Sheeba', 'Thiruvananthapuram', '9037220119', 'Lesen, Hören, Schreiben, Sprechen', 'bsblessy777@gmail.com'),
    ('Abhirami Veliyath Sunimon', 'Kottayam', '8714016332', 'Lesen, Schreiben', 'priyasunimon@gmail.com'),
    ('Athira Renjith', 'Thiruvananthapuram', '7591903459', 'Schreiben', 'athirarenjith3459@gmail.com'),
    ('Abhirami Viswanathan', 'Ernakulam', '8075704425', 'Lesen, Hören', 'abhiramiviswanathan91@gmail.com'),


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
    schedule_time = "20:19:30"
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