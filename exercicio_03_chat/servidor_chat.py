# --------------------------------------------------------
# Trabalho 2 - Redes de Computadores 2
# Professor: Alessandro Vivas Andrade
# Integrantes: Alisson de Souza Rocha, José Inácio de Moraes Santos, Rafael Gomes da Silva
# --------------------------------------------------------
import socket
import threading

# Configurações do servidor
HOST = "127.0.0.1"
PORTA = 5000
TAMANHO_BUFFER = 1024
CODIFICACAO = "utf-8"

# Lista global para armazenar as tuplas de clientes ativos: (socket, endereco)
clientes = []
# Lock para garantir que a manipulação da lista de clientes seja thread-safe
lock_clientes = threading.Lock()

def broadcast(mensagem, socket_remetente):
    """Envia uma mensagem para todos os clientes conectados, exceto para quem enviou."""
    with lock_clientes:
        for cliente_sock, _ in clientes:
            if cliente_sock != socket_remetente:
                try:
                    # Formata para quebrar a linha do "Você:" do outro cliente de forma limpa
                    msg_formatada = f"\n{mensagem}\nVocê: "
                    cliente_sock.sendall(msg_formatada.encode(CODIFICACAO))
                except Exception:
                    # Se falhar ao enviar (cliente caiu abruptamente), removemos depois no fluxo principal
                    pass

def gerenciar_cliente(socket_cliente, endereco_cliente):
    """Thread dedicada a escutar um cliente específico enquanto ele estiver conectado."""
    print(f"[+] Thread iniciada para gerenciar o cliente {endereco_cliente}")
    
    # Avisa a todo mundo na sala que um novo membro entrou
    msg_entrada = f"[Sala] Usuário {endereco_cliente} entrou no chat!"
    broadcast(msg_entrada, socket_cliente)

    try:
        while True:
            # Fica escutando as mensagens do cliente
            dados = socket_cliente.recv(TAMANHO_BUFFER)
            if not dados:
                break
                
            mensagem = dados.decode(CODIFICACAO).strip()
            
            # REQUISITO ADICIONAL: Tratar comando de saída manual
            if mensagem.lower() == "sair":
                break
                
            print(f"[Log] {endereco_cliente} diz: {mensagem}")
            
            # Transmite a mensagem recebida para todos os outros membros da sala
            msg_publica = f"[{endereco_cliente}]: {mensagem}"
            broadcast(msg_publica, socket_cliente)
            
    except Exception as e:
        print(f"[!] Erro na conexão com {endereco_cliente}: {e}")
        
    finally:
        # Remove o cliente da lista global de forma segura antes de fechar o socket
        with lock_clientes:
            # Procura o cliente na lista e remove
            for item in clientes:
                if item[0] == socket_cliente:
                    clientes.remove(item)
                    break
                    
        socket_cliente.close()
        print(f"[-] Conexão encerrada com {endereco_cliente}")
        
        # Avisa a sala que o usuário saiu
        msg_saida = f"[Sala] Usuário {endereco_cliente} saiu do chat."
        broadcast(msg_saida, None)

def main():
    print("[*] Servidor de Chat Multiusuários Ativo...")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((HOST, PORTA))
            servidor.listen()
            
            print(f"[*] Aguardando conexões na porta {PORTA} (Sem limite de usuários)...")
            
            while True:
                # Aceita conexões continuamente sem travar o chat de quem já está dentro
                socket_cliente, endereco_cliente = servidor.accept()
                print(f"[+] Nova conexão aceita de {endereco_cliente}")
                
                # Adiciona o novo cliente à lista de forma segura
                with lock_clientes:
                    clientes.append((socket_cliente, endereco_cliente))
                
                # CRITÉRIO DE AVALIAÇÃO: Uso de threads dinâmicas para múltiplos clientes em paralelo
                # Dispara uma thread exclusiva para este cliente e volta imediatamente para o accept()
                thread = threading.Thread(target=gerenciar_cliente, args=(socket_cliente, endereco_cliente))
                thread.daemon = True # Garante que as threads fechem se o servidor principal cair
                thread.start()

    except KeyboardInterrupt:
        print("\n[*] Servidor de chat finalizado manualmente pelo administrador.")
    except Exception as e:
        print(f"[!] Erro crítico no servidor: {e}")

if __name__ == "__main__":
    main()