import textwrap

def menu():
    menu = """\n
    ===== Bem-vindo ao Sistema Bancário Otimizado! =====\n
    
    Selecione uma opção:
    [1] Extrato
    [2] Depositar
    [3] Sacar
    [4] Nova Conta
    [5] Listar Contas
    [6] Novo Usuário
    [7] Sair
    => """

    return input(textwrap.dedent(menu))

def exibir_extrato(saldo, extrato):
    print("=== Extrato ===")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo: R$ {saldo:.2f}")

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Valor inválido para depósito.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Valor inválido para saque.")
    
    return saldo, extrato, numero_saques

def criar_nova_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Digite o CPF do usuário para vincular à conta: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("Usuário não encontrado. Por favor, crie um usuário antes de criar uma conta.")
        return None
    conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    contas.append(conta)
    return conta


def listar_contas(contas):
    if contas:
        print("=== Contas Criadas ===")
        for conta in contas:
            print(f"Agência: {conta['agencia']} | Número da Conta: {conta['numero_conta']}")
    else:
        print("Nenhuma conta cadastrada.")

def criar_usuario(usuarios):
    cpf = input("Digite o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("Já existe um usuário com esse CPF.")
        return
    
    nome = input("Digite o nome completo: ")
    data_nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")
    endereco = input("Digite o endereço completo: ")
    
    usuario = {"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco}
    usuarios.append(usuario)
    print("Usuário criado com sucesso!")
    return usuario

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None    

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    saldo = 0
    limite = 500    
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    
    while True:
        opcao = menu()

        if opcao == "1": # Extrato
            exibir_extrato(saldo, extrato)

        elif opcao == "2": # Depositar
            valor = float(input("Digite o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
            
        elif opcao == "3": # Sacar
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=float(input("Digite o valor do saque: ")),
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "4":
            criar_nova_conta(AGENCIA, len(contas) + 1, usuarios, contas)    
            numero_conta = len(contas)  # O número da conta é o índice + 1
            print("Conta criada com sucesso!")
        
        elif opcao == "5":  # Listar Contas
            listar_contas(contas)
        
        elif opcao == "6": # Novo Usuário
            criar_usuario(usuarios)
                
        elif opcao == "7": # Sair
            print("Obrigado por usar o Sistema Bancário Otimizado. Até logo!")
            break

        else:
            print("Opção inválida. Por favor, tente novamente.")

main()