# Enable IMAP access in your Gmail account settings

# https://mail.google.com/mail/u/0/#settings/fwdandpop

# Importing Libraries

import imaplib
import email
from collections import defaultdict
import email.header
from email.header import decode_header
import webbrowser
import re

# **Gmail account credentials**

username = "bsaivignesh123s@gmail.com"
password = "svhq xlkg myol pvkl"

# IMAP server settings

imap_server = "imap.gmail.com"
imap_port = 993

# Connect to IMAP server

mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(username, password)
mail.select("inbox")

# Search for all emails

 status, response = mail.search(None, "ALL")  # Search for all emails in the inbox

# status, response = mail.search(None, 'UNSEEN')

# status, response = mail.search(None, 'FROM', 'marketing@engage.canva.com')

# Get email IDs

email_ids = response[0].split()

# Create a dictionary to store emails by domain

emails_by_domain = defaultdict(list)

# Loop through each email

for email_id in email_ids:
    status, msg = mail.fetch(email_id, "(RFC822)")
    raw_email = msg[0][1]

    # Parse email using the email library
    email_message = email.message_from_bytes(raw_email)  # Use the renamed module

    # Extract domain from From address
    from_addr = email_message["From"]
    domain = from_addr.split("@")[-1]

    # Decode the subject line
    subject, encoding = decode_header(email_message["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding) if encoding else subject.decode('utf-8')

    # Extract the email body
    email_body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                email_body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                break
    else:
        email_body = email_message.get_payload(decode=True).decode(email_message.get_content_charset() or 'utf-8')

    # Add email to dictionary by domain
    emails_by_domain[domain].append({
    "Subject": subject,
    "From": from_addr,
    "Body": email_body,
    "ID": email_id
})

# Printing emails subject by Domain

for domain, emails in emails_by_domain.items():
    print(f"Domain: {domain}")
    for email in emails:
        print(f"  Subject: {email['Subject']}, From: {email['From']}")
    print("")

# Printing email address by Domain

for domain, emails in emails_by_domain.items():
    print(f"Domain: {domain}")
    printed = set()
    for email in emails:
        if email['From'] not in printed:
            print(f"From: {email['From']}")
            printed.add(email['From'])
    print("")


# Calculate total emails across all domains



total_emails_across_domains = sum(len(emails) for emails in emails_by_domain.values())

# Print emails by domain with percentage based on the total number of domains

for domain, emails in emails_by_domain.items():
    domain_percentage = (len(emails) / total_emails_across_domains) * 100
    print(f"Domain: {domain} ({domain_percentage:.2f}% )")
    

Delete()



def Delete() :
    sender = input("Enter sender mail to Delete: ")
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
    print("-----------------------------------------------------------------")


# Check if the Subject Or Body contains spam keywords

spam_keywords = [
    "click here", "win a prize", "free gift", "claim your reward", "urgent", "act now", 
    "limited time offer", "apply now", "guaranteed", "risk-free", "no cost", "100% free", 
    "money back", "cheap", "earn money", "exclusive deal", "lower rates", "get rich quick", 
    "credit score", "pre-approved", "save big", "cash bonus", "buy now", "make money", 
    "free", "win", "winner", "limited time offer","Spam"
]

def extract_unsubscribe_link(body):
    # Regex to find unsubscribe links
    unsubscribe_links = re.findall(r'(https?://[^\s]+)', body)
    # You may want to filter these links based on known unsubscribe patterns
    return [link for link in unsubscribe_links if "unsubscribe" in link.lower()]

for domain, emails in emails_by_domain.items():
    for email_info in emails:
        subject = email_info["Subject"].lower()
        body = email_info.get("Body", "").lower()
        
        spam_found = False

        # Check for spam keywords in the subject
        if any(keyword in subject for keyword in spam_keywords) or any(keyword in body for keyword in spam_keywords):
            print(f"Domain: {domain}, Subject: {email_info['Subject']}, From: {email_info['From']}")
            spam_found = True

        # If spam is found, ask for deletion
        if spam_found:
            unsubscribe_links = extract_unsubscribe_link(email_info["Body"])
            if unsubscribe_links:
                print("Unsubscribe link(s) found:")
                for link in unsubscribe_links:
                    print(link)
            print("Choose an action:")
            print("1: Delete and Unsubscribe")
            print("2: Delete Only")
            print("3: Unsubscribe Only")
            action = input("Enter your choice (1/2/3): ").strip()

            if action == "1":
                # Delete the email and unsubscribe
                Delete()
                if unsubscribe_links:
                    webbrowser.open(unsubscribe_links[0])  # Open the first unsubscribe link
                else:
                    print("No unsubscribe link found.\n")   
            elif action == "2":
                # Delete only
                Delete()
            elif action == "3":
                # Unsubscribe only
                if unsubscribe_links:
                    print("Following the unsubscribe link...")
                    webbrowser.open(unsubscribe_links[0])  # Open the first unsubscribe link
                else:
                    print("No unsubscribe link found.\n")
            else :
                print("Enter the correct action")

