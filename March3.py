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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'thrishagireesh30@gmail.com', 'password': 'oefq kchp vyon stzu','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rosemolfrancis105@gmail.com', 'password': 'fpwp bpcv qohc fzwq','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'amruthamariyabiju@gmail.com', 'password': 'pdwe whie lcji fiit','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'stephenashly2@gmail.com', 'password': 'ridv skft mrmy jyak','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'joyaleena45@gmail.com', 'password': 'qmis uvsn xpjb zhrk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jenifersebastian0@gmail.com', 'password': 'huhx abwh ksrl hdep', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'daniyabenny209@gmail.com', 'password': 'fgho xhos wsxe fnyk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annmariasiju121@gmail.com', 'password': 'ouiq xsij gypq eivp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jwalareji2@gmail.com', 'password': 'jqea vdpd ycua wgnb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'alfiyarasheed146@gmail.com', 'password': 'xbhq wkbg ntrl xppo', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bijichacko722018@gmail.com', 'password': 'hkym jbyg hrtx ucnm', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'hareeshprasad34679@gmail.com', 'password': 'gdfu kjtx lkrs gkte', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'mnair0925@gmail.com', 'password': 'zwhw dktl ookb efkq', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sonasabu931@gmail.com', 'password': 'forz wyjo ssuz vjae', 'to': to, 'subject': Subject},
]

# Example dynamic data
data_list = [
    ('Thrisha Gireesh', 'Palakkad', '8848295123', 'Sprechen', 'thrishagireesh30@gmail.com'),
    ('Rosemol Francis', 'Thrissur', '9074121986', 'Sprechen', 'rosemolfrancis105@gmail.com'),
    ('Amrutha Mariya Biju', 'Kottayam', '7306435732', 'Sprechen', 'amruthamariyabiju@gmail.com'),
    ('Ashly Stephen', 'Idukki', '6235727198', 'Sprechen', 'stephenashly2@gmail.com'),
    ('Aleena Joy', 'Ernakulam', '9961411672', 'Schreiben, Sprechen', 'joyaleena45@gmail.com'),
    ('Jenifer Sebastian', 'Alappuzha', '8594026311', 'Schreiben, Sprechen', 'jenifersebastian0@gmail.com'),
    ('Daniya Benny', 'Kannur', '6282068332', 'Schreiben, Sprechen', 'daniyabenny209@gmail.com'),
    ('Ann Mariya Siju', 'Idukki', '8075645378', 'Lesen,Hören,Schreiben,Sprechen', 'annmariasiju121@gmail.com'),
    ('Jwala Reji', 'Ernakulam', '9048497581', 'Hören,Schreiben', 'jwalareji2@gmail.com'),
    ('Alfiya Rasheed', 'Kottayam', '9037972916', 'Schreiben', 'alfiyarasheed146@gmail.com'),
    ('Biji Chacko Kunnethara', 'Pathanamthitta', '7510902772', 'Schreiben', 'bijichacko722018@gmail.com'),
    ('Hareesh Prasad', 'Idukki', '8330026707', 'Lesen, Hören', 'hareeshprasad34679@gmail.com'),
    ('Meera Nair', 'Kottayam', '7306942542', 'Lesen, Hören', 'mnair0925@gmail.com'),
    ('Sona Sabu', 'Alappuhza', '9495746382', 'Lesen, Hören', 'sonasabu931@gmail.com'),
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