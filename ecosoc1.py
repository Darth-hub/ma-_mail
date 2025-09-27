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

# --- Recipient List (Updated and curated for all ECOSOC Delegates) ---
# name = Delegate Name
# portfolio = Allocated Country
recipients = [
        {"name": "Aditya Das", "email": "iec2023008@iiita.ac.in", "portfolio": "Australia"},
        {"name": "Aditya Das", "email": "iit2023189@iiita.ac.in", "portfolio": "Australia"},
#     {"name": "Aditya Das", "email": "iit2025130@iiita.ac.in", "portfolio": "Australia"},
#     {"name": "Pratham Makwana", "email": "iib2025005@iiita.ac.in", "portfolio": "India"},
#     {"name": "Adarsh Yadav", "email": "iec2025109@iiita.ac.in", "portfolio": "India"},
#     {"name": "Rahi Shivshankar Birajdar", "email": "iit2025027@iiita.ac.in", "portfolio": "India"},
#     {"name": "NIDAMARTHI CHANDANA", "email": "iit2025034@iiita.ac.in", "portfolio": "India"},
#     {"name": "Asra Tabassum", "email": "iit2025063@iiita.ac.in", "portfolio": "United States"},
#     {"name": "Ayush Pancholi", "email": "iec2025019@iiita.ac.in", "portfolio": "India"},
#     {"name": "Hema Harshitha Sarvasiddi", "email": "iit2025082@iiita.ac.in", "portfolio": "United States"},
#     {"name": "Venkata siddhant vooda", "email": "iit2025181@iiita.ac.in", "portfolio": "USA"},
#     {"name": "Abhyudaya Kumar", "email": "iec2025055@iiita.ac.in", "portfolio": "India"},
#     {"name": "Debojyoti Chakrabarti", "email": "iec2025003@iiita.ac.in", "portfolio": "India"},
#     {"name": "Rishav Kant Deo", "email": "iib2025010@iiita.ac.in", "portfolio": "Morocco"},
#     {"name": "Soumya Ravi Godghate", "email": "iit2025054@iiita.ac.in", "portfolio": "India"},
#     {"name": "Saksham chadar", "email": "iec2025077@iiita.ac.in", "portfolio": "Pakistan"},
#     {"name": "Rishabh Verma", "email": "iec2025079@iiita.ac.in", "portfolio": "India"},
#     {"name": "Rudransh Joshi", "email": "iec2025083@iiita.ac.in", "portfolio": "India"},
#     {"name": "Sayantan Hait", "email": "iec2025078@iiita.ac.in", "portfolio": "India"},
#     {"name": "Palak Ukey", "email": "iec2025031@iiita.ac.in", "portfolio": "Sweden"},
#     {"name": "Pratik Chaturvedi", "email": "iit2025087@iiita.ac.in", "portfolio": "Nepal"},
#     {"name": "Ishan agrawal", "email": "iec2025064@iiita.ac.in", "portfolio": "El Salvador"},
#     {"name": "Janhavi Shastri", "email": "iit2025091@iiita.ac.in", "portfolio": "Switzerland"},
#     {"name": "Ameya Narayanam", "email": "iit2025051@iiita.ac.in", "portfolio": "Sweden"},
#     {"name": "Harshvardhan Arya", "email": "iec2025060@iiita.ac.in", "portfolio": "North Korea"},
#     {"name": "Bonala Vinoothna Lakshmi", "email": "iib2025016@iiita.ac.in", "portfolio": "India"},
#     {"name": "Ankit Kumar Chaudhary", "email": "iec2025027@iiita.ac.in", "portfolio": "India"},
#     {"name": "Hansika Mudavath", "email": "iit2025089@iiita.ac.in", "portfolio": "Denmark"},
#     {"name": "Mannat Jain", "email": "iit2025262@iiita.ac.in", "portfolio": "Canada"},
#     {"name": "Amrita Singh", "email": "iit2025244@iiita.ac.in", "portfolio": "United States"},
#     {"name": "Mann Kumar Gupta", "email": "iec2025052@iiita.ac.in", "portfolio": "India"},
#     {"name": "Darshil Shah", "email": "iit2025255@iiita.ac.in", "portfolio": "India"},
#     {"name": "Sahitya Gulab Jagtap", "email": "iit2025049@iiita.ac.in", "portfolio": "Ghana"},
#     {"name": "Mohammad Sultan", "email": "sultanpoke123@gmail.com", "portfolio": "United States of America"},
#     {"name": "Sara Nasrat", "email": "pewds072@gmail.com", "portfolio": "Nepal"},
#     {"name": "Prabjyot kaur", "email": "parvinderkaur123454321@gmail.com", "portfolio": "France"},
#     {"name": "Kabir Capoor", "email": "kabiircapoor1808@gmail.com", "portfolio": "Australia"},
#     {"name": "Joanna V. Emmanuel", "email": "joanvemmanuel@gmail.com", "portfolio": "Switzerland"},
#     {"name": "Anvesh Srivastava", "email": "anveshsrivastava936@gmail.com", "portfolio": "UNITED STATES OF AMERICA"},
#     {"name": "Aarush krishna", "email": "aarushk076@gmail.com", "portfolio": "Italy"},
#     {"name": "Shivansh Shekhar", "email": "shivanshshekhar21@gmail.com", "portfolio": "China"},
#     {"name": "Bomedi Shanyu Reddy", "email": "iit2025078@iiita.ac.in", "portfolio": "United States"},
#     {"name": "Atharv Rahul Dehedkar", "email": "iit2025020@iiita.ac.in", "portfolio": "India"},
#     {"name": "Aditi Deshmukh", "email": "iit2025217@iiita.ac.in", "portfolio": "El Salvador"},
#     {"name": "Tanish vaibhav", "email": "tanishvaibhav78@gmail.com", "portfolio": "USA"},
#     {"name": "Gondaliya Vaidehi Pareshbhai", "email": "iit2025146@iiita.ac.in", "portfolio": "United Kingdom"},
#     {"name": "Harshvardhan", "email": "iit2025177@iiita.ac.in", "portfolio": "USA"},
#     {"name": "Sefora Mokena", "email": "iec2025074@iiita.ac.in", "portfolio": "Germany"},
#     {"name": "Tanisha Nayal", "email": "iit2025074@iiita.ac.in", "portfolio": "Sweden"},
#     {"name": "Sanya Sinha", "email": "iit2025001@iiita.ac.in", "portfolio": "United States"},
#     {"name": "AVINASHKUMAR HARESH MANGHNANI", "email": "iib2025031@iiita.ac.in", "portfolio": "Brazil"},
#     {"name": "Supriya Kant", "email": "iec2025089@iiita.ac.in", "portfolio": "India"},
#     {"name": "Prathit Bhadouriya", "email": "prathitb21@gmail.com", "portfolio": "Sweden"},
#     {"name": "Aaradhya Pandey", "email": "aruna.auditor@gmail.com", "portfolio": "Canada"},
#     {"name": "Lakshya Rastogi", "email": "rastogil389@gmail.com", "portfolio": "India"},
#     {"name": "Aarnav Bhargava", "email": "aarnavkrishna0712@gmail.com", "portfolio": "India"},
#     {"name": "Abhiraj Mandal", "email": "abhirajmandal18@gmail.com", "portfolio": "New Zealand"},
#     {"name": "Mohnish Singh", "email": "mohnishsinghdps@gmail.com", "portfolio": "New Zealand"},
#     {"name": "Gaurang Srivastava", "email": "gaurang.srivastava.december@gmail.com", "portfolio": "USA"},
#     {"name": "Siddhi Srivastava", "email": "siddhi.srivastava08@gmail.com", "portfolio": "Germany"},
#     {"name": "Ayush Saha", "email": "iit2025259@iiita.ac.in", "portfolio": "Qatar"},
#     {"name": "Pranshu Sethi", "email": "iit2025283@iiita.ac.in", "portfolio": "Russia"},
#     {"name": "Pushpit Deshmukh", "email": "iit2025138@iiita.ac.in", "portfolio": "India"},
#     {"name": "Nasit Deep Bhupendrabhai", "email": "iec2025072@iiita.ac.in", "portfolio": "Germany"},
#     {"name": "Rudra Mina", "email": "iit2025232@iiita.ac.in", "portfolio": "India"},
#     {"name": "Lakshmish S G", "email": "iec2025034@iiita.ac.in", "portfolio": "USA"},
#     {"name": "Sachin Benakannavar", "email": "iec2025025@iiita.ac.in", "portfolio": "United States of America"},
#     {"name": "Paarth Arora", "email": "iit2025280@iiita.ac.in", "portfolio": "Israel"},
#     {"name": "Sudhanshu Kalekinge", "email": "iec2025013@iiita.ac.in", "portfolio": "Russia"},
#     {"name": "Hansika Malpani", "email": "iec2025111@iiita.ac.in", "portfolio": "Mexico"},
#     {"name": "Aryan Gupta", "email": "iec2025032@iiita.ac.in", "portfolio": "Germany"},
#     {"name": "Anvi Pandey", "email": "aanvipandey2009@gmail.com", "portfolio": "Sweden"},
]


