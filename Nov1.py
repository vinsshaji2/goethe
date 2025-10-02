import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Email account details
to = 'exams.deutschzeit@gmail.com'
Subject = "Testmail-1"

email_accounts = [
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nikhitha4goethe@gmail.com', 'password': 'sjoi ijik arfs tzhl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'astinraju62@gmail.com', 'password': 'xmkt otzy rswi lffs', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'kasinaths467@gmail.com', 'password': 'itrj cyge jerz wtti', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'stephenashly2@gmail.com', 'password': 'zjbf vlbz xvkz uzxx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rimojohnsmdpl@gmail.com', 'password': 'xony vopp knas skrz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'helanajoy133@gmail.com', 'password': 'sehc esle cpqz bnrt', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annaannarajeev@gmail.com', 'password': 'ljkm wfhe rdor ixwn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'Anjanaajithsuja@gmail.com', 'password': 'igpb iimo nezk rwpo', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'snehabenny856@gmail com', 'password': 'ukul iwxj symq oklx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sriyasivan0@gmail.com', 'password': 'qtmx dnwv ncln khcf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nimishaeo2001@gmail.com', 'password': 'izan bjfl aivh migf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'vmmeenu3@gmail.com', 'password': 'zadw nggf aqkg erjg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'noblebaisy12@gmail.com', 'password': 'eacf hroh jhqn htib', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'athirarenjith3459@gmail.com', 'password': 'zshe vozi qzma ddrq', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'vaaswin735@gmail.com', 'password': 'jqgb wuxq kxrm nosk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'theresaraju1@gmail.com', 'password': 'qile gmgm lexn yoek', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'stephytitty18@gmail.com', 'password': 'lebw qowj galt rubg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'adithyaprasadachu@gmail.com', 'password': 'bqqt uais mnlq cbma', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'samueljohnson7592@gmail.com', 'password': 'hznm fmsp akyt mzvz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'blessyb567@gmail.com', 'password': 'ptlb sllu zbds wpax', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'menonadithya916@gmail.com', 'password': 'sima aqgm kygg zftq', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aidanaradan@gmail.com', 'password': 'pxgn mshk tkfa atrj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jinumonsajimon0@gmail.com', 'password': 'wlof dxej fnjp oiyn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'raniyanasrin21@gmail.com', 'password': 'wgrv nqit ozzr eapj', 'to': to, 'subject': Subject},

]

# Example dynamic data
data_list = [
    ('Nikhitha Jose', 'Eranakulam', '9207113885', 'Sprechen', 'nikhitha4goethe@gmail.com'),
    ('Astine Raju', 'Kozhikode', '8606737185', 'Sprechen', 'astinraju62@gmail.com'),
    ('Kasinath Sreekumar', 'Kottayam', '8606855122', 'Sprechen', 'kasinaths467@gmail.com'),
    ('Ashly Stephen', 'Idukki', '6235727198', 'Sprechen', 'stephenashly2@gmail.com'),
    ('Rimo Johns', 'Kottayam', '6235437059', 'Sprechen', 'rimojohnsmdpl@gmail.com'),
    ('Helana Joy', 'Malapuram', '9946500840', 'Sprechen', 'helanajoy133@gmail.com'),
    ('Anna Rajeev', 'Ernakulam', '8891747119', 'Sprechen', 'annaannarajeev@gmail.com'),
    ('Anjana Ajith', 'Kollam', '8921792126', 'Sprechen', 'Anjanaajithsuja@gmail.com'),
    ('Sneha Benny', 'Kottayam', '8921885606', 'Sprechen', 'snehabenny856@gmail com'),
    ('Sriya Edassery Sivan', 'Thrissur', '7558048986', 'Schreiben,Sprechen', 'sriyasivan0@gmail.com'),
    ('Nimisha Elanjikkaparambu Omanakuttan', 'Ernakulam', '7994164030', 'Schreiben,Sprechen', 'nimishaeo2001@gmail.com'),
    ('Meenakshy Vallassery Murphy', 'Ernakulam', '7356043339', 'Schreiben,Sprechen', 'vmmeenu3@gmail.com'),
    ('Noble Kalambal Baisy Joseph', 'Thrissur', '8714509388', 'Schreiben,Sprechen', 'noblebaisy12@gmail.com'),
    ('Athira Renjith', 'Trivandrum', '7591903459', 'Schreiben,Sprechen', 'athirarenjith3459@gmail.com'),
    ('Aswin vattakuzhiyil anil', 'Ernakulam', '9074146309', 'Schreiben,Sprechen', 'vaaswin735@gmail.com'),
    ('Theresa Raju', 'Kottayam', '7306800941', 'Lesen,Schreiben', 'theresaraju1@gmail.com'),
    ('Stephy Chacko Sabu', 'Alappuzha', '6282046574', 'Lesen,Hören,Schreiben', 'stephytitty18@gmail.com'),
    ('Adithya Prasad Minimol', 'Kollam', '9778137097', 'Schreiben', 'adithyaprasadachu@gmail.com'),
    ('Samuel Johnson', 'Kollam', '7592075219', 'Schreiben', 'samueljohnson7592@gmail.com'),
    ('Blessy Babu', 'Idukki', '9778214305', 'Schreiben', 'blessyb567@gmail.com'),
    ('Adithya Raj Menon', 'Ernakulam', '8075481232', 'Lesen,Hören', 'menonadithya916@gmail.com'),
    ('Aidan Ronal Aradan', 'Kollam', '9746167264', 'Lesen,Hören', 'aidanaradan@gmail.com'),
    ('Jinumon Sajimon', 'Kollam', '9961200369', 'Hören', 'jinumonsajimon0@gmail.com'),
    ('Raniya Nasrin Puthuvalparambu Raheem', 'Ernakulam', '8943356160', 'Hören', 'raniyanasrin21@gmail.com'),
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
