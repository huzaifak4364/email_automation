import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from dotenv import load_dotenv


PORT = 587
EMAIL_SERVER = "smtp.gmail.com"

current_dir = Path(__file__).resolver(
).parent if "_file_" in locals() else Path.cwd()
envars = current_dir / "email.env"
load_dotenv(envars)

sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")
app_password = os.getenv("APP_PASSWORD")


def send_email(row):
    subject = "Your order is on its way"
    name = row[0]
    last_name = row[1]
    reciever_email = row[2]
    number = row[4]
    street_address = row[5]
    city = row[6]
    province = row[7]
    postal_code = row[8]
    payment_method = row[9]
    date = row[10]
    items = row[13].replace('\n', '</br>')
    items = row[13].replace('\n', '</br>')

    items_list = items.split('\n')
    new_items = ' '
    for item in items_list:
        new_items += '\n' + item
        print(item)



    with open('email_template.html', 'r') as file:
        email_template = file.read()
    email_template = email_template.format(name=name, last_name=last_name, city=city,
                                           province=province, postal_code=postal_code, street_address=street_address, number=number, reciever_email=reciever_email)

    msg = EmailMessage()
    msg['Subject'] = subject
    msg["From"] = formataddr(("Khana", f"{sender_email}"))
    msg["To"] = row[0]

    msg.set_content(
        f"""\
            First Name: {name},
            City: {city}
            Province: {province}
            Postal Code: {postal_code}
            Street Address: {street_address}
            Number: {number}
            Last Name: {last_name}
            """

    )

    msg.add_alternative(
        f"""\<html>
<head>
  <title>Order Confirmation</title>
</head>
<body>
  <h1>Your order has been placed</h1>
  <h2> Below our the details of your order</h2>
  <p>Date:{date}</p>
  <p>First Name:{name}</p>
  <p>Last Name:{last_name}</p>
  <p>Email Address:{reciever_email}</p>
  <p>Phone Number:{number}</p>
  <p>Street Address:{street_address}</p>
  <p>City:{city}</p>
  <p>Province:{province}</p>
  <p>Postal Code:{postal_code}</p>
  <p>Payment Method:{payment_method}</p>
  <p>Order Details:{items}</p>
  <p>If there are any concerns please reply to this email with your problem</p>
</body>
</html>
""",
subtype="html"
    )
        

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, reciever_email, msg.as_string())


if __name__ == "__main__":
    send_email(row=["Arsh", "Kamran",
               "coolarshkamran@gmail.com", "Waterloo", "647", "horizon", "", "Ontario", "L4B"])
