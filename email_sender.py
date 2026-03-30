import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

def parse_contacts(contacts_text):
    """
    Parses contacts text where each line has a name and email.
    """
    names = []
    emails = []
    for line in contacts_text.strip().split('\n'):
        if not line.strip(): continue
        parts = line.split()
        if len(parts) >= 2:
            names.append(" ".join(parts[:-1])) # Everything except last is name
            emails.append(parts[-1]) # Last is email
    return names, emails

def send_emails(host, port, my_address, password, contacts_text, template_text, subject):
    names, emails = parse_contacts(contacts_text)
    message_template = Template(template_text)
    
    try:
        s = smtplib.SMTP(host=host, port=port)
        s.starttls()
        s.login(my_address, password)
    except Exception as e:
        return False, f"Failed to connect or login: {str(e)}"
    
    success_count = 0
    errors = []
    
    for name, email in zip(names, emails):
        msg = MIMEMultipart()
        
        try:
            # Add in the actual person name to the message template
            message = message_template.substitute(PERSON_NAME=name.title())
            
            # Setup the parameters of the message
            msg['From'] = my_address
            msg['To'] = email
            msg['Subject'] = subject
            
            # Add in the message body
            msg.attach(MIMEText(message, 'plain'))
            
            # Send the message via the server set up earlier.
            s.send_message(msg)
            success_count += 1
        except Exception as e:
            errors.append(f"Failed to send to {email}: {str(e)}")
        finally:
            del msg
            
    s.quit()
    
    if errors:
        return True, f"Sent {success_count} emails, but encountered errors:\n" + "\n".join(errors)
    return True, f"Successfully sent {success_count} emails."
