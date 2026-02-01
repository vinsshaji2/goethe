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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'vaikendhukv@gmail.com', 'password': 'qhcx timv mcco cmuo','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'merinageorgemerinageorge@gmail.com', 'password': 'lukx mjjc sdls nlor','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jincyjohn031@gmail.com', 'password': 'hutd slhr jxmj rzfz','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'mariaphilip422@gmail.com', 'password': 'iggd luae ghcm vgty','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'delmychacko2002@gmail.com', 'password': 'qypf jldh keax wvil', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jolsnachacko2@gmail.com', 'password': 'ckqq lbhr cpdk zzae', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aryabenny987@gmail.com', 'password': 'wfax aaxb bvgs oxjh', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'marysania2004@gmail.com', 'password': 'otmf zddw swvo limc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'tomrijo2@gmail.com', 'password': 'ibtt spdd hufh bjit', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'diyam4677@gmail.com', 'password': 'uxvz uvva eypt zjif', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'eshahanzil@gmail.com', 'password': 'jqgg qqor ifax yphm', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bleswinjosephde@gmail.com', 'password': 'chvd essu ctfr sxnp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjithar81@gmail.com', 'password': 'aulc hnvd lffo rpzf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'avaneethgoethe@gmail.com', 'password': 'hvgo hbxn qxxp rhvk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'yathinpradeep42@gmail.com', 'password': 'htsd oyvg mfnq jioz', 'to': to, 'subject': Subject},
]

# Example dynamic data
data_list = [
    ('Vaikendhu Krishnakripa Vinodkumar', 'Wayanad', '8590961804', 'Sprechen', 'vaikendhukv@gmail.com'),
    ('Merina George', 'Idukki', '7907548034', 'Sprechen', 'merinageorgemerinageorge@gmail.com'),
    ('Jincy John', 'Kollam', '9633045575', 'Sprechen', 'jincyjohn031@gmail.com'),
    ('Maria Philip', 'Idukki', '9947039207', 'Sprechen', 'mariaphilip422@gmail.com'),
    ('Delmy Chacko', 'Idukki', '9061073645', 'Sprechen', 'delmychacko2002@gmail.com'),
    ('Jolsna Chacko', 'Ernakulam', '9656557242', 'Schreiben, Sprechen', 'jolsnachacko2@gmail.com'),
    ('Arya Benny', 'Ernakulam', '7306692700', 'Schreiben, Sprechen', 'aryabenny987@gmail.com'),
    ('Mary Sania', 'Ernakulam', '9048918641', 'Schreiben, Sprechen', 'marysania2004@gmail.com'),
    ('Tom Rijo Kurian', 'Idukki', '8921742803', 'Lesen, Sprechen', 'tomrijo2@gmail.com'),
    ('Diya Muttanchery Sumesh', 'Ernakulam', '9037627618', 'Schreiben', 'diyam4677@gmail.com'),
    ('Esha Hansil', 'Idukki', '8921570539', 'Schreiben', 'eshahanzil@gmail.com'),
    ('Valiyamangalathu Bleswin Joseph', 'Idukki', '9666825961', 'Lesen, Hören', 'bleswinjosephde@gmail.com'),
    ('Anjitha Ratheesh Nair', 'Kottayam', '9562994669', 'Lesen, Hören', 'anjithar81@gmail.com'),
    ('Avaneeth P', 'Malappuram', '9778242742', 'Sprechen Schreiben', 'avaneethgoethe@gmail.com'),
    ('Yathin Pradeep', 'Kannur', '9747486890', 'Schreiben, Sprechen', 'yathinpradeep42@gmail.com'),


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