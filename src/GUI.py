import steganography
import crypto

import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
import os

class GUI(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Image Steganography")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid()

        self.label0 = tk.Label(self, text="Input image:")
        self.filename = tk.Entry(self)
        self.browse_button0 = tk.Button(self, text="Browse", command=self.browse_file)
        self.label0.grid(row=1, column=0)
        self.filename.grid(row=1, column=1)
        self.browse_button0.grid(row=1, column=2)

        self.label1 = tk.Label(self, text="Password:")
        self.password = tk.Entry(self, show="*")
        self.label1.grid(row=2, column=0)
        self.password.grid(row=2, column=1)

        self.label2 = tk.Label(self, text="Output folder:")
        self.output_folder = tk.Entry(self)
        self.browse_button1 = tk.Button(self, text="Browse", command=self.browse_folder)
        self.label2.grid(row=3, column=0)
        self.output_folder.grid(row=3, column=1)
        self.browse_button1.grid(row=3, column=2)

        self.label3 = tk.Label(self, text="Output file name:")
        self.output_file = tk.Entry(self)
        self.label3.grid(row=4, column=0)
        self.output_file.grid(row=4, column=1)

        self.label4 = tk.Label(self, text="Secret file (hide only):")
        self.secret_name = tk.Entry(self)
        self.browse_button2 = tk.Button(self, text="Browse", command=self.browse_secret)
        self.label4.grid(row=5, column=0)
        self.secret_name.grid(row=5, column=1)
        self.browse_button2.grid(row=5, column=2)

        self.hide_button = tk.Button(self, text='Hide', command=self.hide)
        self.find_button = tk.Button(self, text='Find', command=self.find)
        hide_success = StringVar()
        self.hide_success_label = tk.Label(self, textvariable=hide_success)
        self.hide_button.grid(row=6, column=0, columnspan=2)
        self.find_button.grid(row=6, column=1, columnspan=2)
        self.hide_success_label.grid(row=7, column=0, columnspan=4)


    def hide(self):
        image_name = self.filename.get()
        new_image_name = os.path.join(self.output_folder.get(), self.output_file.get())
        secret_name = self.secret_name.get()

        password = self.password.get()
        self.password.delete(0, tk.END)
        key = crypto.create_key(password)
        del(password)  # delete password variable, so no one can use it later

        if image_name and new_image_name and secret_name:
            if not steganography.hide(image_name, new_image_name, secret_name, key):
                self.hide_success = 'Could not fit all secret data into the image.'
            else:
                self.hide_success = 'Success!'

    def find(self):
        image_name = self.filename.get()
        secret_name = os.path.join(self.output_folder.get(), self.output_file.get())

        key = crypto.create_key(self.password.get())
        self.password.delete(0, tk.END)

        steganography.find(image_name, secret_name, key)

        self.hide_success = 'Success!'

    def browse_secret(self):
        return self.browse_file(secret=True)

    def browse_file(self, secret=False):
        filename = askopenfilename()
        if filename:
            if secret:
                self.secret_name.delete(0, tk.END)
                self.secret_name.insert(0, filename)
            else:
                self.filename.delete(0, tk.END)
                self.filename.insert(0, filename)

    def browse_folder(self):
        foldername = askdirectory()
        if foldername:
            self.output_folder.delete(0, tk.END)
            self.output_folder.insert(0, foldername)


if __name__ == "__main__":
    GUI().mainloop()
