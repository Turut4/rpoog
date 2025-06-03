from abc import ABC, abstractmethod
from .entidades import Raca, Classe, Atributos
from .itens import Item, Arma, Pocao, RaridadeItem


class ItemFactory:
    """Factory Method para criar diferentes tipos de Item."""

    def criar_item(self, tipo_item: str, **kwargs) -> Item:
        if tipo_item == 'arma':
            return Arma(**kwargs)
        if tipo_item == 'pocao':
            return Pocao(**kwargs)
        raise ValueError(f"Tipo de item desconhecido: {tipo_item}")


class IPersonagemFactory(ABC):
    """Interface da Abstract Factory para criar kits de personagem."""
    @abstractmethod
    def criar_raca(self) -> Raca: pass
    @abstractmethod
    def criar_classe(self) -> Classe: pass
    @abstractmethod
    def definir_atributos_base(self) -> dict: pass
    @abstractmethod
    def criar_equipamento_inicial(self) -> list[Item]: pass


class GuerreiroFactory(IPersonagemFactory):
    """Fábrica concreta para o arquetipo Guerreiro."""

    def criar_raca(self) -> Raca:
        return Raca("Anão", Atributos(forca=2, vigor=2, sorte=-1))

    def criar_classe(self) -> Classe:
        return Classe("Guerreiro")

    def definir_atributos_base(self) -> dict:
        return {'forca': 10, 'inteligencia': 4, 'destreza': 6, 'vigor': 8, 'sorte': 5}

    def criar_equipamento_inicial(self) -> list[Item]:
        item_factory = ItemFactory()
        arma = item_factory.criar_item(
            'arma', nome="Machado de Anão", descricao="Um machado robusto.", peso=5.0, raridade=RaridadeItem.INCOMUM, dano=12)
        pocao = item_factory.criar_item('pocao', nome="Poção de Cura Menor",
                                        descricao="Restaura um pouco de vida.", peso=0.5, raridade=RaridadeItem.COMUM, cura=20)
        return [arma, pocao]


class MagoFactory(IPersonagemFactory):
    """Fábrica concreta para o arquetipo Mago."""

    def criar_raca(self) -> Raca:
        return Raca("Elfo", Atributos(inteligencia=2, destreza=2, vigor=-1))

    def criar_classe(self) -> Classe:
        return Classe("Mago")

    def definir_atributos_base(self) -> dict:
        return {'forca': 4, 'inteligencia': 32, 'destreza': 8, 'vigor': 5, 'sorte': 7}

    def criar_equipamento_inicial(self) -> list[Item]:
        item_factory = ItemFactory()
        arma = item_factory.criar_item(
            'arma', nome="Cajado Místico", descricao="Canaliza poder arcano.", peso=2.0, raridade=RaridadeItem.INCOMUM, dano=4)
        return [arma]
