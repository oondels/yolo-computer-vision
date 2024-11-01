import websockets
import asyncio
from ultralytics import YOLO
from PIL import ImageGrab
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:/Users/hendrius.santana/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
)


async def send_message(message):
    async with websockets.connect("ws://192.168.26.90:9003") as websocket:
        await websocket.send(message)


model = YOLO("./dataset/runs/detect/train/weights/best.pt")


async def main():
    while True:
        screen = ImageGrab.grab()

        width, height = screen.size
        new_width = (width // 32) * 32
        new_height = (height // 32) * 32
        screen = screen.resize((new_width, new_height))

        results = model.predict(
            source="takt_menor.mp4",
            stream=True,
            conf=0.15,
            imgsz=(new_width, new_height),
            save=True,
            show=True,
        )

        for result in results:
            boxes = result.boxes.xyxy

            for box in boxes:

                x1, y1, x2, y2 = (
                    box[0].item(),
                    box[1].item(),
                    box[2].item(),
                    box[3].item(),
                )

                roi = screen.crop((x1, y1, x2, y2))

                texto_extraido = pytesseract.image_to_string(roi)

                texto_extraido = texto_extraido.strip()
                print(texto_extraido)
                if (
                    texto_extraido
                    == """TAKT TIME
00:00:00"""
                ):

                    # await send_message("Takt liberado")
                    print("Envia mensagem")

        await asyncio.sleep(1)


asyncio.run(main())
