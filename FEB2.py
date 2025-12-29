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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'dvndu3@gmail.com', 'password': 'mkob xgbv ivbe hpxq', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sonajinish@gmail.com', 'password': 'pbqh mbbt auuv qqqs', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'gracemonchristopher@gmail.com', 'password': 'oyhy iymq rwhh odmp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'alintageorge2001@gmail.com', 'password': 'rrka bjij oczt fuhp', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'swetha6629@gmail.com', 'password': 'nemd jhmr wriu cjuu', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'mohananarchana098@gmail.com', 'password': 'qjgh fkyo pncp kero', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjalijoseph587@gmail.com', 'password': 'pnwz fxmo xafy lbtz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jenifersebastian0@gmail.com', 'password': 'jmvt iqwx qvzv hzrb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rincybaby90@gmail.com', 'password': 'cpqm horn aeym ltkk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aleenaelizabethbabu261@gmail.com', 'password': 'eutt oxlp scxs vwwx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aswinisanthosh2007@gmail.com', 'password': 'oalt vbno xosf cjsi', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jelittajose7902@gmail.com', 'password': 'duft afck wikl yigz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'deolabhram001@gmail.com', 'password': 'giyj hgxn dvue dghc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bisminsafriya@gmail.com', 'password': 'vszf drcd cxgb gjfs', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'diyashaji49251@gmail.com', 'password': 'oqsd ngwf xmby wyda', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aswathimp003@gmail.com', 'password': 'aask lwny ainc rgth', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'krishnabindhunegil@gmail.com', 'password': 'qgdm ubnc lgtj mqmw', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'poornimakp12@gmail.com', 'password': 'vdeg mgft ydkr btli', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nibumathew224@gmail.com', 'password': 'qnak nrqb xgnu ffeh', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ihsankodali112@gmail.com', 'password': 'obzk xpuj iynl tthi', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'meenakshikp379@gmail.com', 'password': 'frqx eooh atbo jlwz', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sonamolsaji98@gmail.com', 'password': 'dfnx guwn qvcl ulqv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annmariyatenson651@gmail.com', 'password': 'lvwx jllg vdyt tqqi', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rinzilasaleem1@gmail.com', 'password': 'bcja iznc qyyd fsam', 'to': to, 'subject': Subject},

]

# Example dynamic data
data_list = [
    ('Deveendu Poothamveettil Thambi', 'Thrissur', '6238166159', 'Sprechen', 'dvndu3@gmail.com'),
    ('Sona Jinish', 'Kannur', '9961102617', 'Sprechen', 'sonajinish@gmail.com'),
    ('Gracemon Christopher', 'Alappuzha', '7558921136', 'Sprechen', 'gracemonchristopher@gmail.com'),
    ('Alinta George', 'Kannur', '9744389877', 'Schreiben', 'alintageorge2001@gmail.com'),
    ('Swetha Divakara', 'Kasaragod', '9497302949', 'Sprechen', 'swetha6629@gmail.com'),
    ('Archana Mohanan', 'Kannur', '9544488469', 'Schreiben,Sprechen', 'mohananarchana098@gmail.com'),
    ('Anjaly Joseph', 'Ernakulam', '9544573821', 'Schreiben,Sprechen', 'anjalijoseph587@gmail.com'),
    ('Jenifer Sebastian', 'Alappuzha', '8594026311', 'Schreiben,Sprechen', 'jenifersebastian0@gmail.com'),
    ('Rincy Baby', 'Kollam', '9061926682', 'Schreiben,Sprechen', 'rincybaby90@gmail.com'),
    ('Aleena Elizabeth Babu', 'Kottayam', '7034689320', 'Schreiben,Sprechen', 'aleenaelizabethbabu261@gmail.com'),
    ('Aswini Santhosh', 'Kottayam', '6235504550', 'Hören,Sprechen', 'aswinisanthosh2007@gmail.com'),
    ('Jelitta Jose', 'Idukki', '9188453707', 'Lesen,Hören,Schreiben,Sprechen', 'jelittajose7902@gmail.com'),
    ('Deol Abraham', 'Ernakulam', '9207937530', 'Lesen,Schreiben,Sprechen', 'deolabhram001@gmail.com'),
    ('Bismin Safriya Shajahan', 'Ernakulam', '8848281770', 'Lesen,Sprechen', 'bisminsafriya@gmail.com'),
    ('Diya Shaji', 'Ernakulam', '9562867192', 'Hören,Sprechen', 'diyashaji49251@gmail.co'),
    ('Aswathi Manoj', 'Idukki', '7559924532', 'Hören,Schreiben', 'aswathimp003@gmail.com'),
    ('Krishna Bindhu Negil', 'Kollam', '8590408807', 'Hören,Schreiben', 'krishnabindhunegil@gmail.com'),
    ('Poornima Kottampadam Pradeep', 'Kottayam', '8714457563', 'Schreiben', 'poornimakp12@gmail.com'),
    ('Nibu Mathew', 'Kottayam', '9072069418', 'Schreiben', 'nibumathew224@gmail.com'),
    ('Ihsan Kodali', 'Malappuram', '9633278218', 'Schreiben', 'ihsankodali112@gmail.com'),
    ('Meenakshi Kallayil Prabin', 'Trissur', '6282240548', 'Schreiben', 'meenakshikp379@gmail.com'),
    ('Sonamol Saji', 'Idukki', '9778570668', 'Lesen', 'sonamolsaji98@gmail.com'),
    ('Ann Mariya Tenson', 'Ernakulam', '9946920159', 'Lesen, Hören', 'annmariyatenson651@gmail.com'),
    ('Rinzila Mohammad Saleem', 'Palakkad', '7902445774', 'Schreiben', 'rinzilasaleem1@gmail.com')
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
    schedule_time = "22:39:20"
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
