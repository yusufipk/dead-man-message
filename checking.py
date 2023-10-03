import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Configuration
smtp_host = 'your_smpt_server'  # SMTP server hostname
smtp_port = 587  # SMTP server port
smtp_user = 'username'  # SMTP server username
smtp_password = 'password'  # SMTP server password
from_email = 'coming_from'  # Sender's email address
to_email = 'going_to'  # Recipient's email address
checkin_file = "./checkin_file.txt"  # File path for check-in timestamp
counter_file = "./counter_file.txt"  # File path for email counter
DAYS_REMINDER = 25  # Days for the reminder period
DAYS_DEADMAN = 30  # Days for the dead man's switch
SECONDS_IN_A_DAY = 86400  # Number of seconds in a day
count_sent_mail = 7  # Number of dead man mails to send after activation.

family_members = ['mail@example.com']  # List of family members' email addresses

# Email content
reminder_subject = "REMINDER"  # Subject for the reminder email
reminder_message = "Please check-in"  # Message for the reminder email

dead_man_activation_subject = "Dead Man's Switch Activated" # Subject for the activation email
dead_man_activation_message = "You forgot to check-in" # Message for the activation email

dead_man_subject = "I Am Gone"  # Subject for the dead man's switch email
dead_man_message = "I'm dead"  # Message for the dead man's switch email
files_to_attach = ['file.gpg']  # List of files to attach

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
