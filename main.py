import folium
import pandas as pd
import requests

# API key e URL da Open Charge Map
API_KEY = "70826310-b7b0-4e58-ac38-4e2a7984ab62"
BASE_URL = "https://api.openchargemap.io/v3/poi/"

# Parâmetros da requisição
params = {
    "output": "json",
    "countrycode": "BR",  # Brasil
    "maxresults": 1000,  # Número de resultados
    "compact": True,  # Retorno compacto
    "verbose": False,
    "key": API_KEY
}

# Enviando a requisição
response = requests.get(BASE_URL, params=params)

# Processando a resposta
if response.status_code == 200:
    charging_points = response.json()
    print(f"Total de pontos encontrados: {len(charging_points)}")
    
    # Criando um mapa centralizado no Brasil
    map_brazil = folium.Map(location=[-14.2350, -51.9253], zoom_start=5)  # Coordenadas aproximadas do Brasil

    # Iterando sobre os pontos de carregamento para adicionar no mapa
    for point in charging_points:
        name = point.get('AddressInfo', {}).get('Title', 'Desconhecido')
        latitude = point.get('AddressInfo', {}).get('Latitude')
        longitude = point.get('AddressInfo', {}).get('Longitude')

        # Adicionando marcador no mapa para cada ponto de carregamento
        if latitude and longitude:
            folium.Marker(
                location=[latitude, longitude],
                popup=f"<strong>{name}</strong><br>Lat: {latitude}<br>Lon: {longitude}",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(map_brazil)
    
    # Salvar o mapa em um arquivo HTML
    map_brazil.save("mapa_pontos_carregamento.html")
    print("Mapa gerado e salvo como 'mapa_pontos_carregamento.html'")

else:
    print(f"Erro ao acessar API: {response.status_code}")