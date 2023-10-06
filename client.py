import asyncio


async def send_message(message: str, client_num: int) -> None:
    """
    Функция открывает асинхронное соединение с сервером, отправляет
    сообщение, ожидает ответ от сервера, и выводит информацию о
    процессе в консоль. Если сообщение пустое (содержит только
    пробелы), она пропускает отправку и выводит сообщение об этом в
    консоль.

    Параметры:
    - message (str): Строка, представляющая сообщение для отправки на
    сервер.
    - client_num (int): Номер клиента, используется для идентификации в
    выводе.
    """
    if not message.strip():
        print(f"Client {client_num}: Skipping empty message")
        return
    reader, writer = await asyncio.open_connection('127.0.0.1', 8080)
    writer.write(message.encode())
    await writer.drain()
    print(f"Client {client_num}: Sent: {message}")
    data = await reader.read(1024)
    response = data.decode()
    print(f"Client {client_num}: Received: {response}")
    writer.close()
    await writer.wait_closed()

async def main() -> None:
    """
    Функция создает список задач для отправки сообщений на сервер и
    ожидает их выполнения с помощью asyncio.gather.
    """
    messages = ["test", "tEsT", "a1b2c3!", "12 3!", "   ", ""]
    tasks = [
        send_message(message, i) for i, message in enumerate(messages, 1)
    ]
    await asyncio.gather(*tasks)

asyncio.run(main())
