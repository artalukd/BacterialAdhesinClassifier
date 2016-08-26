import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import socket

def sendMail(toaddr, filename, path):
    fromaddr = 'adhesin.niced@gmail.com'
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "BIC-NICED: Adhesin Prediction Result"
    body = "Please find your results file in attachment."
    msg.attach(MIMEText(body, 'plain'))
     
    with open(os.path.join(path, filename)+".txt", 'r') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment", filename = "Adhesin Prediction Results.csv")
        msg.attach(part)
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "niced123")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
