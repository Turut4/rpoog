from rpoog.entidades import BuilderPersonagem, Diretor, Raca, Atributos, Classe


def main():
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


if __name__ == "__main__":
    main()
