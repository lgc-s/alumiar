# ============================================================
# GERENCIAMENTO DE CURSOS (ADMINISTRADOR)
# ============================================================

from dados.dados import cursos


def cadastrar_curso():
    """Coleta e salva dados de um novo curso."""
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
    """Exibe todos os cursos disponíveis."""
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
    """Edita os dados de um curso existente."""
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
    """Deleta um curso da lista."""
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
    """Submenu CRUD de cursos acessado pelo administrador."""
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
