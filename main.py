import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageFont
import math

class GeneradorFractal:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Fractales - Espiral de Oro")
        
        self.width = 600
        self.height = 600
        
        self.undo_stack = []
        self.redo_stack = []
        
        # Canvas para dibujar (Fondo blanco)
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Canvas para mostrar el fractal resultante (Fondo negro)
        self.canvas_resultado = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas_resultado.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Panel de controles superior
        self.frame_controles = tk.Frame(root)
        self.frame_controles.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        # Botones de Historial
        btn_deshacer = tk.Button(self.frame_controles, text="⬅ Deshacer", command=self.deshacer, bg="#FF9800", fg="white")
        btn_deshacer.pack(side=tk.LEFT, padx=2)
        
        btn_rehacer = tk.Button(self.frame_controles, text="Rehacer ➡", command=self.rehacer, bg="#FF9800", fg="white")
        btn_rehacer.pack(side=tk.LEFT, padx=5)
        
        # Entrada de texto (Soporta Kanji/Kana/Texto)
        tk.Label(self.frame_controles, text="Texto:").pack(side=tk.LEFT, padx=2)
        self.entry_texto = tk.Entry(self.frame_controles, width=8)
        self.entry_texto.insert(0, "無駄")
        self.entry_texto.pack(side=tk.LEFT, padx=2)
        
        btn_texto = tk.Button(self.frame_controles, text="Agregar Texto", command=self.agregar_texto_canvas, bg="#2196F3", fg="white")
        btn_texto.pack(side=tk.LEFT, padx=5)
        
        # Control de Escala
        tk.Label(self.frame_controles, text="Escala:").pack(side=tk.LEFT, padx=2)
        self.scale_factor = tk.Scale(self.frame_controles, from_=0.5, to=0.95, resolution=0.01, orient=tk.HORIZONTAL)
        self.scale_factor.set(0.85)
        self.scale_factor.pack(side=tk.LEFT, padx=2)
        
        # Control de Ángulo (Ángulo de Oro por defecto: 137.5°)
        tk.Label(self.frame_controles, text="Ángulo (°):").pack(side=tk.LEFT, padx=2)
        self.scale_angulo = tk.Scale(self.frame_controles, from_=0, to=360, resolution=0.1, orient=tk.HORIZONTAL)
        self.scale_angulo.set(137.5)
        self.scale_angulo.pack(side=tk.LEFT, padx=2)
        
        # Botones principales
        btn_generar = tk.Button(self.frame_controles, text="Generar", command=self.generar_fractal, bg="#4CAF50", fg="white")
        btn_generar.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = tk.Button(self.frame_controles, text="Limpiar", command=self.limpiar, bg="#f44336", fg="white")
        btn_limpiar.pack(side=tk.LEFT, padx=5)

        # Configurar eventos de dibujo
        self.canvas.bind("<Button-1>", self.iniciar_dibujo)
        self.canvas.bind("<B1-Motion>", self.dibujar_en_vivo)
        
        # Imágenes en memoria
        self.imagen_fractal = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.imagen_fractal)
        
        self.imagen_visual = Image.new("RGBA", (self.width, self.height), (255, 255, 255, 255))
        self.draw_visual = ImageDraw.Draw(self.imagen_visual)
        
        self.last_x, self.last_y = None, None
        self.refrescar_canvas()

    def guardar_estado(self):
        self.undo_stack.append((self.imagen_fractal.copy(), self.imagen_visual.copy()))
        self.redo_stack.clear()

    def deshacer(self):
        if self.undo_stack:
            self.redo_stack.append((self.imagen_fractal.copy(), self.imagen_visual.copy()))
            self.imagen_fractal, self.imagen_visual = self.undo_stack.pop()
            self.draw = ImageDraw.Draw(self.imagen_fractal)
            self.draw_visual = ImageDraw.Draw(self.imagen_visual)
            self.refrescar_canvas()

    def rehacer(self):
        if self.redo_stack:
            self.undo_stack.append((self.imagen_fractal.copy(), self.imagen_visual.copy()))
            self.imagen_fractal, self.imagen_visual = self.redo_stack.pop()
            self.draw = ImageDraw.Draw(self.imagen_fractal)
            self.draw_visual = ImageDraw.Draw(self.imagen_visual)
            self.refrescar_canvas()

    def refrescar_canvas(self):
        self.tk_image_base = ImageTk.PhotoImage(self.imagen_visual.convert("RGB"))
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image_base)

    def agregar_texto_canvas(self):
        texto = self.entry_texto.get()
        if not texto:
            return
        
        self.guardar_estado()
        x, y = self.width // 2, self.height // 2
        
        font = None
        for nombre_fuente in ["meiryo.ttc", "msgothic.ttc", "arial.ttf"]:
            try:
                font = ImageFont.truetype(nombre_fuente, 35)
                break
            except IOError:
                continue
        if font is None:
            font = ImageFont.load_default()
            
        self.draw.text((x - (len(texto) * 12), y - 20), texto, fill=(255, 255, 255, 255), font=font)
        self.draw_visual.text((x - (len(texto) * 12), y - 20), texto, fill=(0, 0, 0, 255), font=font)
        self.refrescar_canvas()

    def iniciar_dibujo(self, event):
        self.guardar_estado()
        self.last_x, self.last_y = event.x, event.y

    def dibujar_en_vivo(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill="black", width=3, capstyle=tk.ROUND)
            self.draw_visual.line([self.last_x, self.last_y, event.x, event.y], fill=(0, 0, 0, 255), width=3)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=(255, 255, 255, 255), width=3)
            self.last_x, self.last_y = event.x, event.y

    def limpiar(self):
        self.guardar_estado()
        self.canvas.delete("all")
        self.canvas_resultado.delete("all")
        
        self.imagen_fractal = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.imagen_fractal)
        
        self.imagen_visual = Image.new("RGBA", (self.width, self.height), (255, 255, 255, 255))
        self.draw_visual = ImageDraw.Draw(self.imagen_visual)
        
        self.refrescar_canvas()

    def generar_fractal(self):
        angulo_base = self.scale_angulo.get()
        escala_factor = self.scale_factor.get()
        
        # Creamos una imagen acumulativa en negro para el resultado
        resultado = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 255))
        
        # Generamos la secuencia en espiral (duplicando y transformando iterativamente)
        # Cantidad de pasos en la cadena de la espiral
        pasos = 60
        img_actual = self.imagen_fractal.copy()
        
        # Posición inicial centrada
        cx, cy = self.width / 2, self.height / 2
        
        acumulada = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        
        for i in range(pasos):
            # Calcular ángulo acumulado según el Ángulo de Oro
            angulo_actual = i * angulo_base
            
            # Escala progresiva
            factor = escala_factor ** i
            w, h = self.imagen_fractal.size
            nw, nh = max(1, int(w * factor)), max(1, int(h * factor))
            
            if nw < 2 or nh < 2:
                break
                
            sub = self.imagen_fractal.resize((nw, nh), Image.Resampling.LANCZOS)
            rotada = sub.rotate(angulo_actual, expand=True, resample=Image.Resampling.BICUBIC)
            
            rw, rh = rotada.size
            # Desplazamiento radial en espiral logarítmica
            radio = i * 4.0 * escala_factor
            rad_ang = math.radians(angulo_actual)
            
            px = int(cx - rw / 2 + radio * math.cos(rad_ang))
            py = int(cy - rh / 2 + radio * math.sin(rad_ang))
            
            acumulada.paste(rotada, (px, py), rotada)

        # Mostrar el resultado final en el canvas negro derecho
        self.tk_fractal = ImageTk.PhotoImage(acumulada.convert("RGB"))
        self.canvas_resultado.delete("all")
        self.canvas_resultado.create_image(0, 0, anchor=tk.NW, image=self.tk_fractal)

if __name__ == "__main__":
    root = tk.Tk()
    app = GeneradorFractal(root)
    root.mainloop()