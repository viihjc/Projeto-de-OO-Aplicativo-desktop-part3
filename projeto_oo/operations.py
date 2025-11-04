from models.base import get_session, Base, engine
from models.client import Client
from models.account import Account
from models.checking_account import CheckingAccount
from models.savings_account import SavingsAccount
from models.extrato import Extrato
from models.tax_rate_provider import TaxRateProvider
from services.notification_service import NotificationService

def gerar_numero_conta(session):
    ultima = session.query(Account).order_by(Account.id.desc()).first()
    if ultima and ultima.number:
        try:
            novo = int(ultima.number) + 1
        except ValueError:
            novo = 100000001
    else:
        novo = 100000001
    return str(novo).zfill(9)

def criar_conta():
    session = get_session()
    try:
        print("\n=== CRIAÇÃO DE CONTA ===")

        nome = input("Nome do cliente: ").strip()
        if not nome.replace(" ", "").isalpha():
            print("❌ Nome inválido❌\n Use apenas letras e espaços.")
            return

        tipo = input("Tipo de conta (corrente/poupanca): ").strip().lower()
        if tipo not in ["corrente", "poupanca"]:
            print("❌ Tipo de conta inválido ❌")
            return

        try:
            saldo_inicial = float(input("Saldo inicial R$: ").replace(",", "."))
            if saldo_inicial < 0:
                raise ValueError
        except ValueError:
            print("❌ Valor inválido para saldo inicial ❌")
            return

        cliente = session.query(Client).filter_by(name=nome).first()
        if not cliente:
            cliente = Client(name=nome)
            session.add(cliente)
            session.flush() 

        numero = gerar_numero_conta(session)

        if tipo == "poupanca":
            try:
                meses = int(input("Por quantos meses planeja deixar o dinheiro na poupança? ").strip())
                if meses <= 0:
                    raise ValueError
            except ValueError:
                print("❌ Valor inválido ❌ Digite um número inteiro positivo.")
                session.rollback()
                return

            tax_provider = TaxRateProvider()
            rendimento = tax_provider.calcular_rendimento(saldo_inicial, meses)
            saldo_final = saldo_inicial + rendimento

            conta = SavingsAccount(
                number=numero,
                balance=saldo_final,
                client_id=cliente.id
            )
            session.add(conta)
            session.flush()

            print(f"📈 Rendimento aplicado: +R${rendimento:.2f} em {meses} meses.")
            print(f"📘 Número da conta gerado: {conta.number}")
            print(f"💰 Saldo final inicial: R${saldo_final:.2f}")

        else:
            try:
                limite = float(input("Limite de saque R$: ").replace(",", "."))
                if limite < 0:
                    raise ValueError
            except ValueError:
                print("❌ Valor inválido ❌ Digite um número positivo.")
                session.rollback()
                return

            conta = CheckingAccount(
                number=numero,
                balance=saldo_inicial,
                client_id=cliente.id,
                limit=limite
            )
            session.add(conta)
            session.flush()

            print(f"📘 Número da conta gerado: {conta.number}")
            print(f"💰 Saldo inicial: R${saldo_inicial:.2f}")
            print(f"💳 Limite de saque: R${limite:.2f}")

        sinal = "+" if saldo_inicial >= 0 else "-"
        description = f"Abertura: {sinal}R${abs(saldo_inicial):.2f}"
        extrato_entry = Extrato(account=conta, description=description)
        session.add(extrato_entry)

        session.commit()

        notifier = NotificationService()
        notifier.notify(cliente.name, f"Sua conta {tipo} foi criada com sucesso com número {conta.number}.")

    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao criar conta: {e}")
    finally:
        session.close()


