from ultralytics import YOLO
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

model = YOLO("yolov8n.pt")

data_file = os.path.join(script_dir, "data.yaml")

print(data_file)

model.train(data=data_file, epochs=100, batch=6)
metrics = model.val()
