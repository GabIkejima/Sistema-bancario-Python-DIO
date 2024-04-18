"""""
@autor
Gabriel Higa Ikejima
@version
2.0
@since
18 / 04 / 2024
"""
from time import gmtime, strftime
import re

LIMITE_QUANTIDADE_SAQUE_DIARIO = 3
LIMITE_VALOR_SAQUE = 500.00
quantidade_saques_restantes = 3
saldo = 0.00
extrato = []
usuarios = [] # Exemplo de usuário: {'nome':'Gabriel','data de nascimento':'11/10/2001','cpf':12345678910,'endereço':'Rº das mariposas testadoras de código - São Paulo/SP'}
contas = [{'agência':'0001','número da conta':0,'usuário':'Admin'}]


def set_saldo(saldo_atualizado):
    global saldo
    saldo = saldo_atualizado


def set_qntde_saques_restantes(qntde_saques_restantes):
    global quantidade_saques_restantes
    quantidade_saques_restantes = qntde_saques_restantes


def get_usuarios():
    global usuarios
    return usuarios


def filtrar_usuario_por_cpf(*,cpf_usuario,usuarios):
    response_user = [usuario for usuario in usuarios if usuario["cpf"]==cpf_usuario]
    return response_user[0] if response_user else None


def cadastrar_usuario(usuarios):
    while True:
        try:
            cpf_input = int(input("Informe o CPF (Somente número) Ou digite [0] para Voltar: "))
            cpf_pattern = r"\d{11}"
            if cpf_input == 0:
                return False

            if re.match(cpf_pattern, str(cpf_input)):

            # CPF válido, processo de busca para verificar se cliente existe
                usuario = filtrar_usuario_por_cpf(cpf_usuario=cpf_input,usuarios=usuarios)

                if(usuario is None):
                    # Continuação processo de criação de usuário
                    nome_input = input("Informe o nome completo: ")
                    data_nascimento_input = input("Informe a data de nascimento(dd/mm/aaaa): ")
                    endereco_input = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

                    usuarios.append({'nome':nome_input,'data de nascimento':data_nascimento_input,'cpf':cpf_input,'endereço':endereco_input})
                    print(f'Usuário cadastrado com sucesso! {nome_input}/{cpf_input}')
                    input('Aperte "enter" para continuar. ')
                    return True

                else:
                    print(f'CPF já cadastrado! {cpf_input}/{usuario["nome"]}')
                    continue
            else:
                print('CPF inválido, favor conferir o tamanho do CPF (11 dígitos)')
                continue
        except:
            print('CPF inválido, favor inserir apenas digitos (11 dígitos)')
            continue
        

