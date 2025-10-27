import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time # Used for simulated time in the example

# --- SMTP Server Configuration for The University of Iowa ---
SMTP_SERVER = "ns-mx.uiowa.edu"
SMTP_PORT = 25
# The service is unauthenticated and restricted to systems on GSA/LSA.

def send_uiowa_email(recipient_email, subject, body, sender_email="your_project_system@uiowa.edu"):
    """
    Sends an email using the unauthenticated University of Iowa SMTP server.

    NOTE: This script must be run from a system on the GSA or LSA network,
          and the recipient_email must be a valid University of Iowa M365 domain address.

    Args:
        recipient_email (str): The email address to send the notification to.
        subject (str): The subject line of the email.
        body (str): The main content of the email.
        sender_email (str): The sender's email address (can be a system address).
    """
    try:
        # 1. Create the email message object
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        # 2. Connect to the SMTP server
        # Since this service is on port 25 and is unauthenticated, we use SMTP()
        print(f"Connecting to SMTP server: {SMTP_SERVER}:{SMTP_PORT}...")
        with smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT, timeout=10) as server:
            # The UIowa server on port 25 is unauthenticated, so no login is needed.

            # 3. Send the mail
            server.sendmail(sender_email, [recipient_email], msg.as_string())

            print("Email sent successfully!")

    except smtplib.SMTPException as e:
        print(f"Error: Unable to send email. SMTP Error: {e}")
        print("Please ensure your device is on the GSA/LSA network and the recipient address is a UIowa M365 domain.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Example Usage for the Electric Eye Project ---

def generate_safety_alert_message():
    """Generates the required Critical Safety Event message."""
    # Get the current time and format it as required by the lab document.
    # Format: "Critical Safety Event at HH:MM XX on Month/Day/Year" 
    # HH (00-12), MM (00-59), XX (AM/PM), Month (01-12), Day (01-31)

    # Use 'I' for 12-hour format (01-12), 'M' for minute, 'p' for AM/PM, '%m' for month, '%d' for day, '%Y' for year.
    now = datetime.now()
    formatted_time = now.strftime("%I:%M %p on %m/%d/%Y")
    # Correct for 12 AM/PM format (Python's '%I' handles 01-12; '00' is not strictly required but the format is 00-12)
    # The string '00' to '12' for HH is implied by the 12-hour clock format.

    message = f"Critical Safety Event at {formatted_time}"
    return message

# --- Implementation in your design logic ---

# 1. Define the recipient (e.g., an email-to-SMS gateway for a cell phone notification)
TARGET_RECIPIENT = "scottpearson@uiowa.edu"

# 2. Simulate the event trigger (e.g., when the photodiode signal drops below threshold)
def on_beam_interrupted():
    """This function is called when the electric eye beam is physically obstructed."""
    subject_line = "URGENT: Electric Eye Beam Interruption"
    alert_body = generate_safety_alert_message()
    
    print("\n--- Beam Interrupted! Sending Alert ---")
    send_uiowa_email(
        recipient_email=TARGET_RECIPIENT,
        subject=subject_line,
        body=alert_body
    )
    print("---------------------------------------\n")

# --- Test the functionality ---
if __name__ == "__main__":
    print("Simulating a beam interruption event...")
    # Simulate the event (e.g., a function call from your microcontroller's monitoring loop)
    on_beam_interrupted()
    
    # Wait a bit before simulating the next event
    time.sleep(2)
    
    print("Simulating a second beam interruption event...")
    on_beam_interrupted()
