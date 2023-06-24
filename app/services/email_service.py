import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from os import getenv
import socket

class EmailService:
    def __init__(self) -> None:
        self.sender = "rupay.oficial@gmail.com"
        self.password = "tzsdeyhibkixalgo"

        # Default port for starttls
        port = 587
        # Create a secure SSL context
        context = ssl.create_default_context()

        try: 
            print(">>> Iniciando conexão SMTP...")
            socket.setdefaulttimeout(5000)
            self.server = smtplib.SMTP("smtp.gmail.com", port, timeout=7000)
            self.server.ehlo()
            self.server.starttls(context=context)
            self.server.ehlo()
            self.server.login(self.sender, self.password)
            print(">>> Conexão realizada com sucesso!")
        except Exception as e:
            print(e)
            self.server.quit()

    def send_email(self, email: str):
        print(f">>> Enviando email para {email}....")
        try:
            message = self.get_formatted_email(email, "Kleber", "162524")
            
            self.server.sendmail(self.sender, email, message)
            
            print(">>> Email enviado com sucesso!")
        except Exception as e:
            print(e)
        finally:
            self.server.quit()
    
    def get_formatted_email(self, email: str, student_name: str, code: str):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Código de cadastro RUPay"
        message["From"] = self.sender
        message["To"] = email

        text_version = MIMEText(self.get_text_version(student_name, code), "plain")
        html_version = MIMEText(self.get_html_version(student_name, code), "html")

        message.attach(text_version)
        message.attach(html_version)

        return message.as_string()

    def get_text_version(self, student_name: str, code: str):
        text = f"""\
        Olá, {student_name}

        O seu código de cadastr RUPay é {code}

        Equipe RUPay
        """

        return text

    def get_html_version(self, student_name: str, code: str):
        html = f"""\
        <html>
            <body>
                <p>
                    Olá, {student_name}<br>
                    O seu código de cadastro RUPay é
                </p>
                
                <h3>{code}</h3>

                <p style="font-size:0.8em;">Equipe RUPay</p>
            </body>
        </html>
        """

        return html
    
def get_institucional_email(college_id: str):
    return f"{college_id}@aluno.unb.br"