from ultralytics import YOLO

# Carregar o modelo treinado
model = YOLO('best.pt')

# Fazer predições em uma imagem
results = model('./images/train/Captura-de-tela-2024-04-27-074917_png.rf.4822c088b66dd420737926b34e01e1ba.jpg', classes=[0])

# Mostrar a imagem com as predições
if results:
    results[0].show()
