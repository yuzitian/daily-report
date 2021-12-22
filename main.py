import imaplib, email, yagmail, chardet, re
import time
import schedule
import datetime

user = "yuzitian2021@126.com"
password = "DBZNKPXSQHUIQLFO"

def pinjie(l):
    conn = imaplib.IMAP4_SSL("imap.126.com")
    conn.login(user, password)
    imap_id = ("name", "yuquan", "version", "1.0.0", "vendor", "myclient")
    typ, data = conn.xatom('ID', '("' + '" "'.join(imap_id) + '")')
    result, message = conn.select()

    a, b = conn.search(None, 'ALL')
    msgList = b[0].split()
    daliy_sum = []

    for i in range(len(msgList)):
        daliy_new1 = []
        type, datas = conn.fetch(msgList[i], '(RFC822)')
        msg = email.message_from_string(datas[0][1].decode("utf-8"))
        # print(msg)
        for part in msg.walk():
            if not part.is_multipart():
                head = part.get_content_type()
                if head == 'text/plain':
                    daliy = part.get_payload(decode=True)
                    y = chardet.detect(daliy)
                    daliy = daliy.decode(y['encoding'])
                    daliy_new = daliy.split('\n')
                    for flag1 in daliy_new:
                        test1 = re.search(l, flag1, flags=0)
                        if test1 != None:
                            for flag in daliy_new:
                                if flag != '\r':
                                    test = re.search("原始邮件", flag, flags=0)
                                    if test != None:
                                        break
                                    daliy_new1.append(flag)
                            if re.search('2764537595@qq.com', msg['From']) != None:
                                daliy_sum.append('yuquan:')
                            elif re.search('1437601610@qq.com', msg['From']) != None:
                                daliy_sum.append('lidan:')
                            elif re.search('qin.zhihui@qq.com', msg['From']) != None:
                                daliy_sum.append('zhihui')
                            elif re.search('473359330@qq.com', msg['From']) != None:
                                daliy_sum.append('tanpang')
                            elif re.search('1271545390@qq.com', msg['From']) != None:
                                daliy_sum.append('enhu')
                            elif re.search('905630160@qq.com', msg['From']) != None:
                                daliy_sum.append('linghui')
                            daliy_sum += daliy_new1
                            daliy_sum.append('----------------------\n')

    return '\n'.join(daliy_sum)

def job():
    global final
    yag = yagmail.SMTP( user="yuzitian2021@126.com", password="DBZNKPXSQHUIQLFO", host='smtp.126.com')
    contents = ['Please submit your daily report.']
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    final = 'Daily report' + now_time
    yag.send(['1316367833@qq.com', '473359330@qq.com', '2764537595@qq.com', '1271545390@qq.com', '1437601610@qq.com', '905630160@qq.com'], final, contents)

def job1():
    global final
    yag = yagmail.SMTP( user="yuzitian2021@126.com", password="DBZNKPXSQHUIQLFO", host='smtp.126.com')
    contents = pinjie(final)
    now_time1 = datetime.datetime.now().strftime('%Y-%m-%d')
    dayOfWeek = datetime.datetime.now().isoweekday()
    title = now_time1 + ' ' + '星期' + str(dayOfWeek) + ' ' + 'daily report'
    yag.send(['1316367833@qq.com', '473359330@qq.com', '2764537595@qq.com', '1271545390@qq.com', '1437601610@qq.com', '905630160@qq.com', 'liuxiaotong@88.com', 'ytyangmei@bistu.edu.cn', 'tongq85@bistu.edu.cn'], title, contents)

schedule.every().day.at("16:00").do(job)
schedule.every().day.at("05:00").do(job1)
#schedule.every().day.at("10:30").do(job)
#schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1000)
