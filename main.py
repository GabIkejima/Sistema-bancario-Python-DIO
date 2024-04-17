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
    global saldo
    if(valor>LIMITE_VALOR_SAQUE):
        print(f'Valor informado R${valor:.2f} ultrapassa o limite de saque R${LIMITE_VALOR_SAQUE:.2f}')
        return False
    if(valor<=0):
        print(f"Valor informado R${valor:.2f} é inválido! Forneça um valor maior que zero.")
        return False
    if (valor > saldo):
        print(f"Não foi possível realizar saque, saldo insuficiente.")
        return False
    else:
        saldo -= valor
        print(f"Valor sacado com sucesso!(R${valor:.2f}).")
        print(f"Novo saldo: R${saldo:.2f}")
        extrato.append({'Tipo de operação': 'Saque', 'Valor': valor}) 
        return True

def mostrar_extrato():
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
                            print(f"VALOR R${saldo:.2f}")
                        except:
                            print('Opção inválida.')
                            continue
                case 2:
                    status_saque = False
                    while status_saque == False:
                        try:
                            valor_saque = float(input("Informe o valor de saque: "))
                            print(f'{valor_saque}')
                            status_saque = sacar_valor(valor_saque)
                        except:
                            print('Opção inválida')
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