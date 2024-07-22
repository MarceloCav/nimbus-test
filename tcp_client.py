import socket

def send_data_to_tcp_server(data):
    host = "127.0.0.1"
    port = 5784 

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(data.encode('utf-8'))
        response = client_socket.recv(1024)
        print(f"Received response: {response.decode('utf-8')}")

if __name__ == "__main__":
    # Lista de diferentes conjuntos de dados para testar
    data_samples = [
        "MarceloCavalcanti,marcelocn95@gmail.com,9999999999,30",  # Dados corretos
        "MarceloCavalcanti,,9999999999,30",  # Falta o e-mail
        "MarceloCavalcanti,marcelo_at_gmail.com,9999999999,30",  # Formato de e-mail inválido
        "MarceloCavalcanti,marcelocn95@gmail.com,99999,30",  # Número de telefone inválido
        "MarceloCavalcanti,marcelocn95@gmail.com,9999999999,30"  # Dados duplicados (mesmo que o primeiro)
    ]

    # Envia cada conjunto de dados
    for data in data_samples:
        print(f"Sending data: {data}")
        send_data_to_tcp_server(data)
        print("-------------------------------------------------")