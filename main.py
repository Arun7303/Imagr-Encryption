import os
from tkinter import filedialog
from tkinter import *
from tkinter import simpledialog
from cryptography.fernet import Fernet
from tkinter import messagebox

def encrypt_image(image_path, output_directory):
    key = Fernet.generate_key()
    f = Fernet(key)

    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    encrypted_image = f.encrypt(image_data)
    encrypted_image_path = os.path.join(output_directory, 'encrypted_image.png')

    with open(encrypted_image_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_image)

    return key, encrypted_image_path

def copy_key_to_clipboard(key_text):
    key = key_text.get("1.0", "end-1c")
    root.clipboard_clear()
    root.clipboard_append(key)
    root.update()

def decrypt_image(encrypted_image_path, key):
    f = Fernet(key)

    with open(encrypted_image_path, 'rb') as encrypted_file:
        encrypted_image = encrypted_file.read()

    decrypted_image = f.decrypt(encrypted_image)

    return decrypted_image

def save_decrypted_image(decrypted_image, output_directory):
    output_filename = 'decrypted_image.png'
    output_path = os.path.join(output_directory, output_filename)

    with open(output_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_image)

    return output_path

def open_image_with_default_app(output_path):
    os.system(f'xdg-open {output_path}')

root = Tk()
root.withdraw()

choice = messagebox.askquestion("Image Encryption/Decryption", "Do you want to encrypt or decrypt an image?")
if choice == "yes":

    image_path = filedialog.askopenfilename(title="Select Image to Encrypt", filetypes=(("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")))
    if not image_path:
        messagebox.showinfo("Information", "No image selected. Exiting.")
    else:
        output_directory = filedialog.askdirectory(title="Select Output Directory for Encrypted Image")
        if not output_directory:
            messagebox.showinfo("Information", "No output directory selected. Exiting.")
        else:
            key, encrypted_image_path = encrypt_image(image_path, output_directory)
            key_window = Tk()
            key_window.title("Encryption Key")
            key_text = Text(key_window, height=1, width=45)
            key_text.insert(END, key.decode())
            key_text.pack()
            copy_button = Button(key_window, text="Copy Key", command=lambda: copy_key_to_clipboard(key_text))
            copy_button.pack()
            ok_button = Button(key_window, text="OK", command=key_window.destroy)
            ok_button.pack()
            key_window.mainloop()
            messagebox.showinfo("Encryption Complete", f"Image encrypted successfully.\nEncrypted image saved at: {encrypted_image_path}")
elif choice == "no":
    encrypted_image_path = filedialog.askopenfilename(title="Select Encrypted Image", filetypes=(("Image files", "*.png"), ("All files", "*.*")))
    if not encrypted_image_path:
        messagebox.showinfo("Information", "No encrypted image selected. Exiting.")
    else:
        output_directory = filedialog.askdirectory(title="Select Output Directory for Decrypted Image")
        if not output_directory:
            messagebox.showinfo("Information", "No output directory selected. Exiting.")
        else:
            key_text = simpledialog.askstring("Input", "Enter the encryption key:", show="*")
            key = key_text.encode()
            try:
                decrypted_image = decrypt_image(encrypted_image_path, key)
                output_path = save_decrypted_image(decrypted_image, output_directory)
                open_image_with_default_app(output_path)
                print(f"Image decrypted successfully. Decrypted image saved at: {output_path}")
            except Exception as e:
                print(f"Error: {e}")
else:
    messagebox.showinfo("Information", "Exiting without any action.")

root.destroy()
