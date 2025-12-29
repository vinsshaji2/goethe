import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Email account details
to = 'exams.deutschzeit@gmail.com'
# to = 'EXAMS.REGISTRATION@GOETHE-ZENTRUM.ORG'
# Subject = "FEBRUARY 2026 B2 EXAM REGISTRATION-GOETHE-ZENTRUM"
Subject = "Testmail"

email_accounts = [
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleenawilsonp@gmail.com', 'password': 'usxn kiiz mpem yyrt', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annmariamathukutty@gmail.com', 'password': 'samb yrss mfnv obwz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nivyalibu@gmail.com', 'password': 'hwal lgev kmno klxi', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jincyjohn031@gmail.com', 'password': 'daoo uhks lpjr tgri', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'georgevarghese.georgia2004@gmail.com', 'password': 'ersa tohf xirh zpom', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'mariapanamattathil16@gmail.com', 'password': 'qrte knzi fwaj jzbv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleenababy829@gmail.com', 'password': 'xdmi kvsl rais qcbq', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'diyamariyajohn31@gmail.com', 'password': 'fnav dmmu cfpf qkhb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ANGELVALLIYIL@GMAIL.COM', 'password': 'pkme jscl jyce lunj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'renjudanasree@gmail.com', 'password': 'lcls tgxi emfd qifr', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'andriya2410@gmail.com', 'password': 'wzek dcvb ddma ikqr', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'amalaselten2@gmail.com', 'password': 'aghi iphq xjqt cqxj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'merinbiju124@gmail.com', 'password': 'xjoz gyst yatq eoug', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sanjushazz55@gmail.com', 'password': 'qail rnwk znuw usny', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'pavithraradhakrishnan42@gmail.com', 'password': 'uusl rwoi hiyf psrv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annamolthomas2255@gmail.com', 'password': 'wvjz awzu hmhq nezm', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjitharnair73@gmail.com', 'password': 'coch ewuw tzre uusr', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjanaajithsuja@gmail.com', 'password': 'onaa mpou dwwj jylg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'primalphilipose8@gmail.com', 'password': 'colx xuqe voqj fbwo', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'adhinaaugustinek@gmail.com', 'password': 'thtc tzka oycg xcty', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sindhuaparna2005@gmail.com', 'password': 'ruyj wjcf bqty kzzz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'hemanthginob2005@gmail.com', 'password': 'juop imyx yjpq tyjf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjuksks8@gmail.com', 'password': 'cpok tpjk oasc yoth', 'to': to, 'subject': Subject},


]

# Example dynamic data
data_list = [
    ('Aleena Wilson', 'Thrissur', '9605438745', 'Sprechen', 'aleenawilsonp@gmail.com'),
    ('Ann Maria Mathukutty', 'Kottayam', '8075373722', 'Sprechen', 'annmariamathukutty@gmail.com'),
    ('Nivya Thomas', 'Kottayam', '7994583918', 'Sprechen', 'nivyalibu@gmail.com'),
    ('Jincy John', 'Kollam', '9633045575', 'Sprechen', 'jincyjohn031@gmail.com'),
    ('George Varghese', 'Kollam', '8590373358', 'Sprechen', 'georgevarghese.georgia2004@gmail.com'),
    ('Maria Johnson', 'Kasaragod', '9778153071', 'Sprechen', 'mariapanamattathil16@gmail.com'),
    ('Aleena Baby', 'Ernakulam', '8113936442', 'Schreiben,Sprechen', 'aleenababy829@gmail.com'),
    ('Diya Mariya John', 'Ernakulam', '6235708327', 'Schreiben,Sprechen', 'diyamariyajohn31@gmail.com'),
    ('Angel Thomas', 'Kannur', '8075994349', 'Schreiben,Sprechen', 'angelvalliyil@gmail.com'),
    ('Renju Jayachandren', 'Pathanamthitta', '8078419052', 'Schreiben,Sprechen', 'renjudanasree@gmail.com'),
    ('Andriya Marit Jose', 'Ernakulam', '7306154023', 'Schreiben,Sprechen', 'andriya2410@gmail.com'),
    ('Amala Selten', 'Idukki', '6238695884', 'Schreiben,Sprechen', 'amalaselten2@gmail.com'),
    ('Merin Biju', 'Ernakulam', '9544274650', 'Hören,Schreiben,Sprechen', 'merinbiju124@gmail.com'),
    ('Sanjid Panachikkathodi', 'Malappuram', '9778758990', 'Lesen,Sprechen', 'sanjushazz55@gmail.com'),
    ('Pavithra Radhakrishnan', 'Pathanamthitta', '9400029178', 'Lesen,Sprechen', 'pavithraradhakrishnan42@gmail.com'),
    ('Annamol Abrahammadam Thomas', 'Alappuzha', '9645747862', 'Lesen,Schreiben', 'annamolthomas2255@gmail.com'),
    ('Anjitha Reghunathan Nair', 'Alappuzha', '8281009538', 'Lesen,Schreiben', 'anjitharnair73@gmail.com'),
    ('Anjana Ajith', 'Kolam', '89217 92126', 'Schreiben', 'anjanaajithsuja@gmail.com'),
    ('Primal Philipose', 'Kottayam', '9778111512', 'Schreiben', 'primalphilipose8@gmail.com'),
    ('Adhina Augustine', 'Kannur', '9496318365', 'Schreiben', 'adhinaaugustinek@gmail.com'),
    ('Aparna Suresh', 'Kottayam', '9074904899', 'Schreiben', 'sindhuaparna2005@gmail.com'),
    ('Hemanth Kollamkudy Ginob', 'Ernakulam', '9037029582', 'Lesen', 'hemanthginob2005@gmail.com'),
    ('Anju Kompenkeril Satheesh', 'Pathanamthitta', '8590815717', 'Lesen, Hören', 'anjuksks8@gmail.com'),





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
    schedule_time = "22:41:58"
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
