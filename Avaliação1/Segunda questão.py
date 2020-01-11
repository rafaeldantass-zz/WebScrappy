#Importando o scrapy

import scrapy
from scrapy.utils.response import open_in_browser


class MercadoSpider(scrapy.Spider):
    #Nomeando a classe
    name = "MercadoSpider"

    def _init_(self, produto="", **kwargs):
        self.start_urls = {"https://lista.mercadolivre.com.br/%s" % produto}
        super()._init_(**kwargs)

    
    def parse(self, response):
        nomes_produtos = response.css(".main-title::text").extract()
        preco_produtos = []

        for item in response.css(".item__price"):
            preco = item.css(".price__fraction::text").extract_first()

            if item.css(".price__decimals::text").extract_first():
                preco += "," + item.css(".price__decimals::text").extract_first()

            preco_produtos.append(preco)

        for nome, preco in zip(nomes_produtos, preco_produtos):
            yield {
                "nome" : nome,
                "preco" : preco
            }
        pagination = response.xpath("//ul[@role]/li[last()]/a")
		
