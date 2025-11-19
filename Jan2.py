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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ebengeotho05@gmail.com', 'password': 'hjkb ujek ehvf ujct', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bettyjoseph4123@gmail.com', 'password': 'khna ajhr gaqr rqir', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'zardra958@gmail.com', 'password': 'ktvl ispg fuiz kxco', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'kalidasnj2026@gmail.com', 'password': 'uffl syky owik qeno', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ambikakumary01@gmail.com', 'password': 'sdwl jaup vhsk tnqb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annmariamathukutty@gmail.com', 'password': 'kblg hrhi tjfy jmwh', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'athirarenjith3459@gmail.com', 'password': 'zdjj grzi fvle elcx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ashrafrafeek99@gmail.com', 'password': 'ibtb ryya xuuc xlpu', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'santhoshchaithanya01@gmail.com', 'password': 'jikf jawk gwux dsle', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'amithasreekumar2003@gmail.com', 'password': 'urqd hkbu ufyg sfak', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jelittajose7902@gmail.com', 'password': 'ppuw ipmb zkec wlvg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aswinibabu230@gmail.com', 'password': 'gvvd gomy jyus onnq', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'staniyathomas43@gmail.com', 'password': 'dttt qmet dkgd jsfu', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'shorn2701@gmail.com', 'password': 'iean pnkd cnhe zjki', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anujaanilkumar53@gmail.com', 'password': 'yrgz qlri gufx xpzz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'meerakrishna8590@gmail.com', 'password': 'xibq jbiu ruyo krno', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'milanbabukalady@gmail.com', 'password': 'pldz onko zmtl dxas', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'karthikaprasad1804@gmail.com', 'password': 'zkwc quth gadh kjhx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ranidominic.kochu@gmail.com', 'password': 'qdsx iqbn tzgl qnkd', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sinukvarughese44@gmail.com', 'password': 'vaou vwqz yvdy emhu', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ahmedyaseengoethe@gmail.com', 'password': 'vgbr cdcj nhrz kuan', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'saviobinu544@gmail.com', 'password': 'joxe dclh otcr nlny', 'to': to, 'subject': Subject},



]

# Example dynamic data
data_list = [
    ('Eshwin George Benny', 'idukki', '9645558938', 'Sprechen', 'ebengeotho05@gmail.com'),
    ('Bettymol Joseph', 'Kottayam', '9567321341', 'Sprechen', 'bettyjoseph4123@gmail.com'),
    ('Ardra Meenakumary Suseelan Pillai', 'Kollam', '9995224065', 'Sprechen', 'zardra958@gmail.com'),
    ('Kalidas Nadappurakil Jaimon', 'Kottayam', '9526885975', 'Sprechen', 'kalidasnj2026@gmail.com'),
    ('Adithya Raghunathakurup', 'Kollam', '8590164305', 'Sprechen', 'ambikakumary01@gmail.com'),
    ('Ann Maria Mathukutty', 'Kottayam', '8075373722', 'Sprechen', 'annmariamathukutty@gmail.com'),
    ('Athira Renjith', 'Thiruvananthapuram', '7591903459', 'Schreiben,Sprechen', 'athirarenjith3459@gmail.com'),
    ('Muhammad Ashraf', 'Thriuvananthapuram', '9894061091', 'Schreiben', 'ashrafrafeek99@gmail.com'),
    ('Chaithanya Santhosh', 'Pathanamthitta', '9946599948', 'Schreiben,Sprechen', 'santhoshchaithanya01@gmail.com'),
    ('Amitha Sreekumar', 'Kollam', '6238160870', 'Lesen,Hören,Schreiben,Sprechen', 'amithasreekumar2003@gmail.com'),
    ('Jelitta Jose', 'Idukki', '9188453707', 'Lesen,Hören,Schreiben,Sprechen', 'jelittajose7902@gmail.com'),
    ('Aswini Babu', 'Kannur', '7034748254', 'Lesen,Hören,Schreiben,Sprechen', 'aswinibabu230@gmail.com'),
    ('Staniya Thomas', 'Idukki', '8547503947', 'Lesen,Schreiben,Sprechen', 'staniyathomas43@gmail.com'),
    ('Shorn Saji', 'Idukki', '9526911236', 'Lesen, Schreiben', 'shorn2701@gmail.com'),
    ('Anuja Ranjana', 'Alappuzha', '7025609746', 'Hören,Schreiben', 'anujaanilkumar53@gmail.com'),
    ('Meerakrishna Thayyil Rajesh', 'Thrissur', '8848763294', 'Schreiben', 'meerakrishna8590@gmail.com'),
    ('Milan Babu', 'Ernakulam', '9048955367', 'Schreiben', 'milanbabukalady@gmail.com'),
    ('Karthika Prasad', 'Kottayam', '9744151804', 'Lesen, Hören', 'karthikaprasad1804@gmail.com'),
    ('Rani Dominic', 'Kottayam', '9747214390', 'Lesen,Hören', 'ranidominic.kochu@gmail.com'),
    ('Sinu Kaleeckal Varughese', 'Pathanamthitta', '9526336151', 'Lesen, Hören', 'sinukvarughese44@gmail.com'),
    ('Ahmed Yaseen', 'Malappuram', '7736256206', 'Schreiben, Sprechen', 'ahmedyaseengoethe@gmail.com'),
    ('Savio Binu', 'Wayanad', '80755 01844', 'Schreiben, Sprechen', 'saviobinu544@gmail.com'),


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
    schedule_time = "23:21:00"
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
