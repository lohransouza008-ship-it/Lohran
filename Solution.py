import datetime
import requests

def cotar():
    lista = []
    hoje = datetime.date.today()

    # de 364 dias atrás até hoje = 365 dias
    for i in range(364, -1, -1):
        data = hoje - datetime.timedelta(days=i)
        data_str = data.strftime("%m-%d-%Y") # formato que o BC espera

        url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data_str}'&$top=1&$format=json"

        try:
            resp = requests.get(url, timeout=10)
            dados = resp.json()

            if dados.get('value'):
                # pegou cotação do dia
                cotacao = dados['value'][0]['cotacaoCompra']
            else:
                # sem cotação (fds/feriado) - repete a última
                cotacao = lista[-1] if lista else 0
        except:
            # se der erro de rede, repete a última também
            cotacao = lista[-1] if lista else 0

        lista.append(cotacao)

    return lista

# pra testar local:
if __name__ == "__main__":
    print(cotar())