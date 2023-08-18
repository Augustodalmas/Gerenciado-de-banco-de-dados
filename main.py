import tkinter as tk
from tkinter import messagebox
import sqlite3

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=Interface Gráfica=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


class ProductManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Produtos")
        self.root.geometry("800x600")
        root.configure(bg="lightblue")

        self.db_connection = sqlite3.connect("products.db")
        self.create_table()

        frame_botao = tk.Frame(root)
        frame_botao.pack(side="left", padx=10, pady=10)

        self.add_button = tk.Button(
            frame_botao, text="Adicionar Produto", command=self.Adicionar_produto, bg="black", fg="white", width=20, height=2)
        self.add_button.pack(fill='x', expand=True)
        self.add_button = tk.Button(
            frame_botao, text="Atualizar produto", command=self.Atualizar_produto, bg="black", fg="white", height=2)
        self.add_button.pack(fill='x', expand=True)

        self.add_button = tk.Button(
            frame_botao, text="Remover produto", command=self.remover_produto, bg="black", fg="white", height=2)
        self.add_button.pack(fill='x', expand=True)

        frame_tabela = tk.Frame(root)
        frame_tabela.pack(side="right", padx=1, pady=1)

        self.label_id = tk.Label(
            frame_tabela, text="ID - NOME - PREÇO")
        self.label_id.pack()

        self.product_listbox = tk.Listbox(
            frame_tabela, width=80, height=40, bg="#e8e8e8")
        self.product_listbox.pack(side="right", padx=10, pady=10)

        self.update_product_listbox()

    def Adicionar_produto(self):
        newWindow = tk.Toplevel(root)
        newWindow.title("Adicionar Produto")
        newWindow.geometry("200x200")

        self.label_name = tk.Label(
            newWindow, text="Nome do Produto:")
        self.label_name.pack()

        self.entry_name = tk.Entry(newWindow)
        self.entry_name.pack()

        self.label_price = tk.Label(
            newWindow, text="Preço")
        self.label_price.pack()

        self.entry_price = tk.Entry(newWindow)
        self.entry_price.pack()

        self.button = tk.Button(
            newWindow, text='Adicionar', command=self.add_product)
        self.button.pack()

    def Atualizar_produto(self):
        newWindow = tk.Toplevel(root)
        newWindow.title("New Window")
        newWindow.geometry("200x200")

        self.label_name = tk.Label(
            newWindow, text="Nome do Produto:")
        self.label_name.pack()

        self.entry_name = tk.Entry(newWindow)
        self.entry_name.pack()

        self.label_price = tk.Label(
            newWindow, text="preço")
        self.label_price.pack()

        self.entry_price = tk.Entry(newWindow)
        self.entry_price.pack()

        self.label_id = tk.Label(
            newWindow, text="ID")
        self.label_id.pack()

        self.entry_id = tk.Entry(newWindow)
        self.entry_id.pack()

        self.button = tk.Button(
            newWindow, text='Adicionar', command=self.update_product)
        self.button.pack()

    def remover_produto(self):
        newWindow = tk.Toplevel(root)
        newWindow.title("New Window")
        newWindow.geometry("200x200")

        self.label_id = tk.Label(
            newWindow, text="ID")
        self.label_id.pack()

        self.entry_id = tk.Entry(newWindow)
        self.entry_id.pack()

        self.button = tk.Button(
            newWindow, text='Remover', command=self.remove_product)
        self.button.pack()

    def show_message(self):
        messagebox.showinfo("Mensagem", "Ação realizada com sucesso!")

    def show_erro(self):
        messagebox.showinfo("Mensagem", "Foi encontrado um erro!")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=Criação da tabela=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL
        )
        """
        self.db_connection.execute(query)
        self.db_connection.commit()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=Adição de produtos=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


    def add_product(self):
        try:
            name = str(self.entry_name.get())
            name = name.title()
            price = str(self.entry_price.get())
            price = price.title()

            query = "INSERT INTO products (name, price)\
                    VALUES (?, ?)"
            self.db_connection.execute(query, (name, price))
            self.db_connection.commit()

            self.entry_name.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)

            self.update_product_listbox()
            self.show_message()
        except:
            self.show_erro()

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=Atualização de produtos=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def update_product(self):
        try:
            new_name = str(self.entry_name.get())
            new_name = new_name.title()
            new_price = str(self.entry_price.get())
            new_price = new_price.title()
            id = self.entry_id.get()

            atuais = "SELECT name, price FROM products WHERE id = ?"
            curso = self.db_connection.execute(atuais, (id))
            name_atual, preco_atual = curso.fetchone()

            if new_name == "":
                new_name = name_atual
            if new_price == "":
                new_price = preco_atual

            query = "UPDATE products\
                        SET name = ?,\
                        price = ?\
                            WHERE id = ?"

            self.db_connection.execute(query, (new_name, new_price, id))
            self.db_connection.commit()

            self.entry_name.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.entry_id.delete(0, tk.END)

            self.update_product_listbox()
            self.show_message()
        except:
            self.show_erro()

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=Remover produto=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def remove_product(self):
        try:
            id = self.entry_id.get()

            comando = "DELETE FROM products WHERE id = ?"

            self.db_connection.execute(comando, (id))
            self.db_connection.commit()

            self.entry_id.delete(0, tk.END)

            self.update_product_listbox()
            self.show_message()
        except:
            self.show_erro()

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=Mostrar produtos na tabela=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    def update_product_listbox(self):
        self.product_listbox.delete(0, tk.END)
        products = self.get_products()
        for product in products:
            self.product_listbox.insert(
                tk.END, f"{str(product[0]).rjust(3)} | {str(product[1]).ljust(20)} | R${str(product[2]).ljust(10)}")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=Pegar produtos=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


    def get_products(self):
        query = "SELECT * FROM products"
        cursor = self.db_connection.execute(query)
        return cursor.fetchall()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=Inicializador=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
if __name__ == "__main__":
    root = tk.Tk()
    app = ProductManagementApp(root)
    root.mainloop()
