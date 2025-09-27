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

# --- Recipient List (Combined and cleaned from all your provided data) ---
recipients = [
    # --- From First Batch ---
    {"name": "aa", "email": "ayushranjan112400@gmail.com", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Shaurya Goswami", "email": "shauryathebeast08@gmail.com", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Joanna V. Emmanuel", "email": "joanvemmanuel@gmail.com", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Gaurang Srivastava", "email": "gaurang.srivastava.december@gmail.com", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Siddhi Srivastava", "email": "siddhi.srivastava08@gmail.com", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Aditya Bajpai", "email": "a47b61@gmail.com", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Mohd Jafar Sadiq", "email": "jafarsadiqghost@gmail.com", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Hridyansh", "email": "hridyanshx7@gmail.com", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Lemuel Aaron Singh", "email": "lemuel.aaron.singh@gmail.com", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Anvesh Srivastava", "email": "anveshsrivastava936@gmail.com", "topic": "International Committee (ECOSOC)"},
    {"name": "Aarush krishna", "email": "aarushk076@gmail.com", "topic": "International Committee (ECOSOC)"},
    {"name": "Raghav Mishra", "email": "aditya.25518092@hrc.du.ac.in", "topic": "AIPPM"},
    {"name": "Shivansh Shekhar", "email": "shivanshshekhar21@gmail.com", "topic": "International Committee (ECOSOC)"},
    {"name": "Prathit Bhadouriya", "email": "prathitb21@gmail.com", "topic": "International Committee (ECOSOC)"},
    {"name": "Gg", "email": "iec2023008@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    
    # --- From Second Batch (New Data) ---
    {"name": "Aviral Agarwal", "email": "iit2025156@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Nikhil Raj", "email": "iit2025293@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Venkat Vempati", "email": "iit2025203@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Himanshi Yadav", "email": "iib2025017@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Shourya Sankrit", "email": "iec2025039@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Krishna Taneja", "email": "iit2025167@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Bharat Upadhyay", "email": "iit2025045@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Siddharth Gupta", "email": "iit2025107@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Chaitanya Pradip Wagh", "email": "iit2025123@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Sayak Chakrabarty", "email": "iec2025108@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Roshan Shinde", "email": "iit2025269@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Paarth Sharma", "email": "iit2025233@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Rohit Malik", "email": "iit2025033@iiita.ac.in", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Aditya Das", "email": "iit2025130@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Pratham Makwana", "email": "iib2025005@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Adarsh Yadav", "email": "iec2025109@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Rahi Shivshankar Birajdar", "email": "iit2025027@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "NIDAMARTHI CHANDANA", "email": "iit2025034@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Asra Tabassum", "email": "iit2025063@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Ayush Pancholi", "email": "iec2025019@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Hema Harshitha Sarvasiddi", "email": "iit2025082@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Venkata siddhant vooda", "email": "iit2025181@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Abhyudaya Kumar", "email": "iec2025055@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Debojyoti Chakrabarti", "email": "iec2025003@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Rishav Kant Deo", "email": "iib2025010@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Soumya Ravi Godghate", "email": "iit2025054@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Saksham chadar", "email": "iec2025077@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Rishabh Verma", "email": "iec2025079@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Rudransh Joshi", "email": "iec2025083@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Sayantan Hait", "email": "iec2025078@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Palak Ukey", "email": "iec2025031@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Pratik Chaturvedi", "email": "iit2025087@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Ishan agrawal", "email": "iec2025064@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Janhavi Shastri", "email": "iit2025091@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Ameya Narayanam", "email": "iit2025051@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Harshvardhan Arya", "email": "iec2025060@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Bonala Vinoothna Lakshmi", "email": "iib2025016@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Ankit Kumar Chaudhary", "email": "iec2025027@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Hansika Mudavath", "email": "iit2025089@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Mannat Jain", "email": "iit2025262@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Amrita Singh", "email": "iit2025244@iiita.ac.in", "topic": "International Committee (ECOSOC)"},
    {"name": "Mann Kumar Gupta", "email": "iec2025052@iiita.ac.in", "topic": "International Committee (ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Nimar", "email": "iit2025291@iiita.ac.in", "topic": "International Committee (ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Darshil Shah", "email": "iit2025255@iiita.ac.in", "topic": "International Committee (ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Sahitya Gulab Jagtap", "email": "iit2025049@iiita.ac.in", "topic": "International Committee (ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "ARPIT Mishra", "email": "iec2025094@iiita.ac.in", "topic": "International Committee (ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Chandra vikram sai", "email": "iit2024116@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Bomedi Shanyu Reddy", "email": "iit2025078@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Atharv Rahul Dehedkar", "email": "iit2025020@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Spandana Surepally", "email": "iib2025033@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Aditi Deshmukh", "email": "iit2025217@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Tanish vaibhav", "email": "tanishvaibhav78@gmail.com", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Krish Sushil Kinger", "email": "iit2025281@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Gondaliya Vaidehi Pareshbhai", "email": "iit2025146@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Ayush Saha", "email": "iit2025259@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Amogh S.", "email": "iit2025290@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Pranjali Goel", "email": "iit2025129@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Arihant Sinha", "email": "iit2025008@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Pranshu Sethi", "email": "iit2025283@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Harshvardhan", "email": "iit2025177@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Lalmuankima", "email": "iit2025228@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Bhavya Sagar", "email": "iit2025171@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Nishkarsh Saxena", "email": "iit2025088@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Manisha katariya", "email": "iit2025275@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Pranav Dewangan", "email": "iec2025016@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Advaith Puthanmadathil Sajeev", "email": "iec2025059@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Kondepudi Mani Surya Asrith", "email": "iec2025065@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Pushpit Deshmukh", "email": "iit2025138@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Sanskruti Shailesh Bhamare", "email": "iec2025035@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Kashish Jadhaw", "email": "iec2025018@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Sefora Mokena", "email": "iec2025074@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Tanisha Nayal", "email": "iit2025074@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Diya Dutta", "email": "iec2025005@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Namrata Hooda", "email": "iit2025143@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Sanya Sinha", "email": "iit2025001@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Nasit Deep Bhupendrabhai", "email": "iec2025072@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Rudra Mina", "email": "iit2025232@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Lakshmish S G", "email": "iec2025034@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Sachin Benakannavar", "email": "iec2025025@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "AVINASHKUMAR HARESH MANGHNANI", "email": "iib2025031@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Chandni Agrawal", "email": "iec2025061@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Aaditya Maurya", "email": "iit2025057@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Paarth Arora", "email": "iit2025280@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "SACHIN SURESHKUMAR", "email": "iit2025253@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Pauravi Pathak", "email": "iec2025076@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Dhairya Fofariya", "email": "iit2025119@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Singh Udit Bhanwar", "email": "iib2025012@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Md Shahan Ahmad", "email": "iit2025247@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Sudhanshu Kalekinge", "email": "iec2025013@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "nishihee shah", "email": "iib2025002@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Arnavi", "email": "iib2025009@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Kartikay Arya", "email": "iec2025115@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Supriya Kant", "email": "iec2025089@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Lakshay Arora", "email": "iit2025117@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Hansika Malpani", "email": "iec2025111@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Aryan Gupta", "email": "iec2025032@iiita.ac.in", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Mohammad Sultan", "email": "sultanpoke123@gmail.com", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Anvi Pandey", "email": "aanvipandey29042009@gmail.com", "topic": "International Committee (UNSC/ECOSOC) + All India Political Party Meet (AIPPM)"},
    {"name": "Aaradhya Pandey", "email": "aruna.auditor@gmail.com", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Sara Nasrat", "email": "pewds072@gmail.com", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Prabjyot kaur", "email": "parvinderkaur123454321@gmail.com", "topic": "International Committee (UNSC/ECOSOC)"},
    {"name": "Lakshya Rastogi", "email": "rastogil389@gmail.com", "topic": "International Committee (ECOSOC/UNSC)"},
    {"name": "Aarnav Bhargava", "email": "aarnavkrishna0712@gmail.com", "topic": "International Committee (ECOSOC/UNSC)"},
    {"name": "Abhiraj Mandal", "email": "abhirajmandal18@gmail.com", "topic": "International Committee (ECOSOC/UNSC)"},
    {"name": "Mohnish Singh", "email": "mohnishsinghdps@gmail.com", "topic": "International Committee (ECOSOC/UNSC)"},
    {"name": "Kabir Capoor", "email": "kabiircapoor1808@gmail.com", "topic": "International Committee (ECOSOC)"},
    {"name": "Dev Sachdeva", "email": "devsachdevapankaj@gmail.com", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Shivansh Mangalam", "email": "mangalam9shivansh@gmail.com", "topic": "All India Political Party Meet (AIPPM)"},
    {"name": "Jiya Srivastava", "email": "jiyasrivastava930@gmail.com", "topic": "International Committee (ECOSOC)"},
    {"name": "Tia", "email": "tiiayyh@gmail.com", "topic": "International Committee (ECOSOC)"}
]


# --- Email Content Templates ---
# The script will replace {name} and {topic} with the details from the list above.
email_subject_template = "Confirmation for School-MUN: Your Committee"
email_body_template = """
Dear {name},

Thank you for registering for the School-MUN!

This email is to confirm your participation and your chosen committee: **{topic}**. 

We are excited to have you join us. Further details regarding the committee agenda and background guides will be shared with you in the coming days.

Best regards,
The School-MUN Organizing Committee
"""

# --- Script Logic ---

def send_bulk_emails():
    """
    Connects to the SMTP server and sends a personalized email to each recipient.
    """
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Error: SENDER_EMAIL and SENDER_PASSWORD environment variables are not set.")
        print("Please set them before running the script.")
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
                    
                    message["Subject"] = email_subject_template.format(name=recipient["name"])
                    body = email_body_template.format(name=recipient["name"], topic=recipient["topic"])
                    
                    part = MIMEText(body, "plain")
                    message.attach(part)

                    server.sendmail(SENDER_EMAIL, recipient["email"], message.as_string())
                    print(f"({index + 1}/{len(recipients)}) Email sent successfully to {recipient['name']} <{recipient['email']}>")
                    successful_sends += 1
                except Exception as e:
                    print(f"(!) Failed to send email to {recipient['name']} <{recipient['email']}>. Error: {e}")
                    failed_sends += 1
                
                # IMPORTANT: Delay between emails to avoid being flagged as spam.
                time.sleep(2)

    except smtplib.SMTPAuthenticationError:
        print("\nAuthentication failed. Please check your email/password.")
        print("Tip: If you're using Gmail, make sure to use an 'App Password'.")
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

