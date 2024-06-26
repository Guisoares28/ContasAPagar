import decimal
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, String, DECIMAL, Integer,DateTime,Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

engine= create_engine('sqlite:///contas.db', echo= True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
class Conta(Base):
    __tablename__ = 'ContasAPagar'

    id = Column(Integer, primary_key=True,autoincrement=True, unique=True)
    descricao = Column(String)
    dataVencimento = Column(DateTime)
    valor = Column(DECIMAL)
    status = Column(Boolean)

    def __repr__(self):
        return f'id: {self.id} Descrição: {self.descricao,} valor:{self.valor} Vencimento:{self.dataVencimento} Status:{self.status}'

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
                else:
                    break
            except ValueError:
                print("\nPor favor insira um data correta no formato dd/mm/aaaa !!!!")
        try:
            newConta = Conta(descricao=descricao, valor=valor_decimal, dataVencimento=date_Obejct, status=False)
            session.add(newConta)
            session.commit()
            session.close()
            print("\nConta adicionada com sucesso...")
        except Exception as e:
            logging.error(f"Ocorreu um erro: {str(e)}")

    # Função para consultar todas as contas a pagar cadastradas
    def consultarTodasAsContas(self):
        contas = session.query(Conta).all()
        print("****CONTAS****")
        for conta in contas:
            print(conta)
            print("*"*100)
        session.close()
        return contas

    # Função para deletar contas por id
    def deletarConta(self):
        print("****CONTAS****")
        contas = Conta.consultarTodasAsContas(self)
        while(True):
            while(True):
                try:
                    contaDeletada = int(input("\nQual id da conta deseja deletar: "))
                    contaBuscada = session.query(Conta).filter_by(id=contaDeletada).first()
                    break
                except ValueError:
                    print("\nid informado está incorreto !!!")
            if contaBuscada:
                session.delete(contaBuscada)
                session.commit()
                session.close()
                print("\nConta deletada com Sucesso!!!")
                break
            else:
                print("\nNão existe nenhuma conta vinculada a este id !!!")




