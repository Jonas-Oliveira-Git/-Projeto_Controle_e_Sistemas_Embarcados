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
        self.label_media2.pack(side="left", padx=10)  # Ajuste para exibição lado a lado

        # Nova label para a media_filtro
        self.label_media_filtro = ctk.CTkLabel(self.frame_display, text="Mídia Filtro")
        self.label_media_filtro.pack(side="left", padx=10)  # Exibe ao lado de media2

        # Controle do filtro (desfoque)
        self.filter_size_label = ctk.CTkLabel(self.frame_controls, text="Gaussian Blur")
        self.filter_size_label.pack(pady=5)

        self.filter_size_slider = ctk.CTkSlider(self.frame_controls, from_=0, to=51, command=self.update_filter_size)
        self.filter_size_slider.set(0)  # Filtro desativado por padrão
        self.filter_size_slider.pack(pady=5)

        # Label para exibir o tamanho do desfoque
        self.filter_size_display = ctk.CTkLabel(self.frame_controls, text="Tamanho do Filtro: 0")
        self.filter_size_display.pack(pady=5)

        # Controle do filtro de dilatação
        self.dilation_kernel_size_label = ctk.CTkLabel(self.frame_controls, text="Tamanho do Kernel para Dilatação")
        self.dilation_kernel_size_label.pack(pady=5)

        self.dilation_kernel_size_slider = ctk.CTkSlider(self.frame_controls, from_=0, to=15, command=self.update_dilation_kernel_size)
        self.dilation_kernel_size_slider.set(0)  # Kernel de dilatação inicializado com 0
        self.dilation_kernel_size_slider.pack(pady=5)

        # Label para exibir o tamanho do kernel de dilatação
        self.dilation_kernel_size_display = ctk.CTkLabel(self.frame_controls, text="Tamanho do Kernel: 0")
        self.dilation_kernel_size_display.pack(pady=5)

        # Controle do filtro de erosão
        self.erosion_kernel_size_label = ctk.CTkLabel(self.frame_controls, text="Tamanho do Kernel para Erosão")
        self.erosion_kernel_size_label.pack(pady=5)

        self.erosion_kernel_size_slider = ctk.CTkSlider(self.frame_controls, from_=0, to=15, command=self.update_erosion_kernel_size)
        self.erosion_kernel_size_slider.set(0)  # Kernel de erosão inicializado com 0
        self.erosion_kernel_size_slider.pack(pady=5)

        # Label para exibir o tamanho do kernel de erosão
        self.erosion_kernel_size_display = ctk.CTkLabel(self.frame_controls, text="Tamanho do Kernel: 0")
        self.erosion_kernel_size_display.pack(pady=5)

        # Controle do filtro de abertura
        self.opening_kernel_size_label = ctk.CTkLabel(self.frame_controls, text="Tamanho do Kernel para Abertura")
        self.opening_kernel_size_label.pack(pady=5)

        self.opening_kernel_size_slider = ctk.CTkSlider(self.frame_controls, from_=0, to=15, command=self.update_opening_kernel_size)
        self.opening_kernel_size_slider.set(0)  # Kernel de abertura inicializado com 0
        self.opening_kernel_size_slider.pack(pady=5)

        # Label para exibir o tamanho do kernel de abertura
        self.opening_kernel_size_display = ctk.CTkLabel(self.frame_controls, text="Tamanho do Kernel: 0")
        self.opening_kernel_size_display.pack(pady=5)

        # Controle do filtro de fechamento
        self.closing_kernel_size_label = ctk.CTkLabel(self.frame_controls, text="Tamanho do Kernel para Fechamento")
        self.closing_kernel_size_label.pack(pady=5)

        self.closing_kernel_size_slider = ctk.CTkSlider(self.frame_controls, from_=0, to=15, command=self.update_closing_kernel_size)
        self.closing_kernel_size_slider.set(0)  # Kernel de fechamento inicializado com 0
        self.closing_kernel_size_slider.pack(pady=5)

        # Label para exibir o tamanho do kernel de fechamento
        self.closing_kernel_size_display = ctk.CTkLabel(self.frame_controls, text="Tamanho do Kernel: 0")
        self.closing_kernel_size_display.pack(pady=5)

        # Tabela para exibir cores
        self.color_table = ctk.CTkFrame(self.frame_controls)
        self.color_table.pack(pady=10)

        # Controle de vídeo
        self.video_cap = None
        self.video_running = False
        self.video_paused = False

        # Bolinhas para exibir as cores
        self.color_balls = []

        # Texto acima das bolinhas
        self.label_colors_identified = ctk.CTkLabel(self.frame_controls, text="Cores identificadas na Ref.")
        self.label_colors_identified.pack(pady=5)

        # Inicializa o valor do filtro
        self.filter_size = 0
        self.dilation_kernel_size = 0
        self.erosion_kernel_size = 0
        self.opening_kernel_size = 0
        self.closing_kernel_size = 0
        self.image1 = None
        self.image2 = None

    def update_filter_size(self, value):
        self.filter_size = int(float(value))
        self.filter_size_display.configure(text=f"Tamanho do Filtro: {self.filter_size}")
        
        # Atualizar a imagem da mídia com o filtro aplicado
        if self.image2 is not None:
            self.apply_filter_and_display(self.image2)

    def update_dilation_kernel_size(self, value):
        self.dilation_kernel_size = int(float(value))
        self.dilation_kernel_size_display.configure(text=f"Tamanho do Kernel: {self.dilation_kernel_size}")
        
        # Atualizar a imagem da mídia com a dilatação aplicada
        if self.image2 is not None:
            self.apply_dilation_and_display(self.image2)

    def update_erosion_kernel_size(self, value):
        self.erosion_kernel_size = int(float(value))
        self.erosion_kernel_size_display.configure(text=f"Tamanho do Kernel: {self.erosion_kernel_size}")
        
        # Atualizar a imagem da mídia com a erosão aplicada
        if self.image2 is not None:
            self.apply_erosion_and_display(self.image2)

    def update_opening_kernel_size(self, value):
        self.opening_kernel_size = int(float(value))
        self.opening_kernel_size_display.configure(text=f"Tamanho do Kernel: {self.opening_kernel_size}")
        
        # Atualizar a imagem da mídia com a abertura aplicada
        if self.image2 is not None:
            self.apply_opening_and_display(self.image2)

    def update_closing_kernel_size(self, value):
        self.closing_kernel_size = int(float(value))
        self.closing_kernel_size_display.configure(text=f"Tamanho do Kernel: {self.closing_kernel_size}")
        
        # Atualizar a imagem da mídia com o fechamento aplicado
        if self.image2 is not None:
            self.apply_closing_and_display(self.image2)

    def load_image1(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.image1 = cv2.imread(file_path)
            self.display_image(file_path, self.label_image1)
            self.identify_and_display_colors(file_path)

    def load_media2(self):
        file_path = filedialog.askopenfilename(filetypes=[("Mídia", "*.jpg;*.png;*.jpeg;*.mp4;*.avi")])
        if file_path:
            if file_path.endswith(('.jpg', '.png', '.jpeg')):
                self.process_and_display_image(file_path)
            else:
                self.play_video(file_path)

    def process_and_display_image(self, file_path):
        self.image2 = cv2.imread(file_path)
        processed_image = self.detect_shapes(self.image2)[0]  # Ignorando a legenda
        self.display_image_cv(processed_image, self.label_media2)

        # Aplicando os filtros na imagem
        self.apply_filter_and_display(processed_image)
        self.apply_dilation_and_display(processed_image)
        self.apply_erosion_and_display(processed_image)
        self.apply_opening_and_display(processed_image)
        self.apply_closing_and_display(processed_image)

    def display_image(self, file_path, label):
        image = Image.open(file_path)
        image.thumbnail((600, 400))
        photo = ImageTk.PhotoImage(image)
        label.configure(image=photo, text="")  # Remove texto da label
        label.image = photo

    def display_image_cv(self, cv_image, label):
        image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image.thumbnail((600, 400))
        photo = ImageTk.PhotoImage(image)
        label.configure(image=photo, text="")
        label.image = photo

    def play_video(self, file_path):
        if self.video_cap:
            self.video_cap.release()

        self.video_cap = cv2.VideoCapture(file_path)
        self.video_running = True
        self.video_paused = False
        threading.Thread(target=self.update_video_frame, daemon=True).start()

    def update_video_frame(self):
        while self.video_running and self.video_cap.isOpened():
            if self.video_paused:
                continue

            ret, frame = self.video_cap.read()
            if not ret:
                break

            processed_frame = self.detect_shapes(frame)[0]  # Ignorando a legenda
            self.display_image_cv(processed_frame, self.label_media2)

            # Aplicando os filtros no vídeo
            media_filtro = self.apply_filter(processed_frame)
            media_filtro = self.apply_dilation(media_filtro)
            media_filtro = self.apply_erosion(media_filtro)
            media_filtro = self.apply_opening(media_filtro)
            media_filtro = self.apply_closing(media_filtro)
            self.display_image_cv(media_filtro, self.label_media_filtro)

            self.root.after(30)

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
            processed_frame = self.detect_shapes(frame)[0]  # Ignorando a legenda
            self.display_image_cv(processed_frame, self.label_media2)

            # Aplicando os filtros na câmera ao vivo
            media_filtro = self.apply_filter(processed_frame)
            media_filtro = self.apply_dilation(media_filtro)
            media_filtro = self.apply_erosion(media_filtro)
            media_filtro = self.apply_opening(media_filtro)
            media_filtro = self.apply_closing(media_filtro)
            self.display_image_cv(media_filtro, self.label_media_filtro)

            self.root.after(30)

    def detect_shapes(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            x, y, w, h = cv2.boundingRect(approx)

            # Detecção das formas geométricas
            if len(approx) == 3:
                shape = "Triângulo"
            elif len(approx) == 4:
                aspect_ratio = float(w) / h
                if 0.95 <= aspect_ratio <= 1.05:
                    shape = "Quadrado"
                else:
                    shape = "Retângulo"
            elif len(approx) > 4:
                shape = "Círculo"
            else:
                shape = "Desconhecido"

            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
            cv2.putText(image, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        return image, contours

    def apply_filter_and_display(self, image):
        filtered_image = self.apply_filter(image)
        self.display_image_cv(filtered_image, self.label_media_filtro)

    def apply_dilation_and_display(self, image):
        dilated_image = self.apply_dilation(image)
        self.display_image_cv(dilated_image, self.label_media_filtro)

    def apply_erosion_and_display(self, image):
        eroded_image = self.apply_erosion(image)
        self.display_image_cv(eroded_image, self.label_media_filtro)

    def apply_opening_and_display(self, image):
        opened_image = self.apply_opening(image)
        self.display_image_cv(opened_image, self.label_media_filtro)

    def apply_closing_and_display(self, image):
        closed_image = self.apply_closing(image)
        self.display_image_cv(closed_image, self.label_media_filtro)

    def apply_filter(self, image):
        if self.filter_size > 0:
            return cv2.GaussianBlur(image, (self.filter_size * 2 + 1, self.filter_size * 2 + 1), 0)
        return image

    def apply_dilation(self, image):
        if self.dilation_kernel_size > 0:
            kernel = np.ones((self.dilation_kernel_size, self.dilation_kernel_size), np.uint8)
            return cv2.dilate(image, kernel, iterations=1)
        return image

    def apply_erosion(self, image):
        if self.erosion_kernel_size > 0:
            kernel = np.ones((self.erosion_kernel_size, self.erosion_kernel_size), np.uint8)
            return cv2.erode(image, kernel, iterations=1)
        return image

    def apply_opening(self, image):
        if self.opening_kernel_size > 0:
            kernel = np.ones((self.opening_kernel_size, self.opening_kernel_size), np.uint8)
            return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        return image

    def apply_closing(self, image):
        if self.closing_kernel_size > 0:
            kernel = np.ones((self.closing_kernel_size, self.closing_kernel_size), np.uint8)
            return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        return image

if __name__ == "__main__":
    root = ctk.CTk()
    app = MediaComparerApp(root)
    root.mainloop()
