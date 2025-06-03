# patterns.py

from __future__ import annotations
from abc import ABC, abstractmethod
from .entidades import Personagem, Raca, Classe, Atributos
from .itens import Item


class IBuilderPersonagem(ABC):
    """Interface do Builder."""
    @abstractmethod
    def set_nome(self, nome: str) -> IBuilderPersonagem: pass
    @abstractmethod
    def set_raca(self, raca: Raca) -> IBuilderPersonagem: pass
    @abstractmethod
    def set_classe(self, classe: Classe) -> IBuilderPersonagem: pass
    @abstractmethod
    def set_atributos_base(self, **kwargs) -> IBuilderPersonagem: pass
    @abstractmethod
    def adicionar_item_inicial(self, item: Item) -> IBuilderPersonagem: pass
    @abstractmethod
    def get_personagem(self) -> Personagem: pass


class BuilderPersonagem(IBuilderPersonagem):
    """Implementação concreta do Builder."""

    def __init__(self):
        self.reset()

    def reset(self):
        self._personagem = Personagem("")

    def set_nome(self, nome: str) -> BuilderPersonagem:
        self._personagem.nome = nome
        return self

    def set_raca(self, raca: Raca) -> BuilderPersonagem:
        self._personagem.raca = raca
        return self

    def set_classe(self, classe: Classe) -> BuilderPersonagem:
        self._personagem.classe = classe
        return self

    def set_atributos_base(self, **kwargs) -> BuilderPersonagem:
        self._personagem.atributos = Atributos(**kwargs)
        return self

    def adicionar_item_inicial(self, item: Item) -> BuilderPersonagem:
        self._personagem.inventario.adicionar_item(item)
        return self

    def _aplicar_bonus_raciais(self):
        if self._personagem.raca:
            bonus, attrs = self._personagem.raca.atributo_bonus, self._personagem.atributos
            attrs.forca += bonus.forca
            attrs.inteligencia += bonus.inteligencia
            attrs.destreza += bonus.destreza
            attrs.vigor += bonus.vigor
            attrs.sorte += bonus.sorte
            attrs.vida_maxima = 20 + (attrs.vigor * 5)
            attrs.vida_atual = attrs.vida_maxima

    def get_personagem(self) -> Personagem:
        self._aplicar_bonus_raciais()
        personagem_pronto = self._personagem
        self.reset()
        return personagem_pronto


class IEstrategiaAtaque(ABC):
    """Interface para as Estratégias de ataque."""
    @abstractmethod
    def atacar(self, atacante: Personagem, alvo: Personagem):
        pass


class AtaqueFisico(IEstrategiaAtaque):
    """Estratégia para ataques com Força e Arma."""

    def atacar(self, atacante: Personagem, alvo: Personagem):
        arma = atacante.get_arma_equipada()
        if not arma:
            dano = atacante.atributos.forca // 2
            print(f"{atacante.nome} ataca com os punhos!")
        else:
            dano = atacante.atributos.forca + arma.dano
            print(f"{atacante.nome} ataca com {arma.nome}!")
        alvo.receber_dano(dano)


class AtaqueMagico(IEstrategiaAtaque):
    """Estratégia para ataques com Inteligência."""

    def atacar(self, atacante: Personagem, alvo: Personagem):
        print(f"{atacante.nome} conjura uma bola de fogo contra {alvo.nome}!")
        dano = atacante.atributos.inteligencia * 2
        alvo.receber_dano(dano)
