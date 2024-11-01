from ultralytics import YOLO

# Carregar o modelo treinado
model = YOLO('best.pt')

# Fazer a predição em um vídeo
results = model.predict(source='takt.mp4', show=True, save=True)
