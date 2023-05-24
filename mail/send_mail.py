import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, recipient_email, subject, message):
    
    smtp_server = 'smtp-mail.outlook.com'  
    smtp_port = 587  
    smtp_username = sender_email  

    # MIME multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # message body
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, sender_password)
 
    # Send the email
    server.send_message(msg)

    print('book rental is expiring email sent')
    # Disconnect from the server
    server.quit()


