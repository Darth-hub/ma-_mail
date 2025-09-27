import smtplib
import ssl
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Configuration ---
# IMPORTANT: For security, set these as environment variables in your terminal
# before running the script.
# On Windows: set SENDER_EMAIL="your_email@gmail.com"
# On macOS/Linux: export SENDER_EMAIL="your_email@gmail.com"

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD") # Use a 16-digit App Password for Gmail

# --- Email Server Details (Example for Gmail) ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # For SSL

# --- Recipient List (Curated for AIPPM Delegates) ---
# name = Delegate Name
# person = Allocated Leader/Portfolio
recipients = [
    {"name": "Aaaaa", "email": "iec2023008@iiita.ac.in", "person": "Akhilesh Yadav"},
    {"name": "Aviral Agarwal", "email": "iit2025156@iiita.ac.in", "person": "Akhilesh Yadav"},
    {"name": "Nikhil Raj", "email": "iit2025293@iiita.ac.in", "person": "Himanta Biswa Sarma"},
    {"name": "Venkat Vempati", "email": "iit2025203@iiita.ac.in", "person": "NARA CHANDRABABU NAIDU"},
    {"name": "Himanshi Yadav", "email": "iib2025017@iiita.ac.in", "person": "Arjun Ram Meghwal"},
    {"name": "Shourya Sankrit", "email": "iec2025039@iiita.ac.in", "person": "Rahul Gandhi"},
    {"name": "Krishna Taneja", "email": "iit2025167@iiita.ac.in", "person": "K annamalai"},
    {"name": "Bharat Upadhyay", "email": "iit2025045@iiita.ac.in", "person": "Tejasvi Surya"},
    {"name": "Siddharth Gupta", "email": "iit2025107@iiita.ac.in", "person": "Rajnath Singh"},
    {"name": "Chaitanya Pradip Wagh", "email": "iit2025123@iiita.ac.in", "person": "Uddhav Balasaheb Thackeray"},
    {"name": "Roshan Shinde", "email": "iit2025269@iiita.ac.in", "person": "Shrikant Shinde"},
    {"name": "Paarth Sharma", "email": "iit2025233@iiita.ac.in", "person": "Narendra Damodardas Modi"},
    {"name": "Rohit Malik", "email": "iit2025033@iiita.ac.in", "person": "Raghav Chadha"},
    {"name": "Mann Kumar Gupta", "email": "iec2025052@iiita.ac.in", "person": "Chirag Paswan"},
    {"name": "Darshil Shah", "email": "iit2025255@iiita.ac.in", "person": "Nitish Kumar"},
    {"name": "Sahitya Gulab Jagtap", "email": "iit2025049@iiita.ac.in", "person": "Nirmala Sitaraman"},
    {"name": "ARPIT Mishra", "email": "iec2025094@iiita.ac.in", "person": "Prem Singh Tamang"},
    {"name": "Sanya Sinha", "email": "iit2025001@iiita.ac.in", "person": "Naveen Patnaik"},
    {"name": "Nasit Deep Bhupendrabhai", "email": "iec2025072@iiita.ac.in", "person": "J. P. Nadda"},
    {"name": "Rudra Mina", "email": "iit2025232@iiita.ac.in", "person": "Ajit Anantrao Pawar"},
    {"name": "Lakshmish S G", "email": "iec2025034@iiita.ac.in", "person": "M. K. Stalin"},
    {"name": "Sachin Benakannavar", "email": "iec2025025@iiita.ac.in", "person": "Pinarayi Vijayan"},
    {"name": "AVINASHKUMAR HARESH MANGHNANI", "email": "iib2025031@iiita.ac.in", "person": "Awadhesh Prasad"},
    {"name": "Chandni Agrawal", "email": "iec2025061@iiita.ac.in", "person": "Rekha Gupta"},
    {"name": "Aaditya Maurya", "email": "iit2025057@iiita.ac.in", "person": "Nishikant Dubey"},
    {"name": "Paarth Arora", "email": "iit2025280@iiita.ac.in", "person": "Jairam Ramesh"},
    {"name": "SACHIN SURESHKUMAR", "email": "iit2025253@iiita.ac.in", "person": "Gaurav Gogoi"},
    {"name": "Pauravi Pathak", "email": "iec2025076@iiita.ac.in", "person": "Priyanka Gandhi Vadra"},
    {"name": "Dhairya Fofariya", "email": "iit2025119@iiita.ac.in", "person": "Adhir Ranjan Chowdhury"},
    {"name": "Singh Udit Bhanwar", "email": "iib2025012@iiita.ac.in", "person": "Kiren Rijiju"},
    {"name": "Md Shahan Ahmad", "email": "iit2025247@iiita.ac.in", "person": "Asaduddin Owaisi"},
    {"name": "nishihee shah", "email": "iib2025002@iiita.ac.in", "person": "Bhupesh Baghel"},
    {"name": "Arnavi", "email": "iib2025009@iiita.ac.in", "person": "Mehbooba Mufti"},
    {"name": "Kartikay Arya", "email": "iec2025115@iiita.ac.in", "person": "Manoj Kumar Jha"},
    {"name": "Supriya Kant", "email": "iec2025089@iiita.ac.in", "person": "Supriya Sule"},
    {"name": "Lakshay Arora", "email": "iit2025117@iiita.ac.in", "person": "Shivraj Singh Chauhan"},
    {"name": "Hansika Malpani", "email": "iec2025111@iiita.ac.in", "person": "Mahua Moitra"},
    {"name": "Aryan Gupta", "email": "iec2025032@iiita.ac.in", "person": "Konidela Pawan Kalyan"},
    {"name": "Mohammad Sultan", "email": "sultanpoke123@gmail.com", "person": "Shashi Tharoor"},
    {"name": "Anvi Pandey", "email": "aanvipandey29042009@gmail.com", "person": "Amit Shah"},
    {"name": "Dev Sachdeva", "email": "devsachdevapankaj@gmail.com", "person": "Yogi Adityanath"},
    {"name": "Shivansh Mangalam", "email": "mangalam9shivansh@gmail.com", "person": "Piyush Goyal"},
    {"name": "Raghav Mishra", "email": "aditya.25518092@hrc.du.ac.in", "person": "Subramanian Jayashankar"},
    {"name": "Shaurya Goswami", "email": "shauryathebeast08@gmail.com", "person": "MAMTA BANERJEE"},
    {"name": "Joanna V. Emmanuel", "email": "joanvemmanuel@gmail.com", "person": "Nitin Jairam Gadkari"},
    {"name": "Siddhi Srivastava", "email": "siddhi.srivastava08@gmail.com", "person": "Dharmendra Pradhan"},
    {"name": "Aditya Bajpai", "email": "a47b61@gmail.com", "person": "Hemant Soren"},
    {"name": "Mohd Jafar Sadiq", "email": "jafarsadiqghost@gmail.com", "person": "Omar Abdullah"},
    {"name": "Hridyansh", "email": "hridyanshx7@gmail.com", "person": "Rajeev Ranjan Singh"},
    {"name": "Lemuel Aaron Singh", "email": "lemuel.aaron.singh@gmail.com", "person": "Mallikarjun Kharge"},
]


