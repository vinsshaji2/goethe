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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'wilsondona08@gmail.com', 'password': 'mkxe kjpl awge fzla', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annamariyathomson07@gmail.com', 'password': 'rvlo aqav nrzv wahd', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'renjudanasree@gmail.com', 'password': 'zzsn urnd bbqe eegb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'psvarna313@gmail.com', 'password': 'aisi jwnl fycy rcux', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'fathimanazrinks2007@gmail.com', 'password': 'tndg ywpj wrbd xfui', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'angel07stephen@gmail.com', 'password': 'fome hjbu xphl dwmn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'alshifaazeez786@gmail.com', 'password': 'jjti kzrl oafo bvbe', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'heltythomas80@gmail.com', 'password': 'ozsg yrjp cpnz aebz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'remyabalag@gmail.com', 'password': 'qydx ejoo mors zixg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleenaelizabethbabu261@gmail.com', 'password': 'fpce izjn ayjv bbsk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'eshahanzil@gmail.com', 'password': 'quwr iofb rnuo hcwy', 'to': to, 'subject': Subject},

]

data_list = [
    ('Dona wilson', 'Idukki', '9072482657', 'Sprechen', 'wilsondona08@gmail.com'),
    ('Anna Mariya Thomson', 'Ernakulam', '8589977772', 'Sprechen', 'annamariyathomson07@gmail.com'),
    ('Renju Jayachandren', 'Pathanamthitta', '8078419052', 'Sprechen', 'renjudanasree@gmail.com'),
    ('Varna Puthenveed Sudheer', 'Alappuzha', '8089363213', 'Sprechen', 'psvarna313@gmail.com'),
    ('Fathima Nazrin Kizhakkambilly siyad', 'Ernakulam', '8921901745', 'Schreiben, Sprechen', 'fathimanazrinks2007@gmail.com'),
    ('Angel Stephen', 'Idukki', '9747606744', 'Lesen,Hören,Schreiben,Sprechen', 'angel07stephen@gmail.com'),
    ('Alshifa Azeez', 'Palakkad', '6282867177', 'Lesen, Sprechen', 'alshifaazeez786@gmail.com'),
    ('Hetly Thomas', 'Idukki', '9745920001', 'Schreiben', 'heltythomas80@gmail.com'),
    ('Remya Ramachandran Nair', 'Kottayam', '8547895155', 'Schreiben', 'remyabalag@gmail.com'),
    ('Aleena Elizabeth Babu', 'Kottayam', '7034689320', 'Lesen', 'aleenaelizabethbabu261@gmail.com'),
    ('Esha Hansil', 'Idukki', '8921570539', 'Lesen', 'eshahanzil@gmail.com'),

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
    schedule_time = "23:26:20"
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