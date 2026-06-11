# ============================================================
# VISUALIZAÇÃO DE ARTESÃS (USUÁRIO)
# ============================================================

from dados.dados import usuarios


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
    """Submenu de artesãs do usuário."""
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
