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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'xaviersaniya5@gmail.com', 'password': 'pryc bwqv uwyz iled','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anupaulose8136@gmail.com', 'password': 'ttqm abqq prgs lbnu','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sreelekshmishinoj6@gmail.com', 'password': 'vvki vdvq cryk zuxu','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'alfredbijuvarghese2000@gmail.com', 'password': 'pqsz ghyr pybi pwgj','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjukoodappattu1808@gmail.com', 'password': 'phkm eqfm onbg roew', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'reebajoseph116@gmail.com', 'password': 'mrcn ympi wmwa qjzw', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bibinlukose62@gmail.com', 'password': 'haqd sjxl ojdp cyrr', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'noblebaisy12@gmail.com', 'password': 'gfjw revw lmty llxp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'shamsualmas61@gmail.com', 'password': 'idfp phff gfcw khxz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annamolthomas2255@gmail.com', 'password': 'sebl lvvh isvu tmon', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'leoarmy504@gmail.com', 'password': 'ymco kulc cesp jyyl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'smrithilatr72@gmail.com', 'password': 'bmdp bjfh lzoi xfpz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'angelmariyathankachan2006@gmail.com', 'password': 'vhzn zurm htfn jlxy', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bisminsafriya@gmail.com', 'password': 'eqdj exkb sdpl zdfu', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'amalkrishnaamal4050k@gmail.com', 'password': 'mufv cyiv rkwl bifl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ashaantony650@gmail.com', 'password': 'xlcx bvbv umlo hviw', 'to': to, 'subject': Subject},
]

# Example dynamic data
data_list = [
    ('Saniya Xavier Xavier Alphonsa', 'Thiruvananthapuram', '8848478137', 'Sprechen', 'xaviersaniya5@gmail.com'),
    ('Anu Paulose', 'Idukki', '8590351083', 'Sprechen', 'anupaulose8136@gmail.com'),
    ('Sreelekshmi Shinoj', 'Alappuzha', '6282088274', 'Sprechen', 'sreelekshmishinoj6@gmail.com'),
    ('Alfred Biju Varghese', 'Kasaragod', '9497106119', 'Sprechen', 'alfredbijuvarghese2000@gmail.com'),
    ('Anju Joseph', 'Kottayam', '9400387349', 'Schreiben, Sprechen', 'anjukoodappattu1808@gmail.com'),
    ('Reeba Joseph', 'Kottayam', '9633872267', 'Schreiben, Sprechen', 'reebajoseph116@gmail.com'),
    ('Bibin Lukose', 'Kottayam', '8281954694', 'Schreiben, Sprechen', 'bibinlukose62@gmail.com'),
    ('Noble Kalambal baisy Joseph', 'Thrissur', '8714509388', 'Lesen, Schreiben, Sprechen', 'noblebaisy12@gmail.com'),
    ('Almas Kalathil Muhammedrafeek', 'Thrissur', '9605282924', 'Lesen,Hören,Schreiben', 'shamsualmas61@gmail.com'),
    ('Annamol AT', 'Alappuzha', '9645747862', 'Schreiben', 'annamolthomas2255@gmail.com'),
    ('Kripa Johnbosco', 'Alappuzha', '7012580670', 'Lesen', 'leoarmy504@gmail.com'),
    ('SMRITHILA T.R', 'Ernakulam', '6282449072', 'Lesen', 'smrithilatr72@gmail.com'),
    ('Angel Mariya Thankachan', 'Idukki', '6235461702', 'Sprechen', 'angelmariyathankachan2006@gmail.com'),
    ('Bismin Safriya', 'Ernakulam', '88482 81770', 'Schreiben', 'bisminsafriya@gmail.com'),
    ('Amal Krishna Kalathiparambil Unni Krishnan', 'Thrissur', '7510748139', 'Sprechen', 'amalkrishnaamal4050k@gmail.com'),
    ('Asha Antony', 'Ernakulam', '9349912428', 'sprechen', 'ashaantony650@gmail.com')
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