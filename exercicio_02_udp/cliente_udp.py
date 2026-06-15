# --------------------------------------------------------
# Trabalho 2 - Redes de Computadores 2
# Professor: Alessandro Vivas Andrade
# Integrantes: Alisson de Souza Rocha, José Inácio de Moraes Santos, Rafael Gomes da Silva
# --------------------------------------------------------
import socket

# Configurações do cliente UDP
HOST_SERVIDOR = "127.0.0.1"
PORTA_SERVIDOR = 6000
TAMANHO_MAX_UDP = 65535  # Limite de 64 KB exigido pelo enunciado
CODIFICACAO = "utf-8"

def main():
    print("--- Cliente Echo UDP Iniciado ---")
    print("Digite suas mensagens abaixo. Digite 'sair' para encerrar.\n")

    # Cria o socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        # REQUISITO ADICIONAL: Definir um tempo limite para tratamento de erros (ex: perda de pacotes)
        cliente.settimeout(5.0)  # Se o servidor não responder em 5 segundos, estoura um erro

        # Loop contínuo de envio conforme solicitado
        while True:
            try:
                mensagem = input("Você: ").strip()

                # REQUISITO ADICIONAL: Comando de saída manual do usuário
                if mensagem.lower() == "sair":
                    print("Encerrando o cliente UDP. Até logo!")
                    break

                # Codifica a mensagem para calcular o tamanho real em bytes
                dados_enviar = mensagem.encode(CODIFICACAO)

                # REQUISITO ADICIONAL: Validar o tamanho máximo da mensagem (64 KB)
                if len(dados_enviar) > TAMANHO_MAX_UDP:
                    print(f"[!] Erro: A mensagem excede o limite máximo permitido pelo UDP ({TAMANHO_MAX_UDP} bytes).")
                    continue

                # Evita enviar dados vazios sem necessidade
                if not mensagem:
                    print("[!] Mensagens vazias não serão enviadas.")
                    continue

                # Envia o datagrama UDP para o servidor
                cliente.sendto(dados_enviar, (HOST_SERVIDOR, PORTA_SERVIDOR))

                # Aguarda o Eco vindo do servidor
                dados_recebidos, endereco_servidor = cliente.recvfrom(TAMANHO_MAX_UDP)
                
                # Exibe a resposta obtida no console
                eco = dados_recebidos.decode(CODIFICACAO)
                print(f"Eco do Servidor: {eco}\n")

            except socket.timeout:
                # Tratar erros de comunicação (como perda de pacotes ou queda do servidor)
                print("[!] Erro: Tempo limite esgotado (Timeout). O servidor não respondeu.\n")
            except Exception as e:
                print(f"[!] Ocorreu um erro inesperado: {e}\n")
                break

if __name__ == "__main__":
    main()