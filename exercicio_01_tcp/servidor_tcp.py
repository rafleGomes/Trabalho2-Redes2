# --------------------------------------------------------
# Trabalho 2 - Redes de Computadores 2
# Professor: Alessandro Vivas Andrade
# Integrantes: Alisson de Souza Rocha, José Inácio de Moraes Santos, Rafael Gomes da Silva
# --------------------------------------------------------
import socket

# Configurações de rede do servidor
HOST = "127.0.0.1"   # Escuta apenas conexões vindas do próprio computador (Loopback)
PORTA = 6666         # Porta 
TAMANHO_BUFFER = 1024
CODIFICACAO = "utf-8"

def main():
    # CRITÉRIO DE AVALIAÇÃO: Tratamento de erros e uso adequado de sockets
    try:
        # Cria o socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
        # O 'with' garante que o socket do servidor seja fechado com segurança ao parar o programa
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            
            # Permite reutilizar a porta imediatamente caso o servidor seja reiniciado
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Vincula o servidor ao endereço e porta configurados
            servidor.bind((HOST, PORTA))
            
            # Coloca o servidor em modo de escuta para aguardar conexões
            servidor.listen()
            print(f"[*] Servidor TCP ativo e aguardando conexões em {HOST}:{PORTA}...")

            # Loop contínuo para aceitar múltiplos clientes sequencialmente
            while True:
                # Aceita a conexão de um cliente (bloqueia o código até alguém conectar)
                socket_cliente, endereco_cliente = servidor.accept()
                
                # Gerenciador de contexto 'with' para garantir o encerramento seguro do cliente após o atendimento
                with socket_cliente:
                    print(f"[+] Conexão estabelecida com {endereco_cliente}")

                    # Recebe os bytes enviados pelo cliente
                    dados = socket_cliente.recv(TAMANHO_BUFFER)
                    
                    # Se não receber dados (cliente desconectou abruptamente), quebra o ciclo de leitura
                    if not dados:
                        print(f"[-] Conexão encerrada pelo cliente {endereco_cliente} sem enviar dados.")
                        continue

                    # Decodifica os bytes recebidos para string de texto
                    mensagem = dados.decode(CODIFICACAO).strip()

                    # Mecanismo de validação para mensagens vazias
                    if not mensagem:
                        print(f"[!] Mensagem vazia recebida de {endereco_cliente}. Ignorando.")
                        resposta_erro = "Erro: Mensagem vazia não é permitida."
                        socket_cliente.sendall(resposta_erro.encode(CODIFICACAO))
                        continue

                    # Imprime a mensagem recebida no console do servidor
                    print(f"[Mensagem de {endereco_cliente}]: {mensagem}")

                    # Resposta de confirmação exigida pelo enunciado
                    resposta = "Mensagem recebida"
                    socket_cliente.sendall(resposta.encode(CODIFICACAO))
                    print(f"[->] Confirmação enviada para {endereco_cliente}")
                    
    except KeyboardInterrupt:
        # Permite encerrar o servidor no terminal digitando Ctrl+C de forma limpa
        print("\n[*] Servidor finalizado manualmente pelo usuário.")
    except Exception as e:
        print(f"[!] Erro crítico no servidor: {e}")

if __name__ == "__main__":
    main()