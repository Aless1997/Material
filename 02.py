import tkinter as tk
from tkinter import messagebox
import os
import csv

class Materiale:
    def __init__(self, cod, descr, qta=0):
        self.setCod(cod)
        self.setDescr(descr)
        self.setQta(qta)

    def setCod(self, cod):
        self.__cod = cod

    def setDescr(self, descr):
        self.__descr = descr

    def setQta(self, qta):
        self.__qta = qta

    def addQta(self, qta):
        self.__qta += qta

    def exportCsv(self):
        if not os.path.exists('Prova.csv'):
            with open('Prova.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['codice', 'descrizione', 'qta'])
                writer.writerow([self.__cod, self.__descr, self.__qta])
        else:
            with open('Prova.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([self.__cod, self.__descr, self.__qta])

    @staticmethod
    def modifica_qta_csv(cod, new_qta):
        file_path = 'Prova.csv'
        found = False

        if os.path.exists(file_path):
            temp_data = []
            with open(file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader)  
                temp_data.append(header)

                for row in reader:
                    if row[0] == cod:  
                        row[2] = str(new_qta)
                        found = True
                    temp_data.append(row)

            if found:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(temp_data)
                messagebox.showinfo("Successo", "Quantità aggiornata con successo!")
            else:
                messagebox.showerror("Errore", "Codice non trovato.")
        else:
            messagebox.showerror("Errore", "Il file CSV non esiste.")

    @staticmethod
    def visualizza_materiali():
        file_path = 'Prova.csv'
        materials = []
        if os.path.exists(file_path):
            with open(file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    materials.append(f"Codice: {row[0]}, Descrizione: {row[1]}, Quantità: {row[2]}")
        return materials

def inserisci_materiale():
    cod = cod_entry.get()
    descr = descr_entry.get()
    try:
        qta = int(qta_entry.get())
        materiale = Materiale(cod, descr, qta)
        materiale.exportCsv()
        messagebox.showinfo("Successo", "Materiale aggiunto con successo!")
        cod_entry.delete(0, tk.END)
        descr_entry.delete(0, tk.END)
        qta_entry.delete(0, tk.END)
        aggiorna_lista_materiali()
    except ValueError:
        messagebox.showerror("Errore", "La quantità deve essere un numero intero.")

def modifica_qta():
    cod = cod_mod_entry.get()
    try:
        new_qta = int(qta_mod_entry.get())
        Materiale.modifica_qta_csv(cod, new_qta)
        cod_mod_entry.delete(0, tk.END)
        qta_mod_entry.delete(0, tk.END)
        aggiorna_lista_materiali()
    except ValueError:
        messagebox.showerror("Errore", "La nuova quantità deve essere un numero intero.")

def aggiorna_lista_materiali():
    materials = Materiale.visualizza_materiali()
    lista_materiali_text.delete(1.0, tk.END)
    if materials:
        for mat in materials:
            lista_materiali_text.insert(tk.END, mat + "\n")
    else:
        lista_materiali_text.insert(tk.END, "Nessun materiale salvato.\n")

# Creazione della finestra principale
root = tk.Tk()
root.title("Gestione Materiali")
root.geometry("600x500")  # Impostazione delle dimensioni predefinite della finestra

# Frame per centrare gli elementi
main_frame = tk.Frame(root)
main_frame.pack(padx=20, pady=20)

# Sezione per aggiungere nuovo materiale
cod_label = tk.Label(main_frame, text="Codice Materiale")
cod_label.grid(row=0, column=0, pady=5)
cod_entry = tk.Entry(main_frame)
cod_entry.grid(row=0, column=1, pady=5)

descr_label = tk.Label(main_frame, text="Descrizione")
descr_label.grid(row=1, column=0, pady=5)
descr_entry = tk.Entry(main_frame)
descr_entry.grid(row=1, column=1, pady=5)

qta_label = tk.Label(main_frame, text="Quantità")
qta_label.grid(row=2, column=0, pady=5)
qta_entry = tk.Entry(main_frame)
qta_entry.grid(row=2, column=1, pady=5)

add_button = tk.Button(main_frame, text="Aggiungi Materiale", command=inserisci_materiale)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

# Sezione per modificare la quantità di un materiale
modifica_label = tk.Label(main_frame, text="Modifica Quantità (in base al Codice)")
modifica_label.grid(row=4, column=0, columnspan=2, pady=10)

cod_mod_label = tk.Label(main_frame, text="Codice Materiale")
cod_mod_label.grid(row=5, column=0, pady=5)
cod_mod_entry = tk.Entry(main_frame)
cod_mod_entry.grid(row=5, column=1, pady=5)

qta_mod_label = tk.Label(main_frame, text="Nuova Quantità")
qta_mod_label.grid(row=6, column=0, pady=5)
qta_mod_entry = tk.Entry(main_frame)
qta_mod_entry.grid(row=6, column=1, pady=5)

modifica_button = tk.Button(main_frame, text="Modifica Quantità", command=modifica_qta)
modifica_button.grid(row=7, column=0, columnspan=2, pady=10)

# Sezione per visualizzare la lista dei materiali
lista_materiali_label = tk.Label(main_frame, text="Lista Materiali Salvati")
lista_materiali_label.grid(row=8, column=0, columnspan=2, pady=10)

lista_materiali_text = tk.Text(main_frame, height=10, width=50)
lista_materiali_text.grid(row=9, column=0, columnspan=2, pady=5)

aggiorna_button = tk.Button(main_frame, text="Aggiorna Lista", command=aggiorna_lista_materiali)
aggiorna_button.grid(row=10, column=0, columnspan=2, pady=10)

# Avvia l'interfaccia
aggiorna_lista_materiali()
root.mainloop()
