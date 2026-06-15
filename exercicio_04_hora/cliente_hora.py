# --------------------------------------------------------
# Trabalho 2 - Redes de Computadores 2
# Professor: Alessandro Vivas Andrade
# Integrantes: Alisson de Souza Rocha, [Nome do Integrante 2], [Nome do Integrante 3]
# --------------------------------------------------------
import socket

# Configurações do cliente
HOST_SERVIDOR = "127.0.0.1"
PORTA_SERVIDOR = 7000
TAMANHO_BUFFER = 1024
CODIFICACAO = "utf-8"

def main():
    print("--- Cliente de Solicitação de Hora TCP ---")
    
    try:
        # REQUISITO DO EXERCÍCIO: Conectar-se ao servidor e solicitar a hora
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            print(f"Conectando ao servidor em {HOST_SERVIDOR}:{PORTA_SERVIDOR}...")
            cliente.connect((HOST_SERVIDOR, PORTA_SERVIDOR))
            
            # Aguarda o recebimento da hora enviada pelo servidor
            dados = cliente.recv(TAMANHO_BUFFER)
            
            if dados:
                hora_recebida = dados.decode(CODIFICACAO)
                # REQUISITO DO EXERCÍCIO: Exibir a hora recebida no console
                print(f"\n[Hora do Servidor]: {hora_recebida}")
            else:
                print("[!] O servidor fechou a conexão sem enviar dados.")
                
    except ConnectionRefusedError:
        print("[!] Erro: Servidor de hora offline ou inacessível.")
    except Exception as e:
        print(f"[!] Ocorreu um erro ao obter a hora: {e}")
        
    print("\n--- Conexão Encerrada ---")

if __name__ == "__main__":
    main()