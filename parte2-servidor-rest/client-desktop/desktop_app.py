import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json

SERVER_URL = "http://localhost:5000"

class GhibliApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Studio Ghibli - Sistema de Favoritos")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f0f0')
        
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Criar abas
        self.create_people_tab()
        self.create_favorites_tab()
        self.create_details_tab()
        
        # Carregar dados iniciais
        self.load_people()
        self.load_favorites()
    
    def create_people_tab(self):
        """Aba de personagens"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='📋 Personagens')
        
        # Título
        title = tk.Label(tab, text="Todos os Personagens", 
                        font=('Arial', 16, 'bold'), bg='white')
        title.pack(fill='x', pady=10)
        
        # Frame para lista
        frame = tk.Frame(tab, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        # Listbox
        self.people_listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set,
                                         font=('Arial', 11), height=15)
        self.people_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.people_listbox.yview)
        
        # Bind duplo clique
        self.people_listbox.bind('<Double-Button-1>', self.show_person_details)
        
        # Botões
        btn_frame = tk.Frame(tab, bg='white')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        btn_details = tk.Button(btn_frame, text="Ver Detalhes", 
                               command=self.show_person_details,
                               bg='#667eea', fg='white', font=('Arial', 10, 'bold'),
                               padx=20, pady=8)
        btn_details.pack(side='left', padx=5)
        
        btn_add_fav = tk.Button(btn_frame, text="⭐ Adicionar aos Favoritos", 
                               command=self.add_to_favorites,
                               bg='#48bb78', fg='white', font=('Arial', 10, 'bold'),
                               padx=20, pady=8)
        btn_add_fav.pack(side='left', padx=5)
        
        btn_refresh = tk.Button(btn_frame, text="🔄 Atualizar", 
                               command=self.load_people,
                               bg='#4299e1', fg='white', font=('Arial', 10, 'bold'),
                               padx=20, pady=8)
        btn_refresh.pack(side='right', padx=5)
    
    def create_favorites_tab(self):
        """Aba de favoritos"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='⭐ Favoritos')
        
        # Título
        title = tk.Label(tab, text="Meus Favoritos", 
                        font=('Arial', 16, 'bold'), bg='white')
        title.pack(fill='x', pady=10)
        
        # Frame para lista
        frame = tk.Frame(tab, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        # Listbox
        self.favorites_listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set,
                                           font=('Arial', 11), height=15)
        self.favorites_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.favorites_listbox.yview)
        
        # Botões
        btn_frame = tk.Frame(tab, bg='white')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        btn_remove = tk.Button(btn_frame, text="🗑️ Remover dos Favoritos", 
                              command=self.remove_from_favorites,
                              bg='#f56565', fg='white', font=('Arial', 10, 'bold'),
                              padx=20, pady=8)
        btn_remove.pack(side='left', padx=5)
        
        btn_refresh = tk.Button(btn_frame, text="🔄 Atualizar", 
                               command=self.load_favorites,
                               bg='#4299e1', fg='white', font=('Arial', 10, 'bold'),
                               padx=20, pady=8)
        btn_refresh.pack(side='right', padx=5)
    
    def create_details_tab(self):
        """Aba de detalhes"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='📄 Detalhes')
        
        # Título
        title = tk.Label(tab, text="Detalhes do Personagem", 
                        font=('Arial', 16, 'bold'), bg='white')
        title.pack(fill='x', pady=10)
        
        # Text widget para detalhes
        self.details_text = scrolledtext.ScrolledText(tab, wrap=tk.WORD, 
                                                      font=('Arial', 11),
                                                      padx=10, pady=10)
        self.details_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_people(self):
        """Carregar personagens da API"""
        try:
            response = requests.get(f"{SERVER_URL}/people")
            self.people_data = response.json()
            
            self.people_listbox.delete(0, tk.END)
            for person in self.people_data:
                display_text = f"{person['name']} - {person['gender']} - {person.get('age', 'N/A')}"
                self.people_listbox.insert(tk.END, display_text)
            
            messagebox.showinfo("Sucesso", f"{len(self.people_data)} personagens carregados!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar personagens: {str(e)}")
    
    def load_favorites(self):
        """Carregar favoritos da API"""
        try:
            response = requests.get(f"{SERVER_URL}/favorites")
            self.favorites_data = response.json()
            
            self.favorites_listbox.delete(0, tk.END)
            for fav in self.favorites_data:
                display_text = f"{fav['name']} - {fav['gender']} - {fav.get('age', 'N/A')}"
                self.favorites_listbox.insert(tk.END, display_text)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar favoritos: {str(e)}")
    
    def show_person_details(self, event=None):
        """Mostrar detalhes do personagem selecionado"""
        selection = self.people_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um personagem!")
            return
        
        index = selection[0]
        person = self.people_data[index]
        
        # Mudar para aba de detalhes
        self.notebook.select(2)
        
        # Limpar e mostrar detalhes
        self.details_text.delete(1.0, tk.END)
        
        details = f"""
Nome: {person['name']}
=====================================

ID: {person['id']}
Gênero: {person['gender']}
Idade: {person.get('age', 'Desconhecida')}
Cor dos Olhos: {person.get('eye_color', 'N/A')}
Cor do Cabelo: {person.get('hair_color', 'N/A')}
Espécie: {person.get('species', 'N/A')}

Filmes: {len(person.get('films', []))} filme(s)

URL: {person.get('url', 'N/A')}
        """
        
        self.details_text.insert(1.0, details)
    
    def add_to_favorites(self):
        """Adicionar personagem aos favoritos"""
        selection = self.people_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um personagem!")
            return
        
        index = selection[0]
        person = self.people_data[index]
        
        try:
            response = requests.post(
                f"{SERVER_URL}/favorites",
                json={"person_id": person['id']}
            )
            
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", f"{person['name']} adicionado aos favoritos!")
                self.load_favorites()
            else:
                error_msg = response.json().get('error', 'Erro desconhecido')
                messagebox.showerror("Erro", error_msg)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar favorito: {str(e)}")
    
    def remove_from_favorites(self):
        """Remover personagem dos favoritos"""
        selection = self.favorites_listbox.curselection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um favorito!")
            return
        
        index = selection[0]
        favorite = self.favorites_data[index]
        
        try:
            response = requests.delete(f"{SERVER_URL}/favorites/{favorite['id']}")
            
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", f"{favorite['name']} removido dos favoritos!")
                self.load_favorites()
            else:
                error_msg = response.json().get('error', 'Erro desconhecido')
                messagebox.showerror("Erro", error_msg)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover favorito: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = GhibliApp(root)
    root.mainloop()
