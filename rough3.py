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

# --- Recipient List (Updated with Final UNSC Double Delegation Allocations & Contact Numbers) ---
recipients = [

    {
        "name": "Spandana Surepally", "email": "iib2025033@iiita.ac.in", "portfolio": "USA",
        "co_delegate_details": "Name: Krish Sushil Kinger\nEmail: iit2025281@iiita.ac.in\nContact: 9307229628"
    },
    {
        "name": "Krish Sushil Kinger", "email": "iit2025281@iiita.ac.in", "portfolio": "USA",
        "co_delegate_details": "Name: Spandana Surepally\nEmail: iib2025033@iiita.ac.in\nContact: 8135500758"
    },
    {
        "name": "Pranjali", "email": "iit2025129@iiita.ac.in", "portfolio": "China",
        "co_delegate_details": "Name: Arihant Sinha\nEmail: iit2025008@iiita.ac.in\nContact: 9625956065"
    },
    {
        "name": "Arihant Sinha", "email": "iit2025008@iiita.ac.in", "portfolio": "China",
        "co_delegate_details": "Name: Pranjali\nEmail: iit2025129@iiita.ac.in\nContact: 9667225595"
    },
    {
        "name": "Pranshu Sethi", "email": "iit2025283@iiita.ac.in", "portfolio": "Russia",
        "co_delegate_details": "Name: Ayush Saha\nEmail: iit2025259@iiita.ac.in\nContact: 9883906709"
    },
    {
        "name": "Ayush Saha", "email": "iit2025259@iiita.ac.in", "portfolio": "Russia",
        "co_delegate_details": "Name: Pranshu Sethi\nEmail: iit2025283@iiita.ac.in\nContact: 8607791934"
    },
    {
        "name": "Nishkarsh Saxena", "email": "iit2025088@iiita.ac.in", "portfolio": "Canada",
        "co_delegate_details": "Name: Bhavya Sagar\nEmail: iit2025171@iiita.ac.in\nContact: 9915557970"
    },
    {
        "name": "Bhavya Sagar", "email": "iit2025171@iiita.ac.in", "portfolio": "Canada",
        "co_delegate_details": "Name: Nishkarsh Saxena\nEmail: iit2025088@iiita.ac.in\nContact: 9540491284"
    },
    {
        "name": "Advaith Puthanmadathil Sajeev", "email": "iec2025059@iiita.ac.in", "portfolio": "Turkiye",
        "co_delegate_details": "Name: Kondepudi Mani Surya Asrith\nEmail: iec2025065@iiita.ac.in\nContact: 8179761974"
    },
    {
        "name": "Kondepudi Mani Surya Asrith", "email": "iec2025065@iiita.ac.in", "portfolio": "Turkiye",
        "co_delegate_details": "Name: Advaith Puthanmadathil Sajeev\nEmail: iec2025059@iiita.ac.in\nContact: 8590746262"
    },
    {
        "name": "Kashish Jadhaw", "email": "iec2025018@iiita.ac.in", "portfolio": "Greece",
        "co_delegate_details": "Name: Sanskruti Shailesh Bhamare\nEmail: iec2025035@iiita.ac.in\nContact: 8830380158"
    },
    {
        "name": "Sanskruti Shailesh Bhamare", "email": "iec2025035@iiita.ac.in", "portfolio": "Greece",
        "co_delegate_details": "Name: Kashish Jadhaw\nEmail: iec2025018@iiita.ac.in\nContact: 8109755718"
    },
    {
        "name": "Namrata Hooda", "email": "iit2025143@iiita.ac.in", "portfolio": "South Korea",
        "co_delegate_details": "Name: Diya Dutta\nEmail: iec2025005@iiita.ac.in\nContact: 9973839029"
    },
    {
        "name": "Diya Dutta", "email": "iec2025005@iiita.ac.in", "portfolio": "South Korea",
        "co_delegate_details": "Name: Namrata Hooda\nEmail: iit2025143@iiita.ac.in\nContact: 9350866855"
    },
    {
        "name": "Sachin Benakannavar", "email": "iec2025025@iiita.ac.in", "portfolio": "Netherlands",
        "co_delegate_details": "Name: Lakshmish S G\nEmail: iec2025034@iiita.ac.in\nContact: 9035662346"
    },
    {
        "name": "Lakshmish S G", "email": "iec2025034@iiita.ac.in", "portfolio": "Netherlands",
        "co_delegate_details": "Name: Sachin Benakannavar\nEmail: iec2025025@iiita.ac.in\nContact: 7975414051"
    },
    {
        "name": "Aaditya Maurya", "email": "iit2025057@iiita.ac.in", "portfolio": "Belarus",
        "co_delegate_details": "Name: Chandni Agrawal\nEmail: iec2025061@iiita.ac.in\nContact: 6263674950"
    },
    {
        "name": "Chandni Agrawal", "email": "iec2025061@iiita.ac.in", "portfolio": "Belarus",
        "co_delegate_details": "Name: Aaditya Maurya\nEmail: iit2025057@iiita.ac.in\nContact: 9867187373"
    },
    {
        "name": "Pauravi Pathak", "email": "iec2025076@iiita.ac.in", "portfolio": "Belgium",
        "co_delegate_details": "Name: Dhairya Fofariya\nEmail: iit2025119@iiita.ac.in\nContact: 8591911283"
    },
    {
        "name": "Dhairya Fofariya", "email": "iit2025119@iiita.ac.in", "portfolio": "Belgium",
        "co_delegate_details": "Name: Pauravi Pathak\nEmail: iec2025076@iiita.ac.in\nContact: 7819019890"
    },
    {
        "name": "Arnavi", "email": "iib2025009@iiita.ac.in", "portfolio": "Germany",
        "co_delegate_details": "Name: Nishihee Shah\nEmail: iib2025002@iiita.ac.in\nContact: 8200486999"
    },
    {
        "name": "Nishihee Shah", "email": "iib2025002@iiita.ac.in", "portfolio": "Germany",
        "co_delegate_details": "Name: Arnavi\nEmail: iib2025009@iiita.ac.in\nContact: 9322582699"
    },
    {
        "name": "Singh Udit Bhanwar", "email": "iib2025012@iiita.ac.in", "portfolio": "Israel",
        "co_delegate_details": "Name: SACHIN SURESHKUMAR\nEmail: iit2025253@iiita.ac.in\nContact: 7397064301"
    },
    {
        "name": "SACHIN SURESHKUMAR", "email": "iit2025253@iiita.ac.in", "portfolio": "Israel",
        "co_delegate_details": "Name: Singh Udit Bhanwar\nEmail: iib2025012@iiita.ac.in\nContact: 9604991574"
    },
    {
        "name": "Arpit Mishra", "email": "iec2025094@iiita.ac.in", "portfolio": "Poland",
        "co_delegate_details": "Name: Kartikay Arya\nEmail: iec2025115@iiita.ac.in\nContact: 7456855449"
    },
    {
        "name": "Kartikay Arya", "email": "iec2025115@iiita.ac.in", "portfolio": "Poland",
        "co_delegate_details": "Name: Arpit Mishra\nEmail: iec2025094@iiita.ac.in\nContact: 7666503850"
    },
    {
        "name": "Gaurang Srivastava", "email": "gaurang.srivastava.december@gmail.com", "portfolio": "India",
        "co_delegate_details": "Name: Siddhi Srivastava\nEmail: siddhi.srivastava08@gmail.com\nContact: 8953295990"
    },
    {
        "name": "Siddhi Srivastava", "email": "siddhi.srivastava08@gmail.com", "portfolio": "India",
        "co_delegate_details": "Name: Gaurang Srivastava\nEmail: gaurang.srivastava.december@gmail.com\nContact: 7275375611"
    },
    {
        "name": "Abhiraj Mandal", "email": "abhirajmandal18@gmail.com", "portfolio": "UK",
        "co_delegate_details": "Name: Mohnish Singh\nEmail: mohnishsinghdps@gmail.com\nContact: 7897103686"
    },
    {
        "name": "Mohnish Singh", "email": "mohnishsinghdps@gmail.com", "portfolio": "UK",
        "co_delegate_details": "Name: Abhiraj Mandal\nEmail: abhirajmandal18@gmail.com\nContact: 7439318128"
    },
    {
        "name": "Aarnav Bhargava", "email": "aarnavkrishna0712@gmail.com", "portfolio": "Egypt",
        "co_delegate_details": "Name: Lakshya Rastogi\nEmail: rastogil389@gmail.com\nContact: 6394562402"
    },
    {
        "name": "Lakshya Rastogi", "email": "rastogil389@gmail.com", "portfolio": "Egypt",
        "co_delegate_details": "Name: Aarnav Bhargava\nEmail: aarnavkrishna0712@gmail.com\nContact: 9369137785"
    },
    {
        "name": "Aaradhya Pandey", "email": "aruna.auditor@gmail.com", "portfolio": "Denmark",
        "co_delegate_details": "Name: Anvi Pandey\nEmail: aanvipandey29042009@gmail.com\nContact: 9235606522"
    },
    {
        "name": "Anvi Pandey", "email": "aanvipandey29042009@gmail.com", "portfolio": "Denmark",
        "co_delegate_details": "Name: Aaradhya Pandey\nEmail: aruna.auditor@gmail.com\nContact: 9452541000"
    },
    {
        "name": "Aviral Agarwal", "email": "iit2025156@iiita.ac.in", "portfolio": "Panama",
        "co_delegate_details": "Name: Lakshay Arora\nEmail: iit2025117@iiita.ac.in\nContact: 9667043930"
    },
    {
        "name": "Lakshay Arora", "email": "iit2025117@iiita.ac.in", "portfolio": "Panama",
        "co_delegate_details": "Name: Aviral Agarwal\nEmail: iit2025156@iiita.ac.in\nContact: 7017715552"
    },
    {
        "name": "Sudhanshu Kalekinge", "email": "iec2025013@iiita.ac.in", "portfolio": "France",
        "co_delegate_details": "Name: Aryan Gupta\nEmail: iec2025032@iiita.ac.in\nContact: 9140899844"
    },
    {
        "name": "Aryan Gupta", "email": "iec2025032@iiita.ac.in", "portfolio": "France",
        "co_delegate_details": "Name: Sudhanshu Kalekinge\nEmail: iec2025013@iiita.ac.in\nContact: 9699976476"
    },
    {
        "name": "Paarth Arora", "email": "iit2025280@iiita.ac.in", "portfolio": "Iran",
        "co_delegate_details": "Name: Lalmuankima\nEmail: iit2025228@iiita.ac.in\nContact: 6009174577"
    },
    {
        "name": "Lalmuankima", "email": "iit2025228@iiita.ac.in", "portfolio": "Iran",
        "co_delegate_details": "Name: Paarth Arora\nEmail: iit2025280@iiita.ac.in\nContact: 8934033009"
    },
    {
        "name": "Rudra Mina", "email": "iit2025232@iiita.ac.in", "portfolio": "Norway",
        "co_delegate_details": "Name: Nasit Deep Bhupendrabhai\nEmail: iec2025072@iiita.ac.in\nContact: 9409530565"
    },
    {
        "name": "Nasit Deep Bhupendrabhai", "email": "iec2025072@iiita.ac.in", "portfolio": "Norway",
        "co_delegate_details": "Name: Rudra Mina\nEmail: iit2025232@iiita.ac.in\nContact: 8890018259"
    },
    {
        "name": "Pushpit Deshmukh", "email": "iit2025138@iiita.ac.in", "portfolio": "Sweden",
        "co_delegate_details": "Name: Amogh S.\nEmail: iit2025290@iiita.ac.in\nContact: 9467498153"
    },
    {
        "name": "Amogh S.", "email": "iit2025290@iiita.ac.in", "portfolio": "Sweden",
        "co_delegate_details": "Name: Pushpit Deshmukh\nEmail: iit2025138@iiita.ac.in\nContact: 7028739773"
    },
    {
        "name": "Md Shahan Ahmad", "email": "iit2025247@iiita.ac.in", "portfolio": "Singapore",
        "co_delegate_details": "Name: Hansika Malpani\nEmail: iec2025111@iiita.ac.in\nContact: 8003702102"
    },
    {
        "name": "Hansika Malpani", "email": "iec2025111@iiita.ac.in", "portfolio": "Singapore",
        "co_delegate_details": "Name: Md Shahan Ahmad\nEmail: iit2025247@iiita.ac.in\nContact: 9162967170"
    },
    {
        "name": "Manisha katariya", "email": "iit2025275@iiita.ac.in", "portfolio": "Japan",
        "co_delegate_details": "Name: Pranav Dewangan\nEmail: iec2025016@iiita.ac.in\nContact: 9969628871"
    },
    {
        "name": "Pranav Dewangan", "email": "iec2025016@iiita.ac.in", "portfolio": "Japan",
        "co_delegate_details": "Name: Manisha katariya\nEmail: iit2025275@iiita.ac.in\nContact: 9617683969"
    },
]


