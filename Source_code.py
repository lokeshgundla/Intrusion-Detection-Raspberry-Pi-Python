import RPi.GPIO as GPIO
import time
from datetime import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from email.MIMEImage import MIMEImage
import os
#for SMS client
import nexmo

gmail_user = "#############" #Sender email address
gmail_pwd = "############" #Sender email password
to = '' #Receiver email address
subject = 'Security Breach'
text= 'There is some activity in your home.'

sensor = 2

# Set up the door sensor pin.
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, pull_up_down = GPIO.PUD_UP)


current_state = False


def Function(x):
        if(x == True):
                print ('###########################Door is Open')
                client = nexmo.Client(key='################', secret='###########')
                client.send_message({
                        'from': '##########',
                        'to': '#############',
                        'text': 'INTRUDER ALERT!!!',
                        })

                os.system("fswebcam test.jpg")


                msgRoot = MIMEMultipart('related')
                msgRoot['Subject'] = subject
                msgRoot['From'] = gmail_user
                msgRoot['To'] = to
                msgRoot.preamble = 'This is a multi-part message in MIME format.'

                msgAlternative = MIMEMultipart('alternative')
                msgRoot.attach(msgAlternative)

                msgText = MIMEText('This is the alternative plain text message.')
                msgAlternative.attach(msgText)

                msgText = MIMEText('<b>There is some activity in your room</b> and here is a snap of it.<br><img src="cid:image1"><br>Something CREEPY!!!', 'html')
                msgAlternative.attach(msgText)


                fp = open('test.jpg', 'rb')
                msgImage = MIMEImage(fp.read())
                fp.close()


                msgImage.add_header('Content-ID', '<image1>')
                msgRoot.attach(msgImage)

                print "Sending email"
                mailServer = smtplib.SMTP('smtp.gmail.com', 587)
                mailServer.ehlo()
                mailServer.starttls()
                mailServer.ehlo()
                mailServer.login(gmail_user, gmail_pwd)
                mailServer.sendmail(gmail_user, to, msgRoot.as_string())
                mailServer.quit()
                print "Email Sent"
        else:
                print("##########################Don't worry Door is closed back")


#for checking state of the sensor continuosly 
m=0
n=0
while True:
        current_state = GPIO.input(sensor)
        if current_state==True and m == 0:
                Function(current_state)
                n=0
                m=m+1
        if current_state==False and n == 0:
                Function(current_state)
                m=0
                n=n+1
        time.sleep(2)

