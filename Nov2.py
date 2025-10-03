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
Subject = "Testmail"

email_accounts = [
{'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'akshayaes132006@gmail.com', 'password': 'kzxy fclm boaq csnn',  'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'devanandarajesh27@gmail.com',
     'password': 'ymic gmwo qhab nbzo', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'karolinajijo9c@gmail.com',
     'password': 'fqxf jhyx kfvf yvny', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'shanijoseph5197@gmail.com',
     'password': 'otmu inwv qjci byuv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sreelakshmivr06@gmail.com',
     'password': 'mmxt zqlo uepy aojx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sherin10414@gmail.com',
     'password': 'fxjz cpgf ycpc hgda', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'johnniranjana2@gmail.com',
     'password': 'mqzo gpix wqgk ccpf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'snehasatheesh0839@gmail.com',
     'password': 'nbcg bajt cghg ucbn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ihsankodali112@gmail.com',
     'password': 'znss pdqb nrod jtax', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'paruzzz1230@gmail.com',
     'password': 'iwmv drvn ahap csdp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'niranjanbose54@gmail.com',
     'password': 'qpfg wrai keuc ruwp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'elmyjaison@gmail.com',
     'password': 'jomb jqqi gsap hgyb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'tjacobvaidian@gmail.com',
     'password': 'rpmx ofwq ltip rkrh', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bessy.ambili@gmail.com',
     'password': 'mekc fppk ugul nvcy', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'samithaparasad1992@gmail.com',
     'password': 'tkuv swge lytl uiif', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anusreenew5431@gmail.com',
     'password': 'cihk wulm vdvd phzg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'namithajoji59@gmail.com',
     'password': 'zmis ztlm jhbr oirs', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'milanbabukalady@gmail.com',
     'password': 'twep rnbf nwwh jrnf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sangeethasanthosh0186@gmail.com',
     'password': 'ciqr lkjw wkhl omao', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rr8522782@gmail.com', 'password': 'dplk cbua worg hknf',
     'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sindhuaparna2005@gmail.com',
     'password': 'qtwg sovw lyfw foyj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aswingireesh0534@gmail.com',
     'password': 'fzck qhvg ugeb fqit', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'abhinavabhishek795@gmail.com',
     'password': 'bjux iosx nkza qtrw', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anandboss287@gmail.com',
     'password': 'kqit dwis zhiq pwkj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'manutomym@gmail.com',
     'password': 'toss ojsh tjnk gkto', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'amiyajose21@gmail.com', 'password': 'ynvk gyyt acio hhbs', 'to': to, 'subject': Subject}
]

# Example dynamic data
data_list = [
    ('Akshaya Edathottiyil Santhosh', 'Kannur', '', 'Sprechen', 'akshayaes132006@gmail.com'),
    ('Devananda Rajesh', 'Wayanad', '7902970175', 'sprechen', 'devanandarajesh27@gmail.com'),
    ('Karolina Jijo', 'Ernakulam', '8943690446', 'Sprechen', 'karolinajijo9c@gmail.com'),
    ('Shani joseph', 'Trivandrum', '7909103191', 'Sprechen', 'shanijoseph5197@gmail.com'),
    ('Sreelakshmi Vengamattathil Rajesh', 'Idukki', '6282578993', 'Sprechen', 'sreelakshmivr06@gmail.com'),
    ('Sherine Mathew', 'Kasaragod', '9947175672', 'Sprechen', 'sherin10414@gmail.com'),
    ('Niranjana John Christy', 'Idukki', '9497651820', 'Sprechen', 'johnniranjana2@gmail.com'),
    ('Sneha Satheesh', 'Idukki', '8075248308', 'Sprechen', 'snehasatheesh0839@gmail.com'),
    ('Ihsan kodali', 'Malapuram', '9633278218', 'Sprechen', 'ihsankodali112@gmail.com'),
    ('Ettiyedath madathil Ajikumar Gowrinanda', 'Ernakulam', '9847715466', 'Schreiben,Sprechen',
     'paruzzz1230@gmail.com'),
    ('Niranjan Bose', 'Thirssur', '6235131489', 'Schreiben,Sprechen', 'niranjanbose54@gmail.com'),
    ('Elmi Jaison', 'Ernakulam', '8590794660', 'Schreiben,Sprechen', 'elmyjaison@gmail.com'),
    ('Tom Jacob Vaidian', 'Kollam', '9847073301', 'Schreiben,Sprechen', 'tjacobvaidian@gmail.com'),
    ('Bessymol Joseph', 'Ernakulam', '9847614413', 'Schreiben,Sprechen', 'bessy.ambili@gmail.com'),
    ('Samitha Vazhekattil Saji', 'Thirssur', '6235551984', 'Lesen,Horen,Schrebien', 'samithaparasad1992@gmail.com'),
    ('Anusree Vaipilappallathu Mohanan', 'Ernakulam', '7306434570', 'Lesen,Schreiben', 'anusreenew5431@gmail.com'),
    ('Namitha Joji', 'Alappuzha', '8137823611', 'Hören,Schreiben', 'namithajoji59@gmail.com'),
    ('Milan Babu', 'Ernakulam', '9048955367', 'Schreiben', 'milanbabukalady@gmail.com'),
    ('Sangeetha Santhosh', 'Kottayam', '8139807205', 'Schreiben', 'sangeethasanthosh0186@gmail.com'),
    ('Remya Ranga', 'Kollam', '8547925342', 'Schreiben', 'rr8522782@gmail.com'),
    ('Aparna Suresh', 'Kottayam', '9074904899', 'Hören', 'sindhuaparna2005@gmail.com'),
    ('Aswin Girish', 'Ernakulam', '7356748862', 'Lesen,Hören', 'aswingireesh0534@gmail.com'),
    ('Abhinav vinod', 'Alappuzha', '7592828793', 'Lesen,Hören', 'abhinavabhishek795@gmail.com'),
    ('Anand Boss', 'Idukki', '8086013918', 'lesen, Schreiben', 'anandboss287@gmail.com'),
    ('Manu Tomy', 'Kannur', '9947322372', 'Sprechen', 'manutomym@gmail.com'),
    ('Amiya Jose', 'Kannur', '8301016065', 'sprechen', 'amiyajose21@gmail.com')
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
    schedule_time = "08:05:00"
    print(f"⏰ Scheduled to send emails at {schedule_time} every day to {to}.")

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == schedule_time:
            success = send_all_emails()
            if not success:
                print("⚠️ Some emails failed. Retrying in 10 seconds...")
                time.sleep(5)
                send_all_emails()  # retry failed ones
            time.sleep(1)
        time.sleep(0.5)
