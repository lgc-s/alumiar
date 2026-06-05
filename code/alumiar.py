# ============================================================
# CRUD de Cadastro de Artesãs
# Gerencia o cadastro, listagem e login de usuárias artesãs,
# com validações de idade, telefone e e-mail via regex.
# ============================================================

from re import fullmatch

# Dicionário principal que armazena todos os usuários cadastrados.
# Chave: ID inteiro | Valor: dicionário com os dados do usuário
usuarios = {}

# Contador global de ID, incrementado a cada novo cadastro
id = 1

# Variável global que armazena o ID registrado durante após login
id_logado = None

def listar_usuarios():
    """Exibe no terminal todos os usuários cadastrados com ID, nome e e-mail."""
    for id, usuario in usuarios.items():
        print(f"ID: {id}\nNome: {usuario["nome"]}\nEmail: {usuario["email"]}")


def validar_telefone(telefone):
    """
    Valida se o telefone informado é um celular brasileiro válido.

    Formato esperado: DDD (2 dígitos) + 9 + 8 dígitos = 11 dígitos no total.
    Exemplo válido: 81999999999

    Args:
        telefone (str): Número de telefone contendo apenas dígitos.

    Returns:
        bool: True se válido, False caso contrário.
    """
    regex = r'^\d{2}9\d{8}$'
    if fullmatch(regex,telefone):
        return True
    else:
        return False


def validar_idade(idade):
    """
    Valida se a idade informada está no intervalo permitido (1 a 120).

    A regex cobre quatro faixas:
        - [1-9]       → 1 a 9
        - [1-9][0-9]  → 10 a 99
        - 1[0-1][0-9] → 100 a 119
        - 120         → exatamente 120

    Args:
        idade (str): Idade como string contendo apenas dígitos.

    Returns:
        bool: True se válida, False caso contrário.
    """
    regex = r'^(1[0-1][0-9]|120|[1-9][0-9]|[1-9])$'
    if fullmatch(regex,idade):
        return True
    else:
        return False


def validar_email(email):
    """
    Valida se o e-mail informado possui um formato válido.

    Formato esperado: usuario@dominio.extensao
    A extensão pode ter entre 2 e 7 caracteres (ex: .com, .com.br).

    Args:
        email (str): Endereço de e-mail a ser validado.

    Returns:
        bool: True se válido, False caso contrário.
    """
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,7}$'
    if fullmatch(regex,email):
        return True
    else:
        return False


def verificar_email_existente(email):
    """
    Verifica se um e-mail já está vinculado a algum usuário cadastrado.

    Percorre todos os usuários no dicionário e compara os e-mails,
    impedindo duplicatas no sistema.

    Args:
        email (str): E-mail a ser verificado.

    Returns:
        bool: True se o e-mail já existe, False caso contrário.
    """
    for usuario in usuarios.values():
        if usuario["email"] == email:
            return True
        else:
            return False


def cadastrar():
    """
    Coleta e valida os dados do usuário via input, então salva no dicionário.

    Campos coletados:
        - Nome (formatado com title case)
        - Idade (validada por regex, espaços removidos)
        - Tipo de artesanato
        - Bairro
        - Telefone (validado por regex, espaços removidos)
        - Formalização (S/N)
        - E-mail (validado por regex e unicidade)
        - Senha

    O ID é incrementado globalmente a cada cadastro realizado.
    """
    global id

    print("\n==== CADASTRO ====\n")

    nome = input("- Nome: ").strip().title()

    idade = (input("- Idade: ")).replace(" ","")

    # Rejeita a entrada enquanto a idade não passar na validação
    while validar_idade(idade) == False:
        idade = (input("Idade Inválida, tente novamente...\n - Idade: ")).replace(" ","")

    tipo_artesanato = input("- Tipo de Artesanato: ").strip().title()

    bairro  = input("- Bairro: ").strip().title()

    telefone = (input("- Telefone (Ex.: 81999999999): ")).replace(" ","")

    # Rejeita a entrada enquanto o telefone não passar na validação
    while validar_telefone(telefone) == False:
        telefone = (input("Telefone Inválido, tente novamente...\n- Telefone (Ex.: 81999999999): ")).replace(" ","")

    formalizacao = input("- Formalizada? (S/N): ").strip().upper()

    # Aceita apenas "S" ou "N" como resposta válida
    while formalizacao not in "SN":
        formalizacao = input("Resposta Inválida, tente novamente...\n- Formalizada? (S/N): ").strip().upper()

    email = input("- Email: ").strip()

    # Loop para validar o email
    while True:
        if not validar_email(email):
            email = input("\nEmail inválido, tente novamente...\n- Email: ")
        elif verificar_email_existente(email):
            email = input("\nEmail já cadastrado, tente novamente...\n- Email: ")
        else:
            break  # Email válido E disponível → sai do loop

    senha = input("- Senha: ").strip()

    # Salva todos os dados do usuário usando o ID atual como chave
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

    # Avança o contador para o próximo cadastro
    id += 1

def menu_dev():
    while True:
        opcao = input("""\n============================================================

                ALUMIAR APP (Menu Administrador)

============================================================
                  
1 - Usuários
2 - Eventos
0 - Sair

Escolha: """).strip()
    
        if opcao == "1":
            print("Gerenciamento de Usuários")
        elif opcao == "2":
            print("Gerenciamento de Eventos")
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")

def menu_user():
    print("menu_usuario")

def login():

    global id_logado

    while True:
        
        print("\n==== Login ====\n")
        email = input("- Email: ").strip()
        senha = input("- Senha: ").strip()

        if email == "ADM" and senha == "123":
            menu_dev()
        else:
            for id, usuario in usuarios.items():
                if usuario["email"] == email and usuario["senha"] == senha:
                    id_logado = id
                    menu_user()
                    return
        print("Email ou Senha inválidos, tente novamente...")
        
def menu_inicial():
    """
    Exibe o menu principal em loop e direciona para as funcionalidades do sistema.

    Opções disponíveis:
        1 - Cadastrar novo usuário
        2 - Login
        0 - Encerrar o programa
    """
    while True:

        opcao = input("""\n============================================================

                ALUMIAR APP (Menu Inicial)

============================================================

1 - Cadastro
2 - Login
0 - Sair
            
Escolha: """).strip()
        

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            login()
        elif opcao == "0":
            break  # Encerra o loop e finaliza o programa
        else:
            print("Comando inválido, tente novamente...")

# Ponto de entrada do programa
menu_inicial()
