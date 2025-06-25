# Visão computacional passo 1 (UM) - Bola branca em um fundo preto
## 📖 Sobre o Projeto

A primeira parte do projeto conhecido como BallInPlate, 

1.  **Sistema de Visão (PC):** Um script em Python, utilizando a biblioteca OpenCV, é responsável por capturar o vídeo de uma webcam, processar os frames em tempo real para detectar a posição `(x, y)` de uma bola, e enviar essas coordenadas via comunicação serial (USB).
Em geral, acredito que o código já esteja bem comentado, mas por via de didática, deixarei algumas observações bem específicas.

##Somente cunho explicativo
OBS 1.0 :
- O kernel representa uma espécie de pincel que usaremos para "scannear" a imagem e o 'np.ones' cria uma matriz  de tamanho 5x5  preenchida com números 1, quanto maior o kernel , mais agressivo é a limpeza, quanto um menor é uma limpeza mais suave e por fim seta o formato da matriz que é o formato padrão para imagens (valores de 0 a 255).
OBS 1.1 :
- 'cv2.morphologyEx' é a função do OpenCV para executar operações morfológicas "estendidas" ou "complexas" e passamos 'MORPH_CLOSE'.
- MOTPH_CLOSE expande as áreas brancas em todas as direções, como se estivesse passando massa corrida sobre a bola. Essa expansão "cobre" os pequenos buracos pretos que estavam no meio dela.
OBS 1.2 :
- '.erode' : ela encolhe as áreas brancas de volta ao tamanho original, como se estivesse "lixando" o excesso de massa.
OBS 1.3 :
- '.dilate' : depois do erode, a bola pode ter ficado "magra" demais, para isso dilatamos  para destaca-la, e fazemos isso duas vezes com 'iterations=2'.
  
```python
    kernel = np.ones((5, 5), np.uint8) #cria um kernel 5x5 de uns
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)#expanse a area branca para tampar buracos
    mask = cv2.erode(mask, None, iterations=1)# Encolhe um pouco as áreas brancas, o que ajuda a eliminar pequenos ruídos brancos que estejam isolados no fundo
    mask = cv2.dilate(mask, None, iterations=2)#Expande as áreas brancas. Como isso vem depois da erosão, enquanto o ruído pequeno, que foi eliminado, não volta, mantendo somente a bola
```
##Pyserial

Caso precise descobrir a porta COM do sue computador, rode:
```bash
python -m serial.tools.list_ports
 ```

##Calibração 

1.  **Calibrar a Cor da Bola:**
    * No terminal com o ambiente `(venv)` ativado, rode a ferramenta de calibração:
      ```bash
      python calibrador_hsv.py
      ```
    * Use os controles deslizantes para ajustar o filtro de cor até que **somente a bola** apareça como uma mancha branca sólida na janela "Mascara".
    * Salve os valores e altere diretamente no código 'webcam_teste.py'

