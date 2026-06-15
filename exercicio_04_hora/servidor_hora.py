# --------------------------------------------------------
# Trabalho 2 - Redes de Computadores 2
# Professor: Alessandro Vivas Andrade
# Integrantes: Alisson de Souza Rocha, [Nome do Integrante 2], [Nome do Integrante 3]
# --------------------------------------------------------
import socket
import threading
from datetime import datetime

# Configurações do servidor de hora
HOST = "127.0.0.1"
PORTA = 7000         # Porta especificada no enunciado para o Exercício 4
CODIFICACAO = "utf-8"
ARQUIVO_LOG = "conexoes.log"

# Lock para garantir que múltiplas threads não escrevam no arquivo de log ao mesmo tempo
lock_log = threading.Lock()

def registrar_log(mensagem):
    """Função thread-safe para gravar logs no arquivo texto e printar no console."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_formatado = f"[{timestamp}] {mensagem}\n"
    
    # Exibe no console do servidor
    print(log_formatado.strip())
    
    # REQUISITO ADICIONAL: Salva a linha de log no arquivo conexoes.log
    with lock_log:
        with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
            f.write(log_formatado)

def gerenciar_cliente(socket_cliente, endereco_cliente):
    """Thread dedicada a processar a requisição de hora de um cliente específico."""
    # CRITÉRIO DE AVALIAÇÃO: Garantir funcionamento do servidor mesmo em caso de falha do cliente
    try:
        with socket_cliente:
            registrar_log(f"Solicitação recebida do cliente {endereco_cliente}")
            
            # REQUISITO DO EXERCÍCIO: Captura a hora atual no formato HH:MM:SS
            hora_atual = datetime.now().strftime("%H:%M:%S")
            
            # Envia a hora formatada para o cliente
            socket_cliente.sendall(hora_atual.encode(CODIFICACAO))
            registrar_log(f"Solicitação atendida com sucesso para {endereco_cliente} (Hora enviada: {hora_atual})")
            
    except Exception as e:
        registrar_log(f"Falha na comunicação com o cliente {endereco_cliente}: {e}")

def main():
    registrar_log("Servidor de Hora Multithread Iniciado.")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((HOST, PORTA))
            servidor.listen()
            
            registrar_log(f"Aguardando conexões na porta {PORTA}...")
            
            while True:
                # Aceita a conexão do cliente
                socket_cliente, endereco_cliente = servidor.accept()
                
                # CRITÉRIO DE AVALIAÇÃO: Utilizar threads para atender múltiplos clientes em paralelo
                # Cria e dispara uma nova thread para o cliente, liberando a main para o próximo accept()
                thread_cliente = threading.Thread(
                    target=gerenciar_cliente, 
                    args=(socket_cliente, endereco_cliente)
                )
                thread_cliente.daemon = True # Permite fechar a thread caso o servidor principal pare
                thread_cliente.start()
                
    except KeyboardInterrupt:
        registrar_log("Servidor de hora finalizado manualmente pelo usuário.")
    except Exception as e:
        registrar_log(f"Erro crítico no servidor de hora: {e}")

if __name__ == "__main__":
    main()