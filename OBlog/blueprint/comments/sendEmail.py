import smtplib
from email.mime.text import MIMEText
from email.header import Header

from ..admin.main import getSiteConfigDict


def localSMTP():
    smtpObj = smtplib.SMTP('localhost')
    return smtpObj


def thirdSMTP(_host, _user, _password, _port=25):
    smtpObj = smtplib.SMTP_SSL(_host, _port)
    print("connecting...")
    smtpObj.connect(_host, _port)
    print("loging...")
    smtpObj.login(_user, _password)
    return smtpObj


def sendEmail(_from, _fromname, _to, _toname, _subject, _message, _smtp):

    message = MIMEText(_message, 'html', 'utf-8')
    message['From'] = Header(_fromname, 'utf-8')
    message['To'] = Header(_toname, 'utf-8')
    message['Subject'] = Header(_subject, 'utf-8')

    print('\n【sendemail】 from:%s(%s) to:%s(%s) subject:%s message:%s'
          % (_from, _fromname, _to, _toname, _subject, _message))
    try:
        _smtp.sendmail(_from, _to, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def Email(_to, _toname, _subject, _message):
    config = getSiteConfigDict()
    if config['smtp']['value'] == '1':
        sendEmail(config['smtpemail']['value'], config['smtpemail']['value'],
                  _to,  _toname,
                  _subject, _message,
                  thirdSMTP(config['smtpservice']['value'], config['smtpuser']['value'],
                            config['smtppassword']['value'], config['smtpport']['value']))


if __name__ == '__main__':
    TencentExMail = thirdSMTP("smtp.exmail.qq.com",
                              "", "", 465)
    sendEmail("oyohyee@oyohyee.com", "oyohyee@oyohyee.com",
              ["oyohyee@oyohyee.com"], "896817156",
              "测试", "<a href='www.oyohyee.com'>OhYee</a>",
              TencentExMail)
