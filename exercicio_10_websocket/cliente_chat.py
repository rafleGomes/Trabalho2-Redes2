import asyncio
import websockets
import sys

async def escutar_servidor(websocket):
    """Fica escutando as mensagens vindas do servidor e exibe na tela."""
    try:
        async for mensagem in websocket:
            print(f"\n[Chat]: {mensagem}")
            # Mantém o prompt visual no terminal após receber uma mensagem
            print("Digite sua mensagem: ", end="", flush=True)
    except websockets.exceptions.ConnectionClosed:
        print("\nConexão com o servidor foi perdida.")

async def enviar_mensagens(websocket, nome_usuario):
    """Fica escutando o terminal local e envia as mensagens para o servidor."""
    # Loop de leitura assíncrona do terminal
    loop = asyncio.get_event_loop()
    while True:
        # Lê a entrada do usuário sem travar a recepção de mensagens
        mensagem = await loop.run_in_executor(None, input, "Digite sua mensagem: ")
        if mensagem.strip():
            msg_formatada = f"{nome_usuario}: {mensagem}"
            await websocket.send(msg_formatada)

async def main():
    # Solicita o nickname do usuário para identificar no chat
    nome_usuario = input("Escolha seu nome de usuário: ").strip()
    if not nome_usuario:
        nome_usuario = "Anonimo"

    url_servidor = "ws://localhost:8765"
    print(f"Conectando ao servidor em {url_servidor}...")
    
    try:
        async with websockets.connect(url_servidor) as websocket:
            print("Conectado com sucesso! Digite as mensagens abaixo.\n")
            
            # Roda as duas funções (escutar e enviar) simultaneamente de forma assíncrona
            await asyncio.gather(
                escutar_servidor(websocket),
                enviar_mensagens(websocket, nome_usuario)
            )
    except Exception as e:
        print(f"Erro ao conectar ou manter a sessão: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCliente desconectado.")
        sys.exit(0)