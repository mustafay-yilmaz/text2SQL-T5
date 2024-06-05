import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import tkinter.font as tkfont


class App(tk.Tk):
    def __init__(self):
        super().__init__()


        self.title("Text to SQL")
        self.geometry("670x400+725+390")
        self.resizable(False, False)

        self.language = tk.StringVar(value="tr")  # Default language is Turkish
        self.model = tk.StringVar(value="model1")  # Default model

        # Load and round flag images
        self.tr_flag = self.round_image("turkish_flag.png", (50, 50))
        self.en_flag = self.round_image("english_flag.png", (50, 50))

        self.create_widgets()

    def create_widgets(self):
        # Frame to hold flag buttons and center them at the top
        self.flag_frame = ttk.Frame(self)
        self.flag_frame.grid(row=0, column=0, columnspan=2, pady=10)
        self.flag_frame.columnconfigure(0, weight=1)
        self.flag_frame.columnconfigure(1, weight=1)

        # Canvas for Turkish flag
        self.tr_canvas = tk.Canvas(self.flag_frame, width=60, height=60, highlightthickness=0)
        self.tr_canvas.grid(row=0, column=0, padx=10)
        self.tr_oval = self.tr_canvas.create_oval(5, 5, 55, 55, outline="black", width=2)
        self.tr_image = ImageTk.PhotoImage(self.tr_flag)
        self.tr_canvas.create_image(30, 30, image=self.tr_image)

        # Canvas for English flag
        self.en_canvas = tk.Canvas(self.flag_frame, width=60, height=60, highlightthickness=0)
        self.en_canvas.grid(row=0, column=1, padx=10)
        self.en_oval = self.en_canvas.create_oval(5, 5, 55, 55, outline="black", width=2)
        self.en_image = ImageTk.PhotoImage(self.en_flag)
        self.en_canvas.create_image(30, 30, image=self.en_image)
        self.tr_canvas.bind("<Enter>", lambda event: self.on_enter(self.tr_canvas))
        self.tr_canvas.bind("<Leave>", lambda event: self.on_leave(self.tr_canvas))
        self.en_canvas.bind("<Enter>", lambda event: self.on_enter(self.en_canvas))
        self.en_canvas.bind("<Leave>", lambda event: self.on_leave(self.en_canvas))


        # Bind canvas click events to change language and highlight the selected flag
        self.tr_canvas.bind("<Button-1>", self.set_tr)
        self.en_canvas.bind("<Button-1>", self.set_en)

        # Radio buttons for model selection
        self.model_frame = ttk.Frame(self)
        self.model_frame.grid(row=16, column=0, columnspan=3, padx=10, pady=10)
        self.model_frame.columnconfigure(0, weight=1)
        self.model_frame.columnconfigure(1, weight=1)
        self.model_frame.columnconfigure(2, weight=1)

        self.model1_radio = ttk.Radiobutton(self.model_frame, text="Model 1", variable=self.model, value="model1")
        self.model1_radio.grid(row=0, column=0, padx=10)

        self.model2_radio = ttk.Radiobutton(self.model_frame, text="Model 2", variable=self.model, value="model2")
        self.model2_radio.grid(row=0, column=1, padx=10)

        # Font settings
        font = tkfont.Font(family="Georgia", size=16)

        # TextBox for user input
        self.entry = tk.Text(self, width=50,height=1,font=font)
        self.entry.grid(row=15, column=0, columnspan=2, padx=10, pady=10)
        
        # Button to submit the text
        self.process_button = tk.Button(self, text="Gönder", command=self.process_text,bg='green',fg='white',width=10,height=2,font=font)
        self.process_button.grid(row=20, column=0, columnspan=2, padx=10, pady=0)

        self.process_button.bind("<Enter>", self.on_button_enter)
        self.process_button.bind("<Leave>", self.on_button_leave)

        # Label to display the model's response
        self.response_label = ttk.Label(self, text="", wraplength=400,justify="center",font=font)
        self.response_label.grid(row=25, column=0, columnspan=2, padx=10, pady=20)

    def round_image(self, image_path, size):
        image = Image.open(image_path).resize(size, Image.Resampling.LANCZOS).convert("RGBA")
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        rounded_image = Image.new("RGBA", size)
        rounded_image.paste(image, (0, 0), mask=mask)
        return rounded_image

    def on_enter(self, canvas):
        canvas.config(cursor="hand2")

    def on_leave(self, canvas):
        canvas.config(cursor="")
    
    def on_button_enter(self, event):
        event.widget.config(bg='darkgreen',cursor="hand2")

    def on_button_leave(self, event):
        event.widget.config(bg='green')

    def set_tr(self, event=None):
        self.language.set("tr")
        self.process_button.config(text="Gönder")
        self.tr_canvas.itemconfig(self.tr_oval, outline="green", width=10)
        self.en_canvas.itemconfig(self.en_oval, outline="black", width=2)

    def set_en(self, event=None):
        self.language.set("en")
        self.process_button.config(text="Submit")
        self.en_canvas.itemconfig(self.en_oval, outline="green", width=10)
        self.tr_canvas.itemconfig(self.tr_oval, outline="black", width=2)


    def process_text(self):
        input_text = self.entry.get("1.0", tk.END).strip()
        response = self.mock_model_response(input_text, self.model.get())
        # Etiket metnini iki satıra ayırarak oluştur
        response_text = f" {response}"
        self.response_label.config(text=response_text)

    def mock_model_response(self, text, model):
        # Bu fonksiyon, seçilen modele göre bir modelin cevabını simüle eder.
        if model == "model1" and self.language.get() == 'tr':
            return f"Model 1 cevabı (TR):\n \n {text}"
        elif model == "model1" and self.language.get() == 'en':
            return f"Model 1 cevabı:(EN)\n \n{text}"
        elif "model2" and self.language.get() == 'tr':
            return f"Model 2 cevabı:(TR)\n \n{text}"
        else:
            return f"Model 2 cevabı:(EN)\n \n{text}"

if __name__ == "__main__":
    app = App()
    app.mainloop()