import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from twilio.rest import Client

# --------------- PDF Generation ---------------

# Data for the table
DATA = [
    ["Date", "Name", "Subscription", "Price (Rs.)"],
    ["16/11/2020", "Full Stack Development with React & Node JS - Live", "Lifetime", "10,999.00/-"],
    ["16/11/2020", "Geeks Classes: Live Session", "6 months", "9,999.00/-"],
    ["Sub Total", "", "", "20,9998.00/-"],
    ["Discount", "", "", "-3,000.00/-"],
    ["Total", "", "", "17,998.00/-"]
]

pdf_file_name = "receipt.pdf"
pdf = SimpleDocTemplate(pdf_file_name, pagesize=A4)

styles = getSampleStyleSheet()
title_style = styles["Heading1"]
title_style.alignment = 1

# Title and table
title = Paragraph("Billing Information", title_style)
style = TableStyle(
    [
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("GRID", (0, 0), (4, 4), 1, colors.black),
        ("BACKGROUND", (0, 0), (3, 0), colors.gray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ]
)

table = Table(DATA, style=style)
pdf.build([title, table])

# --------------- Sender's Credentials (Hardcoded) ---------------

# Email credentials (Sender's info)
sender_email = "sg1201333@gmail.com"
sender_password = "bsot nqhz jkqh dapa"  # Use an app-specific password if necessary

# Twilio credentials (Sender's info)
account_sid = "ACd197ef3b909e5d0dde038b9162f15cca"
auth_token = "40727956885535d10489bec60200d5a0"
twilio_number = "+14253827123"  # Your Twilio phone number

# --------------- Get Customer's Email and Mobile Number ---------------

# Input recipient's email and mobile number
customer_email = input("Enter customer's email: ")
customer_mobile = input("Enter customer's mobile number (with country code, e.g., +1234567890): ")

# --------------- Send PDF via Email ---------------

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = customer_email
msg['Subject'] = "Your Bill Receipt"

# Email body
body = "Please find attached your bill receipt."
msg.attach(MIMEText(body, 'plain'))

# Attach the PDF file
with open(pdf_file_name, "rb") as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={pdf_file_name}')
    msg.attach(part)

# Sending the email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, sender_password)
server.sendmail(sender_email, customer_email, msg.as_string())
server.quit()

print(f"Email sent to {customer_email}")

# --------------- Send SMS via Twilio ---------------

client = Client(account_sid, auth_token)

# Bill summary for SMS
bill_summary = """
Billing Information:
Date: 16/11/2020
Full Stack Development with React & Node JS - Live: 10,999.00/-
Geeks Classes: 9,999.00/-
Total: 17,998.00/-
"""

# Send the SMS
message = client.messages.create(
    body=bill_summary,
    from_=twilio_number,  # Your Twilio phone number
    to=customer_mobile  # Customer's mobile number
)

print(f"SMS sent to {customer_mobile}")
