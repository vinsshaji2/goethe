import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Email account details
to = 'exams.deutschzeit@gmail.com'
# to = 'EXAMS.REGISTRATION@GOETHE-ZENTRUM.ORG'
# Subject = "DECEMBER 2025 B2 EXAM REGISTRATION-GOETHE-ZENTRUM"
Subject = "Testmail"

email_accounts = [
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'antonyalisha356@gmail.com', 'password': 'dtih ghud cwhx wezn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jefrinfrancis7656@gmail.com', 'password': 'hpzi cglc mqrv dnfm', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleenabenny172004@gmail.com', 'password': 'aeuh kcix tjvg qihx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rimojohnsmdpl@gmail.com', 'password': 'xpkh qgbk agcf xqmm', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'parvathymp531@gmail.com', 'password': 'hucv buuf cbez lohz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aswathimp003@gmail.com', 'password': 'vwsj tfik hiau zvcx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'xavierancy95@gmail.com', 'password': 'nguz afiy wuix rgwe', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jesnamoljoy2002@gmail.com', 'password': 'xyln woov fvdi fzqo', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'zardra958@gmail.com', 'password': 'kagn sgyl zscn bscp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'melbinrose1@gmail.com', 'password': 'exgr vkqc knwz upxs', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'paruzzz1230@gmail.com', 'password': 'xhxs xkve cpyg bepv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'vaaswin735@gmail.com', 'password': 'eevq wxwx hnjx lrnt', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'staniyathomas43@gmail.com', 'password': 'vrnl gzvo sehl acvs', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'noblebaisy12@gmail.com', 'password': 'zlpv wfjd itzi hntj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sanjushazz55@gmail.com', 'password': 'fdhc uxdt biof uiwy', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'suryanaththundiyath@gmail.com', 'password': 'xvth oupg ecdp snzq', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'milanbabukalady@gmail.com', 'password': 'fbtu ayct wsjc yvui', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'akhilmanikuttanparathanam2021@gmail.com', 'password': 'sfbv cfft tbka xdms', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bisminsafriya@gmail.com', 'password': 'musa rktv dvjx gfyw', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nilunihal21@gmail.com', 'password': 'jafl yiro vckg fhkx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nayanaks0820@gmail.com', 'password': 'dsla grax bdik dmrc','to': to, 'subject': Subject},
]

# Example dynamic data
data_list = [
    ('Alisha Antony', 'Kollam', '8714550076', 'Sprechen', 'antonyalisha356@gmail.com'),
    ('Jefrin Francis', 'Kollam', '7907399455', 'Sprechen', 'jefrinfrancis7656@gmail.com'),
    ('Aleena Benny', 'Idukki', '8078589307', 'Sprechen', 'aleenabenny172004@gmail.com'),
    ('Rimo Johns', 'Kottayam', '6235437059', 'Sprechen', 'rimojohnsmdpl@gmail.com'),
    ('Parvathy Mangayil Prasadkumar', 'Kottayam', '9778710162', 'Sprechen', 'parvathymp531@gmail.com'),
    ('Aswathi Manoj', 'idukki', '7559924532', 'Sprechen', 'aswathimp003@gmail.com'),
    ('Ancy Xavier', 'Ernakulam', '9747065301', 'Sprechen', 'xavierancy95@gmail.com'),
    ('Jesnamol Joy', 'idukki', '9562458819', 'Sprechen', 'jesnamoljoy2002@gmail.com'),
    ('Ardra M   eenakumary Suseelan Pillai', 'Kollam', '9995224065', 'Sprechen', 'zardra958@gmail.com'),
    ('Melbin Rose Babu', 'Thrissur', '7356115325', 'Schreiben,Sprechen', 'melbinrose1@gmail.com'),
    ('Ettiyedath Madathil Ajikumar Gowrinanda', 'Ernakulam', '9847715466', 'Schreiben,Sprechen', 'paruzzz1230@gmail.com'),
    ('Aswin Vattakuzhiyil Anil', 'Ernakulam', '9074146309', 'Lesen, Schreiben, Sprechen', 'vaaswin735@gmail.com'),
    ('Staniya Thomas', 'Idukki', '8547503947', 'Lesen, Schreiben, Sprechen', 'staniyathomas43@gmail.com'),
    ('Noble Kalambal Baisy Joseph', 'Thrissur', '8714509388', 'Lesen,Schreiben,Sprechen', 'noblebaisy12@gmail.com'),
    ('Sanjid Panachikkathodi', 'Malappuram', '9778758990', 'Lesen,Hören,Sprechen', 'sanjushazz55@gmail.com'),
    ('Suryanath Thundiyath', 'Malapuram', '8921555137', 'Hören Schreiben', 'suryanaththundiyath@gmail.com'),
    ('Milan Babu', 'Ernakulam', '9048955367', 'Schreiben', 'milanbabukalady@gmail.com'),
    ('Akhil Manikuttan', 'Kottayam', '8921552110', 'Schreiben', 'akhilmanikuttanparathanam2021@gmail.com'),
    ('Bismin Safriya Shajahan', 'Ernakulam', '8848281770', 'Schreiben', 'bisminsafriya@gmail.com'),
    ('Muhammed Nihal Chakkitta Parambil', 'Kozhikode', '8848607244', 'Lesen', 'nilunihal21@gmail.com'),
    ('Nayana Karupuzha Sunilkumar', 'Ernakulam', '9400366638', 'Schreiben', 'nayanaks0820@gmail.com'),
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
    schedule_time = "08:16:30"
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