def depositar():
    session = get_session()
    try:
        print("\n=== DEPÓSITO ===")
        numero = input("Número da conta: ").strip()
        if not numero:
            print("❌ Número da conta não pode estar vazio ❌")
            return

        conta = session.query(Account).filter_by(number=numero).first()
        if not conta:
            print("❌ Conta não encontrada ❌")
            return

        try:
            valor = float(input("Valor para depósito R$: ").replace(",", "."))
            if valor <= 0:
                raise ValueError
        except ValueError:
            print("❌ Valor inválido para depósito ❌")
            return

        conta.balance = (conta.balance or 0.0) + valor
        
        description = f"Depósito: +R${valor:.2f}"
        extrato = Extrato(account=conta, description=description)
        session.add(extrato)
        
        session.commit()

        notifier = NotificationService()
        notifier.notify(conta.client.name, f"Depósito de R${valor:.2f} realizado com sucesso.")
        print(f"💰 Depósito de R${valor:.2f} realizado. Saldo atual: R${conta.balance:.2f}")

    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao depositar: {e}")
    finally:
        session.close()

def sacar():
    session = get_session()
    try:
        print("\n=== SAQUE ===")
        numero = input("Número da conta: ").strip()
        if not numero:
            print("❌ Número da conta não pode estar vazio ❌")
            return

        conta = session.query(Account).filter_by(number=numero).first()
        if not conta:
            print("❌ Conta não encontrada ❌")
            return

        try:
            valor = float(input("Valor para saque R$: ").replace(",", "."))
            if valor <= 0:
                raise ValueError
        except ValueError:
            print("❌ Valor inválido para saque ❌")
            return

        if hasattr(conta, "limit"):
            if valor > (conta.limit or 0.0):
                print(f"❌ Valor do saque excede o limite permitido. Limite: R${conta.limit:.2f}")
                return
            
            if valor > (conta.balance or 0.0):
                print(f"❌ Saldo insuficiente. Saldo atual: R${conta.balance:.2f}")
                return
                
            conta.balance -= valor
            
        else:
            if valor > (conta.balance or 0.0):
                print(f"❌ Saldo insuficiente. Saldo atual: R${conta.balance:.2f}")
                return
            conta.balance -= valor

        description = f"Saque: -R${valor:.2f}"
        extrato = Extrato(account=conta, description=description)
        session.add(extrato)
        
        session.commit()

        notifier = NotificationService()
        notifier.notify(conta.client.name, f"Saque de R${valor:.2f} realizado.")
        
        if hasattr(conta, "limit"):
            print(f"💸 Saque de R${valor:.2f} realizado com sucesso!")
            print(f"💰 Saldo atual: R${conta.balance:.2f}")
            print(f"💳 Limite por saque: R${conta.limit:.2f}")
        else:
            print(f"💸 Saque de R${valor:.2f} realizado. Saldo atual: R${conta.balance:.2f}")

    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao sacar: {e}")
    finally:
        session.close()

def ver_extrato():
    session = get_session()
    try:
        print("\n=== EXTRATO ===")
        numero = input("Número da conta: ").strip()
        if not numero:
            print("❌ Número da conta não pode estar vazio ❌")
            return

        conta = session.query(Account).filter_by(number=numero).first()
        if not conta:
            print("❌ Conta não encontrada ❌")
            return

        entries = conta.extratos
        print(f"\n{'='*60}")
        print(f"📊 EXTRATO DA CONTA {conta.number}")
        print(f"{'='*60}")

        if not entries:
            print("📭 Nenhuma movimentação registrada.")
        else:
            for i, entry in enumerate(entries, start=1):
                date_str = entry.date.strftime("%d/%m/%Y %H:%M")
                print(f"{i:2d}. {date_str} - {entry.description}")

        print(f"{'='*60}")
        print(f"💰 SALDO ATUAL: R${conta.balance:.2f}")
        print(f"{'='*60}")

    except Exception as e:
        print(f"❌ Erro ao ver extrato: {e}")
    finally:
        session.close()

def listar_contas():
    session = get_session()
    try:
        print("\n=== LISTA DE CONTAS ===")
        contas = session.query(Account).all()
        if not contas:
            print("Nenhuma conta cadastrada.")
            return

        for conta in contas:
            tipo = "Corrente" if conta.type == "checking_account" else "Poupança"
            print(f"📄 {conta.number} - {conta.client.name} - {tipo} - R$ {conta.balance:.2f}")

    except Exception as e:
        print(f"❌ Erro ao listar contas: {e}")
    finally:
        session.close()