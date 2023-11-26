from xmlrpc.client import ServerProxy
import tkinter as tk
from tkinter import messagebox
import json
import time

class MedicalQueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Queue System")

        self.label = tk.Label(root, text="Antrean Registrasi Medis", font=("Helvetica", 16))
        self.label.pack(pady=10)
        
        self.antrean_info_label = tk.Label(root, text="")
        self.antrean_info_label.pack(pady=10)

        self.name_label = tk.Label(root, text='Username')
        self.name_entry = tk.Entry(root, textvariable = name_var)
        
        self.pass_label = tk.Label(root, text='Password')
        self.pass_entry = tk.Entry(root, textvariable = pass_var)

        self.update_button = tk.Button(root, text="Daftar Antrean", command=self.update_antrean)
        self.update_button.pack(pady=10)

        self.server_proxy = ServerProxy('http://127.0.0.1:8000')
        #self.update_antrean()
        #self.root.after(5000, self.auto_update_antrean)  # Auto-update every 5 seconds

    def update_antrean(self):
        try:
            antrean_data_str = self.server_proxy.get_antrean()
            print("Response from server:", antrean_data_str)
            antrean_data = json.loads(antrean_data_str)

            if antrean_data:
                name = name_var.get()
                password = pass_var.get()
                i = 1
                print("The name is : " + name)
                print("The password is : " + password)
                info_text = f"Nomor Antrean: {antrean_data['{i}']}\nEstimasi Waktu: {antrean_data['estimasi_waktu']}"
                self.antrean_info_label.config(text=info_text)
                name_var.set("")
                pass_var.set("")
                i = i+1
            else:
                self.antrean_info_label.config(text="Tidak ada data antrean.")

        except Exception as e:
            print(f"Error updating antrean: {e}")
            messagebox.showerror("Error", "Gagal mengupdate antrean. Periksa koneksi Anda.") 
    
    def auto_update_antrean(self):
        self.update_antrean()
        self.root.after(5000, self.auto_update_antrean)

if __name__ == "__main__":
    root = tk.Tk()
    name_var = tk.StringVar()
    pass_var = tk.StringVar()
    
    app = MedicalQueueApp(root)
    
    root.geometry("300x200")
    root.mainloop()
