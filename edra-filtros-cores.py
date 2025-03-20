import cv2
import numpy as np
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
from sklearn.cluster import KMeans

class MediaComparerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Mídias")
        self.root.geometry("900x700")

        # Layout
        self.frame_controls = ctk.CTkFrame(self.root)
        self.frame_controls.pack(side="left", fill="y")

        self.frame_display = ctk.CTkFrame(self.root)
        self.frame_display.pack(side="right", fill="both", expand=True)

        # Botões de seleção de mídia
        self.btn_load_image1 = ctk.CTkButton(self.frame_controls, text="Carregar Imagem 1", command=self.load_image1)
        self.btn_load_image1.pack(pady=10)

        self.btn_load_media2 = ctk.CTkButton(self.frame_controls, text="Carregar Mídia 2", command=self.load_media2)
        self.btn_load_media2.pack(pady=10)

        # Botão de câmera ao vivo
        self.btn_live_camera = ctk.CTkButton(self.frame_controls, text="Câmera ao Vivo", command=self.start_live_camera)
        self.btn_live_camera.pack(pady=10)

        # Labels para exibição de mídia
        self.label_image1 = ctk.CTkLabel(self.frame_display, text="Imagem 1")
        self.label_image1.pack(pady=10)

        self.label_media2 = ctk.CTkLabel(self.frame_display, text="Mídia 2")
        self.label_media2.pack(side="left", padx=10)

        # Nova label para a imagem filtrada
        self.label_media_filtro = ctk.CTkLabel(self.frame_display, text="Mídia Filtro")
        self.label_media_filtro.pack(side="left", padx=10)

        # Controle do filtro (desfoque)
        self.filter_size_label = ctk.CTkLabel(self.frame_controls, text="Gaussian Blur")
        self.filter_size_label.pack(pady=5)

        self.filter_size_slider = ctk.CTkSlider(self.frame_controls, from_=0, to=51, command=self.update_filter_size)
        self.filter_size_slider.set(0)
        self.filter_size_slider.pack(pady=5)

        # Label para exibir o tamanho do desfoque
        self.filter_size_display = ctk.CTkLabel(self.frame_controls, text="Tamanho do Filtro: 0")
        self.filter_size_display.pack(pady=5)

        # Controle de vídeo
        self.video_cap = None
        self.video_running = False
        self.video_paused = False

        # Bolinhas para exibir as cores
        self.color_balls_image1 = []  # Bolinhas para imagem 1
        self.color_balls_media2 = []   # Bolinhas para media 2

        # Frame para Cores da Imagem 1
        self.frame_colors_image1 = ctk.CTkFrame(self.frame_controls)
        self.frame_colors_image1.pack(pady=10)

        self.label_colors_image1 = ctk.CTkLabel(self.frame_colors_image1, text="Cores da Imagem 1")
        self.label_colors_image1.pack(pady=5)

        self.label_colors_image1_info = ctk.CTkLabel(self.frame_colors_image1, text="Bolinhas com as cores da Imagem 1")
        self.label_colors_image1_info.pack(pady=5)

        # Frame para Cores da Mídia 2
        self.frame_colors_media2 = ctk.CTkFrame(self.frame_controls)
        self.frame_colors_media2.pack(pady=10)

        self.label_colors_media2 = ctk.CTkLabel(self.frame_colors_media2, text="Cores da Mídia 2")
        self.label_colors_media2.pack(pady=5)

        self.label_colors_media2_info = ctk.CTkLabel(self.frame_colors_media2, text="Bolinhas da Mídia 2")
        self.label_colors_media2_info.pack(pady=5)

        # Botão para restaurar cores
        self.btn_restore_colors = ctk.CTkButton(self.frame_controls, text="Restaurar Cores", command=self.restore_colors)
        self.btn_restore_colors.pack(pady=10)

        # Botão para detectar contornos
        self.btn_detect_contours = ctk.CTkButton(self.frame_controls, text="Detectar Contornos", command=self.detect_contours)
        self.btn_detect_contours.pack(pady=10)

        # Botão para restaurar detecção de contornos
        self.btn_restore_contours = ctk.CTkButton(self.frame_controls, text="Restaurar Detecção de Contornos", command=self.restore_contours)
        self.btn_restore_contours.pack(pady=10)

        # Inicializa o valor do filtro
        self.filter_size = 0
        self.image1 = None
        self.image2 = None
        self.image_cor = None  # Nova variável para a imagem de cor
        self.image_cor_original = None  # Nova variável para armazenar a imagem original

    def load_image1(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.image1 = cv2.imread(file_path)
            self.display_image(file_path, self.label_image1)
            self.identify_and_display_colors(self.image1, "image1")

    def load_media2(self):
        file_path = filedialog.askopenfilename(filetypes=[("Mídia", "*.jpg;*.png;*.jpeg;*.mp4;*.avi")])
        if file_path:
            if file_path.endswith(('.jpg', '.png', '.jpeg')):
                self.process_and_display_image(file_path)
                self.identify_and_display_colors(self.image2, "media2")  # Alteração aqui
            else:
                self.play_video(file_path)

    def process_and_display_image(self, file_path):
        self.image2 = cv2.imread(file_path)
        processed_image = self.image2  # Usando a imagem carregada como está
        self.display_image_cv(processed_image, self.label_media2)

        # Aplicando os filtros na imagem
        self.apply_filter_and_display(processed_image)

    def display_image(self, file_path, label):
        image = Image.open(file_path)
        image.thumbnail((600, 400))
        photo = ImageTk.PhotoImage(image)
        label.configure(image=photo, text="")
        label.image = photo

    def display_image_cv(self, cv_image, label):
        image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image.thumbnail((600, 400))
        photo = ImageTk.PhotoImage(image)
        label.configure(image=photo, text="")
        label.image = photo

    def identify_and_display_colors(self, image, source):
        # Redimensionar a imagem para acelerar o processamento
        image_resized = cv2.resize(image, (100, 100))
        pixels = image_resized.reshape(-1, 3)
        
        # Usar KMeans para encontrar as cores dominantes
        kmeans = KMeans(n_clusters=5)
        kmeans.fit(pixels)
        colors = kmeans.cluster_centers_.astype(int)

        if source == "image1":
            # Limpar bolinhas anteriores da imagem 1
            for ball in self.color_balls_image1:
                ball.destroy()
            self.color_balls_image1.clear()

            # Criar novas bolinhas para imagem 1
            for color in colors:
                color_ball = ctk.CTkFrame(self.frame_colors_image1, width=30, height=30, corner_radius=15, fg_color=f"#{color[2]:02x}{color[1]:02x}{color[0]:02x}")
                color_ball.pack(side="left", padx=5, pady=5)
                color_ball.bind("<Button-1>", lambda e, c=color: self.apply_color_filter(c))
                self.color_balls_image1.append(color_ball)

        elif source == "media2":
            # Limpar bolinhas anteriores da mídia 2
            for ball in self.color_balls_media2:
                ball.destroy()
            self.color_balls_media2.clear()

            # Criar novas bolinhas para mídia 2
            for color in colors:
                color_ball = ctk.CTkFrame(self.frame_colors_media2, width=30, height=30, corner_radius=15, fg_color=f"#{color[2]:02x}{color[1]:02x}{color[0]:02x}")
                color_ball.pack(side="left", padx=5, pady=5)
                color_ball.bind("<Button-1>", lambda e, c=color: self.apply_color_filter(c))
                self.color_balls_media2.append(color_ball)

    def apply_color_filter(self, selected_color):
        if self.image2 is not None:
            # Cria uma máscara para a cor selecionada
            lower_bound = np.array(selected_color) - 40
            upper_bound = np.array(selected_color) + 40
            mask = cv2.inRange(self.image2, lower_bound, upper_bound)

            # Aplica a máscara à imagem
            filtered_image = cv2.bitwise_and(self.image2, self.image2, mask=mask)

            # Converte o resto da imagem para branco
            self.image_cor = np.full_like(self.image2, 255)
            self.image_cor[mask > 0] = filtered_image[mask > 0]

            # Armazena a imagem original para restaurar contornos
            self.image_cor_original = self.image_cor.copy()

            # Exibe a imagem filtrada
            self.display_image_cv(self.image_cor, self.label_media_filtro)

    def restore_colors(self):
        if self.image2 is not None:
            # Restaura a imagem original na label de mídia filtrada
            self.display_image_cv(self.image2, self.label_media_filtro)

    def detect_contours(self):
        if self.image_cor is not None:
            # Converter a imagem filtrada para escala de cinza
            gray = cv2.cvtColor(self.image_cor, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

            # Encontrar contornos
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Desenhar contornos e identificar formas
            for contour in contours:
                # Aproximar contornos
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                # Identificar formas
                if len(approx) == 3:
                    shape_name = "Triângulo"
                elif len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(approx)
                    aspect_ratio = float(w) / h
                    shape_name = "Quadrado" if aspect_ratio >= 0.95 and aspect_ratio <= 1.05 else "Retângulo"
                elif len(approx) == 5:
                    shape_name = "Pentágono"
                elif len(approx) == 6:
                    shape_name = "Hexágono"
                else:
                    shape_name = "Círculo"

                # Desenhar contorno e nome da forma
                cv2.drawContours(self.image_cor, [approx], 0, (0, 255, 0), 5)
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.putText(self.image_cor, shape_name, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Exibir a imagem com contornos detectados
            self.display_image_cv(self.image_cor, self.label_media_filtro)

    def restore_contours(self):
        if self.image_cor_original is not None:
            # Restaura a imagem original antes da detecção de contornos
            self.image_cor = self.image_cor_original.copy()
            self.display_image_cv(self.image_cor, self.label_media_filtro)

    def start_live_camera(self):
        if self.video_cap:
            self.video_cap.release()

        self.video_cap = cv2.VideoCapture(0)
        if not self.video_cap.isOpened():
            print("Não foi possível acessar a câmera.")
            return

        self.video_running = True
        self.video_paused = False
        threading.Thread(target=self.update_live_camera_frame, daemon=True).start()

    def update_live_camera_frame(self):
        while self.video_running and self.video_cap.isOpened():
            if self.video_paused:
                continue

            ret, frame = self.video_cap.read()
            if not ret:
                break

            # Processar o frame para detectar cores
            self.identify_and_display_colors(frame, "live_camera")

            # Aplicar a detecção de contornos se a imagem filtrada estiver disponível
            if self.image_cor is not None:
                self.detect_contours()

            # Exibir o frame da câmera
            self.display_image_cv(frame, self.label_media2)

            # Aplicando os filtros na câmera ao vivo
            media_filtro = self.apply_filter(frame)
            self.display_image_cv(media_filtro, self.label_media_filtro)

            self.root.after(30)

    def apply_filter_and_display(self, image):
        filtered_image = self.apply_filter(image)
        self.display_image_cv(filtered_image, self.label_media_filtro)

    def apply_filter(self, image):
        if self.filter_size > 0:
            return cv2.GaussianBlur(image, (self.filter_size * 2 + 1, self.filter_size * 2 + 1), 0)
        return image

    def update_filter_size(self, value):
        self.filter_size = int(value)
        self.filter_size_display.configure(text=f"Tamanho do Filtro: {self.filter_size}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = MediaComparerApp(root)
    root.mainloop()