# --- Email Content Templates ---
email_subject_template = "Portfolio Allocation for {name}: UNSC - IIIT-A MUN'25"

# This is a fallback version for email clients that don't support HTML.
email_body_plain = """
Dear {name},

Greetings from the Organizing Committee!

We are pleased to inform you of your portfolio allocation for the United Nations Security Council (UNSC). This is a double delegation committee.

Your allocated portfolio is: {portfolio}

You will be working with your co-delegate. Here are their details for coordination:
{co_delegate_details}

Please get in touch with your partner at your earliest convenience to begin preparations.
Also, please find the Whatsapp group given below and stay updated: https://chat.whatsapp.com/BsJNpioXgDYBMyDsfQyTXo

Best regards,
The Secretariat
"""

# This is the main HTML version that supports bold text and links.
email_body_html = """
<html>
  <head></head>
  <body>
    <p>Dear <b>{name}</b>,</p>
    <p>Greetings from the Organizing Committee!</p>
    <p>We are pleased to inform you of your portfolio allocation for the <b>United Nations Security Council (UNSC)</b>. This is a double delegation committee.</p>
    <p>Your allocated portfolio is: <b>{portfolio}</b></p>
    <p>You will be working with your co-delegate. Here are their details for coordination:<br>
    <pre>{co_delegate_details}</pre>
    </p>
    <p>Please get in touch with your partner at your earliest convenience to begin preparations.<br>
    Also, please find the Whatsapp group given below and stay updated: <a href="https://chat.whatsapp.com/BsJNpioXgDYBMyDsfQyTXo">Join the whatsapp group here</a></p>
    <p>Best regards,<br>
    The Secretariat</p>
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
                    message["Subject"] = email_subject_template.format(name=recipient["name"])

                    # Create the plain-text and HTML versions of your message
                    plain_text_part = MIMEText(email_body_plain.format(name=recipient["name"], portfolio=recipient["portfolio"], co_delegate_details=recipient["co_delegate_details"]), "plain", "utf-8")
                    html_part = MIMEText(email_body_html.format(name=recipient["name"], portfolio=recipient["portfolio"], co_delegate_details=recipient["co_delegate_details"]), "html", "utf-8")

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

