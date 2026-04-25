# Teste de git

# definição de um dicionario com os meses numéricos como chave e meses por extenso como valor
meses = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}

import pandas as pd

tabela = pd.DataFrame()

tabela['Meses'] = meses.values()

