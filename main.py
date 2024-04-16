LIMITE_QUANTIDADE_SAQUE_DIARIO = 3
LIMITE_VALOR_SAQUE = 500.00
saldo = 0.00
extrato = [{'Tipo de operação':'Saque','Valor':0},
           {'Tipo de operação':'Depósito','Valor':0}]


def depositar_valor(valor):
    if(valor>LIMITE_VALOR_SAQUE):
        print(f'Valor informado R${valor} ultrapassa o limite de saque R${LIMITE_VALOR_SAQUE}')
        return False
    if(valor<=0):
        print(f"Valor informado R${valor} é inválido! Forneça um valor maior que zero.")
        return False
    else:
        saldo =+ valor
        print(f"Valor depositado com sucesso!")
        return True

def sacar_valor(valor):
    if (valor > saldo):
        print(f"Não foi possível realizar saque, saldo insuficiente.")
    else:
        saldo =- valor

def mostrar_extrato():
    print(f"Seu saldo é: R${saldo}")


def menu_inicial():
    while True:
        try:        
            opcao_escolhida = int(input(
'''=-=-=-=-=-=-=-=-=-=Menu Inicial-=-=-==-=-=-=-=-=-=
    Bem-vindo(a) ao Banco GabIke! Selecione uma opção:
    [1] - Depósito
    [2] - Saque
    [3] - Extrato
========================================================
            '''))
            match opcao_escolhida:
                case 1:
                    status_deposito = False
                    while status_deposito == False:
                        try:
                            valor_deposito = int(input("Informe o valor para depósito: "))
                            status_deposito = depositar_valor(valor_deposito)
                        except:
                            print('Opção inválida.')
                            continue
                    continue
                case 2:
                    continue
                case 3:
                    continue
                case _:
                    print('Opção inválida.')
                    continue
        except:
            print('Opção inválida.')
            continue
    



menu_inicial()