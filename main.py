# Enable IMAP access in your Gmail account settings

# https://mail.google.com/mail/u/0/#settings/fwdandpop

# Importing Libraries

import imaplib                          # IMAP protocol for email handling
import email                            # Parse and manage email messages
from collections import defaultdict     # Default dictionary for organized data
import email.header                     # Encode/decode email headers
from email.header import decode_header  # Decode encoded headers
import webbrowser                       # Open links in a browser
import re                               # Regular expression handling
import os                               # Interact with the operating system (files, paths, directories).
import email as email_lib               # Rename module reference

# **Gmail account credentials**

username = input("Enter your Username")
password = input("Enter your Password")

# IMAP server settings

imap_server = "imap.gmail.com"  # The IMAP server address for Gmail to connect and fetch emails
imap_port = 993                 # The standard port for secure IMAP (uses SSL/TLS)

# Connect to IMAP server

mail = imaplib.IMAP4_SSL(imap_server, imap_port)  # Establish a secure connection to the IMAP server
mail.login(username, password)                    # Log in to the email account using the provided credentials
mail.select("inbox")                              # Select the "inbox" folder to access its emails

# Search for all emails

status, response = mail.search(None, "ALL")  # Search for all emails in the inbox

# status, response = mail.search(None, 'UNSEEN')
# status, response = mail.search(None, 'FROM', 'do_not_reply@mailersp2.binance.com')

# Get email IDs

email_ids = response[0].split()  # Extracts and splits the email IDs from the server response into a list

# Create a dictionary to store emails by domain

emails_by_domain = defaultdict(list)  # Creates a dictionary with default values as lists, used to group emails by domain

# Loop through each email

for email_id in email_ids:
    status, msg = mail.fetch(email_id, "(RFC822)")
    raw_email = msg[0][1]

    # Parse email using the email library
    email_message = email.message_from_bytes(raw_email)  
    

    # Extract domain from From address
    from_addr = email_message["From"]
    domain = from_addr.split("@")[-1]

    # Decode the subject line
    subject, encoding = decode_header(email_message["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding) if encoding else subject.decode('utf-8')

    # Extract the email body
    email_body = ""
    if email_message.is_multipart():         # Check if the email has multiple parts (like attachments)
        for part in email_message.walk():    # Walk through each part of the email
            if part.get_content_type() == "text/plain":      # Find the text part
                email_body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                break
    else:                                     # If the email is not multipart
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

# Printing email address by Domain

for domain, emails in emails_by_domain.items():  
    print(f"Domain: {domain}")  # Print domain name
    printed = set()  # Track printed addresses
    for email in emails:  
        if email['From'] not in printed:  
            print(f"From: {email['From']}")  # Print unique sender address
            printed.add(email['From'])  
    print("")  # Separate domains


# Calculate total emails across all domains



total_emails_across_domains = sum(len(emails) for emails in emails_by_domain.values())

# Print emails by domain with percentage based on the total number of domains

for domain, emails in emails_by_domain.items():
    domain_percentage = (len(emails) / total_emails_across_domains) * 100
    print(f"Domain: {domain} ({domain_percentage:.2f}% )")
    

# Delete Mails from Any Domain

print("Choose an action:")
print("1: Delete mails from any Domain")
print("2: Do not delete any emais")
action = input("Enter your choice (1/2): ").strip()
if action == "1":
    Delete()
elif action=="2":
    print("No deletion made")
else:
    print("Invalid action.")

# Check if the Subject Or Body contains spam keywords

spam_keywords = [
    "click here", "win a prize", "free gift", "claim your reward", "urgent", "act now", 
    "limited time offer", "apply now", "guaranteed", "risk-free", "no cost", "100% free", 
    "money back", "cheap", "earn money", "exclusive deal", "lower rates", "get rich quick", 
    "credit score", "pre-approved", "save big", "cash bonus", "buy now", "make money", 
    "winner", "limited time offer","Spam"
]

# Extracting Unsubscribe link

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
        detected_keyword = None

        # Check for spam keywords in the subject and body
        for keyword in spam_keywords:
            if keyword in subject or keyword in body:
                detected_keyword = keyword
                spam_found = True
                break  # Exit the loop as soon as a spam keyword is found

        # If spam is found, display details
        if spam_found:
            print(f"Spam Detected!")
            print(f"Domain: {domain}")
            print(f"Subject: {email_info['Subject']}")
            print(f"From: {email_info['From']}")
            print(f"Detected Spam Keyword: {detected_keyword}")

            # If spam is found, ask for deletion
            unsubscribe_links = extract_unsubscribe_link(email_info.get("Body", ""))
            if unsubscribe_links:
                print("Unsubscribe link(s) found:")
                for link in unsubscribe_links:
                    print(link)
            print("Choose an action:")
            print("1: Delete and Unsubscribe")
            print("2: Delete Only")
            print("3: Unsubscribe Only")
            print("4: None")
            action = input("Enter your choice (1/2/3/4): ").strip()

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
            else:
                print("Invalid action. Please try again.")

# Storing All files in a Folder

# Function to clean folder[] names
def clean_folder_name(name):
    return "".join(c if c.isalnum() else "_" for c in name)

# Function to categorize attachments based on file type
def categorize_file(filename):
    file_ext = filename.split('.')[-1].lower()
    if file_ext in ['jpg', 'jpeg', 'png', 'gif']:
        return 'Images'
    elif file_ext in ['pdf', 'doc', 'docx', 'txt' , 'xml']:
        return 'Documents'
    elif file_ext in ['mp4', 'mkv']:
        return 'Videos'
    else:
        return 'Others'

# Updated function to prevent conflicts
def fetch_and_save_attachments():
    for domain, emails in emails_by_domain.items():
        for email_info in emails:
            email_id = email_info['ID']

            # Fetch the email content
            status, msg = mail.fetch(email_id, "(RFC822)")
            if isinstance(msg[0], tuple):  # Ensure valid email content
                raw_email = msg[0][1]
                email_message = email_lib.message_from_bytes(raw_email)

                # Check for attachments
                for part in email_message.walk():
                    if part.get_content_disposition() == "attachment":
                        filename = part.get_filename()
                        if filename:
                            # Decode filename if necessary
                            filename = decode_header(filename)[0][0]
                            if isinstance(filename, bytes):
                                filename = filename.decode()

                            # Categorize and save the file
                            category = categorize_file(filename)
                            save_path = os.path.join("attachments", category)
                            os.makedirs(save_path, exist_ok=True)
                            filepath = os.path.join(save_path, filename)

                            # Save the attachment
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            print(f"Saved {filename} to {save_path}")
            else:
                print("Invalid email format encountered.")

# Call the function
fetch_and_save_attachments()

# Close IMAP connection
mail.close()
mail.logout()
