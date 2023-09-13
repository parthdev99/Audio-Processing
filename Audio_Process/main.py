import tkinter as tk
import tkinter.filedialog as filedialog
import whisper
import threading
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk
from PIL import Image, ImageTk

logo_image = None


def drop_inside_list_box(event):
    files = event.data
    for file_path in files:
        listb.insert(tk.END, file_path)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if file_path:
        listb.insert(tk.END, file_path)

def clear_file():
    selected_index = listb.curselection()
    if not selected_index:
        return
    listb.delete(selected_index[0])

def clear_all_file():
    listb.delete(0, tk.END)

def transcribe_file():
    if listb.curselection():
        progress_window = tk.Toplevel(window)
        progress_window.title("Transcription in progress")
        progress_window.geometry("400x50")
        progressbar = ttk.Progressbar(progress_window, orient="horizontal", length=400, mode="indeterminate")
        progressbar.pack()
        progressbar.start()

        def transcribe():
            selected_item = listb.get(listb.curselection())
            model = whisper.load_model("large")
            result = model.transcribe(selected_item)

            text.delete('1.0', tk.END)
            text.insert(tk.END, result["text"])

            text.clipboard_clear()
            text.clipboard_append(text.get('1.0', tk.END))

            progressbar.stop()
            progress_window.destroy()

        thread = threading.Thread(target=transcribe)
        thread.start()

    else:
        text.delete(1.0, tk.END)
        text.insert(tk.END, "Select an item")

window = TkinterDnD.Tk()
window.geometry('800x600')
window.config(bg='#232323')  # New edge website background color
window.wm_title("Transcriber")

# Add your company logo here
logo_path = r"C:\Users\parth\Downloads\Audio_Process\logo.jpeg"  # Replace with the path to your logo image
logo_image = Image.open(logo_path).resize((200, 200), Image.LANCZOS)
logo_image = ImageTk.PhotoImage(logo_image)

# Company logo label
logo_label = tk.Label(window, image=logo_image, bg='#232323')  # Match background color
logo_label.grid(row=0, column=0, columnspan=2, pady=20)

welcome_text = "Welcome to Procfas Transcriber\n\n1) Please add audio files to the box below\n2) Select the file you want to transcribe and hit 'transcribe'\n3)The text will appear and will be automatically added to the clipboard\n"
label = tk.Label(window, text=welcome_text, justify=tk.LEFT, font=("Arial", 16), bg='#232323', fg='white')  # Match background color, set text color to white
label.grid(row=1, column=0, columnspan=2, pady=20)

# Drag and drop box with scrollbar
listb = tk.Listbox(window, selectmode=tk.SINGLE, width=70, height=2)
listb.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")
listb.drop_target_register(DND_FILES)
listb.dnd_bind("<<Drop>>", drop_inside_list_box)

# Add File button
add_file_button = tk.Button(window, text="Add File", font=("Arial", 16), command=select_file, bg='#ff6f00', fg='white', activebackground='#ffa000', activeforeground='white', bd=0)
add_file_button.grid(row=3, column=0, padx=(0,200))

# Clear File button
clear_file_button = tk.Button(window, text="Clear", font=("Arial", 16), command=clear_file, bg='#ff6f00', fg='white', activebackground='#ffa000', activeforeground='white', bd=0)
clear_file_button.grid(row=3, column=0, padx=(50,50))

# Clear All Files button
clear_all_button = tk.Button(window, text="Clear All", font=("Arial", 16), command=clear_all_file, bg='#ff6f00', fg='white', activebackground='#ffa000', activeforeground='white', bd=0)
clear_all_button.grid(row=3, column=0, padx=(220,30))

# Transcribe button
transcribe_button = tk.Button(window, text="Transcribe", font=("Arial", 16), command=transcribe_file, bg='#1976d2', fg='white', activebackground='#2196F3', activeforeground='white', bd=0)
transcribe_button.grid(row=4, column=0, columnspan=3, pady=20)

# Scrollbar for the text box
scrollbar_text = tk.Scrollbar(window)
scrollbar_text.grid(row=5, column=2, sticky='ns')

# Text box to display extracted text
text = tk.Text(window, wrap="word", font=("Arial", 14), fg="white", yscrollcommand=scrollbar_text.set, bg='#232323', bd=0, highlightthickness=0)  # Set background color to white
text.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
scrollbar_text.config(command=text.yview)

window.grid_rowconfigure(5, weight=1)
window.grid_columnconfigure(0, weight=1)

window.mainloop()
