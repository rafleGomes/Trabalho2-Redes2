# --------------------------------------------------------
# Trabalho 2 - Redes de Computadores 2
# Professor: Alessandro Vivas Andrade
# Integrantes: Alisson de Souza Rocha, [Nome do Integrante 2], [Nome do Integrante 3]
# --------------------------------------------------------
import socket

# Configurações de rede do cliente
HOST = "127.0.0.1"   # Endereço de loopback (local)
PORTA = 6666         # Porta padrão definida no enunciado
TAMANHO_BUFFER = 1024
CODIFICACAO = "utf-8"

def main():
    # Lê a mensagem que será enviada ao servidor TCP e remove espaços extras
    mensagem = input("Digite a mensagem para enviar ao servidor TCP: ").strip()

    # REQUISITO ADICIONAL: Mecanismo de validação para mensagens vazias
    if not mensagem:
        print("Erro: A mensagem não pode ser vazia. Encerrando o cliente.")
        return

    # CRITÉRIO DE AVALIAÇÃO: Tratamento de erros na comunicação por socket
    try:
        # Cria o socket TCP e garante o encerramento seguro (close) ao final do bloco com 'with'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            print(f"Tentando conectar ao servidor {HOST}:{PORTA}...")
            cliente.connect((HOST, PORTA)) # Conecta ao servidor

            # Envia a mensagem codificada em bytes para a rede
            cliente.sendall(mensagem.encode(CODIFICACAO))

            # Aguarda a resposta de confirmação do servidor
            resposta = cliente.recv(TAMANHO_BUFFER).decode(CODIFICACAO)
            
            # Exibe a resposta recebida no console
            print(f"Resposta do servidor: {resposta}")
            
    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor. Verifique se ele está ativo.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado na comunicação: {e}")

if __name__ == "__main__":
    main()