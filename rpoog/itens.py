from enum import Enum


class RaridadeItem(Enum):
    COMUM = "Comum"
    INCOMUM = "Incomum"
    RARO = "Raro"


class TipoItem(Enum):
    ARMA = "Arma"
    POCAO = "Po��o"
    GENERICO = "Gen�rico"


class Item:
    """Classe base para todos os itens do jogo."""

    def __init__(self, nome: str, descricao: str, peso: float, raridade: RaridadeItem, tipo: TipoItem):
        self.nome, self.descricao, self.peso, self.raridade, self.tipo = nome, descricao, peso, raridade, tipo

    def __str__(self):
        return f"- {self.nome} ({self.raridade.value})"


class Arma(Item):
    """Uma especialização de Item."""

    def __init__(self, nome: str, descricao: str, peso: float, raridade: RaridadeItem, dano: int):
        super().__init__(nome, descricao, peso, raridade, TipoItem.ARMA)
        self.dano = dano

    def __str__(self):
        return f"- {self.nome} (Dano: {self.dano}, {self.raridade.value})"


class Pocao(Item):
    """Outra especialização de Item."""

    def __init__(self, nome: str, descricao: str, peso: float, raridade: RaridadeItem, cura: int):
        super().__init__(nome, descricao, peso, raridade, TipoItem.POCAO)
        self.cura = cura

    def __str__(self):
        return f"- {self.nome} (Cura: {self.cura}, {self.raridade.value})"


class Inventario:
    """Gerencia os itens de um personagem."""

    def __init__(self, capacidade: int):
        self.capacidade = capacidade
        self.itens = []

    def adicionar_item(self, item: Item) -> bool:
        if len(self.itens) < self.capacidade:
            self.itens.append(item)
            return True
        return False

    def __str__(self):
        if not self.itens:
            return "Inventário: Vazio"
        lista_itens = "\n".join([f"  {item}" for item in self.itens])
        return f"Invent�rio ({len(self.itens)}/{self.capacidade}):\n{lista_itens}"
