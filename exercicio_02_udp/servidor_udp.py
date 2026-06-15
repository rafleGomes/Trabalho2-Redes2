# --------------------------------------------------------
# Trabalho 2 - Redes de Computadores 2
# Professor: Alessandro Vivas Andrade
# Integrantes: Alisson de Souza Rocha, [Nome do Integrante 2], [Nome do Integrante 3]
# --------------------------------------------------------
import socket

# Configurações do servidor UDP
HOST = "127.0.0.1"   
PORTA = 6000         
TAMANHO_BUFFER = 65535  # Buffer de 64 KB 

def main():
    try:
        # Cria o socket UDP (AF_INET = IPv4, SOCK_DGRAM = UDP / Datagrama)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
            # Vincula o socket à porta configurada
            servidor.bind((HOST, PORTA))
            print(f"[*] Servidor Echo UDP ativo e ouvindo na porta {PORTA}...")

            # Loop contínuo para receber e ecoar mensagens
            while True:
                # recvfrom() bloqueia o código aguardando um pacote. 
                # Retorna os dados e uma tupla (ip, porta) do remetente.
                dados, endereco_cliente = servidor.recvfrom(TAMANHO_BUFFER)
                
                # Traduz os bytes recebidos para texto
                mensagem = dados.decode("utf-8").strip()
                
                # Imprime a mensagem recebida no console do servidor
                print(f"[Recebido de {endereco_cliente}]: {mensagem}")
                
                # REQUISITO DO EXERCÍCIO: Enviar a mensagem de volta (Eco)
                # Como não há conexão persistente, precisamos passar explicitamente o endereço de destino
                servidor.sendto(dados, endereco_cliente)
                print(f"[->] Eco enviado de volta para {endereco_cliente}")

    except KeyboardInterrupt:
        print("\n[*] Servidor UDP finalizado manualmente pelo usuário.")
    except Exception as e:
        print(f"[!] Erro crítico no servidor UDP: {e}")

if __name__ == "__main__":
    main()