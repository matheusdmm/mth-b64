import base64
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        return base64.b64encode(image_data).decode("utf-8")


def encode_images():
    file_types = [("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
    file_paths = filedialog.askopenfilenames(filetypes=file_types)

    if not file_paths:
        return

    if not html_var.get() and not txt_var.get():
        messagebox.showwarning("Attention!", "You forgot to select an option.")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))

    for file_path in file_paths:
        base64_string = image_to_base64(file_path)
        base_filename = os.path.splitext(os.path.basename(file_path))[0]

        if html_var.get():
            alt_text = alt_entry.get()
            file_extension = os.path.splitext(file_path)[1][1:]
            img_tag = f'<img src="data:image/{file_extension};base64,{
                base64_string}" alt="{alt_text}">'
            with open(os.path.join(script_dir, base_filename + ".html"), "w") as f:
                f.write(img_tag)

        if txt_var.get():
            with open(os.path.join(script_dir, base_filename + ".txt"), "w") as f:
                f.write(base64_string)
            root.clipboard_clear()
            root.clipboard_append(base64_string)
            log_text.insert(tk.END, f"Image '{os.path.basename(
                file_path)}' encoded and copied to clipboard.\n")
            print(f"Image '{os.path.basename(file_path)}' encoded and copied to clipboard.\n")
            print(base64_string)
        else:
            log_text.insert(tk.END, f"Image '{os.path.basename(
                file_path)}' encoded successfully.\n")


root = tk.Tk()
root.title("MTH-Base64")
root.geometry("500x450")

title_label = tk.Label(
    root, text="Image to Base64 Encoder", font=("Roboto", 24))
title_label.pack(pady=20)

supported_label = tk.Label(root, text="Supported Files:", font=("Roboto", 12))
supported_label.pack()
supported_text = tk.Label(root, text="JPEG, PNG", font=("Roboto", 10))
supported_text.pack()

select_button = tk.Button(root, text="SELECT IMAGES",
                          bg="#3B82F6", fg="white", command=encode_images)
select_button.pack(pady=20)

options_frame = tk.Frame(root)
options_frame.pack(pady=10, padx=20)

alt_label = tk.Label(options_frame, text="HTML Alt Text (optional):")
alt_label.pack()
alt_entry = tk.Entry(options_frame, width=300)
alt_entry.pack(pady=5)

html_var = tk.BooleanVar(value=False)
txt_var = tk.BooleanVar(value=True)
tk.Checkbutton(options_frame, text="HTML", variable=html_var).pack(pady=5)
tk.Checkbutton(options_frame, text="Base64 Text",
               variable=txt_var).pack(pady=5)

log_text = tk.Text(root, width=400, height=150)
log_text.pack(pady=10)

root.mainloop()
