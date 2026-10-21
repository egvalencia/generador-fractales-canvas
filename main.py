import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageOps

class GeneradorFractal:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Fractales a partir de Dibujo")
        
        self.width = 600
        self.height = 600
        
        # Canvas para dibujar
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Canvas para mostrar el fractal resultante
        self.canvas_resultado = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas_resultado.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Panel de controles
        self.frame_controles = tk.Frame(root)
        self.frame_controles.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        # Control de Iteraciones
        tk.Label(self.frame_controles, text="Iteraciones:").pack(side=tk.LEFT, padx=5)
        self.scale_iter = tk.Scale(self.frame_controles, from_=1, to=8, orient=tk.HORIZONTAL)
        self.scale_iter.set(4)
        self.scale_iter.pack(side=tk.LEFT, padx=5)
        
        # Control de Escala (Reducción por nivel)
        tk.Label(self.frame_controles, text="Escala:").pack(side=tk.LEFT, padx=5)
        self.scale_factor = tk.Scale(self.frame_controles, from_=0.2, to=0.8, resolution=0.05, orient=tk.HORIZONTAL)
        self.scale_factor.set(0.5)
        self.scale_factor.pack(side=tk.LEFT, padx=5)
        
        # Control de Ángulo de Rotación
        tk.Label(self.frame_controles, text="Ángulo (°):").pack(side=tk.LEFT, padx=5)
        self.scale_angulo = tk.Scale(self.frame_controles, from_=0, to=360, orient=tk.HORIZONTAL)
        self.scale_angulo.set(45)
        self.scale_angulo.pack(side=tk.LEFT, padx=5)
        
        # Botones
        btn_generar = tk.Button(self.frame_controles, text="Generar Fractal", command=self.generar_fractal, bg="#4CAF50", fg="white")
        btn_generar.pack(side=tk.LEFT, padx=10)
        
        btn_limpiar = tk.Button(self.frame_controles, text="Limpiar Dibujo", command=self.limpiar, bg="#f44336", fg="white")
        btn_limpiar.pack(side=tk.LEFT, padx=5)

        # Configurar eventos de dibujo
        self.canvas.bind("<Button-1>", self.iniciar_dibujo)
        self.canvas.bind("<B1-Motion>", self.dibujar)
        
        # Crear imagen en memoria usando Pillow
        self.imagen_base = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.imagen_base)
        self.last_x, self.last_y = None, None

    def iniciar_dibujo(self, event):
        self.last_x, self.last_y = event.x, event.y

    def dibujar(self, event):
        if self.last_x and self.last_y:
            # Dibujar en el canvas de Tkinter
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill="white", width=3, capstyle=tk.ROUND)
            # Dibujar en la imagen interna de Pillow
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=(255, 255, 255, 255), width=3)
            self.last_x, self.last_y = event.x, event.y

    def limpiar(self):
        self.canvas.delete("all")
        self.canvas_resultado.delete("all")
        self.imagen_base = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.imagen_base)

    def aplicar_fractal_recursivo(self, img, iteracion, max_iter, escala, angulo):
        if iteracion >= max_iter:
            return img

        # Redimensionar y rotar el lienzo base
        w, h = img.size
        nuevo_w, nuevo_h = int(w * escala), int(h * escala)
        if nuevo_w < 2 or nuevo_h < 2:
            return img

        sub_img = img.resize((nuevo_w, nuevo_h), Image.Resampling.LANCZOS)
        
        # Aplicar copias en distintas orientaciones/posiciones
        resultado = img.copy()
        
        # Hacemos 2 copias rotadas y desplazadas para crear ramificación
        for signo in [-1, 1]:
            rotada = sub_img.rotate(signo * angulo, expand=True, resample=Image.Resampling.BICUBIC)
            rw, rh = rotada.size
            
            # Posicionamiento recursivo (alrededor del centro/superior)
            pos_x = (w - rw) // 2 + int(signo * w * 0.2)
            pos_y = (h - rh) // 2 - int(h * 0.1)
            
            resultado.paste(rotada, (pos_x, pos_y), rotada)

        # Siguiente nivel de recursión
        return self.aplicar_fractal_recursivo(resultado, iteracion + 1, max_iter, escala, angulo)

    def generar_fractal(self):
        max_iter = self.scale_iter.get()
        escala = self.scale_factor.get()
        angulo = self.scale_angulo.get()

        # Generar la imagen recursiva
        fractal_img = self.aplicar_fractal_recursivo(self.imagen_base, 0, max_iter, escala, angulo)

        # Convertir para mostrar en Tkinter
        self.tk_fractal = ImageTk.PhotoImage(fractal_img)
        self.canvas_resultado.delete("all")
        self.canvas_resultado.create_image(0, 0, anchor=tk.NW, image=self.tk_fractal)

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneradorFractal(root)
    root.mainloop()