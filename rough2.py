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

# --- Recipient List (Curated from your data for UNSC Double Delegation) ---
recipients = [

    {
         "name": "Spandana Surepally", "email": "iec2023008@iiita.ac.in", "portfolio": "USA",
         "co_delegate_details": "Name: Aditi Deshmukh\nEmail: iit2025217@iiita.ac.in\nContact: 9819062437\nCollege: IIIT Allahabad"
    },
    {
        "name": "Aditi Deshmukh", "email": "iit2023189@iiita.ac.in", "portfolio": "USA",
        "co_delegate_details": "Name: Spandana Surepally\nEmail: iib2025033@iiita.ac.in\nContact: 8135500758\nCollege: IIIT Allahabad"
    }

    # {
    #      "name": "Spandana Surepally", "email": "iib2025033@iiita.ac.in", "portfolio": "USA",
    #      "co_delegate_details": "Name: Krish Sushil Kinger\nEmail: iit2025281@iiita.ac.in\nContact: 9307229628\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Krish Sushil Kinger", "email": "iit2025281@iiita.ac.in", "portfolio": "USA",
    #     "co_delegate_details": "Name: Spandana Surepally\nEmail: iib2025033@iiita.ac.in\nContact: 8135500758\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Pranjali Goel", "email": "iit2025129@iiita.ac.in", "portfolio": "Russia",
    #     "co_delegate_details": "Name: Arihant Sinha\nEmail: iit2025008@iiita.ac.in\nContact: 9625956065\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Arihant Sinha", "email": "iit2025008@iiita.ac.in", "portfolio": "Russia",
    #     "co_delegate_details": "Name: Pranjali Goel\nEmail: iit2025129@iiita.ac.in\nContact: 9667225595\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Bhavya Sagar", "email": "iit2025171@iiita.ac.in", "portfolio": "China",
    #     "co_delegate_details": "Name: Nishkarsh Saxena\nEmail: iit2025088@iiita.ac.in\nContact: 9540491284\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Nishkarsh Saxena", "email": "iit2025088@iiita.ac.in", "portfolio": "China",
    #     "co_delegate_details": "Name: Bhavya Sagar\nEmail: iit2025171@iiita.ac.in\nContact: 9915557970\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Advaith Puthanmadathil Sajeev", "email": "iec2025059@iiita.ac.in", "portfolio": "Denmark",
    #     "co_delegate_details": "Name: Kondepudi Mani Surya Asrith\nEmail: iec2025065@iiita.ac.in\nContact: 8179761974\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Kondepudi Mani Surya Asrith", "email": "iec2025065@iiita.ac.in", "portfolio": "Denmark",
    #     "co_delegate_details": "Name: Advaith Puthanmadathil Sajeev\nEmail: iec2025059@iiita.ac.in\nContact: 8590746262\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Sanskruti Shailesh Bhamare", "email": "iec2025035@iiita.ac.in", "portfolio": "Norway",
    #     "co_delegate_details": "Name: Kashish Jadhaw\nEmail: iec2025018@iiita.ac.in\nContact: 8109755718\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Kashish Jadhaw", "email": "iec2025018@iiita.ac.in", "portfolio": "Norway",
    #     "co_delegate_details": "Name: Sanskruti Shailesh Bhamare\nEmail: iec2025035@iiita.ac.in\nContact: 8830380158\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Diya Dutta", "email": "iec2025005@iiita.ac.in", "portfolio": "India",
    #     "co_delegate_details": "Name: Namrata Hooda\nEmail: iit2025143@iiita.ac.in\nContact: 9350866855\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Namrata Hooda", "email": "iit2025143@iiita.ac.in", "portfolio": "India",
    #     "co_delegate_details": "Name: Diya Dutta\nEmail: iec2025005@iiita.ac.in\nContact: 9973839029\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Chandni Agrawal", "email": "iec2025061@iiita.ac.in", "portfolio": "Germany",
    #     "co_delegate_details": "Name: Aaditya Maurya\nEmail: iit2025057@iiita.ac.in\nContact: 9867187373\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Aaditya Maurya", "email": "iit2025057@iiita.ac.in", "portfolio": "Germany",
    #     "co_delegate_details": "Name: Chandni Agrawal\nEmail: iec2025061@iiita.ac.in\nContact: 6263674950\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Pauravi Pathak", "email": "iec2025076@iiita.ac.in", "portfolio": "Brazil",
    #     "co_delegate_details": "Name: Dhairya Fofariya\nEmail: iit2025119@iiita.ac.in\nContact: 8591911283\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Dhairya Fofariya", "email": "iit2025119@iiita.ac.in", "portfolio": "Brazil",
    #     "co_delegate_details": "Name: Pauravi Pathak\nEmail: iec2025076@iiita.ac.in\nContact: 7819019890\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "nishihee shah", "email": "iib2025002@iiita.ac.in", "portfolio": "France",
    #     "co_delegate_details": "Name: Arnavi\nEmail: iib2025009@iiita.ac.in\nContact: 9322582699\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Arnavi", "email": "iib2025009@iiita.ac.in", "portfolio": "France",
    #     "co_delegate_details": "Name: nishihee shah\nEmail: iib2025002@iiita.ac.in\nContact: 8200486999\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Aviral Agarwal", "email": "iit2025156@iiita.ac.in", "portfolio": "Finland",
    #     "co_delegate_details": "Name: Atharv Rahul Dehedkar\nEmail: iit2025020@iiita.ac.in\nContact: 8149900501\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Atharv Rahul Dehedkar", "email": "iit2025020@iiita.ac.in", "portfolio": "Finland",
    #     "co_delegate_details": "Name: Aviral Agarwal\nEmail: iit2025156@iiita.ac.in\nContact: 7017715552\nCollege: IIIT Allahabad"
    # },

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
IIITA MUN'25
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
    The Secretariat
    </p>
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





Aaradhya Pandey	9452541000
Anvi Pandey	9235606522
Lakshya Rastogi 	6394562402
Aarnav Bhargava 	9369137785
Abhiraj Mandal	7439318128
Mohnish Singh	7897103686
Gaurang Srivastava	7275375611
Siddhi Srivastava 	8953295990
Spandana Surepally	8135500758
Krish Sushil Kinger	9307229628
Ayush Saha	9883906709
Amogh S.	94674 98153 
Pranjali Goel	9667225595
Arihant Sinha	9625956065
Pranshu Sethi	8607791934
Lalmuankima	6009174577
Bhavya Sagar	9915557970
Nishkarsh Saxena 	9540491284
Manisha katariya 	9617683969
Pranav Dewangan	9969628871
Advaith Puthanmadathil Sajeev	8590746262
Kondepudi Mani Surya Asrith	8179761974
Pushpit Deshmukh 	7028739773
Sanskruti Shailesh Bhamare 	8830380158
Kashish Jadhaw 	8109755718
Diya Dutta 	9973839029
Namrata Hooda	9350866855
Nasit Deep Bhupendrabhai 	9409530565
Rudra Mina	8890018259
Lakshmish S G	9035662346
Sachin Benakannavar 	7975414051
Chandni Agrawal 	6263674950
Aaditya Maurya 	9867187373
Paarth Arora	8934033009
SACHIN SURESHKUMAR 	7397064301
Pauravi Pathak	7819019890
Dhairya Fofariya	8591911283
Singh Udit Bhanwar	9604991574
Md Shahan Ahmad 	9162967170
Sudhanshu Kalekinge 	9699976476
nishihee shah	8200486999
Arnavi	9322582699
Kartikay Arya 	7456855449
Lakshay Arora 	9667043930
Hansika Malpani 	8003702102
Aryan Gupta	9140899844
Aviral Agarwal 	7017715552
ARPIT Mishra 	7666503850