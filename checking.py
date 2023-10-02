import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Necessary files. You should create these.
checkin_file = "./checkin_file.txt"  # replace with your checkin file path
counter_file = "./counter_file.txt" # this is needed to stop spamming mails to the loved ones
count_sent_mail = 7

DAYS_REMINDER = 25  # Modify these as per your need
DAYS_DEADMAN = 30  # Modify these as per your need
SECONDS_IN_A_DAY = 86400  # No need to modify this

# Replace these with your SMTP settings and email
smtp_host = 'your_smpt_server'
smtp_port = 587 
smtp_user = 'username'
smtp_password = 'password'

# Reminder message
from_email = 'coming_from'
to_email = 'going_to'

#Dead man message
family_members = ['mail@example.com']  # You can specify multiple email ids separated by commas
message = "I'm dead"
files_to_attach = ['file.gpg']  # specify your files
dead_man_subject = "I Am Gone"

def send_email(subject, message):
    # Setup smtp
    s = smtplib.SMTP(host=smtp_host, port=smtp_port)
    s.starttls()
    s.login(smtp_user, smtp_password)

    # Create message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # Send the email
    s.send_message(msg)
    del msg

    s.quit()


def execute_deadman_switch():
    # check if counter file exists
    try:
        with open(counter_file, "r") as file:
            counter = int(file.read())
    except FileNotFoundError:
        counter = 0

    if counter < count_sent_mail:
        s = smtplib.SMTP(host=smtp_host,  port=smtp_port)
        s.starttls()
        s.login(smtp_user,  smtp_password)

        msg = MIMEMultipart()

        msg['From'] = from_email
        msg['To'] = ', '.join(family_members)
        msg['Subject'] = dead_man_subject

        msg.attach(MIMEText(message,  'plain'))

        # Attach multiple files
        for file in files_to_attach:
            with open(file, 'rb') as file_in:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file_in.read())

            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {file}")
            msg.attach(part)

        # Send the email
        s.send_message(msg)
        del msg

        s.quit()

        # increment counter and write to file
        with open(counter_file, "w") as file:
            file.write(str(counter +  1))

def check_deadman():
    with open(checkin_file, "r") as file:
        last_checkin_time = float(file.read().strip())

    time_difference = time.time() - last_checkin_time

    if time_difference > DAYS_REMINDER * SECONDS_IN_A_DAY:

        if time_difference > DAYS_DEADMAN * SECONDS_IN_A_DAY:
            send_email("Dead Man's Switch Activated", "You forgot to check-in")
            execute_deadman_switch()

        else:
            send_email("REMINDER", "Please check-in")


if __name__ == '__main__':
    check_deadman()
