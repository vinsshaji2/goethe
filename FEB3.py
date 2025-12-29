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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'treesahanna1308@gmail.com', 'password': 'byyn gdqx vefb fjoq', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ayonajohn4240@gmail.com', 'password': 'rwuw ahtt abbb wfdu', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'vmmeenu3@gmail.com', 'password': 'nrma eyra ezhr yhrl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjuanjanabiju16@gmail.com', 'password': 'oafj hqgt bgpr fmjy', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'abhiramipr777@gmail.com', 'password': 'sfqf gdmt inap knoq', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'benssonmathew@gmail.com', 'password': 'tyqn cjzu pjty wwpd', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'mencymariya22@gmail.com', 'password': 'claz vooa oxvc zrqr', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sreelekshmikripa@gmail.com', 'password': 'xxem rjwo akda rjht', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anmariyathomas6@gmail.com', 'password': 'tbdk lhha idwt nije', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'meerakrishna8590@gmail.com', 'password': 'pxag ejia cmpv egpo', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sreelakshmimanu30@gmail.com', 'password': 'qqtf tfbl lryd tcbp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'abinsunny3106@gmail.com', 'password': 'cpze pdcc tynp qpmp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bileenakuruvila@gmail.com', 'password': 'nxrk jtqe fgyl nvnf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'viniantony18@gmail.com', 'password': 'vnie spsb zvrv xypg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nikhitharajesh4612@gmail.com', 'password': 'cnaq vzjf cdwm vtkj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleena08112002@gmail.com', 'password': 'xwow awhy sybe qxvb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jincyot1@gmail.com', 'password': 'reva uase sqhj rvyv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'merinageorgemerinageorge@gmail.com', 'password': 'qnoj sgjn mqnt xzgk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'helanajoy133@gmail.com', 'password': 'yiam wbmo tvwf fhki', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'Karunanjeevaabitha@gmail.com', 'password': 'hlzl uwia ofpu pqik', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 't59156705@gmail.com', 'password': 'sebh yzou gewf qthe', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjanasiva15@gmail.com', 'password': 'gbrd ttot lkub srax', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'archanasanoop70@gmail.com', 'password': 'bkxo lbal nkji pjyl', 'to': to, 'subject': Subject},

]

# Example dynamic data
data_list = [
    ('Treesahanna', 'Ernakulam', '8590964552', 'Sprechen', 'treesahanna1308@gmail.com'),
    ('Ayona John', 'Idukki', '70128 99342', 'Sprechen', 'ayonajohn4240@gmail.com'),
    ('Meenakshy Vallassery Murphy', 'Ernakulam', '7356043339', 'Sprechen', 'vmmeenu3@gmail.com'),
    ('Anjana Biju', 'Alappuzha', '8589073201', 'Sprechen', 'anjuanjanabiju16@gmail.com'),
    ('Abhirami Peedikathara Rekha', 'Alappuzha', '6282180021', 'Sprechen', 'abhiramipr777@gmail.com'),
    ('Bensson Mathew', 'Kottayam', '7907612901', 'Sprechen', 'benssonmathew@gmail.com'),
    ('Mency Mariya Jaison', 'Kozhikode', '9496715194', 'Sprechen', 'mencymariya22@gmail.com'),
    ('Sreelekshmi Aswin', 'Alappuzha', '8891788630', 'Schreiben,Sprechen', 'sreelekshmikripa@gmail.com'),
    ('Anmariya Thomas', 'Thrissur', '8075633895', 'Schreiben,Sprechen', 'anmariyathomas6@gmail.com'),
    ('Meerakrishna Thayyil Rajesh', 'Thrisur', '8848763294', 'Schreiben,Sprechen', 'meerakrishna8590@gmail.com'),
    ('Sreelakshmi Manu', 'Kottayam', '9496911607', 'Schreiben,Sprechen', 'sreelakshmimanu30@gmail.com'),
    ('Abin Sunny', 'Kannur', '8848580086', 'Schreiben,Sprechen', 'abinsunny3106@gmail.com'),
    ('Beleena Kuruvila', 'Idukki', '8590322306', 'Lesen,Hören,Schreiben,Sprechen', 'bileenakuruvila@gmail.com'),
    ('Vini Antony', 'Ernakulam', '9495270596', 'Lesen,Schreiben,Sprechen', 'viniantony18@gmail.com'),
    ('Nikhitha Rajesh', 'Kottayam', '7356144996', 'Hören,Schreiben', 'nikhitharajesh4612@gmail.com'),
    ('Aleena Johny', 'Ernakulam', '7510399498', 'Schreiben', 'aleena08112002@gmail.com'),
    ('Jincy Ottalankal Thankachan', 'Kannur', '7306726523', 'Schreiben', 'jincyot1@gmail.com'),
    ('Merina George', 'Idukki', '7907548034', 'Schreiben', 'merinageorgemerinageorge@gmail.com'),
    ('Helana Joy', 'Malappuram', '9946500840', 'Schreiben', 'helanajoy133@gmail.com'),
    ('Jeeva Abitha Malar Jayakarunan', 'Kanniyakumari', '9486982841', 'Lesen, Hören', 'Karunanjeevaabitha@gmail.com'),
    ('Teza Prince', 'Ernakulam', '8891449003', 'Lesen', 't59156705@gmail.com'),
    ('Anjana Sivakumar', 'Palakkad', '8089106626', 'Schreiben', 'anjanasiva15@gmail.com'),
    ('Archana Chettiyathuparambil Pushparjunan', 'Kottayam', '9540668976', 'Schreiben,Sprechen', 'archanasanoop70@gmail.com')

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
    schedule_time = "22:41:20"
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
