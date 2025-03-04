# -Projeto_Controle_e_Sistemas_Embarcados
Visão Computacional para Detecção de Formas Geométricas Coloridas

### 1️⃣ Opção 1: Visão Computacional para Detecção de Formas Geométricas Coloridas

**Objetivo:** Desenvolver um programa em Python com OpenCV para detectar features geométricos de uma base de pouso de drones com cores predefinidas em imagens ou vídeos. O projeto visa propor o estudo de conceitos fundamentais da visão computacional como o uso de filtros de imagem, operações no espaços de cores, transformações morfológicas, thresholding, detecção de bordas e criação e tipificação de contornos utilizando OpenCV.

**📚 Materiais de Estudo:**

*   **OpenCV Documentação e Tutoriais:**
    *   [Documentação Oficial OpenCV](https://docs.opencv.org/master/)
        *   **Uso:** Referência completa da biblioteca OpenCV, útil para pesquisa detalhada de funções e módulos.
    *   [Tutoriais OpenCV-Python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html): Focar em: Basic Image Operations, Image Filtering, Morphological Transformations, Color Spaces, Image Thresholding, Contours e GUI Features.
        *   **Uso:** Guia prático com exemplos em Python, ideal para aprender os fundamentos do processamento de imagens com OpenCV. Concentre-se nos seguintes módulos:
            *   **Basic Image Operations:** Operações básicas como leitura, escrita e manipulação de pixels em imagens. Essencial para começar a trabalhar com imagens no OpenCV.
            *   **Image Filtering:** Técnicas para suavizar imagens, remover ruído e realçar bordas. Inclui filtros como Gaussian Blur e Median Blur, importantes para pré-processamento.
            *   **Morphological Transformations:** Operações morfológicas como erosão, dilatação, abertura e fechamento. Úteis para refinar formas geométricas detectadas e remover pequenos ruídos ou imperfeições.
            *   **Color Spaces:** Conversão entre diferentes espaços de cor (RGB, HSV, Gray). O espaço HSV é particularmente útil para segmentação de cores, pois separa a informação de cor (Hue) da intensidade (Value) e saturação (Saturation).
            *   **Image Thresholding:** Técnicas para segmentar imagens baseadas em limiares, criando imagens binárias. Essencial para isolar regiões de interesse baseadas em cor ou intensidade.
            *   **Contours:** Detecção e análise de contornos em imagens binárias. Funções como `findContours` e `approxPolyDP` são cruciais para identificar e aproximar formas geométricas.
            *   **GUI Features:** Ferramentas de Interface Gráfica do Usuário, como sliders e trackbars. Permitem criar interfaces interativas para ajustar parâmetros em tempo real.
    *   [Tutoriais de Processamento de Imagem OpenCV-Python](https://docs.opencv.org/4.x/d2/d96/tutorial_py_table_of_contents_imgproc.html)
        *   **Uso:** Tabela de conteúdos detalhada dos tutoriais de processamento de imagem em Python, facilitando a navegação por tópicos específicos.
    *   [Exemplo de interface com parâmetros para teste](https://cloudvision.app/image.html?rid=-M94KlEHAR6uSimUr61M)
        *   **Uso:** Referência visual de uma interface de usuário interativa para ajuste de parâmetros em um detector de formas geométricas. Demonstra uma sequência de operações de visão computacional e como os parâmetros podem ser controlados via interface.
    *  [Exemplo de detecção de formas geométricas com OpenCV](https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/)
        *   **Uso:** Tutorial prático de detecção de formas geométricas básicas (triângulos, quadrados, círculos) em imagens usando OpenCV e Python. Útil para entender a detecção de contornos e formas.

*   **Conceitos Fundamentais:**
    *   **Filtros de Imagem:** Compreender filtros como Gaussian Blur, Median Blur para redução de ruído e suavização de imagens, facilitando a detecção de formas ao remover detalhes desnecessários e imperfeições.
    *   **Morfologia Matemática:** Estudar operações de erosão, dilatação, abertura e fechamento para refinar formas detectadas, remover ruídos menores, preencher lacunas em contornos e separar objetos que se tocam.
    *   **Segmentação por Cor:** Aprender a converter espaços de cor (RGB, HSV) e usar *thresholding* para isolar cores específicas, permitindo focar em regiões da imagem que correspondam às cores da base de pouso. O HSV é especialmente útil por separar a cor da luminosidade, tornando a detecção mais robusta a variações de iluminação.
    *   **Detecção de Contornos e Formas:** Utilizar `findContours` e `approxPolyDP` para detectar e aproximar contornos de formas geométricas, permitindo identificar as formas (círculos, quadrados, cruzes) presentes na base de pouso a partir dos contornos extraídos da imagem segmentada.


**🎯 Requisitos Funcionais:**

*   **Requisitos Obrigatórios:**
    1.  **Detecção de Formas Geométricas:** O programa deve detectar as formas geométricas básicas (círculos, quadrados, cruzes) contidas na base de pouso determinada (foto da definição abaixo no corpo do texto, uma pasta com mais fotos de angulos diversos para exemplo será disponibilizada) em imagens e vídeos, o programa deve ser capaz de associar um contorno e um ponto central para cada detecção. A detecção pode ser das formas básicas individualmente ou do conjunto definido pela união delas.
    
    <img src="Base_comum.png" height="200">  <img src="Base_de_Takeoff.png" height="200">
    
    2.  **Parametrização dos argumentos usados:** As formas geométricas a serem detectadas devem ter cores específicas (e.g., círculos e cruzes amarelos, quadrados azuis ou quadrados amarelos etc), o programa deve lidar com isso internamente com parâmetros, assim como deve também parametrizar fatores fundamentais de filtros e qualquer argumento do tipo que for usada no código (permitir mudar em um unico lugar de maneira simples os valores usados, mesmo que atribua um valor padrão), tanto para a conveniência dos seus testes, para descobrir a configuração traz os melhores resultados, quanto para a demonstração que será feita.
    3.  **Interface de Usuário (UI) Básica:** Utilizar elementos de GUI (Interface Gráfica do Usuário) do OpenCV como sliders, select e afins para ajustar em tempo real parâmetros de filtros e algoritmos (limites HSV, tamanho do kernel, blur etc) usados, que foram criados de maneira conveniente para isso.
    4.  **Visualização:** Exibir a imagem original com as formas geométricas detectadas e contornadas, mostrando o tipo de forma e a cor detectada (texto sobreposto na forma ou na janela).

*   **Requisitos Opcionais (Escolher pelo menos 2):**
    1.  **Detecção em algum dataset próprio:** Criar um conjunto de fotos e vídeos (pode-se usar simplesmente a webcam ao vivo detectando numa tela ou numa impressão no papel) com uma réplica da base (pode ser em tamanho reduzido) esteja visível (é interessante criar diferentes condições para os testes) e validar o seu algoritmo para esse exemplo também.
    2.  **Reconhecimento de Formas Compostas:**  Em alternativa à deteção das formas geométricas básicas (círculo, quadrado e cruz) implementar um algoritmo que use a detecção dessas em conjunto para garantir a detecção com maior confiança (não detectar por confusão uma base onde não há ao detectar um quadrado no chão que não seja uma base por exemplo) ao usar, por exemplo, uma combinação das detecções das formas com os centros dentro de uma distância pequena o suficiente entre si para confirmar como um conjunto que represente a base (ao escolher essa opção deve-se demonstrar também separadamente o funcionamento da detecção de formas básicas).
    3.  **Medição de Distância:** Estimar em relação à posição da câmera a posição da base detectada. Ou faça isso para um dataset próprio usando as medidas que vpcê projetar para o lado da base e a amplitude da visão da câmera que usar ou, para as fotos fornecidas, use como referência 1m para o tamanho do lado da base e decida algum valor arbitrário para a amplitude do campo de visão da câmera para fins demonstrativos.
    4.  **Comparativo Entre Ferramentas/Algoritmos no Opencv:** Trazer um comparativo de diferentes opções disponíveis (dentre essas básicas usadas com o OpenCV) para implementar alguma etapa (filtro, método de segmentação por cor, método de extração de contorno, método de categorização de contorno etc) do algoritmo, fazer a demonstração de semelhanças e diferenças entre abordagens escolhidas para comparar e explicar na parte escrita algumas diferenças teóricas e dos resultados.
    5.  **Comparativo com Outros Métodos de Visão Computacional para essa Tarefa:** Trazer o comparativo do uso dos métodos básicos, como eles estão propostos na parte principal da atividade, com métodos de aprendizado de máquina como redes neurais convolucionais usadas em sistemas como o [YOLO](https://docs.ultralytics.com/), para isso deve-se treinar algum modelo de aprendizado de máquina (no sistema da sua escolha), fazer a demonstração comparando ao com OpenCv e explicar na parte escrita algumas diferenças teóricas e dos resultados.

**✅ Checklist de Desenvolvimento:**

*   [ ] Configurar o ambiente Python com OpenCV.
*   [ ] Estudar a documentação e tutoriais de OpenCV sobre filtros, morfologia, cores e detecção de contornos.
*   [ ] Implementar a detecção básica de formas geométricas e cores em imagens estáticas.
*   [ ] Adicionar sliders para ajuste de parâmetros de cor.
*   [ ] Implementar a visualização das formas detectadas.
*   [ ] Implementar pelo menos dois requisitos opcionais.
*   [ ] Testar o programa com diferentes imagens e vídeos.
*   [ ] Documentar o código e preparar a apresentação.
*   [ ] Criar a documentação/relatório do projeto em forma de README.
