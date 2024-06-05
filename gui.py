import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from database import add_record, get_records, update_record, delete_record, get_sorted_records, get_filtered_records, get_joined_records, get_column_names

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Baza Danych Sklepu Samochodowego")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#ececec")
        self.style.configure("TLabel", background="#ececec", font=('Arial', 12))
        self.style.configure("TButton", font=('Arial', 12), padding=5)
        self.style.configure("TEntry", font=('Arial', 12))
        self.style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))

        self.db_path = filedialog.askopenfilename(title="Wybierz plik bazy danych", filetypes=[("SQLite files", "*.sqlite *.db")])
        if not self.db_path:
            messagebox.showerror("Błąd", "Musisz wybrać plik bazy danych, aby kontynuować.")
            root.destroy()
            return

        self.conn = sqlite3.connect(self.db_path)
        self.create_widgets()
        self.configure_grid()
        self.open_add_record_window()

    def on_closing(self):
        self.root.destroy()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.left_frame = ttk.Frame(self.frame)
        self.left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.right_frame = ttk.Frame(self.frame)
        self.right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.table_label = ttk.Label(self.right_frame, text="Wybierz tabelę")
        self.table_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.table_name = tk.StringVar()
        self.table_menu = ttk.OptionMenu(self.right_frame, self.table_name, '', *self.get_tables(), command=self.load_records)
        self.table_menu.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.records_label = ttk.Label(self.left_frame, text="Rekordy:")
        self.records_label.grid(row=0, column=0, pady=(0, 10))

        self.records_tree = ttk.Treeview(self.left_frame, show='headings')
        self.records_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.records_tree.bind('<Double-1>', self.on_edit_record)

        self.add_button = ttk.Button(self.right_frame, text="Dodaj", command=self.open_add_record_window)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.delete_button = ttk.Button(self.right_frame, text="Usuń", command=self.delete_record)
        self.delete_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.export_button = ttk.Button(self.right_frame, text="Eksportuj do CSV", command=self.export_to_csv)
        self.export_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.import_button = ttk.Button(self.right_frame, text="Importuj z CSV", command=self.import_from_csv)
        self.import_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.sort_column = tk.StringVar(value="rowid")
        self.sort_order = tk.StringVar(value="ASC")

        self.sort_column_menu = ttk.OptionMenu(self.right_frame, self.sort_column, "rowid")
        self.sort_column_menu.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

        self.sort_order_menu = ttk.OptionMenu(self.right_frame, self.sort_order, "ASC", "ASC", "DESC")
        self.sort_order_menu.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        self.sort_button = ttk.Button(self.right_frame, text="Sortuj", command=self.sort_records)
        self.sort_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.filter_column = tk.StringVar(value="")
        self.filter_value = tk.StringVar()

        self.filter_column_menu = ttk.OptionMenu(self.right_frame, self.filter_column, "")
        self.filter_column_menu.grid(row=8, column=0, padx=5, pady=5, sticky="ew")

        self.filter_entry = ttk.Entry(self.right_frame, textvariable=self.filter_value)
        self.filter_entry.grid(row=8, column=1, padx=5, pady=5, sticky="ew")
        self.filter_entry.bind("<KeyRelease>", lambda event: self.filter_records())

        self.filter_button = ttk.Button(self.right_frame, text="Filtruj", command=self.filter_records)
        self.filter_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.joined_records_button = ttk.Button(self.right_frame, text="Pokaż połączone rekordy", command=self.show_joined_records)
        self.joined_records_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def open_add_record_window(self):
        table = self.table_name.get()
        if not table:
            messagebox.showerror("Powiadomienie", "Najpierw wybierz tabelę.")
            return
        columns = get_column_names(self.db_path, table)[1:]  # Skip the ID column

        add_window = tk.Toplevel(self.root)
        add_window.title("Dodaj rekord")
        add_window.configure(background="#ececec")

        entries = []
        for idx, column in enumerate(columns):
            label = ttk.Label(add_window, text=column)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky="ew")
            entry = ttk.Entry(add_window)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="ew")
            entries.append(entry)

        def add_record_to_db():
            data = [entry.get() for entry in entries]
            add_record(self.db_path, table, columns, data)
            self.load_records()
            add_window.destroy()

        save_button = ttk.Button(add_window, text="Dodaj", command=add_record_to_db)
        save_button.grid(row=len(columns), column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def load_records(self, *args):
        table = self.table_name.get()
        if not table:
            return

        self.records_tree.delete(*self.records_tree.get_children())

        columns = get_column_names(self.db_path, table)
        self.records_tree["columns"] = columns
        for col in columns:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, stretch=tk.YES)

        records = get_records(self.db_path, table)
        for record in records:
            self.records_tree.insert("", tk.END, values=record)

        self.sort_column_menu.set_menu(*columns)
        self.filter_column_menu.set_menu(*columns)

    def delete_record(self):
        selected_item = self.records_tree.selection()[0]
        record_id = self.records_tree.item(selected_item)['values'][0]
        table = self.table_name.get()
        delete_record(self.db_path, table, record_id)
        self.load_records()

    def on_edit_record(self, event):
        selected_item = self.records_tree.selection()[0]
        record_id = self.records_tree.item(selected_item)['values'][0]
        table = self.table_name.get()

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edytuj rekord")
        edit_window.configure(background="#ececec")

        columns = get_column_names(self.db_path, table)[1:]
        entries = []

        for idx, column in enumerate(columns):
            label = ttk.Label(edit_window, text=column)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky="ew")
            entry = ttk.Entry(edit_window)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="ew")
            entries.append(entry)

        record = get_records(self.db_path, table)
        record_data = [r for r in record if r[0] == record_id][0][1:]

        for entry, data in zip(entries, record_data):
            entry.insert(0, data)

        def save_edit():
            new_data = [entry.get() for entry in entries]
            update_record(self.db_path, table, record_id, columns, new_data)
            self.load_records()
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Zapisz", command=save_edit)
        save_button.grid(row=len(columns), column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def sort_records(self):
        table = self.table_name.get()
        column = self.sort_column.get()
        order = self.sort_order.get()
        records = get_sorted_records(self.db_path, table, column, order)

        self.records_tree.delete(*self.records_tree.get_children())
        for record in records:
            self.records_tree.insert("", tk.END, values=record)

    def filter_records(self):
        table = self.table_name.get()
        column = self.filter_column.get()
        value = self.filter_value.get()
        records = get_filtered_records(self.db_path, table, column, value)

        self.records_tree.delete(*self.records_tree.get_children())
        for record in records:
            self.records_tree.insert("", tk.END, values=record)

    def show_joined_records(self):
        records = get_joined_records(self.db_path)
        self.records_tree.delete(*self.records_tree.get_children())
        self.records_tree["columns"] = ("ID", "Imię klienta", "Nazwisko klienta", "Marka samochodu", "Model samochodu", "Imię sprzedawcy", "Nazwisko sprzedawcy", "Data sprzedaży")
        for col in self.records_tree["columns"]:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, stretch=tk.YES)

        for record in records:
            self.records_tree.insert("", tk.END, values=record)

    def export_to_csv(self):
        table = self.table_name.get()
        if not table:
            messagebox.showerror("Błąd", "Najpierw wybierz tabelę.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        records = get_records(self.db_path, table)
        columns = get_column_names(self.db_path, table)

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            writer.writerows(records)

    def import_from_csv(self):
        table = self.table_name.get()
        if not table:
            messagebox.showerror("Błąd", "Najpierw wybierz tabelę.")
            return

        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            columns = next(reader)
            for row in reader:
                add_record(self.db_path, table, columns[1:], row[1:])  # Skip ID column

        self.load_records()

    def get_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables

    def configure_grid(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(1, weight=1)
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.columnconfigure(1, weight=1)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
