import websockets
import asyncio
from ultralytics import YOLO
from PIL import ImageGrab
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = (
    r"C:/Users/hendrius.santana/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
)
model = YOLO("./dataset/runs/detect/train/weights/best.pt")


async def send_message(message):
    async with websockets.connect("ws://192.168.26.90:9003") as websocket:
        await websocket.send(message)


async def main():
    while True:
        # Capturar a tela em tempo real
        screen = ImageGrab.grab()
        screen_np = np.array(screen)

        # Converter a imagem para o formato do OpenCV (RGB -> BGR)
        frame = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

        # Fazer a predição no frame atual
        results = model.predict(source=frame, stream=False, conf=0.15)

        # Para cada resultado, desenhar a caixa delimitadora e extrair a região de interesse
        for result in results:
            for box in result.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box[:4])
                roi = frame[y1:y2, x1:x2]

                # Mostrar a região de interesse
                # cv2.imshow("ROI", roi)

                # Usando pytesseract para extração do texto
                texto_extraido = pytesseract.image_to_string(roi)
                texto_extraido = texto_extraido.strip()

                if (
                    texto_extraido == """TAKT TIME\n00:00:00"""
                    or texto_extraido == """TAKT TIME\n\n00:00:00"""
                    or texto_extraido == """TART TIME\n\n00:00:00"""
                    or texto_extraido == """TAKT TIME\n\n"""
                    or texto_extraido == """TAKT TIME\n"""
                ):
                    print(texto_extraido)
                    print("Takt Time detected")

                    # Encerrar o loop e o programa quando a mensagem for detectada
                    cv2.destroyAllWindows()
                    return

                # Pressionar 'q' para sair
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    return

        await asyncio.sleep(0.1)  # Pequeno delay para não sobrecarregar o sistema


asyncio.run(main())
