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
    # {"name": "Aditya Das", "email": "ayushranjan112400@gmail.com", "portfolio": "Australia"},
    # {"name": "Aditya Das", "email": "iit2023096@iiita.ac.in", "portfolio": "Australia"},
    {"name": "Aditya Das", "email": "iit2025130@iiita.ac.in", "portfolio": "Australia"},
    {"name": "Rishav Kant Deo", "email": "iib2025010@iiita.ac.in", "portfolio": "Bangladesh"},
    {"name": "AVINASHKUMAR HARESH MANGHNANI", "email": "iib2025031@iiita.ac.in", "portfolio": "Brazil"},
    {"name": "Darshil Shah", "email": "iit2025255@iiita.ac.in", "portfolio": "Cambodia"},
    {"name": "Mannat Jain", "email": "iit2025262@iiita.ac.in", "portfolio": "Canada"},
    {"name": "Mohammad Sultan", "email": "sultanpoke123@gmail.com", "portfolio": "China"},
    {"name": "Rudransh Joshi", "email": "iec2025083@iiita.ac.in", "portfolio": "Colombia"},
    {"name": "Ishan agrawal", "email": "iec2025064@iiita.ac.in", "portfolio": "Cuba"},
    {"name": "Hansika Mudavath", "email": "iit2025089@iiita.ac.in", "portfolio": "Denmark"},
    {"name": "Ankit Kumar Chaudhary", "email": "iec2025027@iiita.ac.in", "portfolio": "Egypt"},
    {"name": "Aditi Deshmukh", "email": "iit2025217@iiita.ac.in", "portfolio": "El Salvador"},
    {"name": "Hema Harshitha Sarvasiddi", "email": "iit2025082@iiita.ac.in", "portfolio": "Ethiopia"},
    {"name": "Tanish vaibhav", "email": "tanishvaibhav78@gmail.com", "portfolio": "France"},
    {"name": "Sefora Mokena", "email": "iec2025074@iiita.ac.in", "portfolio": "Germany"},
    {"name": "Sahitya Gulab Jagtap", "email": "iit2025049@iiita.ac.in", "portfolio": "Ghana"},
    {"name": "Sayantan Hait", "email": "iec2025078@iiita.ac.in", "portfolio": "Greece"},
    {"name": "Atharv Rahul Dehedkar", "email": "iit2025020@iiita.ac.in", "portfolio": "India"},
    {"name": "Saksham chadar", "email": "iec2025077@iiita.ac.in", "portfolio": "Indonesia"},
    {"name": "Anvesh Srivastava", "email": "anveshsrivastava936@gmail.com", "portfolio": "Iran"},
    {"name": "Aryaman Gulati", "email": "aryamangulati2007@gmail.com", "portfolio": "Israel"},
    {"name": "Aarush krishna", "email": "aarushk076@gmail.com", "portfolio": "Italy"},
    {"name": "Sanya Sinha", "email": "iit2025001@iiita.ac.in", "portfolio": "Japan"},
    {"name": "Asra Tabassum", "email": "iit2025063@iiita.ac.in", "portfolio": "Kenya"},
    {"name": "NIDAMARTHI CHANDANA", "email": "iit2025034@iiita.ac.in", "portfolio": "Libya"},
    {"name": "Ayush Pancholi", "email": "iec2025019@iiita.ac.in", "portfolio": "Ukraine"},
    {"name": "Ameya Narayanam", "email": "iit2025051@iiita.ac.in", "portfolio": "Mexico"},
    {"name": "Shivansh Shekhar", "email": "shivanshshekhar21@gmail.com", "portfolio": "Morocco"},
    {"name": "Venkata siddhant vooda", "email": "iit2025181@iiita.ac.in", "portfolio": "Myanmar"},
    {"name": "Sara Nasrat", "email": "pewds072@gmail.com", "portfolio": "Nepal"},
    {"name": "Gondaliya Vaidehi Pareshbhai", "email": "iit2025146@iiita.ac.in", "portfolio": "Netherlands"},
    {"name": "Pratik Chaturvedi", "email": "iit2025087@iiita.ac.in", "portfolio": "New Zealand"},
    {"name": "Prathit Bhadouriya", "email": "prathitb21@gmail.com", "portfolio": "Nigeria"},
    {"name": "Harshvardhan Arya", "email": "iec2025060@iiita.ac.in", "portfolio": "North Korea"},
    {"name": "Bomedi Shanyu Reddy", "email": "iit2025078@iiita.ac.in", "portfolio": "Pakistan"},
    {"name": "Bonala Vinoothna Lakshmi", "email": "iib2025016@iiita.ac.in", "portfolio": "Panama"},
    {"name": "Debojyoti Chakrabarti", "email": "iec2025003@iiita.ac.in", "portfolio": "Philippines"},
    {"name": "Kabir Capoor", "email": "kabiircapoor1808@gmail.com", "portfolio": "Poland"},
    {"name": "Mann Kumar Gupta", "email": "iec2025052@iiita.ac.in", "portfolio": "Qatar"},
    {"name": "Abhyudaya Kumar", "email": "iec2025055@iiita.ac.in", "portfolio": "Russia"},
    {"name": "Janhavi Shastri", "email": "iit2025091@iiita.ac.in", "portfolio": "Saudi Arabia"},
    {"name": "Harshvardhan", "email": "iit2025177@iiita.ac.in", "portfolio": "Singapore"},
    {"name": "Supriya Kant", "email": "iec2025089@iiita.ac.in", "portfolio": "South Africa"},
    {"name": "Rahi Shivshankar Birajdar", "email": "iit2025027@iiita.ac.in", "portfolio": "South Korea"},
    {"name": "Palak Ukey", "email": "iec2025031@iiita.ac.in", "portfolio": "Spain"},
    {"name": "RAGHAV MISHRA", "email": "aditya.25518092@hrc.du.ac.in", "portfolio": "Sweden"},
    {"name": "Joanna V. Emmanuel", "email": "joanvemmanuel@gmail.com", "portfolio": "Switzerland"},
    {"name": "Pratham Makwana", "email": "iib2025005@iiita.ac.in", "portfolio": "Thailand"},
    {"name": "Soumya Ravi Godghate", "email": "iit2025054@iiita.ac.in", "portfolio": "Türkiye"},
    {"name": "Adarsh Yadav", "email": "iec2025109@iiita.ac.in", "portfolio": "Uganda"},
    {"name": "Amrita Singh", "email": "iit2025244@iiita.ac.in", "portfolio": "United Arab Emirates"},
    {"name": "Prabjyot kaur", "email": "parvinderkaur123454321@gmail.com", "portfolio": "United Kingdom"},
    {"name": "Tanisha Nayal", "email": "iit2025074@iiita.ac.in", "portfolio": "United States"},
    {"name": "Rishabh Verma", "email": "iec2025079@iiita.ac.in", "portfolio": "Venezuela"}
]


# --- Email Content Templates ---
email_subject_template = "Portfolio Allocation: ECOSOC - IIIT-A MUN'25"

# This is a fallback version for email clients that don't support HTML.
email_body_plain = """
Dear {name},

We are pleased to inform you that you have been assigned the portfolio of {portfolio} for the United Nations Economic and Social Council in the IIIT-A MUN'25.

Please find the WhatsApp group given below and stay updated: https://chat.whatsapp.com/FyUXYTGvfOf8ingNloN5B4

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
    <p>We are pleased to inform you that you have been assigned the portfolio of <b>{portfolio}</b> for the United Nations Economic and Social Council in the IIIT-A MUN'25.</p>
    <p>Please find the WhatsApp group given below and stay updated: <a href="https://chat.whatsapp.com/FyUXYTGvfOf8ingNloN5B4">Join the ECOSOC Committee Group</a></p>
    <p>We hope that you have a wonderful time engaging in debate of the highest quality.</p>
    
    <p>Thanks and regards,</p>
    <div>
        The Secretariat,<br>
        IIIT-A MUN'25.
    </div>
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
                    message["Subject"] = email_subject_template

                    # Create the plain-text and HTML versions of your message
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