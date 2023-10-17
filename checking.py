import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json

# Load configuration from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Configuration
smtp_host = config['smtp_host']  # SMTP server hostname
smtp_port = config['smtp_port']  # SMTP server port
smtp_user = config['smtp_user']  # SMTP server username
smtp_password = config['smtp_password']  # SMTP server password
from_email = config['from_email']  # Sender's email address
to_email = config['to_email'] # Recipient's email address
checkin_file = config['checkin_file'] # File path for check-in timestamp
counter_file = config['counter_file'] # File path for email counter
DAYS_REMINDER = config['DAYS_REMINDER'] # Days for the reminder period
DAYS_DEADMAN = config['DAYS_DEADMAN'] # Days for the dead man's switch
SECONDS_IN_A_DAY = config['SECONDS_IN_A_DAY'] # Number of seconds in a day
count_sent_mail = config['count_sent_mail'] # Number of dead man mails to send after activation.

family_members = config['family_members'] # List of family members' email addresses

# Email content
reminder_subject = config['reminder_subject'] # Subject for the reminder email
reminder_message = config['reminder_message'] # Message for the reminder email

dead_man_activation_subject = config['dead_man_activation_subject'] # Subject for the activation email
dead_man_activation_message = config['dead_man_activation_message'] # Message for the activation email

dead_man_subject = config['dead_man_subject'] # Subject for the dead man's switch email
dead_man_message = config['dead_man_message'] # Message for the dead man's switch email
files_to_attach = config['files_to_attach'] # List of files to attach

# Function to send an email
def send_email(subject, message, to, attachments=[]):
    s = smtplib.SMTP(host=smtp_host, port=smtp_port)
    s.starttls()
    s.login(smtp_user, smtp_password)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    for file in attachments:
        with open(file, 'rb') as file_in:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file_in.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={file}")
            msg.attach(part)

    s.send_message(msg)
    s.quit()

# Function to execute the dead man's switch
def execute_deadman_switch():
    try:
        with open(counter_file, "r") as file:
            counter = int(file.read())
    except FileNotFoundError:
        counter = 0

    if counter < count_sent_mail:
        send_email(dead_man_subject, dead_man_message, ', '.join(family_members), files_to_attach)
        
        with open(counter_file, "w") as file:
            file.write(str(counter + 1))

# Function to check the dead man's switch
def check_deadman():
    with open(checkin_file, "r") as file:
        last_checkin_time = float(file.read().strip())

    time_difference = time.time() - last_checkin_time

    if time_difference > DAYS_REMINDER * SECONDS_IN_A_DAY:
        if time_difference > DAYS_DEADMAN * SECONDS_IN_A_DAY:
            send_email(dead_man_activation_subject, dead_man_activation_message, to_email)
            execute_deadman_switch()
        else:
            send_email(reminder_subject, reminder_message, to_email)

if __name__ == '__main__':
    check_deadman()
