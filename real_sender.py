import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time 
import serial # Serial communication library
import serial.tools.list_ports # Utility to help find the port

# --- Configuration (Set these values correctly) ---
SMTP_SERVER = "ns-mx.uiowa.edu"
SMTP_PORT = 25
TARGET_RECIPIENT = "scottpearson@uiowa.edu"
SENDER_EMAIL = "ece4880lab2-system@uiowa.edu"
BAUD_RATE = 9600           # Match this to your Arduino's Serial.begin() speed
TRIGGER_MESSAGE = "BLOCK"  # The specific string the Arduino will send on error

# --- Serial Port Setup ---
def find_arduino_port():
    """Tries to automatically find an Arduino-like serial port."""
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        # Common identifiers for Arduino/Microcontroller boards (modify as needed)
        if 'Arduino' in desc or 'USB Serial Device' in desc or 'ACM' in port or 'USB' in port:
            print(f"Found potential Arduino port: {port}")
            return port
    print("Could not automatically find an Arduino-like port. Please specify manually.")
    # Return a default common port name for manual correction
    return "COM3" # or "/dev/ttyACM0" or "/dev/ttyUSB0"

# --- Email Function ---

def generate_safety_alert_message():
    """Generates the required Critical Safety Event message."""
    now = datetime.now()
    formatted_time = now.strftime("%I:%M %p on %m/%d/%Y")
    message = f"Critical Safety Event at {formatted_time}"
    return message

def send_uiowa_email(recipient_email, subject, body, sender_email=SENDER_EMAIL):
    """Sends an email using the unauthenticated UIowa SMTP server."""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        with smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT, timeout=10) as server:
            server.sendmail(sender_email, [recipient_email], msg.as_string())
            print("  [ALERT] Email sent successfully!")

    except smtplib.SMTPRecipientsRefused as e:
        print(f"  [ERROR] Recipient Refused. SMTP Error: {e}")
    except smtplib.SMTPException as e:
        print(f"  [ERROR] Unable to send email. SMTP Error: {e}")
    except Exception as e:
        print(f"  [ERROR] An unexpected error occurred during email transmission: {e}")

# --- Trigger Function ---

def on_beam_interrupted():
    """Called when the serial monitor receives the critical trigger message."""
    subject_line = "CRITICAL: Electric Eye Beam Interrupted"
    alert_body = generate_safety_alert_message()
    
    print(f"\n📢 CRITICAL EVENT DETECTED! Triggering alert at {datetime.now().strftime('%H:%M:%S')}")
    send_uiowa_email(
        recipient_email=TARGET_RECIPIENT,
        subject=subject_line,
        body=alert_body
    )
    print("------------------------------------------------------------------\n")


# --- Main Serial Monitoring Loop ---

def start_serial_monitor():
    """
    Initializes the serial connection and continuously reads data.
    Triggers the alert when the specific message is received.
    """
    port_name = find_arduino_port()
    print(f"Connecting to port {port_name} at {BAUD_RATE} baud...")
    
    try:
        # Initialize the serial connection
        ser = serial.Serial(port_name, BAUD_RATE, timeout=1)
        # Clear any initial garbage data
        ser.flush() 
        print("Serial Monitor Active. Waiting for Arduino data...")

        while True:
            # Read a line of data (waits up to 'timeout' seconds)
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                
                # Check if the received line is the trigger message
                if line == TRIGGER_MESSAGE:
                    on_beam_interrupted()
                
                # Print all other data for debugging purposes
                if line:
                    print(f"[Arduino]: {line}")

            time.sleep(0.01) # Small delay to keep the CPU happy

    except serial.SerialException as e:
        print(f"\nSERIAL ERROR: Could not open/read port {port_name}.")
        print(f"Please check if the Arduino is plugged in and the port name is correct.")
        print(f"Error details: {e}")
    except KeyboardInterrupt:
        print("\nMonitor stopped by user.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    start_serial_monitor()
