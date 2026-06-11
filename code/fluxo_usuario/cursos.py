# ============================================================
# GERENCIAMENTO DE CURSOS (USUÁRIO)
# ============================================================

import dados.dados


def listar_cursos_usuario():
    """Exibe todos os cursos com vagas disponíveis."""
    if not dados.dados.cursos:
        print("\nNenhum curso disponível.")
        return
    print("\n=== CURSOS DISPONÍVEIS ===")
    for indice, curso in enumerate(dados.dados.cursos):
        inscritos = curso.get('inscritos', [])
        vagas_disponiveis = curso['vagas'] - len(inscritos)
        print(f"""
ID: {indice + 1}
  Título:    {curso['titulo']}
  Tutor:     {curso['tutor']}
  Duração:   {curso['duracao']}
  Vagas:     {vagas_disponiveis}/{curso['vagas']}""")


def pesquisar_curso():
    """Busca um curso por nome."""
    if not dados.dados.cursos:
        print("\nNenhum curso disponível.")
        return

    termo = input("\nDigite o nome do curso: ").strip().lower()

    resultados = [
        (indice, curso) for indice, curso in enumerate(dados.dados.cursos)
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
    """Inscreve o usuário em um curso."""
    if not dados.dados.cursos:
        print("\nNenhum curso disponível.")
        return

    listar_cursos_usuario()

    try:
        id_curso = int(input("\nID do curso para inscrição: ").strip())
        indice = id_curso - 1
    except ValueError:
        print("ID inválido.")
        return

    if indice < 0 or indice >= len(dados.dados.cursos):
        print("Curso não encontrado.")
        return

    curso = dados.dados.cursos[indice]

    if 'inscritos' not in curso:
        curso['inscritos'] = []

    if dados.dados.id_logado in curso['inscritos']:
        print(f"\nVocê já está inscrito em '{curso['titulo']}'.")
        return

    vagas_disponiveis = curso['vagas'] - len(curso['inscritos'])
    if vagas_disponiveis <= 0:
        print(f"\nO curso '{curso['titulo']}' não possui vagas disponíveis.")
        return

    curso['inscritos'].append(dados.dados.id_logado)
    print(f"\nInscrição realizada com sucesso em '{curso['titulo']}'!")
    print(f"Vagas restantes: {vagas_disponiveis - 1}/{curso['vagas']}")


def menu_cursos():
    """Submenu de cursos do usuário."""
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
