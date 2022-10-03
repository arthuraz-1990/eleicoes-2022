import requests
import json
import pandas as pd
import time
import os

import html

from datetime import datetime

def update_resultados() -> float:
    try: 
        data = requests.get(
            'https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/br/br-c0001-e000544-r.json', timeout=10)
    except:
        print('Não foi possível atualizar os resultados.')
        return 0
    else: 
        if data and data.content:
            json_data = json.loads(data.content)
            candidato = []
            votos = []
            porcento = []

            for info in json_data['cand']:
                candidato.append(html.unescape(info['nm']))
                votos.append(info['vap'])
                porcento.append(info['pvap'])

            os.system('clear')
            current_date = datetime.now()
            print(f'Situação em {current_date.strftime("%d/%m/%Y %H:%M:%S")}')

            pc_total: str = json_data['pst']

            print(f'Horário da ultima atualização: {json_data["ht"]}')
            print(f'Total apurado: {json_data["c"]} / {pc_total}%')
            eleicao = pd.DataFrame(list(zip(candidato, votos, porcento)), columns=[
                'Candidato', 'Total de Votos', '%'
            ])

            print(eleicao)

            return float(pc_total.replace(',', '.'))
        else:
            print('Não foi possível recuperar o resultado.')
            return 0        


pc_total = update_resultados()

while pc_total < 100:
    time.sleep(30)
    print('Atualizando...')
    last_pc_total = update_resultados()
    if pc_total < last_pc_total:
        pc_total = last_pc_total

print('Fim da Eleição!!!')