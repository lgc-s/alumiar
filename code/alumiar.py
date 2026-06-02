usuarios = {}
from re import fullmatch
id = 1

def listar_usuarios():
    for id, usuario in usuarios.items():
        print(f"ID: {id}\nNome: {usuario["nome"]}\nEmail: {usuario["email"]}")

def validar_email(email):
    
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,7}$'
    if fullmatch(regex,email):
        return True
    else:
        return False

def verificar_email_existente(email):

    for usuario in usuarios.values():
        if usuario["email"] == email:
            return True
        else:
            return False

def cadastrar():
    global id

    print("\n==== CADASTRO ====\n")

    nome = input("- Nome: ").strip().title()
    idade = (input("- Idade: ")).replace(" ","")
    tipo_artesanato = input("-Tipo de Artesanato: ").strip().title()
    bairro  = input("- Bairro: ").strip().title()
    telefone = (input("- Telefone: ")).replace(" ","")
    formalizacao = input("- Formalizada? (S/N): ").strip().upper()

    while formalizacao not in "SN":
        formalizacao = input("Resposta Inválida, tente novamente...\n- Formalizada? (S/N): ").strip().upper()

    email = input("- Email: ").strip()
    while validar_email(email) == False:
        email = input("\nEmail inválido, tente novamente...\n- Email: ")
    while verificar_email_existente(email) == True:
        email = input("\nEmail já cadastrado, tente novamente...\n- Email: ")

    senha = input("- Senha: ").strip()

    usuarios[id] = {
        "nome": nome,
        "idade": idade,
        "tipo_artesanato": tipo_artesanato,
        "bairro": bairro,
        "telefone": telefone,
        "formalizacao": formalizacao,
        "email": email,
        "senha": senha
    }

    id += 1

def menu():
    while True:

        opcao = input("""\n======== MENU ========
1 - Cadastrar
2 - Login
3 - Listar Usuários
0 - Sair
            
Escolha: """).strip()
        

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            print("login")
        elif opcao == "3":
            listar_usuarios()
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")

menu()