# --- Email Content Templates ---
# ** NEW: Personalized subject line **
email_subject_template = "Portfolio Allocation for {name}: AIPPM - IIIT-A MUN'25"

# This is a fallback version for email clients that don't support HTML.
email_body_plain = """
Dear {name},

We are pleased to inform you that you have been assigned the portfolio of {person} for the All India Political Party Meet in the IIIT-A MUN'25.

Please find the WhatsApp group given below and stay updated: https://chat.whatsapp.com/KkNJQC4nqHg09Wgqda9Hc9

We hope that you have a wonderful time engaging in debate of the highest quality.

Thanks and regards,
The Secretariat,
IIIT-A MUN'25.
"""

# This is the main HTML version that supports bold text and links.
email_body_html = """
<html>
  <body>
    <p>Dear <b>{name}</b>,</p>
    <p>We are pleased to inform you that you have been assigned the portfolio of <b>{person}</b> for the All India Political Party Meet in the IIIT-A MUN'25.</p>
    <p>Please find the WhatsApp group given below and stay updated: <a href="https://chat.whatsapp.com/KkNJQC4nqHg09Wgqda9Hc9">Join the AIPPM Committee Group</a></p>
    <p>We hope that you have a wonderful time engaging in debate of the highest quality.</p>
    <p>Thanks and regards,<br>
    The Secretariat,<br>
    IIIT-A MUN'25.</p>
  </body>
</html>
"""

# --- Script Logic ---

def send_bulk_emails():
    """
    Connects to the SMTP server and sends a personalized email to each recipient.
    """
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Error: SENDER_EMAIL and SENDER_PASSWORD environment variables are not set.")
        return

    context = ssl.create_default_context()
    successful_sends = 0
    failed_sends = 0

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            print(f"Connecting to {SMTP_SERVER}...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("Login successful.")
            print(f"Starting to send {len(recipients)} personalized emails...")

            for index, recipient in enumerate(recipients):
                try:
                    # Create the main container. The 'alternative' subtype is critical.
                    message = MIMEMultipart("alternative")
                    message["From"] = SENDER_EMAIL
                    message["To"] = recipient["email"]
                    # ** NEW: Use the personalized subject line **
                    message["Subject"] = email_subject_template.format(name=recipient["name"])

                    # Create the plain-text and HTML versions of your message
                    plain_text_part = MIMEText(email_body_plain.format(name=recipient["name"], person=recipient["person"]), "plain", "utf-8")
                    html_part = MIMEText(email_body_html.format(name=recipient["name"], person=recipient["person"]), "html", "utf-8")

                    # Attach both versions to the message container.
                    # Email clients will prefer the last one attached, which is our HTML version.
                    message.attach(plain_text_part)
                    message.attach(html_part)

                    server.sendmail(SENDER_EMAIL, recipient["email"], message.as_string())
                    print(f"({index + 1}/{len(recipients)}) Email sent successfully to {recipient['name']} <{recipient['email']}>")
                    successful_sends += 1
                except Exception as e:
                    print(f"(!) Failed to send email to {recipient['name']} <{recipient['email']}>. Error: {e}")
                    failed_sends += 1
                
                time.sleep(2) # Delay to avoid being marked as spam

    except smtplib.SMTPAuthenticationError:
        print("\nAuthentication failed. Please check your credentials and use an App Password for Gmail.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        print("\n--- Sending Report ---")
        print(f"Total emails attempted: {len(recipients)}")
        print(f"Successfully sent: {successful_sends}")
        print(f"Failed to send: {failed_sends}")
        print("------------------------")

if __name__ == "__main__":
    send_bulk_emails()

