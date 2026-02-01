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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'abhiyacb598@gmail.com', 'password': 'fktr ttwv uerj wjre','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nivyashaju@gmail.com', 'password': 'xffn thib rzzv mxjf','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rosemariyarajesh554@gmail.com', 'password': 'eeoa djoa zbnb vusv','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ameesha810@gmail.com', 'password': 'ioqp cfge urqb fntf','to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleenajoby1042000@gmail.com', 'password': 'rydx ongl xepi zjfx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anvrithaanu@gmail.com', 'password': 'lutr pweq eglc ogds', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anaswararajeev06@gmail.com', 'password': 'cbig mkfo qyce brow', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aswinisanthosh2007@gmail.com', 'password': 'cres hrwe iteu ejux', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'princypaullucy@gmail.com', 'password': 'rmby zgiz dtvz iopc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'vaaswin735@gmail.com', 'password': 'fkhf dcch mkwm nphf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'shintujoe6755@gmail.com', 'password': 'zuru ysfc ysfh jahc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'johnaagi3@gmail.com', 'password': 'tlvq qktq ctaj vgjt', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'saniyathomas6282@gmail.com', 'password': 'rmjy adaz soll xpqa', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'examgoethe1@gmail.com', 'password': 'wmyp mdxx dets dxse', 'to': to, 'subject': Subject},

]

# Example dynamic data
data_list = [
    ('Abhiya Chakkalakkal Biju', 'Thrissur', '7736610270', 'Sprechen', 'abhiyacb598@gmail.com'),
    ('Nivya Shaju', 'Ernakulam', '8078356229', 'Sprechen', 'nivyashaju@gmail.com'),
    ('Rose maria Rajesh', 'Kasaragod', '7560976710', 'Sprechen', 'rosemariyarajesh554@gmail.com'),
    ('Ameesha Chonedan Jaison', 'Thrissur', '7034485032', 'Sprechen', 'ameesha810@gmail.com'),
    ('Aleena Joby', 'Idukki', '6238462028', 'Schreiben, Sprechen', 'aleenajoby1042000@gmail.com'),
    ('Anvritha Rosh', 'Thrissur', '8907779531', 'Schreiben, Sprechen', 'anvrithaanu@gmail.com'),
    ('Anaswara Thattamparambil Rajeev', 'Idukki', '9778335283', 'Schreiben, Sprechen', 'anaswararajeev06@gmail.com'),
    ('Aswini Santhosh', 'Kottayam', '6235504550', 'Schreiben, Sprechen', 'aswinisanthosh2007@gmail.com'),
    ('Princy Paul Nellikunnel', 'Kottayam', '8891976616', 'Lesen,Hören,Schreiben,Sprechen', 'princypaullucy@gmail.com'),
    ('Aswin Vattakuzhiyil Anil', 'Ernakulam', '9074146309', 'Lesen, Sprechen', 'vaaswin735@gmail.com'),
    ('Shintu Yohannan Raju', 'Kollam', '8606324703', 'Schreiben', 'shintujoe6755@gmail.com'),
    ('Aagi John', 'Idukki', '9188348965', 'Lesen, Hören', 'johnaagi3@gmail.com'),
    ('Saniya Thomas', 'Kollam', '6282553475', 'Lesen, Hören', 'saniyathomas6282@gmail.com'),
    ('Adithyan Saji', 'Ernakulam', '7306758358', 'Lesen', 'examgoethe1@gmail.com'),


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