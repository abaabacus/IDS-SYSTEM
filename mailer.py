import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

def send_malicious_ip_alert(data, recipients):
    SMTP_SERVER = "smtp.gmail.com"
    PORT = 587
    SENDER_EMAIL = 'ananya19032002@gmail.com'
    SENDER_PASSWORD = 'upuk gsgs pbrk mhhq'

    data = pd.DataFrame(data)
    data = data[data['Label'] != 'Normal']

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Malicious IP Address Alert</title>
        <style>
            /* Global Styles */
            body {
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                color: #333;
                line-height: 1.6;
            }

            .container {
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }

            h1 {
                color: #007bff;
            }

            p {
                margin-bottom: 20px;
            }

            /* Table Styles */
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }

            th, td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }

            th {
                background-color: #f0f0f0;
                font-weight: bold;
            }

            /* Button Styles */
            .btn {
                display: inline-block;
                padding: 10px 20px;
                background-color: #007bff;
                color: #fff;
                text-decoration: none;
                border-radius: 5px;
                transition: background-color 0.3s ease-in-out;
            }

            .btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Malicious IP Address Alert</h1>
            <p>Hello Admin,</p>
            <p>Please be informed about the following IP addresses that are flagged as malicious:</p>
            
            <table>
                <thead>
                    <tr>
                        <th>Slno</th>
                        <th>IP Address</th>
                        <th>Reason</th>
                    </tr>
                </thead>
                <tbody>
    """

    i = 1
    for index, row in data.iterrows():
        html_content += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{row['IP_Address']}</td>
                        <td>{row['Label']}</td>
                    </tr>
        """
        i += 1

    html_content += """
                </tbody>
            </table>

            <p>Thank you for your attention.</p>
            <a href="http://127.0.0.1:8080/home" class="btn">Monitor</a>
        </div>
    </body>
    </html>
    """

    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['Subject'] = "Alert: Malicious IP Address Requests"

    message.attach(MIMEText(html_content, 'html'))

    for recipient in recipients:
        message['To'] = recipient
        try:
            with smtplib.SMTP(SMTP_SERVER, PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, recipient, message.as_string())
            print(f"Email sent successfully to {recipient}!")
        except Exception as e:
            print(f"Error sending email to {recipient}: {e}")

# recipients_list = ['recipient1@example.com', 'recipient2@example.com', 'recipient3@example.com']
# data = {'IP Address': ['192.168.1.1', '10.0.0.1'], 'Reason': ['Suspicious activity', 'Malware detected'], 'Label': ['Malicious', 'Malicious']}
# send_malicious_ip_alert(data, recipients_list)
