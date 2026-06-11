# ============================================================
# GERENCIAMENTO DE USUÁRIOS (ADMINISTRADOR)
# ============================================================

from dados.dados import (
    usuarios, validar_telefone, validar_e_calcular_idade,
    validar_email, verificar_email_existente, cursos, eventos
)

id_global = None  # Será acessado através do módulo dados


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
    from dados.dados import id as id_atual

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
    import dados.dados as dados_module
    usuarios[dados_module.id] = {
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
    dados_module.id += 1


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

        # Remove o usuário de todos os cursos em que estava inscrito
        for curso in cursos:
            if id_del in curso.get('inscritos', []):
                curso['inscritos'].remove(id_del)

        # Remove o usuário de todos os eventos em que estava inscrito
        for evento in eventos:
            if id_del in evento.get('inscritos', []):
                evento['inscritos'].remove(id_del)

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
