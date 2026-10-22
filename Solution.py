import requests
import folium
from folium.plugins import MarkerCluster

TOKEN = 9f4d1f2f53b5f131e2552c848ac28a13302a36f3f73cbe57153b381d928bf589
BASE = "http://api.olhovivo.sptrans.com.br/v2.1"
LINHA = "8000-10" # DIFERENTE do slide que é 175T-10

session = requests.Session()

def autenticar():
    url = f"{BASE}/Login/Autenticar?token={TOKEN}"
    r = session.post(url)
    return r.text == "true"

def solution():
    # 1. Autentica
    autenticar()

    # 2. Busca linha
    linha = session.get(f"{BASE}/Linha/Buscar?termosBusca={LINHA}").json()[0]
    codigo = linha['cl']
    print(f"Linha encontrada: {linha['lt']}")

    # 3. Busca paradas
    paradas = session.get(f"{BASE}/Parada/BuscarParadasPorLinha?codigoLinha={codigo}").json()

    # 4. Posição em tempo real
    pos = session.get(f"{BASE}/Posicao?codigoLinha={codigo}").json()
    onibus = pos.get('vs', [])

    # 5. Cria mapa - REQUISITO PRINCIPAL
    lat = sum(p['py'] for p in paradas) / len(paradas)
    lon = sum(p['px'] for p in paradas) / len(paradas)
    mapa = folium.Map(location=[lat, lon], zoom_start=13)

    cluster = MarkerCluster().add_to(mapa)
    for p in paradas:
        # PIN AZUL PARA PARADA
        folium.Marker([p['py'], p['px']], popup=p['np'],
                      icon=folium.Icon(color='blue', icon='info-sign')).add_to(cluster)

    for o in onibus:
        # PIN VERMELHO PARA ÔNIBUS - cor diferente
        folium.Marker([o['py'], o['px']], popup=f"Ônibus {o['p']}",
                      icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(mapa)

    mapa.save("mapa_frota_8000_10.html")
    print(f"Mapa criado com {len(paradas)} paradas e {len(onibus)} ônibus")

if _name_ == "_main_":
    solution()
