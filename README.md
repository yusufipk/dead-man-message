# Dead Man's Switch Python Script

This Python script provides a Dead Man's Switch functionality that sends reminder and activation emails based on a specified time interval.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Customization](#customization)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## Prerequisites

Before using the script, you need to have the following prerequisites in place:

- Python 3 installed on your system.
- Access to an SMTP server with the necessary credentials.
- Necessary files:
  - `checkin_file.txt`: A file to store the last check-in timestamp.
  - `counter_file.txt`: A file to keep track of the number of sent emails.

## Configuration

You need to configure the config.json file with your SMTP server settings and email details. Open the config file and modify the following variables:

- `config.json`: JSON configuration file containing the following settings:
  - `smtp_host`: SMTP server hostname.
  - `smtp_port`: SMTP server port.
  - `smtp_user`: Your SMTP server username.
  - `smtp_password`: Your SMTP server password.
  - `from_email`: Your email address (the sender).
  - `to_email`: Recipient's email address.
  - `checkin_file`: Path to the check-in timestamp file.
  - `counter_file`: Path to the email counter file.
  - `DAYS_REMINDER`: Number of days for the reminder period.
  - `DAYS_DEADMAN`: Number of days for the Dead Man's Switch activation.
  - `SECONDS_IN_A_DAY`: Number of seconds in a day.
  - `count_sent_mail`: Number of dead man mails to send after activation.
  - `family_members`: List of family members' email addresses.
  - `files_to_attach`: List of files to attach to the emails.

## Customization

You can customize the email content by modifying the following variables in the config:

- `reminder_subject`: Subject for the reminder email.
- `reminder_message`: Message for the reminder email.
- `dead_man_activation_subject`: Subject for the Dead Man's Switch activation email.
- `dead_man_activation_message`: Message for the Dead Man's Switch activation email.

## Usage

1. Ensure that you have met the prerequisites and configured the script as described above.

2. Run the script using Python:

   ```shell
   python checking.py
   ```
3.  The script will check if a check-in is required based on the specified time intervals. It will send reminder emails if necessary and activate the Dead Man's Switch if the activation time has passed.
    
4.  The Dead Man's Switch activation email will be sent to the specified recipients with attached files.
## Contributors

- [Yusuf İpek](https://github.com/yusufipk)
- [Koray Üstündağ](https://github.com/korayustundag)
- [Mugo Squero](https://github.com/MugoSquero)
## License

This script is provided under the GPL-3.0 License. You are free to use, modify, and distribute it as needed. See the [LICENSE](https://github.com/yusufipk/dead-man-message/blob/master/LICENSE) file for details.
