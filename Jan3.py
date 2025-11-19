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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'snehasatheesh0839@gmail.com', 'password': 'khrt qwyp pcnj jkhb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sreelekshmikripa@gmail.com', 'password': 'wvgl zclu khoa gdbx', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'xavierancy95@gmail.com', 'password': 'bizl jvju vmso vxod', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'boneybenny2006off@gmail.com', 'password': 'owpk gyjp xewt emce', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'kasinaths467@gmail.com', 'password': 'lesi xbqo vhbi whop', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'anjanajose230@gmail.com', 'password': 'vmly pstv tubq fbuw', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'bijudiya47@gmail.com', 'password': 'zhgn lzln aigj zuev', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'marysania2004@gmail.com', 'password': 'ihqv eutl dxbu hudk', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'Joicyjoy906@gmail.com', 'password': 'iroc liqg rkme kyia', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rosemariyajince69@gmail.com', 'password': 'wsjc dqxk yrkf tfsb', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'minzxn9@gmail.com', 'password': 'dcxj mtrw oqsg bfin', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jissrosejayis@gmail.com', 'password': 'ocqg xsny wrfb vfyn', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'asinalna545@gmail.com', 'password': 'qfaz nxlr agjf udgc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aeinrose2233@gmail.com', 'password': 'ipir yocm lyan dkvi', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'treesahanna1308@gmail.com', 'password': 'bkdc hdgx ymph oxfm', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nayanaks0820@gmail.com', 'password': 'ubve nrfm xrpa bvlt', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jijikuriakosejoseph@gmail.com', 'password': 'bxry ladh hrwu xshd', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aswinisanthosh2007@gmail.com', 'password': 'pqjc lioe rlqa fzep', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'milulalu06@gmail.com', 'password': 'ubxc wnmy amkq usmv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'yuktha061@gmail.com', 'password': 'vqbh uuwc apcv vifo', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'delnaschalil02002@gmail.com', 'password': 'iyjr jcey ottx dcun', 'to': to, 'subject': Subject},

]

# Example dynamic data
data_list = [
    ('Sneha Satheesh', 'Idukki', '8075248308', 'Sprechen', 'snehasatheesh0839@gmail.com'),
    ('Sreelekshmi Aswin', 'Alappuzha', '8891788630', 'Sprechen', 'sreelekshmikripa@gmail.com'),
    ('Ancy Xavier', 'Ernakulam', '9747065301', 'Sprechen', 'xavierancy95@gmail.com'),
    ('Boney Benny', 'Kottayam', '9037548669', 'Sprechen', 'boneybenny2006off@gmail.com'),
    ('Kasinath Sreekumar', 'Kottaam', '8606855122', 'Sprechen', 'kasinaths467@gmail.com'),
    ('Anjana Jose', 'Ernakulam', '6282488448', 'Sprechen', 'anjanajose230@gmail.com'),
    ('Diya Biju', 'Kottayam', '9778206044', 'Schreiben,Sprechen', 'bijudiya47@gmail.com'),
    ('Mary Sania', 'Ernakulam', '9048918641', 'Schreiben,Sprechen', 'marysania2004@gmail.com'),
    ('Joicy Joy', 'Kannur', '7022573759', 'Sprechen', 'Joicyjoy906@gmail.com'),
    ('Rosemariya Jince', 'Idukki', '8590896760', 'Schreiben,Sprechen', 'rosemariyajince69@gmail.com'),
    ('Ameeliya Manthattil Abraham', 'Kannur', '7907334974', 'Lesen,Hören,Schreiben,Sprechen', 'minzxn9@gmail.com'),
    ('Jissrose Jayis Mekkunnel', 'Kannur', '8943441612', 'Lesen,Hören,Schreiben,Sprechen', 'jissrosejayis@gmail.com'),
    ('Asin Manoj Charuvelil Chacko', 'Kannur', '9747316809', 'Lesen,Hören,Schreiben,Sprechen', 'asinalna545@gmail.com'),
    ('Aein Rose John', 'Wayanad', '6238542906', 'Hören,Schreiben', 'aeinrose2233@gmail.com'),
    ('Treesahanna', 'Ernakulam', '8590964552', 'Schreiben', 'treesahanna1308@gmail.com'),
    ('Nayana Karupuzha Sunilkumar', 'Ernakulam', '9400366638', 'Schrieben', 'nayanaks0820@gmail.com'),
    ('Jiji Kalathimanthuruthil Kuriakose', 'Ernakulam', '8129190664', 'Lesen, Hören', 'jijikuriakosejoseph@gmail.com'),
    ('Aswini santhosh', 'Kottayam', '6235504550', 'Lesen', 'aswinisanthosh2007@gmail.com'),
    ('Milu Lalu', 'Kannur', '9961652916', 'schriben, hören', 'milulalu06@gmail.com'),
    ('Sreeyuktha Shaji', 'Ernakulam', '9061787553', 'Lesen, Hören', 'yuktha061@gmail.com'),
    ('Delna Shibu Chalil', 'Kannur', '98464 82170', 'Schreiben, Sprechen', 'delnaschalil02002@gmail.com'),

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
    schedule_time = "23:23:30"
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
