# Estudo de Imagens de Drones

## Descrição

Este projeto tem como objetivo realizar o processamento e a comparação de imagens capturadas por drones, aplicando diversos filtros para realce e análise visual. A interface gráfica permite carregar imagens, aplicar filtros personalizados e visualizar os resultados de forma interativa.

### 1. Bibliotecas Utilizadas
- `cv2` (OpenCV): Usada para carregamento, manipulação e processamento de imagens e vídeos.
- `numpy`: Manipulação de arrays numéricos, útil para operações com imagens.
- `customtkinter` (CTk): Interface gráfica moderna baseada em Tkinter.
- `tkinter.filedialog`: Permite abrir um explorador de arquivos para seleção de mídias.
- `PIL` (Pillow): Usada para converter imagens entre diferentes formatos compatíveis com a interface gráfica.
- `threading`: Permite a execução de vídeos e câmera ao vivo sem travar a interface.
- `sklearn.cluster.KMeans`: Algoritmo para agrupamento de cores na imagem.

### 2. Estrutura da Classe `MediaComparerApp`
A classe `MediaComparerApp` é responsável por construir a interface gráfica e definir funcionalidades como carregamento de imagens, vídeos, filtros e captura de cores.

#### 2.1. Interface Gráfica
- O layout é dividido em dois frames:
  - `frame_controls`: Localizado à esquerda, contendo botões e sliders para controle de filtros.
  - `frame_display`: À direita, exibindo as imagens ou vídeos carregados.

- Botões disponíveis:
  - "Carregar Imagem 1"
  - "Carregar Mídia 2" (suporta imagens e vídeos)
  - "Câmera ao Vivo"

- Labels para exibição das imagens:
  - `label_image1`: Exibe a primeira imagem de referência.
  - `label_media2`: Exibe a segunda mídia carregada (imagem ou vídeo).
  - `label_media_filtro`: Exibe a versão filtrada da segunda mídia.

#### 2.2. Controles de Filtros
- `Gaussian Blur`: Aplica um desfoque gaussiano na imagem.
- `Dilatação`: Aumenta áreas brancas na imagem para destacar contornos.
- `Erosão`: Reduz áreas brancas, útil para remover ruídos.
- `Abertura`: Aplica erosão seguida de dilatação, útil para remover ruídos menores.
- `Fechamento`: Aplica dilatação seguida de erosão, útil para preencher buracos em objetos detectados.

Cada controle é representado por um `CTkSlider`, que ajusta o tamanho do kernel de cada operação.

### 3. Funcionalidades do Código
#### 3.1. Carregamento de Arquivos
- `load_image1()`: Permite selecionar uma imagem e exibi-la como referência.
- `load_media2()`: Permite carregar uma segunda mídia (imagem ou vídeo). Se for um vídeo, a função `play_video()` é chamada para reproduzi-lo.
- `process_and_display_image()`: Converte a segunda mídia para um formato processável, aplicando filtros e detectando formas.

#### 3.2. Processamento de Vídeos
- `play_video()`: Inicia a reprodução de um vídeo carregado.
- `update_video_frame()`: Atualiza os frames do vídeo em tempo real e aplica os filtros conforme selecionado.

#### 3.3. Câmera ao Vivo
- `start_live_camera()`: Captura imagens da câmera em tempo real.
- `update_live_camera_frame()`: Processa cada frame da câmera e aplica filtros, exibindo-os dinamicamente.

### 4. Manipulação de Imagens com OpenCV
- `display_image()`: Exibe imagens carregadas no formato Tkinter.
- `display_image_cv()`: Converte imagens do OpenCV para exibição na interface.
- `detect_shapes()`: (Presumivelmente definida em outro trecho) identifica formas na imagem.

### 5. Aplicação dos Filtros
Cada filtro possui uma função específica para aplicar a transformação correspondente e atualizar a exibição na interface gráfica:
- `apply_filter_and_display()`: Aplica o desfoque gaussiano.
- `apply_dilation_and_display()`: Aplica dilatação na imagem.
- `apply_erosion_and_display()`: Aplica erosão.
- `apply_opening_and_display()`: Aplica abertura.
- `apply_closing_and_display()`: Aplica fechamento.

### 6. interfaces



