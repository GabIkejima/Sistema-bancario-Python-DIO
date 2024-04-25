"""""
@autor
Gabriel Higa Ikejima
@version
2.0
@since
18 / 04 / 2024
"""
from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
from time import gmtime, strftime
import re

# Conectar com um DB posteriormente as variáveis que armazenam conta/cliente
contas = []
clientes = []

# Classes:

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __str__(self):
        return f"""
    Nome: {self.nome}
    CPF: {self.cpf}
    Data de nascimento: {self.data_nascimento}
"""
    

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
    

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        if valor < 0:
            print(f"Valor informado R${valor:.2f} é inválido! Forneça um valor maior que zero.")
            return False
        
        elif valor > saldo:
            print(f"Não foi possível realizar saque, saldo insuficiente.")
            return False   
        
        else:
            self._saldo -= valor
            print(f"Valor sacado com sucesso!(R${valor:.2f}).")
            return True
        
    def depositar(self, valor):
 
        if(valor <= 0):
            print(f"Valor informado R${valor} é inválido! Forneça um valor maior que zero.")
            return False
        
        else:
            self._saldo += valor
            print(f"Valor depositado com sucesso!(R${valor:.2f}).")
            print(f"Novo saldo: R${self._saldo:.2f}")
            return True
    
    def __str__(self):
        return f"""
    Títular: {self.cliente.nome}
    C/C: {self.numero}
    Ag: {self.agencia}
"""


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_de_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        if valor > self._limite:
            print(f"Erro! Valor {valor:.2f} excede o valor limite de saque!")
        elif numero_de_saques > self._limite_saques:
            print(f"Erro! Valor número de saques excedido.")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self) -> str:
        return super().__str__()


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor":transacao.valor,
                "data":strftime("%d-%m-%Y %H:%M:%S", gmtime())
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        status_transacao = conta.depositar(self.valor)

        if status_transacao:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):

        status_transacao = conta.sacar(self.valor)

        if status_transacao:
            conta.historico.adicionar_transacao(self)


# Funções:

def validar_cpf(cpf):
    try:
        cpf_input = int(cpf)
        cpf_pattern = r"\d{11}"
        if re.match(cpf_pattern, str(cpf_input)):
            return True
        else:
            return False
    except:
        return False


def verificar_contas_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui contas!")
        return
    else:
        return cliente.contas[0] # Implementar escolha de conta


