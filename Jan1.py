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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'alphysaju33@gmail.com', 'password': 'kjiw pbor tuxn ambz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'avanivsanthosh2003@gmail.com', 'password': 'dihn vuqn njno zgyp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'saniyamariyababu@gmail.com', 'password': 'xmfm cuhn hxik riyd', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annmariabiju1712@gmail.com', 'password': 'mkzv moey popd dyzz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'amalbinoy463@gmail.com', 'password': 'rkym kmdv xlhh cmpg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'dvndu3@gmail.com', 'password': 'pihg lfqm pvqw hfke', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anujoy325@gmail.com', 'password': 'hiwb yrjy yjvv atgl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jasminchacko8@gmail.com', 'password': 'yyjp ddkb fhtu ivpa', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'niranjanbose54@gmail.com', 'password': 'dxev mijw izcz gymw', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bileenakuruvila@gmail.com', 'password': 'cnkf dgzm cvhr szlg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'alonama6323@gmail.com', 'password': 'zoka qwdi opbh hrio', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'evelinsony1@gmail.com', 'password': 'gtsb osho iyxt hicx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'noblebaisy12@gmail.com', 'password': 'rdob jmhr owml fkux', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'tishateena63@gmail.com', 'password': 'bqkx faau hoen bkuv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'alphonsajoseph860@gmail.com', 'password': 'lznu jzti dqsd xhvx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'remyabalag@gmail.com', 'password': 'nxij lzfz ecqu qrfr', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'shanijoseph5197@gmail.com', 'password': 'ocoj jjzw saim sfcu', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'adithyashaji1226@gmail.com', 'password': 'ifdc xewf excb oinn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sheheemem70@gmail.com', 'password': 'akcy fkdb mqyh uxwu', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nadiyamol853@gmail.com', 'password': 'dxqt xicg vqdc ggfw', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aneenajoy742@gmail.com', 'password': 'kkrf rwyk cmpq qgbh', 'to': to, 'subject': Subject},
]

# Example dynamic data
data_list = [
    ('Alphy Saju', 'Ernakulam', '9074414885', 'Sprechen', 'alphysaju33@gmail.com'),
    ('Avani Vazhappillil Santhosh', 'Idukki', '8111850744', 'Sprechen', 'avanivsanthosh2003@gmail.com'),
    ('Saniya Mariya Babu', 'Wayanad', '8848012742', 'Sprechen', 'saniyamariyababu@gmail.com'),
    ('Ann Maria Biju', 'Idukki', '9074176248', 'Sprechen', 'annmariabiju1712@gmail.com'),
    ('Amal Binoy', 'Kottayam', '7510249131', 'Sprechen', 'amalbinoy463@gmail.com'),
    ('Deveendu Poothamveettil Thambi', 'Trissur', '6238166159', 'Sprechen', 'dvndu3@gmail.com'),
    ('Anu Joy', 'Kottayam', '8921403118', 'Schreiben,Sprechen', 'anujoy325@gmail.com'),
    ('Jasmin Chacko', 'Kottayam', '9567827532', 'Schreiben,Sprechen', 'jasminchacko8@gmail.com'),
    ('Niranjan Bose', 'Thrissur', '6235131489', 'Schreiben,Sprechen', 'niranjanbose54@gmail.com'),
    ('Beleena Kuruvila', 'Idukki', '8590322306', 'Lesen,Hören,Schreiben,Sprechen', 'bileenakuruvila@gmail.com'),
    ('Alona Mangattel Antony', 'Idukki', '6238527372', 'Lesen,Hören,Schreiben,Sprechen', 'alonama6323@gmail.com'),
    ('Evelin Sony', 'Idukki', '7907463154', 'Lesen,Hören,Schreiben,Sprechen', 'evelinsony1@gmail.com'),
    ('Noble Kalambal Baisy Joseph', 'Thrissur', '8714509388', 'Lesen,Schreiben,Sprechen', 'noblebaisy12@gmail.com'),
    ('Teena Kavitha Shaji', 'Kottayam', '8075668318', 'Lesen,Schreiben, Sprechen', 'tishateena63@gmail.com'),
    ('Alphonsa Joseph', 'Kannur', '7736127621', 'Lesen, Schreiben', 'alphonsajoseph860@gmail.com'),
    ('Remya Ramachandran Nair', 'Kottayam', '8547895155', 'Schreiben', 'remyabalag@gmail.com'),
    ('Shani Joseph', 'Thiruvananthapuram', '7909103191', 'Lesen', 'shanijoseph5197@gmail.com'),
    ('Adithya Shaji', 'Alappuzha', '8848032900', 'Lesen, Hören', 'adithyashaji1226@gmail.com'),
    ('Sheheem Erinjippurath Mohammed', 'Malappuram', '8590731904', 'Hören', 'sheheemem70@gmail.com'),
    ('Nadiya Sulthana Shukkoor', 'Ernakulam', '8111839003', 'Lesen, Schreiben', 'nadiyamol853@gmail.com'),
    ('Aneena Joy', 'Ernakulam', '7594834763', 'Schreiben Sprechen', 'aneenajoy742@gmail.com'),
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
    schedule_time = "23:16:50"
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
