import requests
import time
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class TelegramBot:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="bb5171ed113342d7ac82b608e47cf68f", client_secret="5adcdff072b74aefa28c16b9605d9069"))
        token = '1422681702:AAGMBF4EGINCKTq8U6QlctyBdh9K9j-WjKc'
        self.url_base = f'https://api.telegram.org/bot{token}/'
        self.msg_boas_vindas = ('menu', 'Menu', 'ola', 'olá', 'oi', 'teste', '/start')
        self.qtdRegistros = 1
        self.enviadoResultado = False

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_novas_mensagens(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    mensagem = str(dado["message"]["text"])
                    chat_id = dado["message"]["from"]["id"]
                    eh_primeira_mensagem = int(dado["message"]["message_id"]) == 1
                    resposta = self.criar_resposta(mensagem, eh_primeira_mensagem)
                    self.responder(resposta, chat_id)
                    if self.enviadoResultado == True:
                        resposta = f'''Gostou do resultado?{os.linesep}{os.linesep}Caso queira pesquisar uma nova música ou artista, basta digitar o nome.{os.linesep}{os.linesep}Para reiniciar, digite "/start"'''
                        self.responder(resposta, chat_id)
                        self.enviadoResultado = False

    # Obter mensagens
    def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    
    # Criar uma resposta
    def criar_resposta(self, mensagem, eh_primeira_mensagem):
        if eh_primeira_mensagem == True or mensagem.lower() in self.msg_boas_vindas:
            return f'''Olá bem vindo a Hu3diger's bot... {os.linesep}{os.linesep}Antes de disponibilizar a pesquisa, digite o número máximo de registros que deseja visualizar.'''
        elif mensagem.isnumeric():
            self.qtdRegistros = int(mensagem)
            return f'''Certo, agora sei que você quer ver {self.qtdRegistros} registros.{os.linesep}{os.linesep}Vamos lá!{os.linesep}Digite o nome ou artista da música'''
        else:
            results = self.sp.search(q=mensagem, limit=self.qtdRegistros)
            msg = f'''Encontrei estes resultados para a sua pesquisa...{os.linesep}{os.linesep}'''
            for idx, track in enumerate(results['tracks']['items']):
                strArtists = ''
                for index, artist in enumerate(track['artists']):
                    strArtists = strArtists + artist['name'] + ','
                msg = msg + f'''Título: {track['name']} {os.linesep}Artista: {strArtists}{os.linesep}Link de acesso: {track['external_urls']['spotify']}{os.linesep}{os.linesep}'''
            self.enviadoResultado = True
            
            return msg
    # Responder
    def responder(self, resposta, chat_id):
        link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_requisicao)


bot = TelegramBot()
bot.Iniciar()