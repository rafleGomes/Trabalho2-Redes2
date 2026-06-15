# --------------------------------------------------------
# Trabalho 2 - Redes de Computadores 2
# Professor: Alessandro Vivas Andrade
# Integrantes: Alisson de Souza Rocha, [Nome do Integrante 2], [Nome do Integrante 3]
# --------------------------------------------------------
import socket
import threading
import sys

HOST_SERVIDOR = "127.0.0.1"
PORTA_SERVIDOR = 5000
TAMANHO_BUFFER = 1024
CODIFICACAO = "utf-8"

def escutar_servidor(cliente_socket):
    """Thread dedicada exclusivamente a receber transmissões da sala e printar na tela."""
    try:
        while True:
            dados = cliente_socket.recv(TAMANHO_BUFFER)
            if not dados:
                print("\n[-] Conexão com o servidor de chat perdida.")
                break
            # Exibe na tela o broadcast recebido
            sys.stdout.write(dados.decode(CODIFICACAO))
            sys.stdout.flush()
    except Exception:
        pass
    finally:
        cliente_socket.close()

def main():
    print("--- Bem-vindo à Sala de Chat TCP ---")
    print("Dica: Digite 'sair' para abandonar a sala a qualquer momento.\n")
    
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST_SERVIDOR, PORTA_SERVIDOR))
        print("[+] Você entrou na sala com sucesso!\n")
        
        # Dispara a thread de recepção de mensagens em background
        thread_receptora = threading.Thread(target=escutar_servidor, args=(cliente,))
        thread_receptora.daemon = True
        thread_receptora.start()
        
        # Loop principal (Thread Main) para envio de mensagens
        while True:
            mensagem = input("Você: ").strip()
            
            # Validação obrigatória para não enviar pacotes vazios
            if not mensagem:
                continue
                
            cliente.sendall(mensagem.encode(CODIFICACAO))
            
            if mensagem.lower() == "sair":
                print("Saindo da sala de chat...")
                break
                
    except ConnectionRefusedError:
        print("[!] Erro: Não foi possível alcançar o servidor de chat.")
    except Exception as e:
        print(f"[!] Ocorreu um erro na sua sessão: {e}")
    finally:
        cliente.close()
        print("--- Sessão Finalizada ---")

if __name__ == "__main__":
    main()