# --- Email Content Templates ---
email_subject_template = "Portfolio Allocation: ECOSOC - IIIT-A MUN'25"

# This is a fallback for email clients that don't support HTML.
email_body_plain = """
Dear {name},

We are pleased to inform you that you have been assigned the portfolio of {portfolio} for the United Nations Economic and Social Council in the IIIT-A MUN'25.

We hope that you have a wonderful time engaging in debate of the highest quality.

Please find the WhatsApp group given below and stay updated: https://chat.whatsapp.com/FyUXYTGvfOf8ingNloN5B4

Thanks and regards,
The Secretariat,
IIIT-A MUN'25.
"""

# This is the main version for modern email clients. It uses HTML to make the text bold.
email_body_html = """
<html>
  <body>
    <p>Dear <b>{name}</b>,</p>
    <p>We are pleased to inform you that you have been assigned the portfolio of <b>{portfolio}</b> for the United Nations Economic and Social Council in the IIIT-A MUN'25.</p>
    <p>We hope that you have a wonderful time engaging in debate of the highest quality.</p>
    <p>Please find the WhatsApp group given below and stay updated: <a href="https://chat.whatsapp.com/FyUXYTGvfOf8ingNloN5B4">Join the ECOSOC Delegates Group</a></p>
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
                    # This creates a message container that can hold multiple versions of the email.
                    message = MIMEMultipart("alternative")
                    message["From"] = SENDER_EMAIL
                    message["To"] = recipient["email"]
                    message["Subject"] = email_subject_template

                    # Create the plain-text and HTML parts of your message
                    # Using 'utf-8' is a best practice for compatibility.
                    plain_text_part = MIMEText(email_body_plain.format(name=recipient["name"], portfolio=recipient["portfolio"]), "plain", "utf-8")
                    html_part = MIMEText(email_body_html.format(name=recipient["name"], portfolio=recipient["portfolio"]), "html", "utf-8")

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

