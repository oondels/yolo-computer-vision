import sys
import asyncio
import websockets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
import pygame


async def play_notification(message):
    pygame.mixer.init()
    pygame.mixer.music.load("../utils/notificacao.wav")
    pygame.mixer.music.play()

    async def check_asyncio_tasks():
        while True:
            await asyncio.sleep(0.01)
            app.processEvents()

    asyncio.create_task(check_asyncio_tasks())


async def handle_message(websocket, path):
    async for message in websocket:
        print(message)
        await play_notification(message)


async def main():
    # Inicializa o servidor WebSocket na porta desejada (por exemplo, 82)
    server = await websockets.serve(handle_message, "0.0.0.0", 82)
    print("Servidor WebSocket rodando na porta 82")
    await server.wait_closed()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    sys.exit(app.exec_())
