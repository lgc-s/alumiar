# ============================================================
# GERENCIAMENTO DE EVENTOS (USUÁRIO)
# ============================================================

import dados.dados


def listar_eventos_usuario():
    """Exibe todos os eventos com vagas disponíveis."""
    if not dados.dados.eventos:
        print("\nNenhum evento disponível.")
        return
    print("\n=== EVENTOS DISPONÍVEIS ===")
    for indice, evento in enumerate(dados.dados.eventos):
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
    """Busca um evento por nome."""
    if not dados.dados.eventos:
        print("\nNenhum evento disponível.")
        return

    termo = input("\nDigite o nome do evento: ").strip().lower()

    resultados = [
        (indice, evento) for indice, evento in enumerate(dados.dados.eventos)
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
    """Inscreve o usuário em um evento."""
    if not dados.dados.eventos:
        print("\nNenhum evento disponível.")
        return

    listar_eventos_usuario()

    try:
        id_evento = int(input("\nID do evento para inscrição: ").strip())
        indice = id_evento - 1
    except ValueError:
        print("ID inválido.")
        return

    if indice < 0 or indice >= len(dados.dados.eventos):
        print("Evento não encontrado.")
        return

    evento = dados.dados.eventos[indice]

    if 'inscritos' not in evento:
        evento['inscritos'] = []

    if dados.dados.id_logado in evento['inscritos']:
        print(f"\nVocê já está inscrito em '{evento['titulo']}'.")
        return

    vagas_disponiveis = evento['vagas'] - len(evento['inscritos'])
    if vagas_disponiveis <= 0:
        print(f"\nO evento '{evento['titulo']}' não possui vagas disponíveis.")
        return

    evento['inscritos'].append(dados.dados.id_logado)
    print(f"\nInscrição realizada com sucesso em '{evento['titulo']}'!")
    print(f"Vagas restantes: {vagas_disponiveis - 1}/{evento['vagas']}")


def menu_eventos():
    """Submenu de eventos do usuário."""
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
