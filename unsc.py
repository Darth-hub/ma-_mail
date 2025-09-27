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
    #      "co_delegate_details": "Name: Aditi Deshmukh\nEmail: iit2025217@iiita.ac.in\nContact: 9819062437\nCollege: IIIT Allahabad"
    # },
    # {
    #     "name": "Aditi Deshmukh", "email": "iit2025217@iiita.ac.in", "portfolio": "USA",
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
email_subject_template = "IIITA MUN'25 : Portfolio Allocation for UNSC"
email_body_template = """
Dear {name},

Greetings from the School-MUN Organizing Committee!

We are pleased to inform you of your portfolio allocation for the **United Nations Security Council (UNSC)**. This is a double delegation committee.

Your allocated portfolio is: **{portfolio}**

You will be working with your co-delegate. Here are their details for coordination:
{co_delegate_details}

Please get in touch with your partner at your earliest convenience to begin preparations. 
Also, please find the Whatsapp group given below and stay updated: https://chat.whatsapp.com/BsJNpioXgDYBMyDsfQyTXo
Best regards,
The Secretariat
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
                    message = MIMEMultipart("alternative")
                    message["From"] = SENDER_EMAIL
                    message["To"] = recipient["email"]
                    
                    # Personalize the email subject and body
                    message["Subject"] = email_subject_template.format(name=recipient["name"])
                    body = email_body_template.format(name=recipient["name"], portfolio=recipient["portfolio"], co_delegate_details=recipient["co_delegate_details"])
                    
                    part = MIMEText(body, "plain")
                    message.attach(part)

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
