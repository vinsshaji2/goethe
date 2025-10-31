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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'snehamariya935@gmail.com', 'password': 'codq vzmc dish bpts', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rosmipj1998@gmail.com', 'password': 'rkpu ualy sztt vhqc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'thomasamareena@gmail.com', 'password': 'wnvu xmpn hhzs gofa', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ihsankodali112@gmail.com', 'password': 'bwnr sbao xsti qqcs', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aravindrnair2552@gmail.com', 'password': 'maox foeu cbju fghu', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'www.georgia733@gmail.com', 'password': 'ylwy acam pkbl xqaj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nimishaeo2001@gmail.com', 'password': 'ngxq ixjx bsfj tzrb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'abhinandaharip@gmail.com', 'password': 'lsrj vxob uxfn sxfw', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjanakummath2007@gmail.com', 'password': 'olpx snab cuts cncm', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'niranjanbose54@gmail.com', 'password': 'gsnk hlpu juln tltv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aswingireesh0534@gmail.com', 'password': 'lepq lpcu rwzk wsrh', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'stellaluna2255@gmail.com', 'password': 'iicy ymqs nuyo vbfd', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rosemolfrancis105@gmail.com', 'password': 'htpn beum qepx gjqk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sinukvarughese44@gmail.com', 'password': 'khhu nghu bqoh swld', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'mohammedroshan.com@gmail.com', 'password': 'dnko uhtz lqpt csck', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'remyabalag@gmail.com', 'password': 'wxdd mgxp npoo pmry', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'kasinaths467@gmail.com', 'password': 'gatu qneu mzur vejy', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nandhunandhana354@gmail.com', 'password': 'xnqr hdmp qfea bjyj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'adithkrishnakj249@gmail.com', 'password': 'vznx xsxi qtql ntby', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'stephytitty18@gmail.com', 'password': 'usmv tokg wujg ovfc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rajeevameya625@gmail.com', 'password': 'qnju xgmp hyes buod', 'to': to, 'subject': Subject},

]

# Example dynamic data
data_list = [
    ('Sneha Mariya Tellus', 'Kollam', '7736053276', 'Sprechen', 'snehamariya935@gmail.com'),
    ('Rosmi Pulikkottil Jose', 'Thrissur', '7306035192', 'Sprechen', 'rosmipj1998@gmail.com'),
    ('Amareena Thomas', 'Ernakulam', '9037685991', 'Sprechen', 'thomasamareena@gmail.com'),
    ('Ihsan kodali', 'Malappuram', '9633278218', 'Sprechen', 'ihsankodali112@gmail.com'),
    ('Aravind Raveendran Nair', 'Kottayam', '6282997753', 'Sprechen', 'aravindrnair2552@gmail.com'),
    ('Georgia George', 'Idukki', '8590855538', 'Sprechen', 'www.georgia733@gmail.com'),
    ('Nimisha Elanjikkaparambu Omanakuttan', 'Ernakulam', '7994164030', 'Sprechen', 'nimishaeo2001@gmail.com'),
    ('Abhinanda Pulikkathara', 'Kozhikode', '9746567187', 'Sprechen', 'abhinandaharip@gmail.com'),
    ('Anjana Kummath', 'Malappuram', '9633796260', 'Sprechen', 'anjanakummath2007@gmail.com'),
    ('Niranjan Bose', 'Thrissur', '6235131489', 'Schreiben,Sprechen', 'niranjanbose54@gmail.com'),
    ('Aswin Girish', 'Ernakulam', '7356748862', 'Schreiben,Sprechen', 'aswingireesh0534@gmail.com'),
    ('Merin Anna Moncy', 'Kottayam', '7025799779', 'Schreiben,Sprechen', 'stellaluna2255@gmail.com'),
    ('Rosemol Francis', 'Thrissur', '9074121986', 'Schreiben,Sprechen', 'rosemolfrancis105@gmail.com'),
    ('Sinu Kaleeckal Varughese', 'Pathanamthitta', '9526336151', 'Lesen,Hören,Schreiben', 'sinukvarughese44@gmail.com'),
    ('Mohammed Roshan Kannangadan', 'Malapuram', '7994801100', 'Lesen,Schreiben', 'mohammedroshan.com@gmail.com'),
    ('Remya Ramachandran Nair', 'Kottayam', '8547895155', 'Schreiben', 'remyabalag@gmail.com'),
    ('Kasinath Sreekumar', 'Kottayam', '8606855122', 'Schreiben', 'kasinaths467@gmail.com'),
    ('Nandhana Perumparambil Sunil', 'Thrissur', '7034980404', 'Schreiben', 'nandhunandhana354@gmail.com'),
    ('Adith Krishna Karuthara Jayan', 'Ernakulam', '6238003816', 'Lesen', 'adithkrishnakj249@gmail.com'),
    ('Stephy Chacko Sabu', 'Alappuzha', '6282046574', 'Lesen, Hören', 'stephytitty18@gmail.com'),
    ('Ameya Rajeev', 'Alappuzha', '9746433510', 'Lesen, Hören', 'rajeevameya625@gmail.com'),

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
    schedule_time = "21:13:20"
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
