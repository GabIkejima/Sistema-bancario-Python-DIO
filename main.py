"""""
@autor
Gabriel Higa Ikejima
@version
1.0
@since
17 / 04 / 2024
"""

LIMITE_QUANTIDADE_SAQUE_DIARIO = 3
LIMITE_VALOR_SAQUE = 500.00
quantidade_saques_restantes = 3
saldo = 0.00
extrato = []


def depositar_valor(valor):
    global saldo
    if(valor<=0):
        print(f"Valor informado R${valor} é inválido! Forneça um valor maior que zero.")
        return False
    else:
        saldo += valor
        print(f"Valor depositado com sucesso!(R${valor:.2f}).")
        print(f"Novo saldo: R${saldo:.2f}")
        extrato.append({'Tipo de operação': 'Depósito', 'Valor': valor}) 
        return True
    

def sacar_valor(valor):
    global saldo, quantidade_saques_restantes
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
        print(f"Valor sacado com sucesso!(R${valor:.2f}).")
        print(f"Novo saldo: R${saldo:.2f}")
        quantidade_saques_restantes -= 1
        extrato.append({'Tipo de operação': 'Saque', 'Valor': valor}) 
        print(f'Quantidade de saques restantes:{quantidade_saques_restantes}/{LIMITE_QUANTIDADE_SAQUE_DIARIO}')
        return True


def mostrar_extrato():
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
    OPERAÇÃO   |    VALOR
    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾''')
        for item in extrato:
            if(item['Tipo de operação'] == 'Saque'):
                quantidade_espacos_print = 6
            elif(item['Tipo de operação'] == 'Depósito'):
                quantidade_espacos_print = 3
            else:
                quantidade_espacos_print = 4
            print(f"    {item['Tipo de operação']}{quantidade_espacos_print*' '}|    R${item['Valor']:.2f}")
        input('Aperte "enter" para continuar. ')


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
            match opcao_escolhida:
                case 0:
                    print("Obrigado por usar o Banco GabIke 😊 até a próxima!")
                    break
                case 1:
                    status_deposito = False
                    while status_deposito == False:
                        try:
                            valor_deposito = float(input("Informe o valor para depósito: "))
                            status_deposito = depositar_valor(valor_deposito)
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
                                status_saque = sacar_valor(valor_saque)

                            except:
                                print('Forneça um valor válido.')
                                continue
                case 3:
                    mostrar_extrato()
                    continue
                case _:
                    print('Opção inválida.')
                    continue
        except:
            print('Opção inválida.')
            continue
    



menu_inicial()