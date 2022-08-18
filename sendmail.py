import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(mail_title, mail_body, receiver):
    sender = 'XXX@XXX.com'
    smtpServer = 'smtp.XXX.com'
    username = 'XXX'
    password = 'XXX'

    message = MIMEText(mail_body, 'plain', 'utf-8')
    message["Accept-Language"] = "zh-CN"
    message["Accept-Charset"] = "ISO-8859-1,utf-8"
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = Header(mail_title, 'utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpServer)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, message.as_string())
        print('邮件发送成功')
        smtp.quit()
    except smtplib.SMTPException:
        print("邮件发送失败")


if __name__ == '__main__':
    send_email("test", "test", "zhangshanbeng@gmail.com")
