import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Email account details
to = 'exams.deutschzeit@gmail.com'
# to = 'EXAMS.REGISTRATION@GOETHE-ZENTRUM.ORG'
# Subject = "JANUARY 2026 EXAM REGISTRATION-GOETHE-ZENTRUM"
Subject = "Testmail"

email_accounts = [
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'kprahana313@gmail.com', 'password': 'fupu bbac xuob fnsd', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'kamalkumar7raj@gmail.com', 'password': 'xbkp fshz hujc chvj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'vinitham250@gmail.com', 'password': 'xpxw qtsv ahaw vawj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rosmipj1998@gmail.com', 'password': 'qphz tshn jxcc yucp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'soumya90molpb@gmail.com', 'password': 'uwlf tuwz ywgd mvay', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aneetathomas333@gmail.com', 'password': 'hotn bxhy mfty slxz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'christyjames920@gmail.com', 'password': 'smwe drma garb gumg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jincyot1@gmail.com', 'password': 'vztv iiey oovb qyvf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rockstargladson@gmail.com', 'password': 'xorz yhvj njcp oypn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'roseamaya805@gmail.com', 'password': 'mfdn lkld abjj lbzl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sebastiankarackaljoseph@gmail.com', 'password': 'ebzw wenk iprj xjyb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jesveenapjohn@gmail.com', 'password': 'yvru pddu qaux eteb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'emiliyasatheesh0@gmail.com', 'password': 'mnns ihus xgio shsl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'shaunjames0620@gmail.com', 'password': 'msmk msxm eggp zzzl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jyotsnaalbert6@gmail.com', 'password': 'flba gnok mgcz sgbd', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'samithaparasad1992@gmail.com', 'password': 'mqpd gmvr ojok mvmb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleenaelizabethbabu261@gmail.com', 'password': 'wjwn jrma vyix ljxy', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'pavanabaiju3@gmail.com', 'password': 'unig nnlj zbbi deaz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'raniyanasrin21@gmail.com', 'password': 'nzal ncaq omvk inux', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'merinageorgemerinageorge@gmail.com', 'password': 'uxkx rzqg radz uuef', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rosemolfrancis105@gmail.com', 'password': 'qnqe mygy jsbj wflx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'angelmariyajose2006@gmail.com', 'password': 'ssow kybf iart kphv', 'to': to, 'subject': Subject},

]

# Example dynamic data
data_list = [
    ('Fathima Rahana Kollakam Parambath', 'Kozhikode', '9072342579', 'Sprechen', 'kprahana313@gmail.com'),
    ('Kamal Kumar Gautham Paswan', 'Alappuzha', '6238826145', 'Sprechen', 'kamalkumar7raj@gmail.com'),
    ('Vinitha Manoj', 'Kollam', '7034540997', 'Sprechen', 'vinitham250@gmail.com'),
    ('Rosmi Pulikkottil Jose', 'Trissur', '7306035192', 'Sprechen', 'rosmipj1998@gmail.com'),
    ('Sowmyamol Puthuvelil Bhaskaran', 'Pathanamthitta', '8310960542', 'Sprechen', 'soumya90molpb@gmail.com'),
    ('Aneeta Thomas', 'Ernakulam', '8590732967', 'Schreiben,Sprechen', 'aneetathomas333@gmail.com'),
    ('Christy James', 'Kannur', '9207265920', 'Schreiben,Sprechen', 'christyjames920@gmail.com'),
    ('Jincy Ottalankal Thankachan', 'Kannur', '7306726523', 'Schreiben,Sprechen', 'jincyot1@gmail.com'),
    ('Gladson Paramabanad Saju', 'Wayanad', '9304989887', 'Schreiben,Sprechen', 'rockstargladson@gmail.com'),
    ('Amaya Rose', 'Wayanad', '8590110136', 'Lesen,Hören,Schreiben,Sprechen', 'roseamaya805@gmail.com'),
    ('Sebastian Karackal Joseph', 'Kannur', '8891787112', 'Lesen,Hören,Schreiben,Sprechen', 'sebastiankarackaljoseph@gmail.com'),
    ('Jesveena John Pulluvelil', 'Kannur', '9778321962', 'Lesen,Hören,Schreiben,Sprechen', 'jesveenapjohn@gmail.com'),
    ('Emiliya Satheesh', 'Idukki', '9778353473', 'Lesen, Sprechen', 'emiliyasatheesh0@gmail.com'),
    ('Shaun James', 'Kollam', '8139071297', 'Schreiben', 'shaunjames0620@gmail.com'),
    ('Jyotsna Albert', 'Alappuzha', '9778432620', 'Schreiben', 'jyotsnaalbert6@gmail.com'),
    ('Vazhekattil saji samitha', 'Thrissur', '6235551984', 'Schrieben', 'samithaparasad1992@gmail.com'),
    ('Aleena Elizabeth Babu', 'Kottayam', '7034689320', 'Lesen, Hören', 'aleenaelizabethbabu261@gmail.com'),
    ('Pavana Baiju', 'Alappuzha', '9037315562', 'Lesen, Hören', 'pavanabaiju3@gmail.com'),
    ('Raniya Nasrin Puthuvalparambu Raheem', 'Ernakulam', '8943356160', 'Schreiben', 'raniyanasrin21@gmail.com'),
    ('Merina George', 'Idukki', '7907548034', 'Lesen horen', 'merinageorgemerinageorge@gmail.com'),
    ('Rosemol Francis', 'Thrissur', '9074121986', 'Schreiben', 'rosemolfrancis105@gmail.com'),
    ('Angel Mariya Jose', 'Idukki', '9747837288', 'Schreiben', 'angelmariyajose2006@gmail.com'),
]


def generate_email_body(full_name, current_district, contact_number, exam_modules, email_id):
    return f"""
    <html>
    <body>
        <table border=1 style="border-collapse: collapse; width: 100%;">
            <tr>
                <th>Full Name</th>
                <th>Current District</th>
                <th>Personal Contact Number</th>
                <th>Exam Modules</th>
                <th>Email Id (Reg-Email used in our website)</th>
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
        print(f"✅ Email sent from {account['username']} to {account['to']}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email from {account['username']} to {account['to']}: {e}")
        return False


def send_all_emails():
    results = []
    with ThreadPoolExecutor(max_workers=len(email_accounts)) as executor:
        future_to_task = {
            executor.submit(send_email, account, *data): (account, data)
            for account, data in zip(email_accounts, data_list)
        }
        for future in as_completed(future_to_task):
            results.append(future.result())
    return all(results)


if __name__ == "__main__":
    schedule_time = "23:28:50"
    print(f"⏰ Scheduled to send emails at {schedule_time} every day to {to}.")

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == schedule_time:
            success = send_all_emails()
            if not success:
                print("⚠️ Some emails failed. Retrying in 10 seconds...")
                time.sleep(10)
                # send_all_emails()  # retry failed ones
            # time.sleep(1)
        time.sleep(0.5)
