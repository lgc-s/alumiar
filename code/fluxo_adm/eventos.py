# ============================================================
# GERENCIAMENTO DE EVENTOS (ADMINISTRADOR)
# ============================================================

from dados.dados import eventos


def listar_eventos():
    """Exibe todos os eventos cadastrados."""
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
    """Coleta e salva dados de um novo evento."""
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
    """Edita os dados de um evento existente."""
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
    """Deleta um evento da lista."""
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
    """Submenu CRUD de eventos acessado pelo administrador."""
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
