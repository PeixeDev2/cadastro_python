import tkinter as tk
from tkinter import messagebox
import sqlite3


conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")
conn.commit()


def adicionar_usuario():
    nome = entry_nome.get()
    email = entry_email.get()

    if nome and email:
        try:
            cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
            conn.commit()
            entry_nome.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            listar_usuarios()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Email já cadastrado!")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")


def listar_usuarios():
    listbox_usuarios.delete(0, tk.END)
    cursor.execute("SELECT id, nome, email FROM usuarios")
    for user in cursor.fetchall():
        listbox_usuarios.insert(tk.END, f"{user[0]} - {user[1]} ({user[2]})")


def excluir_usuario():
    try:
        selecionado = listbox_usuarios.get(listbox_usuarios.curselection())
        user_id = selecionado.split(" - ")[0]
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
        conn.commit()
        listar_usuarios()
        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
    except:
        messagebox.showwarning("Atenção", "Selecione um usuário para excluir!")


root = tk.Tk()
root.title("Cadastro de Usuários")
root.geometry("400x400")


tk.Label(root, text="Nome:").pack()
entry_nome = tk.Entry(root)
entry_nome.pack()

tk.Label(root, text="Email:").pack()
entry_email = tk.Entry(root)
entry_email.pack()

tk.Button(root, text="Adicionar", command=adicionar_usuario).pack()
listbox_usuarios = tk.Listbox(root)
listbox_usuarios.pack(expand=True, fill=tk.BOTH)

tk.Button(root, text="Excluir", command=excluir_usuario).pack()


listar_usuarios()


tk.mainloop()


conn.close()