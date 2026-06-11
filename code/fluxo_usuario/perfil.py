# ============================================================
# GERENCIAMENTO DE PERFIL (USUÁRIO)
# ============================================================

import dados.dados


def ver_perfil():
    """Exibe as informações do usuário logado."""
    usuario = dados.dados.usuarios[dados.dados.id_logado]
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
    u = dados.dados.usuarios[dados.dados.id_logado]
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
        if dados.dados.validar_e_calcular_idade(novo):
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
        if dados.dados.validar_telefone(novo):
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
        if not dados.dados.validar_email(novo):
            print("  Email inválido, tente novamente...")
            continue
        duplicado = any(
            dados['email'] == novo and uid != dados.dados.id_logado
            for uid, dados in dados.dados.usuarios.items()
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
    """Submenu de perfil do usuário."""
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
