# entidades.py

from __future__ import annotations
from itens import Inventario, Arma
from patterns import IEstrategiaAtaque


class Atributos:
    """Armazena os atributos e o estado de um personagem."""

    def __init__(self, forca=0, inteligencia=0, destreza=0, vigor=0, sorte=0):
        self.forca = forca
        self.inteligencia = inteligencia
        self.destreza = destreza
        self.vigor = vigor
        self.sorte = sorte
        self.vida_maxima = 20 + (vigor * 5)
        self.vida_atual = self.vida_maxima

    def __str__(self):
        return f"For:{self.forca}, Int:{self.inteligencia}, Des:{self.destreza}, Vig:{self.vigor}, Sor:{self.sorte}"


class Raca:
    """Representa a Raça de um personagem."""

    def __init__(self, nome, atributo_bonus: Atributos):
        self.nome = nome
        self.atributo_bonus = atributo_bonus


class Classe:
    """Representa a Classe de um personagem."""

    def __init__(self, nome):
        self.nome = nome


class Personagem:
    """Representa o personagem final, pronto para interação."""

    def __init__(self, nome):
        self.nome = nome
        self.raca: Raca | None = None
        self.classe: Classe | None = None
        self.atributos: Atributos = Atributos()
        self.inventario: Inventario = Inventario(capacidade=10)
        self.estrategia_ataque: IEstrategiaAtaque | None = None

    def definir_estrategia_ataque(self, estrategia: IEstrategiaAtaque):
        self.estrategia_ataque = estrategia

    def executar_ataque(self, alvo: Personagem):
        if self.estrategia_ataque:
            self.estrategia_ataque.atacar(self, alvo)
        else:
            print(f"{self.nome} não sabe como atacar!")

    def receber_dano(self, dano: int):
        dano_real = max(0, dano)
        self.atributos.vida_atual -= dano_real
        print(f"-> {self.nome} recebeu {dano_real} de dano! Vida: {self.atributos.vida_atual}/{self.atributos.vida_maxima}")
        if not self.esta_vivo():
            print(f"-> {self.nome} foi derrotado!")

    def esta_vivo(self) -> bool:
        return self.atributos.vida_atual > 0

    def get_arma_equipada(self) -> Arma | None:
        for item in self.inventario.itens:
            if isinstance(item, Arma):
                return item
        return None

    def __str__(self):
        status_vida = f"HP: {self.atributos.vida_atual}/{self.atributos.vida_maxima}"
        return (
            f"========================================\n"
            f" {self.nome} | {self.raca.nome if self.raca else ''} {self.classe.nome if self.classe else ''} | {status_vida}\n"
            f"----------------------------------------\n"
            f" Atributos: [{self.atributos}]\n"
            f"----------------------------------------\n"
            f"{self.inventario}"
            f"========================================\n"
        )
