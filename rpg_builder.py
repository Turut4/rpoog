# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

# =============================================================================
# 1. CLASSES BASE (Inspiradas no seu diagrama)
# =============================================================================


class Atributos:
    """Armazena os atributos de um personagem."""

    def __init__(self, forca=0, inteligencia=0, destreza=0, vigor=0, sorte=0):
        self.forca = forca
        self.inteligencia = inteligencia
        self.destreza = destreza
        self.vigor = vigor
        self.sorte = sorte

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

# =============================================================================
# 2. O PRODUTO (Product)
# O objeto complexo que será construído.
# =============================================================================


class Personagem:
    """
    Representa o personagem final. Seus atributos são preenchidos pelo Builder,
    o que nos permite ter um construtor __init__ simples.
    """

    def __init__(self, nome):
        self.nome = nome
        self.raca: Raca
        self.classe: Classe
        self.atributos: Atributos = Atributos()
        # Outros campos como inventario, experiencia, etc.

    def __str__(self):
        return (
            f"========================================\n"
            f"FICHA DE PERSONAGEM\n"
            f"----------------------------------------\n"
            f"Nome: {self.nome}\n"
            f"Raça: {self.raca.nome if self.raca else 'N/A'}\n"
            f"Classe: {self.classe.nome if self.classe else 'N/A'}\n"
            f"Atributos: [{self.atributos}]\n"
            f"========================================\n"
        )

# =============================================================================
# 3. A INTERFACE BUILDER (Builder Interface)
# Define os métodos para construir as partes do produto.
# =============================================================================


class IBuilderPersonagem(ABC):
    """Interface que define todos os passos para criar um personagem."""

    @abstractmethod
    def set_nome(self, nome: str) -> 'BuilderPersonagem': pass

    @abstractmethod
    def set_raca(self, raca: Raca) -> 'BuilderPersonagem': pass

    @abstractmethod
    def set_classe(self, classe: Classe) -> 'BuilderPersonagem': pass

    @abstractmethod
    def set_atributos_base(self, forca: int, inteligencia: int,
                           destreza: int, vigor: int, sorte: int) -> 'BuilderPersonagem': pass

    @abstractmethod
    def get_personagem(self) -> Personagem: pass

# =============================================================================
# 4. O BUILDER CONCRETO (Concrete Builder)
# Implementa a interface e constrói o objeto passo a passo.
# =============================================================================


class BuilderPersonagem(IBuilderPersonagem):
    """
    Implementação concreta do Builder. É responsável por criar e montar
    o objeto Personagem.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Prepara um novo objeto Personagem em branco para a construção."""
        self._personagem = Personagem("")

    def set_nome(self, nome: str) -> 'BuilderPersonagem':
        self._personagem.nome = nome
        # Retornar 'self' permite o encadeamento de métodos (chaining)
        return self

    def set_raca(self, raca: Raca) -> 'BuilderPersonagem':
        self._personagem.raca = raca
        return self

    def set_classe(self, classe: Classe) -> 'BuilderPersonagem':
        self._personagem.classe = classe
        return self

    def set_atributos_base(self, forca: int, inteligencia: int, destreza: int, vigor: int, sorte: int) -> 'BuilderPersonagem':
        self._personagem.atributos = Atributos(
            forca, inteligencia, destreza, vigor, sorte)
        return self

    def _aplicar_bonus_raciais(self):
        """Método interno para adicionar a lógica de bônus."""
        if self._personagem.raca and self._personagem.raca.atributo_bonus:
            bonus = self._personagem.raca.atributo_bonus
            attrs = self._personagem.atributos
            attrs.forca += bonus.forca
            attrs.inteligencia += bonus.inteligencia
            attrs.destreza += bonus.destreza
            attrs.vigor += bonus.vigor
            attrs.sorte += bonus.sorte

    def get_personagem(self) -> Personagem:
        """
        Finaliza a construção e retorna o personagem completo.
        Aqui é um ótimo lugar para aplicar lógicas finais, como bônus raciais.
        """
        # Aplica os bônus da raça aos atributos base
        self._aplicar_bonus_raciais()

        personagem_pronto = self._personagem
        self.reset()  # Limpa o builder para a próxima construção
        return personagem_pronto

# =============================================================================
# 5. O DIRETOR (Director) (Opcional)
# Define a ordem de construção para criar "presets".
# =============================================================================


class Diretor:
    def __init__(self, builder: IBuilderPersonagem):
        self._builder = builder

    def criar_guerreiro_anao(self, nome: str):
        raca_anao = Raca("Anão", atributo_bonus=Atributos(forca=2, vigor=1))
        classe_guerreiro = Classe("Guerreiro")

        return self._builder.set_nome(nome)\
                            .set_raca(raca_anao)\
                            .set_classe(classe_guerreiro)\
                            .set_atributos_base(forca=10, inteligencia=5, destreza=7, vigor=8, sorte=5)\
                            .get_personagem()

    def criar_mago_elfo(self, nome: str):
        raca_elfo = Raca("Elfo", atributo_bonus=Atributos(
            inteligencia=2, destreza=1))
        classe_mago = Classe("Mago")

        return self._builder.set_nome(nome)\
                            .set_raca(raca_elfo)\
                            .set_classe(classe_mago)\
                            .set_atributos_base(forca=5, inteligencia=10, destreza=8, vigor=5, sorte=7)\
                            .get_personagem()


if __name__ == "__main__":
    print("--- Construção de Personagem com Builder ---")

    # Instancia o builder que vamos usar
    builder = BuilderPersonagem()

    # --- Exemplo 1: Usando o Diretor para criar personagens pré-definidos ---
    print("\n[Usando o Diretor para criar 'presets']\n")

    diretor = Diretor(builder)

    gimli = diretor.criar_guerreiro_anao("Gimli")
    print(gimli)
    # Note que a Força final é 12 (10 base + 2 bônus racial) e Vigor é 9 (8 base + 1 bônus).

    # Apenas para o exemplo :)
    legolas = diretor.criar_mago_elfo("Legolas, o Mago?")
    print(legolas)
    # Note que a Inteligência final é 12 (10 base + 2 bônus racial).

    # --- Exemplo 2: Usando o Builder diretamente para um personagem customizado ---
    print("\n[Usando o Builder manualmente para máxima flexibilidade]\n")

    raca_orc = Raca("Orc", atributo_bonus=Atributos(forca=3, vigor=-1))
    classe_barbaro = Classe("Bárbaro")

    # O cliente controla a construção passo a passo
    orc_barbaro = builder.set_nome("Grommash")\
                         .set_raca(raca_orc)\
                         .set_classe(classe_barbaro)\
                         .set_atributos_base(forca=12, inteligencia=3, destreza=6, vigor=9, sorte=4)\
                         .get_personagem()

    print(orc_barbaro)
    # Força final será 15 (12 + 3) e Vigor final 8 (9 - 1)