def listar_usuarios(usuarios):
    if len(usuarios)>0:
        print(f'=-=-=-=-=-=-=-=-=-=Lista de usuários-=-=-==-=-=-=-=-=-=')
        for usuario in usuarios:
            print(f'Nome: {usuario["nome"]}\nData de nascimento: {usuario["data de nascimento"]}\nCPF: {usuario["cpf"]}\nEndereço: {usuario["endereço"]}')
            print('‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
    else:
        print('Nenhum usuário cadastrado!')
    input('Aperte "enter" para continuar. ')

# Conta só pode ser criada para um usuário cadastrado (cpf)
def criar_conta(*,agencia, usuarios, contas):
    while True:
        try:
            cpf_input = int(input("Informe o CPF (Somente número) Ou digite [0] para Voltar: "))
            cpf_pattern = r"\d{11}"
            if cpf_input == 0:
                return False

            if re.match(cpf_pattern, str(cpf_input)):
                # CPF válido, processo de busca para verificar se cliente existe
                usuario = filtrar_usuario_por_cpf(cpf_usuario=cpf_input,usuarios=usuarios)
                if(usuario is not None):
                    # Continuação processo de criação de conta se o usuário existir
                    numero_nova_conta = int(contas[-1]["número da conta"])+1
                    contas.append({'agência':agencia,'número da conta':numero_nova_conta,'usuário':usuario})
                    print(f'Conta criada com sucesso!\nAgência: {agencia}\nNúmero da conta: {numero_nova_conta}\nUsuário: {usuario["nome"]}')
                    input('Aperte "enter" para continuar. ')
                    return True
                else:
                    print(f'CPF não cadastrado! {cpf_input}, favor cadastrar usuário.')
                    continue
            else:
                print('CPF inválido, favor conferir o tamanho do CPF (11 dígitos)')
                continue
        except:
            print('CPF inválido, favor inserir apenas digitos (11 dígitos)')
            continue
        

def listar_contas(contas):
    if len(contas)>1:
        print(f'=-=-=-=-=-=-=-=-=-=Lista de Contas-=-=-==-=-=-=-=-=-=')
        for conta in contas:
            if(conta['número da conta'] == 0):
                continue
            else:
                print(f'Agência:{conta["agência"]}\nNúmero da conta:{conta["número da conta"]}\nUsuário:{conta["usuário"]["nome"]}')
                print('‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
    else:
        print('Nenhuma conta cadastrada!')

    input('Aperte "enter" para continuar. ')


"""
Função para atualizar variável saldo (+).
Parâmetros:
- valor(float): valor a ser somado com saldo.
    * precisa ser maior que 0.
- saldo(float): saldo atual da conta.
Retorna:
- True se a atualização for possível e False caso contrário.
Outros:
- Função chama set_saldo para atualizar variável sem usar scope global.
"""
def depositar_valor(saldo,valor,/):
    if(valor<=0):
        print(f"Valor informado R${valor} é inválido! Forneça um valor maior que zero.")
        return False
    else:
        saldo += valor
        print(f"Valor depositado com sucesso!(R${valor:.2f}).")
        print(f"Novo saldo: R${saldo:.2f}")

        timestamp = strftime("%d-%m-%Y %H:%M:%S", gmtime()) # Horário atual para adicionar no extrato
        extrato.append({'Tipo de operação': 'Depósito', 'Valor': valor, 'Horário' : timestamp}) 

        # Atualizando saldo
        set_saldo(saldo)
        input('Aperte "enter" para continuar. ')
        return True
    

"""
Função para atualizar variável saldo (-).
Parâmetros:
- valor(float): valor a ser subtraído do saldo ().
    * precisa ser maior que 0, menor ou igual a saldo e menor que LIMITE_VALOR_SAQUE (definida manualmente).
- saldo(float): valor de saldo atual.
- quantidade_saques_restantes(int): quantidade de saques diários restantes do usuário
    * precisa ser maior que 0
Retorna:
- True se a atualização for possível e False caso contrário.
Outros:
- Função chama set_qntde_saques_restantes e set_saldo para atualizar variáveis sem usar scope global.
"""
def sacar_valor(*,saldo,valor,quantidade_saques_restantes):
    if(valor>LIMITE_VALOR_SAQUE):
        print(f'Valor informado R${valor:.2f} ultrapassa o limite de saque R${LIMITE_VALOR_SAQUE:.2f}')
        return False
    elif(valor<=0):
        print(f"Valor informado R${valor:.2f} é inválido! Forneça um valor maior que zero.")
        return False
    elif(valor > saldo):
        print(f"Não foi possível realizar saque, saldo insuficiente.")
        return False
    else:
        saldo -= valor
        quantidade_saques_restantes -= 1
        print(f"Valor sacado com sucesso!(R${valor:.2f}).")
        print(f"Novo saldo: R${saldo:.2f}") 
        print(f'Quantidade de saques restantes:{quantidade_saques_restantes}/{LIMITE_QUANTIDADE_SAQUE_DIARIO}')

        timestamp = strftime("%d-%m-%Y %H:%M:%S", gmtime()) # Horário atual para adicionar no extrato
        extrato.append({'Tipo de operação': 'Saque', 'Valor': valor, 'Horário' : timestamp}) 
        
        # Atualizando variáveis
        set_qntde_saques_restantes(quantidade_saques_restantes)
        set_saldo(saldo)
        input('Aperte "enter" para continuar. ')
        return True


"""
Função para mostrar os items da variável extrato (depósitos e saques realizados)

Parâmetros:
- N/A

Retorna:
- N/A
"""
def mostrar_extrato(saldo):
# Verifica se o extrato está vazio.
    if not extrato:
        print(
'''=-=-=-=-=-=-=-=-=-=Extrato-=-=-==-=-=-=-=-=-=
    Conta ainda não realizou nenhuma movimentação.
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾''')
        input('Aperte "enter" para continuar. ')
    else:
        print(
f'''=-=-=-=-=-=-=-=-=-=Extrato-=-=-==-=-=-=-=-=-=
    Seu saldo atual é: R${saldo:.2f}
    OPERAÇÃO   |    VALOR       | Horário
    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾''')
        # Muda a quantidade de espaços dependendo da quantidade de char de uma palavra, para o print ficar alinhado
        for item in extrato:
            if(item['Tipo de operação'] == 'Saque'):
                quantidade_espacos_print = 6
            elif(item['Tipo de operação'] == 'Depósito'):
                quantidade_espacos_print = 3
            else:
                quantidade_espacos_print = 4
            print(f"    {item['Tipo de operação']}{quantidade_espacos_print*' '}|    R${item['Valor']:.2f}    | Horário:{item['Horário']}")
        input('Aperte "enter" para continuar. ')


"""
Função para mostrar em loop as opções do menu inicial

Parâmetros:
- N/A

Retorna:
- N/A
"""
def menu_inicial():
    while True:
        try:        
            opcao_escolhida = int(input(
'''=-=-=-=-=-=-=-=-=-=Menu Inicial-=-=-==-=-=-=-=-=-=
    Bem-vindo(a) ao Banco GabIke! Selecione uma opção:
    [1] - Depósito
    [2] - Saque
    [3] - Extrato
    [4] - Cadastrar usuário
    [5] - Criar conta
    [6] - Listar usuários
    [7] - Listar contas
    [0] - Sair
========================================================
Opção: '''))
            # Verifica a opção escolhida
            match opcao_escolhida:
                case 0:
                    print("Obrigado por usar o Banco GabIke 😊 até a próxima!")
                    break
                case 1:
                    status_deposito = False
                    while status_deposito == False:
                        try:
                            valor_deposito = float(input("Informe o valor para depósito Ou digite [0] para Voltar: "))
                            if(valor_deposito == 0):
                                break
                            else:
                                status_deposito = depositar_valor(saldo, valor_deposito)
                        except:
                            print('Forneça um valor válido (maior que 0).')
                            continue
                case 2:
                    status_saque = False
                    if(quantidade_saques_restantes==0):
                        print(f'Não foi possível realizar saque. Limite diário de saque atingido ({quantidade_saques_restantes}/{LIMITE_QUANTIDADE_SAQUE_DIARIO})')
                        input('Aperte "enter" para continuar. ')
                        continue
                    else:
                        while status_saque == False:
                            try:
                                print(f'Você possuí ({quantidade_saques_restantes}/{LIMITE_QUANTIDADE_SAQUE_DIARIO}) saques restantes!')
                                valor_saque = float(input("Informe o valor de saque Ou digite [0] para Voltar: "))
                                if(valor_saque == 0):
                                    break
                                else:
                                    status_saque = sacar_valor(saldo=saldo,valor=valor_saque,quantidade_saques_restantes=quantidade_saques_restantes)

                            except:
                                print('Forneça um valor válido (maior que 0).')
                                continue
                case 3:
                    mostrar_extrato(saldo)
                    continue
                case 4:
                    cadastrar_usuario(usuarios=usuarios)
                    continue
                case 5:
                    criar_conta(agencia='0001', usuarios=usuarios, contas=contas)
                    continue
                case 6:
                    listar_usuarios(usuarios)
                case 7:
                    listar_contas(contas)
                case _:
                    print('Opção inválida.')
                    continue
        except:
            print('Opção inválida.')
            continue
    

menu_inicial()