# main.py

import time
from rpoog.patterns import BuilderPersonagem, AtaqueFisico, AtaqueMagico
from rpoog.factories import IPersonagemFactory, GuerreiroFactory, MagoFactory
from rpoog.entidades import Personagem


def criar_personagem_com_factory(factory: IPersonagemFactory, nome: str) -> Personagem:
    """Usa uma Fábrica para obter as partes e um Builder para montar o personagem."""
    builder = BuilderPersonagem()

    # A fábrica fornece os componentes do "kit"
    raca = factory.criar_raca()
    classe = factory.criar_classe()
    atributos_base = factory.definir_atributos_base()
    equipamento_inicial = factory.criar_equipamento_inicial()

    # O builder monta o personagem final
    builder.set_nome(nome)\
           .set_raca(raca)\
           .set_classe(classe)\
           .set_atributos_base(**atributos_base)

    for item in equipamento_inicial:
        builder.adicionar_item_inicial(item)

    return builder.get_personagem()


def main():
    """Função principal que executa a simulação."""
    print(">>> Iniciando a criação de personagens com Abstract Factory <<<\n")
    guerreiro = criar_personagem_com_factory(
        GuerreiroFactory(), "Ivar O Aleijado")
    mago = criar_personagem_com_factory(MagoFactory(), "Gandalf O Cinzento")
    print(guerreiro)
    print(mago)

    guerreiro.definir_estrategia_ataque(AtaqueFisico())  # type: ignore
    mago.definir_estrategia_ataque(AtaqueMagico())  # type: ignore

    print("\n>>> O COMBATE COMEÇA! <<<\n")

    combatentes = [guerreiro, mago]
    turno = 0
    while all(p.esta_vivo() for p in combatentes):
        atacante = combatentes[turno % 2]
        alvo = combatentes[(turno + 1) % 2]

        print(f"--- Turno de {atacante.nome} ---")
        atacante.executar_ataque(alvo)

        print("-" * 30)
        time.sleep(3)

        if not alvo.esta_vivo():
            break

        turno += 1

    print("\n>>> FIM DE COMBATE <<<")
    vencedor = next(p for p in combatentes if p.esta_vivo())
    print(f"O grande vencedor é {vencedor.nome}!")
    print(vencedor)


if __name__ == "__main__":
    main()