def filtrar_cliente_por_cpf(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def cadastrar_cliente(clientes):
    while True:
        try:
            cpf_cliente = input("Informe o CPF (Somente número) Ou digite [0] para cancelar: ")
            cpf_valido = validar_cpf(cpf_cliente)

            # Opção para sair do menu
            if cpf_cliente == '0':
                return False
            
            if cpf_valido:
                cliente = filtrar_cliente_por_cpf(cpf_cliente, clientes)

                if cliente:
                    print("Erro! Cliente já cadastrado com esse CPF!")
                    return False
                else:

                    # Continuação processo de criação de usuário
                    nome_input = input("Informe o nome completo: ")
                    data_nascimento_input = input("Informe a data de nascimento(dd/mm/aaaa): ")
                    endereco_input = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

                    novo_cliente = PessoaFisica(cpf=cpf_cliente, nome=nome_input, data_nascimento=data_nascimento_input, endereco=endereco_input)
                    clientes.append(novo_cliente)
                    print(f'Usuário cadastrado com sucesso! {nome_input}/{cpf_cliente}')
                    input('Aperte "enter" para continuar. ')
                    return True
            else:
                print('CPF inválido, favor conferir o tamanho do CPF (11 dígitos)')
                continue
        except:
            print('Erro, processo cancelado.')
            return False
        

def listar_clientes(clientes):

    if len(clientes)>0:
        print(f'=-=-=-=-=-=-=-=-=-=Lista de Clientes-=-=-==-=-=-=-=-=-=')
        for cliente in clientes:
            print(str(cliente))
        print('‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
    else:
        print('Nenhum cliente cadastrado!')
    input('Aperte "enter" para continuar. ')


def criar_conta(*,clientes, contas, numero_conta):
    while True:
        try:
            cpf_cliente = input("Informe o CPF (Somente número) Ou digite [0] para cancelar: ")
            cpf_valido = validar_cpf(cpf_cliente)

            # Opção para sair do menu
            if cpf_cliente == '0':
                return False

            if cpf_valido:

                cliente = filtrar_cliente_por_cpf(cpf_cliente, clientes)
                if not cliente:
                    print("Erro! Cliente não encontrado.")
                    return False
                    
                else:
                    nova_conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)

                    contas.append(nova_conta)

                    cliente.contas.append(nova_conta)
                    print(f'Conta criada com sucesso!\nAgência: 0001\nNúmero da conta: {numero_conta}\nCliente: {cliente.nome}')
                    input('Aperte "enter" para continuar. ')
                    return True
            else:
                print('CPF inválido, favor conferir o tamanho do CPF (11 dígitos)')
                continue
        except:
            print("Erro! processo cancelado.")
            return False
        

def listar_contas(contas):
    print(f'=-=-=-=-=-=-=-=-=-=Lista de Contas-=-=-==-=-=-=-=-=-=')
    for conta in contas:
        print(str(conta))
        print('‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
    input('Aperte "enter" para continuar. ')


def movimentar_valor(clientes,tipo_operacao,/):

    while True:
        cpf_cliente = input("Informe o CPF (Somente número) Ou digite [0] para cancelar: ")
        cpf_valido = validar_cpf(cpf_cliente)

        if cpf_cliente == 0:
            return False
        
        if cpf_valido:
            cliente = filtrar_cliente_por_cpf(cpf_cliente, clientes)

            if not cliente:
                print("Erro! Cliente não encontrado.")
                return False
            
            else:
                print("CPF correto! Prosseguindo operação...")
                try:
                    valor_operacao = float(input(f"Informe o valor de {tipo_operacao} Ou digite [0] para Voltar: "))
                    if(valor_operacao <= 0):
                        return False
                    else:
                        # Tipo de operação Saque
                        if(tipo_operacao == "saque"):
                            print("aqui entrou sac")
                            transacao = Saque(valor_operacao)

                        # Tipo de operação Depósito
                        elif(tipo_operacao == "deposito"):
                            print("aqui entrou")
                            transacao = Deposito(valor_operacao)

                        conta = verificar_contas_cliente(cliente)
                        if not conta:
                            print("Erro, transação não realizada, sua conta não foi encontrada, consulte seu gerente.")
                            return False
                        print("CHEGOU pós conta")
                        cliente.realizar_transacao(conta, transacao)
                        print("CHEGOU pós conta2")
                        print("Transação realizada com sucesso!")
                        return True

                except:
                    print("Erro, transação cancelada.")
                    return False
        else:
            print("CPF inválido, informe um CPF válido.")
            continue


def mostrar_extrato(clientes):
    while True:
        cpf_cliente = input("Informe o CPF (Somente número) Ou digite [0] para cancelar: ")
        cpf_valido = validar_cpf(cpf_cliente)
        if cpf_cliente == 0:
            return False

        if cpf_valido:
            cliente = filtrar_cliente_por_cpf(cpf_cliente, clientes)
            if not cliente:
                print("Erro! Cliente não encontrado.")
                return False
            else:
                conta = verificar_contas_cliente(cliente)
                if not conta:
                    print("Erro, sua conta não foi encontrada, consulte seu gerente.")
                    return False
                # Caso todas as etapas de confirmação estejam corretas:
                transacoes = conta.historico.transacoes
                extrato = ''

                # Verifica se o extrato está vazio.
                if not transacoes:
                    print(
'''=-=-=-=-=-=-=-=-=-=Extrato-=-=-==-=-=-=-=-=-=
    Conta ainda não realizou nenhuma movimentação.
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾''')
                    input('Aperte "enter" para continuar. ')
                    return False
                else:
                    print(
f'''=-=-=-=-=-=-=-=-=-=Extrato-=-=-==-=-=-=-=-=-=
    Seu saldo atual é: R${conta.saldo:.2f}
    OPERAÇÃO   |    VALOR       | Data''')
                    for transacao in transacoes:
                        extrato += f"    {transacao['tipo']}   |   R${transacao['valor']}        | {transacao['data']}\n"
                    print(extrato)
                    input('Aperte "enter" para continuar. ')
                    return True
        else:
            print("CPF inválido, insira um CPF válido.")

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
    [4] - Cadastrar cliente
    [5] - Criar conta
    [6] - Listar clientes
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
                    movimentar_valor(clientes,"deposito")
                    continue
                case 2:
                    movimentar_valor(clientes,"saque")
                    continue
                case 3:
                    mostrar_extrato(clientes)
                    continue
                case 4:
                    cadastrar_cliente(clientes=clientes)
                    continue
                case 5:
                    criar_conta(clientes=clientes, contas=contas, numero_conta=len(contas) +1)
                    continue
                case 6:
                    listar_clientes(clientes)
                    continue
                case 7:
                    listar_contas(contas)
                    continue
                case _:
                    print('Opção inválida.')
                    continue
        except:
            print('Opção inválida.')
            continue
    

menu_inicial()