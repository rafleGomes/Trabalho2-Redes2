### Relatório de Captura - Exercício 6: Estabelecimento de Conexão TCP
Trabalho 2 - Redes de Computadores 2
Professor: Prof. Alessandro Vivas Andrade
Integrantes: Alisson de Souza Rocha, [Nome do Integrante 2], [Nome do Integrante 3]

### Exercício 6: Utilizando o software Wireshark capture o tráfego TCP gerado no estabelecimento de conexão (Three-Way Handshake) através da ferramenta telnet

## 1. Abra o Wireshark e configure o filtro para a porta do serviço
## 2. Execute o utilitário Telnet no terminal simulando o início de uma sessão na porta 80
## 3. Encerre a sessão e pare a captura dos dados
## 4. Analise as flags TCP que compõem o estabelecimento de conexão (SYN, SYN-ACK, ACK) e o encerramento da sessão

### Respostas exercício 6

## 1. Abra o Wireshark e configure o filtro para a porta do serviço

# Selecionei a interface de rede ativa (wlp8s0) para iniciar a captura
# Apliquei o filtro de exibição para monitorar apenas a porta padrão do serviço HTTP: tcp.port == 80

## 2. Execute o utilitário Telnet no terminal simulando o início de uma sessão na porta 80

# Instalar o utilitário via terminal, caso necessário: sudo apt install telnet -y
# Disparei a conexão TCP manual apontando para o servidor de testes: telnet example.com 80
# O terminal indicou sucesso na abertura do socket com a mensagem "Connected to example.com"

## 3. Encerre a sessão e pare a captura dos dados

# Utilizei o atalho Ctrl + ] para abrir o prompt de comandos do Telnet
# Digitei o comando "quit" e apertei Enter para forçar o encerramento da conexão
# O terminal retornou "Connection closed by foreign host"
# Interrompi a captura no botão de parada do Wireshark
# ![Resultado do handshake TCP no Wireshark](quest6.png)

## 4. Analise as flags TCP que compõem o estabelecimento de conexão (SYN, SYN-ACK, ACK) e o encerramento da sessão

# Pacote 279 ([SYN]): Host local envia solicitação de sincronização da porta dinâmica 53892 para a porta servidora 80, definindo o número de sequência inicial Seq = 0
# Pacote 283 ([SYN, ACK]): O servidor responde confirmando o recebimento do pacote (Ack = 1) e envia seu próprio número de sequência com o bit SYN ativo
# Pacote 284 ([ACK]): O host local envia a confirmação final do recebimento (Ack = 1), completando o algoritmo de três etapas (Three-Way Handshake) e estabelecendo a conexão
# Pacotes 557 e 558 ([FIN, ACK]): Registro do aperto de mão de despedida executado após o comando quit, desalocando os buffers e liberando as portas lógicas de forma segura