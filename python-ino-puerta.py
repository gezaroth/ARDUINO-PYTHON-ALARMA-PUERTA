import serial
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from keys import *

# Configura los parámetros del puerto serie
SERIAL_PORT = '' 
BAUD_RATE = 115200

# Configuración de Gmail
EMAIL = ''
PASSWORD = EMAIL_PASSWORD
RECIPIENT_EMAIL = ''

def send_email():
    subject = "Alerta de Proximidad"
    body = "Se ha detectado un objeto cerca del sensor ultrasónico."

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Conexión al servidor SMTP de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Inicia la conexión TLS
        server.login(EMAIL, PASSWORD)  # Inicia sesión con tus credenciales
        server.send_message(msg)  # Envía el mensaje
        server.quit()  # Cierra la conexión
        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

# Configura el puerto serie
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)  # Espera a que el puerto esté listo

# Bucle principal
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line == "ALERTA!":
            send_email()
