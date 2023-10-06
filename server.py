import asyncio


async def handle_echo(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    """
    Обрабатывает входящее сетевое соединение, выполняя простое
    эхо-серверное действие. Входящее сообщение преобразуется в
    верхний регистр и отправляется обратно клиенту.

    Параметры:
    - reader (StreamReader): Объект для чтения данных из входящего
    сетевого соединения. 
    - writer (StreamWriter): Объект для записи данных в исходящее
    сетевое соединение. 
    """
    data = await reader.read(1024)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received: {message} from {addr[0]}:{addr[1]}")
    mod_message = message.upper()
    writer.write(mod_message.encode())
    await writer.drain()
    print(f"Sent: {mod_message} to {addr[0]}:{addr[1]}")
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8080)
server = loop.run_until_complete(coro)
addr = server.sockets[0].getsockname()

# Обрабатывать запросы пока не будет нажато Ctrl+C
print(f"Serving on http://{addr[0]}:{addr[1]}")
try:
    loop.run_forever()
except KeyboardInterrupt:
    print("\nGraceful shutdown...")
    pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
