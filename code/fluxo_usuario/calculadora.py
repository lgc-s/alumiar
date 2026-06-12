# ============================================================
# CALCULADORA DE PREÇOS
# ============================================================


def calcular_valor_hora():
    """Calcula o valor da hora de trabalho com base na renda desejada."""
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
    """Coleta e registra os materiais utilizados e seu custo."""
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
    """Calcula o preço sugerido de um produto baseado em custos e margens."""
    print("================================")
    print("   CALCULADORA DE PREÇOS")
    print("================================")

    materiais, total_materiais = cadastrar_materiais()

    print("\n=== TEMPO DE PRODUÇÃO ===")

    while True:
        try:
            horas = int(input("Horas gastas (sem os minutos): "))
            if horas < 0:
                print("O valor não pode ser negativo...")
                continue
            break
        except ValueError:
            print("  Valor inválido, digite apenas números inteiros...")

    while True:
        try:
            minutos = int(input("Minutos adicionais: "))
            if minutos < 0 or minutos > 59:
                print("Digite um valor entre 0 e 59...")
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
                    print("O valor deve ser maior que zero...")
                    continue
                break
            except ValueError:
                print("Valor inválido, digite apenas números...")
    else:
        print("\nVocê não sabe o valor da sua hora.")

        while True:
            try:
                opcao = int(input(
                    "Escolha uma opção:\n"
                    "1 - Utilizar a média sugerida pelo Alumiar (R$ 15,00/h)\n"
                    "2 - Calcular meu valor da hora\n"
                    "Opção: "
                ))
                if opcao not in (1, 2):
                    print("Digite 1 ou 2...")
                    continue
                break
            except ValueError:
                print("Valor inválido, digite apenas números inteiros...")

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
                print("O valor não pode ser negativo...")
                continue
            break
        except ValueError:
            print("Valor inválido, digite apenas números...")

    while True:
        try:
            margem_lucro = float(input("Margem de lucro desejada (%): "))
            if margem_lucro < 0:
                print("A margem não pode ser negativa...")
                continue
            break
        except ValueError:
            print("Valor inválido, digite apenas números...")

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
