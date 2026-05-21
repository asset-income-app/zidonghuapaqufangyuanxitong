import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
import os


class EmailNotifier:
    def __init__(self, smtp_server: str, smtp_port: int, 
                 sender_email: str, sender_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_notification(self, to_emails: List[str], subject: str, 
                         body: str, attachment_path: Optional[str] = None):
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = ', '.join(to_emails)
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain', 'utf-8'))

        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                message.attach(part)

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(message)
            server.quit()
            print(f"[邮件] 已发送通知邮件到 {', '.join(to_emails)}")
            return True
        except Exception as e:
            print(f"[邮件] 发送失败: {e}")
            return False

    def send_crawl_report(self, to_emails: List[str], stats: dict, 
                         file_path: Optional[str] = None):
        subject = f"房源爬取报告 - {stats.get('爬取时间', '未知时间')}"

        body = f"""
三亚房源爬取报告
{'='*50}

爬取时间: {stats.get('爬取时间', '未知')}
总房源数: {stats.get('总房源数', 0)}
平均价格: {stats.get('平均总价(万)', 0):.2f} 万元
最低价格: {stats.get('最低总价(万)', 0):.2f} 万元
最高价格: {stats.get('最高总价(万)', 0):.2f} 万元
平均面积: {stats.get('平均面积(㎡)', 0):.2f} ㎡

各区域房源数:
{self._format_dict(stats.get('各区域房源数', {}))}

各网站房源数:
{self._format_dict(stats.get('各网站房源数', {}))}

{'='*50}
此邮件由系统自动发送，请勿回复。
        """

        return self.send_notification(to_emails, subject, body, file_path)

    def _format_dict(self, data: dict) -> str:
        if not data:
            return "暂无数据"

        lines = []
        for key, value in data.items():
            lines.append(f"  {key}: {value}")
        return '\n'.join(lines)
