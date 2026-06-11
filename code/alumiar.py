# ============================================================
# CRUD de Cadastro de Artesãs
# Gerencia o cadastro, listagem e login de usuárias artesãs,
# com validações de idade, telefone e e-mail via regex.
# ============================================================

from re import fullmatch
import json
import os
from datetime import datetime, date

# Dicionário principal que armazena todos os usuários cadastrados.
# Chave: ID inteiro | Valor: dicionário com os dados do usuário
usuarios = {}
cursos = []
eventos = []

# Contador global de ID, incrementado a cada novo cadastro
id = 1

# Variável global que armazena o ID registrado durante após login
id_logado = None

def salvar_dados():
    with open('dados_usuarios.json', 'w', encoding='utf-8') as f:
        json.dump({"id": id, "usuarios": usuarios}, f, ensure_ascii=False, indent=2)

    with open('dados_cursos.json', 'w', encoding='utf-8') as f:
        json.dump(cursos, f, ensure_ascii=False, indent=2)

    with open('dados_eventos.json', 'w', encoding='utf-8') as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2)

    print("\nDados salvos com sucesso!")


def carregar_dados():
    global id, usuarios, cursos, eventos

    if os.path.exists('dados_usuarios.json'):
        with open('dados_usuarios.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
            id = dados["id"]
            usuarios = {int(k): v for k, v in dados["usuarios"].items()}

    if os.path.exists('dados_cursos.json'):
        with open('dados_cursos.json', 'r', encoding='utf-8') as f:
            cursos = json.load(f)

    if os.path.exists('dados_eventos.json'):
        with open('dados_eventos.json', 'r', encoding='utf-8') as f:
            eventos = json.load(f)

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
    if fullmatch(regex, telefone):
        return True
    else:
        return False


def validar_e_calcular_idade(data_str):
    """
    Valida a data de nascimento (DD/MM/AAAA) e calcula a idade.
    Retorna a idade (int) se for válida (entre 1 e 120 anos), ou False caso contrário.
    """
    try:
        # Tenta converter a string no formato de data brasileira
        data_nascimento = datetime.strptime(data_str, "%d/%m/%Y").date()
        hoje = date.today()  # Pega a data exata de hoje no calendário do PC

        # Cálculo exato da idade considerando o mês e o dia atual
        idade = hoje.year - data_nascimento.year - \
            ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

        # Mantém a sua regra de negócio original (idade entre 1 e 120 anos)
        if 1 <= idade <= 120:
            return idade
        return False
    except ValueError:
        # Se o usuário digitar letras ou uma data inválida (ex: 30/02/2000)
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
    if fullmatch(regex, email):
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

    while True:
        data_nasci_input = input("- Data de Nascimento (DD/MM/AAAA): ").strip()
        idade_calculada = validar_e_calcular_idade(data_nasci_input)

        if idade_calculada is not False:
            break  # Data válida e idade dentro do limite!
        print("Data inválida ou idade fora do permitido (1-120 anos). Tente novamente...\n")

    tipo_artesanato = input("- Tipo de Artesanato: ").strip().title()

    bairro = input("- Bairro: ").strip().title()

    telefone = (input("- Telefone (Ex.: 81999999999): ")).replace(" ", "")

    # Rejeita a entrada enquanto o telefone não passar na validação
    while validar_telefone(telefone) == False:
        telefone = (input(
            "Telefone Inválido, tente novamente...\n- Telefone (Ex.: 81999999999): ")).replace(" ", "")

    formalizacao = input("- Formalizada? (S/N): ").strip().upper()

    # Aceita apenas "S" ou "N" como resposta válida
    while formalizacao not in ("S", "N"):
        formalizacao = input(
            "Resposta Inválida, tente novamente...\n- Formalizada? (S/N): ").strip().upper()

    email = input("- Email: ").strip()

    # Loop para validar o email
    while True:
        if not validar_email(email):
            email = input("\nEmail inválido, tente novamente...\n- Email: ")
        elif verificar_email_existente(email):
            email = input(
                "\nEmail já cadastrado, tente novamente...\n- Email: ")
        else:
            break  # Email válido E disponível → sai do loop

    senha = input("- Senha: ").strip()

    # Salva todos os dados do usuário usando o ID atual como chave
    usuarios[id] = {
        "nome": nome,
        "idade": idade_calculada,
        "tipo_artesanato": tipo_artesanato,
        "bairro": bairro,
        "telefone": telefone,
        "formalizacao": formalizacao,
        "email": email,
        "senha": senha
    }

    # Avança o contador para o próximo cadastro
    id += 1


def listar_usuarios():
    """Exibe no terminal todos os usuários cadastrados com ID, nome e e-mail."""
    if not usuarios:
        print("\n Nenhum usuário cadastrado.")
        return
    for id, usuario in usuarios.items():
        print(f"""
ID: {id}
  Nome:        {usuario['nome']}
  Idade:       {usuario['idade']}
  Artesanato:  {usuario['tipo_artesanato']}
  Bairro:      {usuario['bairro']}
  Telefone:    {usuario['telefone']}
  Formalizada: {usuario['formalizacao']}
  Email:       {usuario['email']}""")


def editar_usuario():
    """
    Permite ao administrador editar qualquer campo de um usuário pelo ID.
    Pressionar Enter sem digitar nada mantém o valor atual do campo.
    """
    if not usuarios:
        print("\nNenhum usuário cadastrado.")
        return

    listar_usuarios()

    try:
        id_edit = int(input("\nID do usuário a editar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    if id_edit not in usuarios:
        print("Usuário não encontrado.")
        return

    u = usuarios[id_edit]
    print(f"\nEditando '{u['nome']}' — Enter para manter o valor atual.\n")

    # ── Nome ──────────────────────────────────────────────────────────────────
    novo = input(f"- Nome [{u['nome']}]: ").strip()
    if novo:
        u['nome'] = novo.title()

    # ── Idade ─────────────────────────────────────────────────────────────────
    while True:
        novo = input(f"- Idade [{u['idade']}]: ").replace(" ", "")
        if not novo:
            break
        if validar_e_calcular_idade(novo):
            u['idade'] = novo
            break
        print("  Idade inválida, tente novamente...")

    # ── Tipo de artesanato ────────────────────────────────────────────────────
    novo = input(f"- Tipo de Artesanato [{u['tipo_artesanato']}]: ").strip()
    if novo:
        u['tipo_artesanato'] = novo.title()

    # ── Bairro ────────────────────────────────────────────────────────────────
    novo = input(f"- Bairro [{u['bairro']}]: ").strip()
    if novo:
        u['bairro'] = novo.title()

    # ── Telefone ──────────────────────────────────────────────────────────────
    while True:
        novo = input(f"- Telefone [{u['telefone']}]: ").replace(" ", "")
        if not novo:
            break
        if validar_telefone(novo):
            u['telefone'] = novo
            break
        print("  Telefone inválido, tente novamente...")

    # ── Formalização ──────────────────────────────────────────────────────────
    while True:
        novo = input(
            f"- Formalizada? (S/N) [{u['formalizacao']}]: ").strip().upper()
        if not novo:
            break
        if novo in ("S", "N"):
            u['formalizacao'] = novo
            break
        print("  Resposta inválida, tente novamente...")

    # ── Email ─────────────────────────────────────────────────────────────────
    while True:
        novo = input(f"- Email [{u['email']}]: ").strip()
        if not novo:
            break
        if not validar_email(novo):
            print("  Email inválido, tente novamente...")
            continue
        # Verifica duplicata ignorando o próprio usuário
        duplicado = any(
            dados['email'] == novo and uid != id_edit
            for uid, dados in usuarios.items()
        )
        if duplicado:
            print("  Email já cadastrado, tente novamente...")
            continue
        u['email'] = novo
        break

    # ── Senha ─────────────────────────────────────────────────────────────────
    novo = input("- Nova senha (Enter para manter): ").strip()
    if novo:
        u['senha'] = novo

    print(f"\nUsuário '{u['nome']}' atualizado com sucesso!")


def deletar_usuario():
    """
    Remove permanentemente um usuário do dicionário pelo ID,
    após confirmação do administrador.
    """
    if not usuarios:
        print("\nNenhum usuário cadastrado.")
        return

    listar_usuarios()

    try:
        id_del = int(input("\nID do usuário a deletar: ").strip())
    except ValueError:
        print("ID inválido.")
        return

    if id_del not in usuarios:
        print("Usuário não encontrado.")
        return

    nome = usuarios[id_del]['nome']
    confirmacao = input(
        f"\nDeletar '{nome}'? Essa ação é irreversível. (S/N): ").strip().upper()

    if confirmacao == "S":
        del usuarios[id_del]
        print(f"Usuário '{nome}' deletado com sucesso!")
    else:
        print("Operação cancelada.")


def menu_usuarios_adm():
    """Submenu CRUD de usuários acessado pelo administrador."""
    while True:
        opcao = input("""\n============================================================

            ALUMIAR APP (Gerenciamento de Usuários)

============================================================

1 - Listar Usuários
2 - Cadastrar Usuário
3 - Editar Usuário
4 - Deletar Usuário
0 - Voltar

Escolha: """).strip()

        if opcao == "1":
            listar_usuarios()
        elif opcao == "2":
            cadastrar()
        elif opcao == "3":
            editar_usuario()
        elif opcao == "4":
            deletar_usuario()
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")


def cadastrar_curso():

    print("\n=== CADASTRAR CURSO ===")

    # Recebe as informações do curso
    titulo = input("Título do curso: ")
    tutor = input("Tutor responsável: ")
    duracao = input("Duração do curso: ")
    while True:
        try:
            vagas = int(input("Quantidade de vagas: "))
            if vagas <= 0:
                print("A quantidade de vagas deve ser maior que zero...\n")
                continue
            break
        except ValueError:
            print("Quantidade inválida, digite apenas números inteiros...\n")

    # Criação do dicionário que representa um curso
    curso = {
        "titulo": titulo,
        "tutor": tutor,
        "duracao": duracao,
        "vagas": vagas,
        "inscritos": []
    }

    # Adiciona o curso à lista de cursos
    cursos.append(curso)

    print("\nCurso cadastrado com sucesso!")


def listar_cursos():

    print("\n=== CURSOS DISPONÍVEIS ===")

    # Verifica se existem cursos cadastrados
    if not cursos:
        print("\nNenhum curso cadastrado.")
        return

    # Percorre a lista exibindo cada curso
    for n, curso in enumerate(cursos, start=1):

        print(f"\nCurso {n}")
        print(f"Título: {curso['titulo']}")
        print(f"Tutor: {curso['tutor']}")
        print(f"Duração: {curso['duracao']}")
        print(f"Vagas: {curso['vagas']}")


def editar_curso():

    print("\n=== EDITAR CURSO ===")

    # Verifica se existe algum curso cadastrado
    if len(cursos) == 0:
        print("Nenhum curso cadastrado.")
        return

    # Mostra os cursos disponíveis
    listar_cursos()

    # Solicita o curso que será editado
    indice = int(input("\nDigite o número do curso: ")) - 1

    # Verifica se o índice informado é válido
    if 0 <= indice < len(cursos):

        # Atualiza os dados do curso
        cursos[indice]["titulo"] = input("Novo título: ")
        cursos[indice]["tutor"] = input("Novo tutor: ")
        cursos[indice]["duracao"] = input("Nova duração: ")
        while True:
            try:
                cursos[indice]["vagas"] = int(
                    input("Nova quantidade de vagas: "))
                if cursos[indice]["vagas"] < 0:
                    print("A quantidade de vagas não pode ser negativa...")
                    continue
                break
            except ValueError:
                print("Quantidade inválida, digite apenas números inteiros...")

        print("\nCurso atualizado com sucesso!")

    else:
        print("Curso não encontrado.")


def excluir_curso():

    print("\n=== EXCLUIR CURSO ===")

    # Verifica se existem cursos cadastrados
    if len(cursos) == 0:
        print("Nenhum curso cadastrado.")
        return

    # Exibe a lista de cursos
    listar_cursos()

    # Solicita o número do curso que será removido
    indice = int(input("\nDigite o número do curso: ")) - 1

    # Verifica se o índice informado é válido
    if 0 <= indice < len(cursos):

        # Remove o curso da lista
        cursos.pop(indice)

        print("\nCurso removido com sucesso!")

    else:
        print("Curso não encontrado.")


def menu_cursos_adm():
    while True:
        opcao = input("""\n============================================================

              ALUMIAR APP (Gerenciamento de Cursos)

============================================================

1 - Listar Cursos
2 - Cadastrar Curso
3 - Editar Curso
4 - Deletar Curso
0 - Voltar

Escolha: """).strip()

        if opcao == "1":
            listar_cursos()
        elif opcao == "2":
            cadastrar_curso()
        elif opcao == "3":
            editar_curso()
        elif opcao == "4":
            excluir_curso()
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")


def listar_eventos():
    if not eventos:
        print("\nNenhum evento cadastrado.")
        return
    for indice, evento in enumerate(eventos):
        print(f"""
ID: {indice + 1}
  Título:  {evento['titulo']}
  Data:    {evento['data']}
  Horário: {evento['horario']}
  Local:   {evento['local']}
  Vagas:   {evento['vagas']}""")


def cadastrar_evento():
    print("\n==== CADASTRAR EVENTO ====\n")

    titulo = input("- Título: ").strip().title()
    data = input("- Data (DD/MM/AAAA): ").strip()
    horario = input("- Horário (HH:MM): ").strip()
    local = input("- Local: ").strip().title()

    while True:
        try:
            vagas = int(input("- Quantidade de vagas: "))
            if vagas <= 0:
                print("  A quantidade deve ser maior que zero...")
                continue
            break
        except ValueError:
            print("  Quantidade inválida, digite apenas números inteiros...")

    eventos.append({
        "titulo":  titulo,
        "data":    data,
        "horario": horario,
        "local":   local,
        "vagas":   vagas,
        "inscritos": []
    })

    print("\nEvento cadastrado com sucesso!")


def editar_evento():
    if not eventos:
        print("\nNenhum evento cadastrado.")
        return

    listar_eventos()

    try:
        id_edit = int(input("\nID do evento a editar: ").strip())
        indice = id_edit - 1
    except ValueError:
        print("ID inválido.")
        return

    if indice < 0 or indice >= len(eventos):
        print("Evento não encontrado.")
        return

    e = eventos[indice]
    print(f"\nEditando '{e['titulo']}' — Enter para manter o valor atual.\n")

    novo = input(f"- Título [{e['titulo']}]: ").strip()
    if novo:
        e['titulo'] = novo.title()

    novo = input(f"- Data [{e['data']}]: ").strip()
    if novo:
        e['data'] = novo

    novo = input(f"- Horário [{e['horario']}]: ").strip()
    if novo:
        e['horario'] = novo

    novo = input(f"- Local [{e['local']}]: ").strip()
    if novo:
        e['local'] = novo.title()

    while True:
        try:
            novo = input(f"- Vagas [{e['vagas']}]: ").strip()
            if not novo:
                break
            novo = int(novo)
            if novo <= 0:
                print("  A quantidade deve ser maior que zero...")
                continue
            e['vagas'] = novo
            break
        except ValueError:
            print("  Quantidade inválida, digite apenas números inteiros...")

    print(f"\nEvento '{e['titulo']}' atualizado com sucesso!")


def deletar_evento():
    if not eventos:
        print("\nNenhum evento cadastrado.")
        return

    listar_eventos()

    try:
        id_del = int(input("\nID do evento a deletar: ").strip())
        indice = id_del - 1
    except ValueError:
        print("ID inválido.")
        return

    if indice < 0 or indice >= len(eventos):
        print("Evento não encontrado.")
        return

    titulo = eventos[indice]['titulo']
    confirmacao = input(
        f"\nDeletar '{titulo}'? Essa ação é irreversível. (S/N): ").strip().upper()

    if confirmacao == "S":
        eventos.pop(indice)
        print(f"Evento '{titulo}' deletado com sucesso!")
    else:
        print("Operação cancelada.")


def menu_eventos_adm():
    while True:
        opcao = input("""\n============================================================

              ALUMIAR APP (Gerenciamento de Eventos)

============================================================

1 - Listar Eventos
2 - Cadastrar Evento
3 - Editar Evento
4 - Deletar Evento
0 - Voltar

Escolha: """).strip()

        if opcao == "1":
            listar_eventos()
        elif opcao == "2":
            cadastrar_evento()
        elif opcao == "3":
            editar_evento()
        elif opcao == "4":
            deletar_evento()
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")


def menu_adm():
    while True:
        opcao = input("""\n============================================================

                ALUMIAR APP (Menu Administrador)

============================================================
                  
1 - Usuários
2 - Eventos
3 - Cursos
0 - Sair

Escolha: """).strip()

        if opcao == "1":
            menu_usuarios_adm()
        elif opcao == "2":
            menu_eventos_adm()
        elif opcao == "3":
            menu_cursos_adm()
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")


def ver_perfil():
    """Exibe as informações do usuário logado."""
    usuario = usuarios[id_logado]
    print(f"""
=== MEU PERFIL ===

Nome:        {usuario['nome']}
Idade:       {usuario['idade']}
Artesanato:  {usuario['tipo_artesanato']}
Bairro:      {usuario['bairro']}
Telefone:    {usuario['telefone']}
Formalizada: {usuario['formalizacao']}
Email:       {usuario['email']}""")


def atualizar_perfil():
    """Permite ao usuário logado atualizar suas próprias informações."""
    u = usuarios[id_logado]
    print(f"\nAtualizando perfil — Enter para manter o valor atual.\n")

    # ── Nome ──────────────────────────────────────────────────────────────────
    novo = input(f"- Nome [{u['nome']}]: ").strip()
    if novo:
        u['nome'] = novo.title()

    # ── Idade ─────────────────────────────────────────────────────────────────
    while True:
        novo = input(f"- Idade [{u['idade']}]: ").replace(" ", "")
        if not novo:
            break
        if validar_e_calcular_idade(novo):
            u['idade'] = novo
            break
        print("  Idade inválida, tente novamente...")

    # ── Tipo de artesanato ────────────────────────────────────────────────────
    novo = input(f"- Tipo de Artesanato [{u['tipo_artesanato']}]: ").strip()
    if novo:
        u['tipo_artesanato'] = novo.title()

    # ── Bairro ────────────────────────────────────────────────────────────────
    novo = input(f"- Bairro [{u['bairro']}]: ").strip()
    if novo:
        u['bairro'] = novo.title()

    # ── Telefone ──────────────────────────────────────────────────────────────
    while True:
        novo = input(f"- Telefone [{u['telefone']}]: ").replace(" ", "")
        if not novo:
            break
        if validar_telefone(novo):
            u['telefone'] = novo
            break
        print("  Telefone inválido, tente novamente...")

    # ── Formalização ──────────────────────────────────────────────────────────
    while True:
        novo = input(
            f"- Formalizada? (S/N) [{u['formalizacao']}]: ").strip().upper()
        if not novo:
            break
        if novo in ("S", "N"):
            u['formalizacao'] = novo
            break
        print("  Resposta inválida, tente novamente...")

    # ── Email ─────────────────────────────────────────────────────────────────
    while True:
        novo = input(f"- Email [{u['email']}]: ").strip()
        if not novo:
            break
        if not validar_email(novo):
            print("  Email inválido, tente novamente...")
            continue
        duplicado = any(
            dados['email'] == novo and uid != id_logado
            for uid, dados in usuarios.items()
        )
        if duplicado:
            print("  Email já cadastrado, tente novamente...")
            continue
        u['email'] = novo
        break

    # ── Senha ─────────────────────────────────────────────────────────────────
    novo = input("- Nova senha (Enter para manter): ").strip()
    if novo:
        u['senha'] = novo

    print(f"\nPerfil atualizado com sucesso!")


def menu_perfil():
    while True:
        opcao = input("""\n============================================================

                ALUMIAR APP (Meu Perfil)

============================================================

1 - Ver meu perfil
2 - Atualizar informações
0 - Voltar

Escolha: """).strip()

        if opcao == "1":
            ver_perfil()
        elif opcao == "2":
            atualizar_perfil()
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")


def pesquisar_artesa():
    """Busca artesãs pelo nome, aceitando termos parciais."""
    if not usuarios:
        print("\nNenhuma artesã cadastrada.")
        return

    termo = input("\nDigite o nome a pesquisar: ").strip().lower()

    resultados = [
        usuario for usuario in usuarios.values()
        if termo in usuario['nome'].lower()
    ]

    if not resultados:
        print("\nNenhuma artesã encontrada.")
        return

    print(f"\n{len(resultados)} resultado(s) encontrado(s):\n")
    for usuario in resultados:
        print(f"""
Nome:        {usuario['nome']}
Idade:       {usuario['idade']}
Telefone:    {usuario['telefone']}
Email:       {usuario['email']}
Artesanato:  {usuario['tipo_artesanato']}
Bairro:      {usuario['bairro']}
Formalizada: {usuario['formalizacao']}""")


def menu_artesas():
    while True:
        opcao = input("""\n============================================================

                ALUMIAR APP (Artesãs)

============================================================

1 - Ver todas as artesãs
2 - Pesquisar por nome
0 - Voltar

Escolha: """).strip()

        if opcao == "1":
            listar_usuarios()
        elif opcao == "2":
            pesquisar_artesa()
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")


def listar_eventos_usuario():
    if not eventos:
        print("\nNenhum evento disponível.")
        return
    print("\n=== EVENTOS DISPONÍVEIS ===")
    for indice, evento in enumerate(eventos):
        inscritos = evento.get('inscritos', [])
        vagas_disponiveis = evento['vagas'] - len(inscritos)
        print(f"""
ID: {indice + 1}
  Título:    {evento['titulo']}
  Data:      {evento['data']}
  Horário:   {evento['horario']}
  Local:     {evento['local']}
  Vagas:     {vagas_disponiveis}/{evento['vagas']}""")


def pesquisar_evento():
    if not eventos:
        print("\nNenhum evento disponível.")
        return

    termo = input("\nDigite o nome do evento: ").strip().lower()

    resultados = [
        (indice, evento) for indice, evento in enumerate(eventos)
        if termo in evento['titulo'].lower()
    ]

    if not resultados:
        print("\nNenhum evento encontrado.")
        return

    print(f"\n{len(resultados)} resultado(s) encontrado(s):")
    for indice, evento in resultados:
        inscritos = evento.get('inscritos', [])
        vagas_disponiveis = evento['vagas'] - len(inscritos)
        print(f"""
ID: {indice + 1}
  Título:    {evento['titulo']}
  Data:      {evento['data']}
  Horário:   {evento['horario']}
  Local:     {evento['local']}
  Vagas:     {vagas_disponiveis}/{evento['vagas']}""")


def inscrever_evento():
    if not eventos:
        print("\nNenhum evento disponível.")
        return

    listar_eventos_usuario()

    try:
        id_evento = int(input("\nID do evento para inscrição: ").strip())
        indice = id_evento - 1
    except ValueError:
        print("ID inválido.")
        return

    if indice < 0 or indice >= len(eventos):
        print("Evento não encontrado.")
        return

    evento = eventos[indice]

    if 'inscritos' not in evento:
        evento['inscritos'] = []

    if id_logado in evento['inscritos']:
        print(f"\nVocê já está inscrito em '{evento['titulo']}'.")
        return

    vagas_disponiveis = evento['vagas'] - len(evento['inscritos'])
    if vagas_disponiveis <= 0:
        print(f"\nO evento '{evento['titulo']}' não possui vagas disponíveis.")
        return

    evento['inscritos'].append(id_logado)
    print(f"\nInscrição realizada com sucesso em '{evento['titulo']}'!")
    print(f"Vagas restantes: {vagas_disponiveis - 1}/{evento['vagas']}")


def menu_eventos():
    while True:
        opcao = input("""\n============================================================

                ALUMIAR APP (Eventos)

============================================================

1 - Ver todos os eventos
2 - Pesquisar por nome
3 - Inscrever-se em um evento
0 - Voltar

Escolha: """).strip()

        if opcao == "1":
            listar_eventos_usuario()
        elif opcao == "2":
            pesquisar_evento()
        elif opcao == "3":
            inscrever_evento()
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")


def listar_cursos_usuario():
    if not cursos:
        print("\nNenhum curso disponível.")
        return
    print("\n=== CURSOS DISPONÍVEIS ===")
    for indice, curso in enumerate(cursos):
        inscritos = curso.get('inscritos', [])
        vagas_disponiveis = curso['vagas'] - len(inscritos)
        print(f"""
ID: {indice + 1}
  Título:    {curso['titulo']}
  Tutor:     {curso['tutor']}
  Duração:   {curso['duracao']}
  Vagas:     {vagas_disponiveis}/{curso['vagas']}""")


def pesquisar_curso():
    if not cursos:
        print("\nNenhum curso disponível.")
        return

    termo = input("\nDigite o nome do curso: ").strip().lower()

    resultados = [
        (indice, curso) for indice, curso in enumerate(cursos)
        if termo in curso['titulo'].lower()
    ]

    if not resultados:
        print("\nNenhum curso encontrado.")
        return

    print(f"\n{len(resultados)} resultado(s) encontrado(s):")
    for indice, curso in resultados:
        inscritos = curso.get('inscritos', [])
        vagas_disponiveis = curso['vagas'] - len(inscritos)
        print(f"""
ID: {indice + 1}
  Título:    {curso['titulo']}
  Tutor:     {curso['tutor']}
  Duração:   {curso['duracao']}
  Vagas:     {vagas_disponiveis}/{curso['vagas']}""")


def inscrever_curso():
    if not cursos:
        print("\nNenhum curso disponível.")
        return

    listar_cursos_usuario()

    try:
        id_curso = int(input("\nID do curso para inscrição: ").strip())
        indice = id_curso - 1
    except ValueError:
        print("ID inválido.")
        return

    if indice < 0 or indice >= len(cursos):
        print("Curso não encontrado.")
        return

    curso = cursos[indice]

    if 'inscritos' not in curso:
        curso['inscritos'] = []

    if id_logado in curso['inscritos']:
        print(f"\nVocê já está inscrito em '{curso['titulo']}'.")
        return

    vagas_disponiveis = curso['vagas'] - len(curso['inscritos'])
    if vagas_disponiveis <= 0:
        print(f"\nO curso '{curso['titulo']}' não possui vagas disponíveis.")
        return

    curso['inscritos'].append(id_logado)
    print(f"\nInscrição realizada com sucesso em '{curso['titulo']}'!")
    print(f"Vagas restantes: {vagas_disponiveis - 1}/{curso['vagas']}")


def menu_cursos():
    while True:
        opcao = input("""\n============================================================

                ALUMIAR APP (Cursos)

============================================================

1 - Ver todos os cursos
2 - Pesquisar por nome
3 - Inscrever-se em um curso
0 - Voltar

Escolha: """).strip()

        if opcao == "1":
            listar_cursos_usuario()
        elif opcao == "2":
            pesquisar_curso()
        elif opcao == "3":
            inscrever_curso()
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")


def calcular_valor_hora():
    print("\n=== CÁLCULO DO VALOR DA HORA ===")

    while True:
        try:
            renda_desejada = float(
                input("Quanto deseja ganhar por mês (R$)? "))
            if renda_desejada <= 0:
                print("  O valor deve ser maior que zero...")
                continue
            break
        except ValueError:
            print("  Valor inválido, digite apenas números...")

    while True:
        try:
            horas_por_dia = float(input("Quantas horas trabalha por dia? "))
            if horas_por_dia <= 0:
                print("  O valor deve ser maior que zero...")
                continue
            break
        except ValueError:
            print("  Valor inválido, digite apenas números...")

    while True:
        try:
            dias_por_semana = int(input("Quantos dias trabalha por semana? "))
            if dias_por_semana < 1 or dias_por_semana > 7:
                print("  Digite um valor entre 1 e 7...")
                continue
            break
        except ValueError:
            print("  Valor inválido, digite apenas números inteiros...")

    horas_por_mes = horas_por_dia * dias_por_semana * 4
    valor_hora = renda_desejada / horas_por_mes

    print(f"\nSeu valor estimado por hora é R$ {valor_hora:.2f}")
    return valor_hora


def cadastrar_materiais():
    materiais = []
    total_materiais = 0

    print("\n=== MATERIAIS UTILIZADOS ===")

    while True:
        nome = input("\nNome do material: ").strip()

        while True:
            try:
                valor = float(input("Valor gasto (R$): "))
                if valor <= 0:
                    print("  O valor deve ser maior que zero...")
                    continue
                break
            except ValueError:
                print("  Valor inválido, digite apenas números...")

        materiais.append((nome, valor))
        total_materiais += valor

        continuar = input(
            "Deseja adicionar outro material? (s/n): ").strip().lower()
        while continuar not in ("s", "n"):
            continuar = input(
                "  Resposta inválida, digite s ou n: ").strip().lower()

        if continuar == "n":
            break

    return materiais, total_materiais


def calculadora_precos():
    print("================================")
    print("   CALCULADORA DE PREÇOS")
    print("================================")

    materiais, total_materiais = cadastrar_materiais()

    print("\n=== TEMPO DE PRODUÇÃO ===")

    while True:
        try:
            horas = int(input("Horas gastas (sem os minutos): "))
            if horas < 0:
                print("  O valor não pode ser negativo...")
                continue
            break
        except ValueError:
            print("  Valor inválido, digite apenas números inteiros...")

    while True:
        try:
            minutos = int(input("Minutos adicionais: "))
            if minutos < 0 or minutos > 59:
                print("  Digite um valor entre 0 e 59...")
                continue
            break
        except ValueError:
            print("  Valor inválido, digite apenas números inteiros...")

    tempo_gasto = horas + (minutos / 60)

    print("\n=== MÃO DE OBRA ===")
    resposta = input(
        "Você já sabe o valor da sua hora de trabalho? (s/n): ").strip().lower()

    if resposta == "s":
        while True:
            try:
                valor_hora = float(input("Informe o valor da sua hora (R$): "))
                if valor_hora <= 0:
                    print("  O valor deve ser maior que zero...")
                    continue
                break
            except ValueError:
                print("  Valor inválido, digite apenas números...")
    else:
        print("\nVocê não sabe o valor da sua hora.")

        while True:
            try:
                opcao = int(input(
                    "\nEscolha uma opção:\n"
                    "1 - Utilizar a média sugerida pelo Alumiar (R$ 15,00/h)\n"
                    "2 - Calcular meu valor da hora\n"
                    "Opção: "
                ))
                if opcao not in (1, 2):
                    print("  Digite 1 ou 2...")
                    continue
                break
            except ValueError:
                print("  Valor inválido, digite apenas números inteiros...")

        if opcao == 1:
            valor_hora = 15.0
            print("\nValor da hora definido como R$ 15,00.")
        else:
            valor_hora = calcular_valor_hora()

    print("\n=== CUSTOS EXTRAS ===")

    while True:
        try:
            custos_extras = float(input("Informe os custos extras (R$): "))
            if custos_extras < 0:
                print("  O valor não pode ser negativo...")
                continue
            break
        except ValueError:
            print("  Valor inválido, digite apenas números...")

    while True:
        try:
            margem_lucro = float(input("Margem de lucro desejada (%): "))
            if margem_lucro < 0:
                print("  A margem não pode ser negativa...")
                continue
            break
        except ValueError:
            print("  Valor inválido, digite apenas números...")

    # Cálculos
    valor_mao_obra = tempo_gasto * valor_hora
    custo_total = total_materiais + valor_mao_obra + custos_extras
    lucro = custo_total * (margem_lucro / 100)
    preco_sugerido = custo_total + lucro
    preco_recomendado = preco_sugerido * 1.10
    preco_premium = preco_sugerido * 1.20

    # Resultado
    print("\n================================")
    print("          RESULTADO")
    print("================================")

    print("\nFaixa de preço sugerida:")
    print(f"Mínimo:      R$ {preco_sugerido:.2f}")
    print(f"Recomendado: R$ {preco_recomendado:.2f}")
    print(f"Premium:     R$ {preco_premium:.2f}")

    print(f"\nLucro estimado: R$ {lucro:.2f}")
    print(f"Custo total:    R$ {custo_total:.2f}")
    print(f"Tempo gasto:    {horas}h {minutos}min")

    print("\n===== DETALHAMENTO =====")
    for nome, valor in materiais:
        print(f"{nome}: R$ {valor:.2f}")

    print(f"\nTotal dos materiais:  R$ {total_materiais:.2f}")
    print(f"Valor da mão de obra: R$ {valor_mao_obra:.2f}")
    print(f"Custos extras:        R$ {custos_extras:.2f}")
    print(f"Valor da hora:        R$ {valor_hora:.2f}")
    print(f"Margem de lucro:      {margem_lucro:.0f}%")


def forum_apoio():
    print("Fórum de Apoio")


def menu_user():
    while True:
        opcao = input("""\n============================================================

                ALUMIAR APP (Menu Usuário)

============================================================

1 - Perfil
2 - Artesãs
3 - Eventos
4 - Cursos
5 - Calculadora de Preços
0 - Sair

Escolha: """).strip()

        if opcao == "1":
            menu_perfil()
        elif opcao == "2":
            menu_artesas()
        elif opcao == "3":
            menu_eventos()
        elif opcao == "4":
            menu_cursos()
        elif opcao == "5":
            calculadora_precos()
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")


def login():

    global id_logado

    while True:

        print("\n==== Login ====\n")
        email = input("- Email: ").strip()
        senha = input("- Senha: ").strip()

        if email == "ADM" and senha == "123":
            menu_adm()
            return
        else:
            for id, usuario in usuarios.items():
                if usuario["email"] == email and usuario["senha"] == senha:
                    id_logado = id
                    menu_user()
                    return
        print("Email ou Senha inválidos, tente novamente...")

        continuar = input("Tentar novamente? [S/N]: \n").strip().upper()
        while continuar not in ("S", "N"):
            continuar = input(
                "Resposta Inválida, tente novamente...\n- Tentar novamente? [S/N]): ").strip().upper()

        if continuar == "N":
            break


def menu_inicial():
    """
    Exibe o menu principal em loop e direciona para as funcionalidades do sistema.

    Opções disponíveis:
        1 - Cadastrar novo usuário
        2 - Login
        0 - Encerrar o programa
    """
    carregar_dados()
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
            salvar_dados()
            break  # Encerra o loop e finaliza o programa
        else:
            print("Comando inválido, tente novamente...")


# Ponto de entrada do programa
menu_inicial()
