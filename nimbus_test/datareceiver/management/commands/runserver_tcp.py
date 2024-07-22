import socket
import threading
import logging
import re
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from datareceiver.models import ReceivedData

# Configuração do logger
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the TCP server'

    def handle(self, *args, **options):
        HOST = '0.0.0.0'
        PORT = 5784

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(5)

        def handle_client(client_socket):
            try:
                data = client_socket.recv(1024).decode('utf-8').strip()
                logger.info(f'Received data: {data}')

                if re.match(r'^[^,]+,[^,]+,[^,]+,\d+$', data):
                    name, email, phone, age = data.split(',')

                    # Validação adicional
                    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                        client_socket.sendall(b'Erro: Formato de e-mail invalido')
                        logger.warning(f'Invalid email format: {email}')
                        return

                    if not re.match(r'^\d{10}$', phone):
                        client_socket.sendall(b'Erro: Formato de telefone invalido')
                        logger.warning(f'Invalid phone format: {phone}')
                        return

                    try:
                        ReceivedData.objects.create(name=name, email=email, phone=phone, age=int(age))
                        client_socket.sendall(b'Ok')
                        logger.info(f'Data saved: {name}, {email}, {phone}, {age}')
                    except IntegrityError as e:
                        error_message = str(e)
                        logger.error(f'IntegrityError: {error_message}')
                        if 'UNIQUE constraint failed' in error_message or 'duplicate key value violates unique constraint' in error_message:
                            client_socket.sendall(b'Erro: Nome ou telefone ja existe')
                        else:
                            client_socket.sendall(b'Erro ao salvar os dados')
                else:
                    client_socket.sendall(b'Erro: Dados invalidos')
                    logger.warning('Invalid data format received')
            except Exception as e:
                logger.error(f'Error processing data: {e}')
                client_socket.sendall(b'Erro ao processar dados')
            finally:
                client_socket.close()
                logger.info('Client connection closed')

        def start_server():
            logger.info(f'Server listening on {HOST}:{PORT}')
            while True:
                client_socket, addr = server.accept()
                logger.info(f'Connection received from {addr}')
                client_handler = threading.Thread(target=handle_client, args=(client_socket,))
                client_handler.start()

        start_server()
