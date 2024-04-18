"""""
@autor
Gabriel Higa Ikejima
@version
1.0
@since
17 / 04 / 2024
"""
from time import gmtime, strftime

LIMITE_QUANTIDADE_SAQUE_DIARIO = 3
LIMITE_VALOR_SAQUE = 500.00
quantidade_saques_restantes = 3
saldo = 0.00
extrato = []


def set_saldo(saldo_atualizado):
    global saldo
    saldo = saldo_atualizado

def set_qntde_saques_restantes(qntde_saques_restantes):
    global quantidade_saques_restantes
    quantidade_saques_restantes = qntde_saques_restantes

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
                            valor_deposito = float(input("Informe o valor para depósito: "))
                            status_deposito = depositar_valor(saldo, valor_deposito)
                        except:
                            print('Forneça um valor válido.')
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
                                valor_saque = float(input("Informe o valor de saque: "))
                                status_saque = sacar_valor(saldo=saldo,valor=valor_saque,quantidade_saques_restantes=quantidade_saques_restantes)

                            except:
                                print('Erro: Operação de saque cancelada.')
                                break
                case 3:
                    mostrar_extrato(saldo)
                    continue
                case _:
                    print('Opção inválida.')
                    continue
        except:
            print('Opção inválida.')
            continue
    



menu_inicial()