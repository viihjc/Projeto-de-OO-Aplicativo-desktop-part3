from operations import criar_conta, depositar, sacar, ver_extrato, listar_contas
from models.base import Base, engine

def menu_principal():
    while True:
        print("\n" + "="*40)
        print("=== SISTEMA BANCÁRIO ===")
        print("="*40)
        print("1 - Criar conta")
        print("2 - Depositar")
        print("3 - Sacar")
        print("4 - Ver extrato")
        print("5 - Listar todas as contas")
        print("0 - Sair")
        print("="*40)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            criar_conta()
        elif opcao == "2":
            depositar()
        elif opcao == "3":
            sacar()
        elif opcao == "4":
            ver_extrato()
        elif opcao == "5":
            listar_contas()
        elif opcao == "0":
            print("Saindo do sistema... Até logo! 👋")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

def main():
    Base.metadata.create_all(engine)
    print("=== SISTEMA BANCÁRIO INICIADO ===")
    menu_principal()

if __name__ == "__main__":
    main()