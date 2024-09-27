# Enable IMAP access in your Gmail account settings
# https://mail.google.com/mail/u/0/#settings/fwdandpop

import imaplib
import email
from collections import defaultdict
import email.header
from email.header import decode_header


# Gmail account credentials
username = input("Enter your Username :")
# Note : Do not use your Own Gmail password , use the app generated password. More info in Readme.md
password = input("Enter your Password :")

print("Valid Gmail account credentials")

# IMAP server settings
imap_server = "imap.gmail.com"
imap_port = 993
print("Login Success to Server ")



# Connect to IMAP server
mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(username, password)
mail.select("inbox")
print("Login Success to Gmail account")
print("Inbox is Selected")

# Search for all emails

# status, response = mail.search(None, "ALL")  # Search for all emails in the inbox
# status, response = mail.search(None, 'UNSEEN')
# status, response = mail.search(None, 'FROM', 'marketing@engage.canva.com')
status, response = mail.search(None, 'FROM', 'noreply@waveroom.com')

print("Searching for mails in Inbox")

# Get email IDs
email_ids = response[0].split()

# Create a dictionary to store emails by domain
emails_by_domain = defaultdict(list)

print(" Loop through each email")
# Loop through each email
for email_id in email_ids:
    status, msg = mail.fetch(email_id, "(RFC822)")
    raw_email = msg[0][1]

    # Parse email using email library
    email_message = email.message_from_bytes(raw_email)

    # Extract domain from From address
    from_addr = email_message["From"]
    domain = from_addr.split("@")[-1]

    # Decode the subject line
    subject, encoding = decode_header(email_message["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding) if encoding else subject.decode('utf-8')


    # Add email to dictionary by domain
    emails_by_domain[domain].append({
        "Subject": subject,
        "From": from_addr
    })

print("Printing Emailsby Domain")
# Print emails by domain
for domain, emails in emails_by_domain.items():
    print(f"Domain: {domain}")
    for email in emails:
        print(f"  Subject: {email['Subject']}, From: {email['From']}")
    print("")

print("\n")

print("Printing All Email Domains")

for domain, emails in emails_by_domain.items():
    print(f"Domain: {domain}")


print("\n")

print("Deleting emails from specific domain")
# Domain to delete
sender = input("Enter domain name to delete:")

# Search for emails from sender
status, response = mail.search(None, f'(FROM "{sender}")')
# Get email IDs
email_ids = response[0].split()
# Move emails to "Bin" folder
for email_id in email_ids:
    mail.store(email_id, '+X-GM-LABELS', '\\Trash')
# Expunge deleted emails
mail.expunge()
print(f"Successfully moved {len(email_ids)} emails from {sender} to Bin!")

# Close IMAP connection
mail.close()
mail.logout()
