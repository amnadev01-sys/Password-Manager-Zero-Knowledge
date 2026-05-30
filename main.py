from vault import create_vault, load_vault, save_vault
from strength import check_strength
from breach import check_breach
import os
import tkinter as tk
import pyperclip
from tkinter import messagebox, simpledialog

class VaultGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("My Vault")
        self.root.geometry("350x450")
        self.root.configure(bg="#2c3e50")
        self.vault, self.key, self.salt = {}, None, None
        self.setup_auth()

    def setup_auth(self):
        for widget in self.root.winfo_children(): widget.destroy()
        exists = os.path.exists("vault.json")
        tk.Label(self.root, text="Create Vault" if not exists else "Login", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=(50, 20))
        self.entry = tk.Entry(self.root, show="*", font=("Helvetica", 12), bd=0, highlightthickness=2, highlightbackground="#34495e", highlightcolor="#3498db")
        self.entry.pack(pady=5)
        btn_text = "Initialize" if not exists else "Unlock"
        cmd = self.init_vault if not exists else self.unlock
        tk.Button(self.root, text=btn_text, command=cmd, bg="#3498db", fg="white", font=("Helvetica", 10, "bold"), relief=tk.FLAT, pady=8, cursor="hand2", activebackground="#2980b9", activeforeground="white").pack(pady=20, padx=50, fill=tk.X)

    def init_vault(self):
        if master := self.entry.get():
            create_vault(master)
            messagebox.showinfo("Vault", "Vault created successfully!")
            self.setup_auth()

    def unlock(self):
        try:
            self.vault, self.key, self.salt = load_vault(self.entry.get())
            self.show_dashboard()
        except Exception:
            messagebox.showerror("Error", "Incorrect Master Password")

    def show_dashboard(self):
        for widget in self.root.winfo_children(): widget.destroy()
        tk.Label(self.root, text="Stored Credentials", font=("Helvetica", 12, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=15)
        self.listbox = tk.Listbox(self.root, exportselection=False, bg="#34495e", fg="white", font=("Helvetica", 10), borderwidth=0, highlightthickness=0, selectbackground="#1abc9c")
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.update_list()

        frame = tk.Frame(self.root, bg="#2c3e50")
        frame.pack(pady=20)
        tk.Button(frame, text="Add New", command=self.add_password, bg="#27ae60", fg="white", relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="View Info", command=self.view_password, bg="#3498db", fg="white", relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Delete", command=self.delete_password, bg="#e74c3c", fg="white", relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(
            frame,
            text="Auto Fill",
            command=self.auto_fill,
            bg="#f39c12",
            fg="white",
            relief=tk.FLAT,
            padx=10
        ).pack(side=tk.LEFT, padx=5)

    def delete_password(self):
        selection = self.listbox.curselection()
        if selection:
            site = self.listbox.get(selection[0])
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the credentials for {site}?"):
                del self.vault[site]
                save_vault(self.vault, self.key, self.salt)
                self.update_list()
        else:
            messagebox.showwarning("Selection Error", "Please select a site from the list first.")

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for site in self.vault:
            self.listbox.insert(tk.END, site)

    def add_password(self):
        site = simpledialog.askstring("Input", "Site Name:")
        user = simpledialog.askstring("Input", "Username:")
        pwd = simpledialog.askstring("Input", "Password:", show="*")
        
        if site and user and pwd:
            strength = check_strength(pwd)
            leaked = check_breach(pwd)
            msg = f"Strength: {strength}"
            if leaked: msg += "\n\n⚠️ WARNING: This password has been leaked!"
            messagebox.showwarning("Security Check", msg) if leaked else messagebox.showinfo("Security Check", msg)
            
            self.vault[site] = {"username": user, "password": pwd}
            save_vault(self.vault, self.key, self.salt)
            self.update_list()

    def view_password(self):
        selection = self.listbox.curselection()
        if selection:
            site = self.listbox.get(selection[0])
            data = self.vault[site]
            messagebox.showinfo(site, f"Username: {data['username']}\nPassword: {data['password']}")
        else:
            messagebox.showwarning("Selection Error", "Please select a site from the list first.")

    def auto_fill(self):
        selection = self.listbox.curselection()

        if selection:
            site = self.listbox.get(selection[0])
            data = self.vault[site]

            credentials = (
                f"Username: {data['username']}\n"
                f"Password: {data['password']}"
        )

            pyperclip.copy(credentials)

            messagebox.showinfo(
                "Auto Fill",
                "Credentials copied to clipboard successfully!"
        )

        else:
            messagebox.showwarning(
                "Selection Error",
                "Please select a site first."
        )     

def main():
    root = tk.Tk()
    VaultGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()