import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from openai import OpenAI
import base64
import threading

client = OpenAI(api_key="YOUR_API_KEY")


def generate_image():
    prompt = prompt_entry.get()
    if not prompt.strip():
        status_label.config(text="Please enter a prompt!", foreground="#e74c3c")
        return

    status_label.config(text="Generating picture...", foreground="#f39c12")

    def run():
        try:
            response = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size="1024x1024"
            )

            image_base64 = response.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            with open("pic.png", "wb") as f:
                f.write(image_bytes)

            img = Image.open("pic.png").resize((350, 350))
            img_tk = ImageTk.PhotoImage(img)

            image_label.config(image=img_tk)
            image_label.image = img_tk

            status_label.config(text="Finished!", foreground="#2ecc71")
        except Exception as e:
            status_label.config(text=f"Error: {e}", foreground="#e74c3c")

    threading.Thread(target=run).start()


def show_frame(frame):
    frame.tkraise()



root = tk.Tk()
root.title("AI Picture Generator")
root.geometry("500x650")
root.configure(bg="#1a1a2e")
root.resizable(False, False)


style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12, "bold"), foreground="black", background="#0b3d91")
style.map("TButton",background=[('active', '#1f51b0')],foreground=[('active', 'black')])



style.configure("TEntry", font=("Arial", 12))




home_frame = tk.Frame(root, bg="#1a1a2e")
home_frame.place(relwidth=1, relheight=1)

generator_frame = tk.Frame(root, bg="#1a1a2e")
generator_frame.place(relwidth=1, relheight=1)

title_label = tk.Label(home_frame, text="Welcome to AI Image Generator", font=("Helvetica", 20, "bold"), fg="#ffffff", bg="#1a1a2e", wraplength=400, justify="center")

title_label.pack(pady=(100, 20))

desc_label = tk.Label(home_frame, text="Create images with AI in seconds!", font=("Helvetica", 14), fg="#bdc3c7", bg="#1a1a2e", wraplength=400, justify="center")

desc_label.pack(pady=(0, 40))

start_button = ttk.Button(home_frame, text="Start Generating", command=lambda: show_frame(generator_frame))
start_button.pack(pady=20)




back_button = ttk.Button(generator_frame, text="← Home", command=lambda: show_frame(home_frame))
back_button.pack(pady=10, anchor="w", padx=20)

prompt_entry = ttk.Entry(generator_frame, width=40)
prompt_entry.pack(pady=10)
prompt_entry.insert(0, "Enter your prompt here...")



generate_button = ttk.Button(generator_frame, text="Generate Picture", command=generate_image)
generate_button.pack(pady=10)

status_label = tk.Label(generator_frame, text="", font=("Arial", 11), bg="#1a1a2e", fg="#ffffff")
status_label.pack(pady=5)

image_label = tk.Label(generator_frame, bg="#1a1a2e")
image_label.pack(pady=15)


show_frame(home_frame)

root.mainloop()
