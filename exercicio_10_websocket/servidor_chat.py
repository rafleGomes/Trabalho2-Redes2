import asyncio
import websockets

# Conjunto para armazenar todas as conexões de clientes ativas
clientes_conectados = set()

async def gerenciar_cliente(websocket):
    # Registra o novo cliente quando ele se conecta
    clientes_conectados.add(websocket)
    print(f"Novo cliente conectado de: {websocket.remote_address}")
    
    try:
        # Loop para escutar as mensagens deste cliente específico
        async for mensagem in websocket:
            print(f"Mensagem recebida: {mensagem}")
            
            # BROADCAST: Retransmite a mensagem para todos os outros clientes conectados
            if clientes_conectados:
                # Cria tarefas paralelas para enviar a mensagem a todos de forma eficiente
                tarefas = [cl.send(mensagem) for cl in clientes_conectados]
                await asyncio.gather(*tarefas)
                
    except websockets.exceptions.ConnectionClosed:
        print(f"Conexão encerrada com: {websocket.remote_address}")
    finally:
        # Remove o cliente do conjunto ao desconectar
        clientes_conectados.remove(websocket)

async def main():
    # Inicia o servidor na porta 8765 em todas as interfaces locais
    async with websockets.serve(gerenciar_cliente, "0.0.0.0", 8765):
        print("Servidor Chat WebSocket rodando na porta 8765...")
        await asyncio.Event().wait() # Mantém o servidor rodando indefinidamente

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor finalizado pelo usuário.")