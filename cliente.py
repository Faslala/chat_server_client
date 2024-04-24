import socket
import threading
import tkinter
from tkinter import *
from tkinter import simpledialog

class Chat:
    def __init__(self):
        HOST = 'localhost'
        PORT = 55557
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client.connect((HOST, PORT))
        
        # self.login = tkinter.Tk()
        # self.login.withdraw()
        self.login = Tk()
        self.login.withdraw()
        
        self.janela_carregada = False
        self.ativo = True
        
        self.nome = simpledialog.askstring('Nome', 'Digite seu nome!', parent=self.login)
        self.sala = simpledialog.askstring('Sala', 'Digite a sala que deseja entrar!', parent=self.login)
        
        thread = threading.Thread(target=self.conecta)
        thread.start()

        self.janela()
    
    def janela(self):
        self.root = tkinter.Tk()
        self.root.geometry('800x800')
        self.root.title('Chat')
        
        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.01, width=700, height=600)
        
        self.envia_mensagem = Entry(self.root)
        self.envia_mensagem.place(relx=0.05, rely=0.9, width=600, height=30)
        # self.envia_mensagem.bind('<Return>', self.enviarMensagem)
        
        self.btn_enviar = Button(self.root, text='Enviar', command=self.enviarMensagem)
        self.btn_enviar.place(relx=0.75, rely=0.9, width=100, height=30)
        
        self.root.protocol('WM_DELETE_WINDOW', self.fechar)
                
        self.root.mainloop()
        
    def fechar(self):
        # self.ativo = False
        self.root.destroy()
        self.client.close()
        
    
    def conecta(self):
        # while self.ativo:
        #     mensagem = self.client.recv(1024).decode()
        #     self.caixa_texto.insert('end', mensagem+'\n')
        while True:
            recebido = self.client.recv(1024)
            if recebido == 'Sala que eu quero entrar':
                self.client.send(self.sala.encode())
                self.client.send(self.nome.encode())
            else:
                try:
                    self.caixa_texto.insert('end', recebido.enconde())
                except:
                    pass
    
    def enviarMensagem(self):
        mensagem = self.envia_mensagem.get()
        self.client.send(mensagem.encode())
        # self.envia_mensagem.delete(0, 'end')
        
    

chat = Chat()

# o meu texto nao envia