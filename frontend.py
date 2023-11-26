from xmlrpc.client import ServerProxy
import json
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror


class TemperatureConverter:
    @staticmethod
    def fahrenheit_to_celsius(f):
        return (f - 32) * 5 / 9

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Telkom Hospital Queue Management System')
        self.geometry('600x600')
        self.resizable(False, False)
        
        # field options
        options = {'padx': 5, 'pady': 5}

        # Nomor Rekam Medis label
        self.no_medis_label = ttk.Label(self, text='No. Rekam Medis')
        self.no_medis_label.grid(column=0, row=0, **options)

        # Nomor Rekam Medis entry
        self.no_medis = tk.StringVar()
        self.no_medis_entry = ttk.Entry(self, textvariable=self.no_medis)
        self.no_medis_entry.grid(column=1, row=0, columnspan=2, **options)
        self.no_medis_entry.focus()
        
        # Nama Lengkap label
        self.nama_label = ttk.Label(self, text='Nama Lengkap')
        self.nama_label.grid(column=0, row=1, **options)

        # Nama Lengkap entry
        self.nama = tk.StringVar()
        self.nama_entry = ttk.Entry(self, textvariable=self.nama)
        self.nama_entry.grid(column=1, row=1, columnspan=2, **options)
        self.nama_entry.focus()
        
        # Tanggal Lahir label
        self.ttl_label = ttk.Label(self, text='Tempat & Tanggal Lahir')
        self.ttl_label.grid(column=0, row=2, **options)

        # Tanggal Lahir entry
        self.ttl = tk.StringVar()
        self.ttl_entry = ttk.Entry(self, textvariable=self.ttl)
        self.ttl_entry.grid(column=1, row=2, columnspan=2, **options)
        self.ttl_entry.focus()

        self.convert_button = ttk.Button(self, text='Daftar Antrean')
        self.convert_button['command'] = self.update_antrean
        self.convert_button.grid(row=3, columnspan=3, **options)

        # result label
        self.result_label = ttk.Label(self)
        self.result_label.grid(row=4, columnspan=2, **options)

        # add padding to the frame and show it
        # self.grid(padx=10, pady=10)
        
        self.server_proxy = ServerProxy('http://127.0.0.1:8000')
        
    def convert(self):
        """  Handle button click event
        """
        try:
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
            
        except ValueError as error:
            showerror(title='Error', message=error)
    
    def update_antrean(self):
        try:
            antrean_data_str = self.server_proxy.get_antrean()
            print("Response from server:", antrean_data_str)
            antrean_data = json.loads(antrean_data_str)

            if antrean_data:
                i = 1
                no_rekam_medis = self.no_medis.get()
                nama_lengkap = self.nama.get()
                result = f'Pasien Nomor Antrean ke-{i} Nama = {nama_lengkap}, No. Rekam Medis = {no_rekam_medis}'
                self.result_label.config(text=result)
                i = i + 1                
            else:
                self.result_label.config(text="Tidak ada data antrean.")

        except Exception as e:
            print(f"Error updating antrean: {e}")
            showerror("Error", "Gagal mengupdate antrean. Periksa koneksi Anda.") 

if __name__ == "__main__":
    app = App()
    app.mainloop()