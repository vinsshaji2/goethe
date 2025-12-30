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
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rosemolfrancis105@gmail.com', 'password': 'lope nurm wkai luga', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'rosemariyabiju55@gmail.com', 'password': 'ckdy ykxa rkbs fhue', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'zardra958@gmail.com', 'password': 'byzw uxbo zhfs fmks', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'angelmariyajose2006@gmail.com', 'password': 'dssm bxgo ghql buzv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'Karolinajijo9c@gmail.com', 'password': 'yaiw ydvy hkpq ceuc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'ambikakumary01@gmail.com', 'password': 'foij xyfv gyva tame', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'riyaannpaul562@gmail.com', 'password': 'swzo ofzo pwqu vfoa', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'marysania2004@gmail.com', 'password': 'nbtd sikz ltqv rqts', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'parvathysnair1007@gmail.com', 'password': 'jrid jxgr buxz rvol', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sudinakgsudinakg@gmail.com', 'password': 'ucjw dpra scpu vpde', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sinchukg14@gmail.com', 'password': 'wfrv addb ladt bxsj', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'vaikendhukv@gmail.com', 'password': 'gxdd jimw ddqy rwzt', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'jizamariyajoy@gmail.com', 'password': 'lbrx bwlv spug tzgl', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'nivyashaju@gmail.com', 'password': 'wzzj guaq mfxd ixly', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'michaelBinoy2005@gmail.com', 'password': 'trmh ymwr nvod hwxt', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'lijocharly7@gmail.com', 'password': 'swgq ipwq ffqy frcf', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'staniyathomas43@gmail.com', 'password': 'irpi anjt xbor ocpv', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'donamariathomas86@gmail.com', 'password': 'tvdc kbex whet hcdg', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'aparnatr731@gmail.com', 'password': 'papa nlah ptzy wvoc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'sanjusebastian010@gmail.com', 'password': 'vknd kinl bizj vmsr', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'smaria15920@gmail.com', 'password': 'bays yxco cdcs jdwd', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'annaanit841@gmail.com', 'password': 'eyci tprs vhmp ezco', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'shanijoseph5197@gmail.com', 'password': 'lwuv ajax cepp genc', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'blessyb567@gmail.com', 'password': 'iaew ryqh pxoc emzd', 'to': to, 'subject': Subject},
    {'smtp_server': 'smtp.gmail.com', 'port': 587, 'username': 'akshaya63vs@gmail.com', 'password': 'xyvi rhnd gfcy whsu', 'to': to, 'subject': Subject}


]

# Example dynamic data
data_list = [
    ('Rosemol Francis', 'Thrissur', '9074121986', 'sprechen', 'rosemolfrancis105@gmail.com'),
    ('Rose Mariya Biju', 'Ernakulam', '9447093069', 'Sprechen', 'rosemariyabiju55@gmail.com'),
    ('Ardra Meenakumary Suseelan Pillai', 'Kollam', '9995224065', 'Sprechen', 'zardra958@gmail.com'),
    ('Angel Mariya Jose', 'Idukki', '9747837288', 'Sprechen', 'angelmariyajose2006@gmail.com'),
    ('Karolina Jijo', 'Ernakulam', '8943690446', 'Sprechen', 'Karolinajijo9c@gmail.com'),
    ('Adithya Raghunathakurup', 'Kollam', '8590164305', 'Sprechen', 'ambikakumary01@gmail.com'),
    ('Riya Ann Paul', 'Idukki', '7012802060', 'Sprechen', 'riyaannpaul562@gmail.com'),
    ('Mary Sania', 'Ernakulam', '9048918641', 'Schreiben,Sprechen', 'marysania2004@gmail.com'),
    ('Parvathy SureshKumar Nair', 'Kottayam', '9207138529', 'Schreiben,Sprechen', 'parvathysnair1007@gmail.com'),
    ('Sudina Kudali George', 'Chikkamagaluru', '8618953374', 'Schreiben,Sprechen', 'sudinakgsudinakg@gmail.com'),
    ('Sinchana Kudalihouse George', 'Chikkamagaluru', '8296271967', 'Schreiben,Sprechen', 'sinchukg14@gmail.com'),
    ('Vaikendhu Krishnakripa Vinodkumar', 'Wayanad', '8590961804', 'Schreiben,Sprechen', 'vaikendhukv@gmail.com'),
    ('Jiza Mariya Joy', 'Kannur', '7306679472', 'Schreiben,Sprechen', 'jizamariyajoy@gmail.com'),
    ('Nivya Shaju', 'Ernakulam', '8078356229', 'lesen,Hören,Schreiben,Sprechen', 'nivyashaju@gmail.com'),
    ('Michael Binoy', 'Kottayam', '9778742501', 'Lesen,Sprechen', 'michaelBinoy2005@gmail.com'),
    ('Lijo Charly', 'Kottayam', '7907382805', 'Lesen,Hören,Sprechen', 'lijocharly7@gmail.com'),
    ('Staniya Thomas', 'Idukki', '8547503947', 'Lesen,Schreiben', 'staniyathomas43@gmail.com'),
    ('Dona Maria Thomas', 'Idukki', '8075710580', 'Lesen,Schreiben', 'donamariathomas86@gmail.com'),
    ('Aparna Thaikoottathil Rejimon', 'Alappuzha', '9400594614', 'Schreiben', 'aparnatr731@gmail.com'),
    ('Sanju Sebastian', 'Alappuzha', '6282840703', 'Schreiben', 'sanjusebastian010@gmail.com'),
    ('Sandra Maria Roy', 'Kollam', '8137033547', 'Schreiben', 'smaria15920@gmail.com'),
    ('Anit Baby', 'Idukki', '6282266481', 'Schreiben', 'annaanit841@gmail.com'),
    ('Shani Joseph', 'Thiruvananthapuram', '7909103191', 'Hören', 'shanijoseph5197@gmail.com'),
    ('Blessy Babu', 'Idukki', '9778214305', 'Lesen', 'blessyb567@gmail.com'),
    ('Akshaya Valodithara Suresh', 'Alappuzha', '6238871605', 'Sprechen', 'akshaya63vs@gmail.com')

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
    schedule_time = "22:38:50"
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
