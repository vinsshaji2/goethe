import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Email account details
to = 'exams.deutschzeit@gmail.com'
# to = 'EXAMS.REGISTRATION@GOETHE-ZENTRUM.ORG'
# Subject = "NOVEMBER 2025 EXAM REGISTRATION-GOETHE-ZENTRUM"
Subject = "Testmail-1"

email_accounts = [
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anoldajoby@gmail.com', 'password': 'nbha jvqv ftdv zbqa', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'johnsyneha5331@gmail.com', 'password': 'qlcb dihu yevo oecf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nivyalibu@gmail.com', 'password': 'jkrq rvdb hitd lmgw', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'treesahanna1308@gmail.com', 'password': 'otwc hqda bpny iprv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'shinad33@gmail.com', 'password': 'zzwm wznk nvis rwdj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'soumyavarkey1990@gmail.com', 'password': 'wbhw ifqm pynb mqdx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'mohdmusthafapilakkal@gmail.com', 'password': 'zbvu osnz tcbq fknc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anijaa410@gmail.com', 'password': 'zcsq nhiy wgsz vzhz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'shelvin03041998@gmail.com', 'password': 'irrv qkbe burf fxhs', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jincyot1@gmail.com', 'password': 'ajfa vven pfyu wdem', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aswathyshikkar222@gmail.com', 'password': 'jfto bgkw brig tebb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'Avaneethgoethe@gmail.com', 'password': 'bvis dlob jxlz kmts', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'marysania2004@gmail.com', 'password': 'ytcb qumq qwal jaqe', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'kavyamani2018@gmail.com', 'password': 'tmnx zrxy gbnx hkwt', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'shalomialenjose765@gmail.com', 'password': 'khzj tkvu setw xblm', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'gloriathomas2u@gmail.com', 'password': 'firt qkgh syua woqn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'poornimakp12@gmail.com', 'password': 'wrup ubov lint eyla', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sharonakhila831@gmail.com', 'password': 'bpbh aezu jhfk zjzl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jenifersebastian0@gmail.com', 'password': 'fpxj dazf vajj payt', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annamolthomas05@gmail.com', 'password': 'ibgs jigg zqlb aiht', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'omanagopan5@gmail.com', 'password': 'lvmb fnnc xzla bivn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'mottyprecious930@gmail.com', 'password': 'gvzn foeo tzrk nggi', 'to': to, 'subject': Subject}
]

# Example dynamic data
data_list = [
    ('Anolda Joby', 'Ernakulam', '8089268624', 'Schreiben', 'anoldajoby@gmail.com'),
    ('Neha John', 'Kottayam', '8606095331', 'Sprechen', 'johnsyneha5331@gmail.com'),
    ('Nivya Thomas', 'Kottayam', '7994583918', 'Sprechen', 'nivyalibu@gmail.com'),
    ('Treesahanna', 'Ernakulam', '8590964552', 'Sprechen', 'treesahanna1308@gmail.com'),
    ('Shinad Hassan Noushad Tharayan Kandathil', 'Malappuram', '8606503460', 'Sprechen', 'shinad33@gmail.com'),
    ('Soumya Varkey', 'Kollam', '9074715880', 'Sprechen', 'soumyavarkey1990@gmail.com'),
    ('Muhammed musthafa pilakkal', 'Palakkad', '7594957954', 'Sprechen', 'mohdmusthafapilakkal@gmail.com'),
    ('Anija Aji', 'Kottayam', '7012456968', 'Sprechen', 'anijaa410@gmail.com'),
    ('Shelvin Thrissokkaran Shaju', 'Thirssur', '8943308049', 'Schreiben,Sprechen', 'shelvin03041998@gmail.com'),
    ('Jincy Ottalankal Thankachan', 'Kannur', '7306726523', 'Schreiben,Sprechen', 'jincyot1@gmail.com'),
    ('Aswathy Shikkar', 'Ernakulam', '9188161453', 'Schreiben,Sprechen', 'aswathyshikkar222@gmail.com'),
    ('Avaneeth pulikkathodi', 'Malappuram', '9778242742', 'Schreiben,Sprechen', 'Avaneethgoethe@gmail.com'),
    ('Mary Sania', 'Ernakulam', '9048918641', 'Schreiben,Sprechen', 'marysania2004@gmail.com'),
    ('Kavya  Melepatt', 'Palakkad', '7736743123', 'Hören,Schreiben', 'kavyamani2018@gmail.com'),
    ('Shalomi Alen Jose', 'Pathanamthitta', '8943906304', 'Lesen,Schreiben', 'shalomialenjose765@gmail.com'),
    ('Gloriya Thomas', 'Kannur', '9605839144', 'Hören,Schreiben', 'gloriathomas2u@gmail.com'),
    ('Poornima Kottampadam Pradeep', 'Kottayam', '8714457563', 'Schreiben', 'poornimakp12@gmail.com'),
    ('Akhila Sharon', 'Kollam', '7012391136', 'Schreiben', 'sharonakhila831@gmail.com'),
    ('Jenifer Sebastian', 'Alappuzha', '8594026311', 'Lesen', 'jenifersebastian0@gmail.com'),
    ('Annamol Abrahammadam Thomas', 'Alappuzha', '9645747862', 'Lesen', 'annamolthomas05@gmail.com'),
    ('Hena Krishnan', 'Pathanamthitta', '9048927011', 'Lesen,Hören', 'omanagopan5@gmail.com'),
    ('Precious Motty', 'Ernakulam', '6282713033', 'Lesen', 'mottyprecious930@gmail.com')
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
    schedule_time = "23:53:00"
    print(f"⏰ Scheduled to send emails at {schedule_time} every day to {to}.")

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == schedule_time:
            success = send_all_emails()
            if not success:
                print("⚠️ Some emails failed. Retrying in 10 seconds...")
                time.sleep(10)
                send_all_emails()  # retry failed ones
            time.sleep(1)
        time.sleep(0.5)
