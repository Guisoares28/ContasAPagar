import decimal
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DECIMAL, Integer,DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

engine= create_engine('sqlite:///contas.db', echo= True)
Base = declarative_base()
#criando sessao
Session = sessionmaker(bind=engine)
session = Session()


class Conta(Base):
    __tablename__ = 'ContasAPagar'

    id = Column(Integer, primary_key=True,autoincrement=True)
    descricao = Column(String)
    dataVencimento = Column(DateTime)
    valor = Column(DECIMAL)

    def __repr__(self):
        return f'Descrição: {self.descricao,} valor:{self.valor} Vencimento:{self.dataVencimento}'

     # Função para cadastrar usuarios no banco de dados.
    def cadastrarConta(self):

        print("****CADASTRO DE CONTAS****")
        descricao = input("Descrição da conta: ").lower()
        while(True):
            try:
                valor = input("Digite o valor: ")
                valor_decimal = Decimal(valor)
                break
            except decimal.InvalidOperation:
                print("\nValor incorreto por gentileza forneça um valor no formato correto !!!!")

        while(True):
            try:
                data = str(input("Qual a data de vencimento dd/mm/aa: " ))
                date_Obejct = datetime.strptime(data, "%d/%m/%Y")
                data_atual = datetime.today()
                if (date_Obejct < data_atual):
                    print("A data informada é menor do que a data atual !!!!")
                    rep = input("\nDeseja cadastrar mesmo assim? (s/n): ").lower()
                    if (rep == "n"):
                        continue
                    else:
                        break
            except ValueError:
                print("\nPor favor insira um data correta no formato dd/mm/aaaa !!!!")
        try:
            newConta = Conta(descricao=descricao, valor=valor_decimal, dataVencimento=date_Obejct)
            session.add(newConta)
            session.commit()
            print("\nConta adicionada com sucesso...")
        except Exception:
            print("Houve algum problema ao tentar adicionar a conta! tente novamente")


    def consultarTodasAsContas(self):
        contas = session.query(Conta).all()
        print("****CONTAS****")
        for conta in contas:
            print(conta)
            print("*"*100)
        return contas
