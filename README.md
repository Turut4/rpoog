# Projeto RPG em Python com Padrões de Projeto

## 1. Visão Geral

Este projeto é uma aplicação de RPG (Role-Playing Game) baseada em texto, desenvolvida em Python. Seu objetivo principal é demonstrar conceitos de Programação Orientada a Objetos (POO) e a aplicação prática de Padrões de Projeto (Design Patterns) para criar um sistema flexível, coeso e de fácil manutenção.

A aplicação simula a criação de personagens com diferentes raças e classes e, em seguida, executa uma interação de combate entre eles para demonstrar os padrões em ação.

## 2. Estrutura do Projeto

O código foi modularizado para seguir o princípio da Separação de Responsabilidades, resultando na seguinte estrutura de arquivos:

```text
rpoog/
├── main.py
├── rpoog/
│   ├── __init__.py
│   ├── entidades.py
│   ├── itens.py
│   ├── patterns.py
│   └── factories.py
```

* **`main.py`**: Ponto de entrada da aplicação. Orquestra a criação dos personagens e a simulação do combate.
* **`rpoog/__init__.py`**: Arquivo vazio que define a pasta `rpoog` como um pacote Python.
* **`rpoog/entidades.py`**: Contém as classes de dados centrais (`Personagem`, `Raça`, `Classe`, `Atributos`) e a interface de comportamento (`IEstrategiaAtaque`).
* **`rpoog/itens.py`**: Contém as classes relacionadas a itens (`Item`, `Arma`, `Pocao`) e o `Inventario`.
* **`rpoog/patterns.py`**: Implementa os padrões de projeto comportamentais e estruturais (`Strategy` e `Builder`).
* **`rpoog/factories.py`**: Implementa os padrões de projeto criacionais (`Factory Method` e `Abstract Factory`).

## 3. Como Executar

1. Certifique-se de que a estrutura de pastas e arquivos acima esteja correta.
2. Abra um terminal na pasta raiz do projeto (a primeira pasta `rpoog`).
3. Execute o seguinte comando:

    ```bash
    python main.py
    ```

4. A simulação de criação de personagens e o combate serão exibidos no terminal.

## 4. Padrões de Projeto Utilizados

Quatro padrões de projeto foram implementados para resolver problemas específicos de design, tornando o código mais robusto e flexível.

### 4.1. Abstract Factory (Fábrica Abstrata)

* **Justificativa**: A criação de um personagem envolve um conjunto de objetos relacionados (Raça, Classe, Atributos, Equipamento Inicial) que precisam ser compatíveis entre si. O padrão Abstract Factory foi escolhido para encapsular a criação dessas "famílias" de objetos. Em vez de ter uma classe `Diretor` com métodos fixos, criamos fábricas concretas como `GuerreiroFactory` e `MagoFactory`, cada uma sendo um "kit" completo para montar um arquétipo de personagem.

* **Exemplo de Implementação (`factories.py`)**:
    A interface define o "contrato" para os kits, e a fábrica concreta implementa a criação de um kit específico.

    ```python
    # Interface da Fábrica Abstrata
    class IPersonagemFactory(ABC):
        """Interface da Fábrica Abstrata para criar kits de personagem."""
        @abstractmethod
        def criar_raca(self) -> Raca: pass

        @abstractmethod
        def criar_classe(self) -> Classe: pass

        @abstractmethod
        def criar_equipamento_inicial(self) -> list[Item]: pass

    # Implementação de uma Fábrica Concreta
    class GuerreiroFactory(IPersonagemFactory):
        """Fábrica concreta para o arquétipo Guerreiro."""
        def criar_raca(self) -> Raca:
            return Raca("Anão", Atributos(forca=2, vigor=2, sorte=-1))

        def criar_classe(self) -> Classe:
            return Classe("Guerreiro")

        def criar_equipamento_inicial(self) -> list[Item]:
            # ... (cria e retorna uma lista de itens para o guerreiro)
    ```

### 4.2. Factory Method (Método de Fábrica)

* **Justificativa**: Dentro do jogo, existem vários tipos de itens (`Arma`, `Pocao`). Para centralizar a lógica de criação e desacoplar o cliente das classes concretas de itens, foi usado o Factory Method. O cliente (neste caso, as `IPersonagemFactory`) simplesmente solicita um item de um determinado tipo (ex: `'arma'`) sem precisar saber que a classe `Arma` será instanciada.

* **Exemplo de Implementação (`factories.py`)**:
    A classe `ItemFactory` possui um método que decide qual objeto criar com base em um parâmetro.

    ```python
    class ItemFactory:
        """Factory Method para criar diferentes tipos de Item."""
        def criar_item(self, tipo_item: str, **kwargs) -> Item:
            if tipo_item == 'arma':
                return Arma(**kwargs)
            if tipo_item == 'pocao':
                return Pocao(**kwargs)
            raise ValueError(f"Tipo de item desconhecido: {tipo_item}")
    ```

### 4.3. Builder (Construtor)

* **Justificativa**: O objeto `Personagem` é complexo e sua construção requer múltiplos passos. Usar um construtor com muitos parâmetros seria confuso e propenso a erros. O padrão Builder foi utilizado para separar o processo de construção da representação final do objeto. Ele permite montar um `Personagem` passo a passo de forma legível e controlada, culminando em um objeto válido.

* **Exemplo de Implementação (`patterns.py` e `main.py`)**:
    O Builder fornece métodos encadeados para a construção. Ele trabalha em conjunto com a Abstract Factory: a fábrica fornece os componentes e o builder os monta.

    ```python
    # Trecho de main.py mostrando o uso do Builder
    def criar_personagem_com_factory(factory: IPersonagemFactory, nome: str) -> Personagem:
        builder = BuilderPersonagem()
        
        # ... fábrica obtém as partes ...
        raca = factory.criar_raca()
        classe = factory.criar_classe()
        # ...

        # O builder monta o personagem passo a passo
        builder.set_nome(nome)\
               .set_raca(raca)\
               .set_classe(classe)\
               # ...
            
        return builder.get_personagem()
    ```

### 4.4. Strategy (Estratégia)

* **Justificativa**: Um personagem pode atacar de maneiras diferentes dependendo de sua classe (um guerreiro usa força, um mago usa inteligência). Para evitar condicionais (`if/else`) na classe `Personagem`, o padrão Strategy foi aplicado para encapsular os algoritmos de ataque. Cada algoritmo (`AtaqueFisico`, `AtaqueMagico`) se torna uma estratégia intercambiável, que pode ser atribuída a um personagem em tempo de execução.

* **Exemplo de Implementação (`entidades.py` e `patterns.py`)**:
    O `Personagem` possui um "slot" para uma estratégia e um método para executá-la, sem conhecer os detalhes de sua implementação.

    ```python
    # Trecho de entidades.py
    class Personagem:
        def __init__(self, nome):
            # ...
            self.estrategia_ataque: IEstrategiaAtaque | None = None

        def definir_estrategia_ataque(self, estrategia: IEstrategiaAtaque):
            self.estrategia_ataque = estrategia

        def executar_ataque(self, alvo: Personagem):
            if self.estrategia_ataque:
                self.estrategia_ataque.atacar(self, alvo)

    # Trecho de patterns.py
    class AtaqueFisico(IEstrategiaAtaque):
        """Estratégia para ataques com Força e Arma."""
        def atacar(self, atacante: Personagem, alvo: Personagem):
            dano = atacante.atributos.forca + atacante.get_arma_equipada().dano
            alvo.receber_dano(dano)
    ```

## 5. Descrição das Classes Principais

Esta seção detalha as responsabilidades das classes mais importantes do projeto.

### 5.1. Módulo `entidades.py`

* `Atributos`: Armazena as características base de um personagem (força, inteligência, etc.) e também gerencia seu estado dinâmico, como a vida atual e máxima.
* `Raca` / `Classe`: Classes de dados simples que representam a raça e a classe de um personagem, usadas para composição.
* `IEstrategiaAtaque`: A interface (Classe Base Abstrata) para o padrão Strategy. Define o contrato que todas as estratégias de ataque devem seguir, garantindo que possuam um método `atacar`.
* `Personagem`: A classe central do sistema. É composta por `Atributos`, `Raca`, `Classe` e `Inventario`. Ela não contém lógica de ataque, mas delega essa responsabilidade a um objeto `IEstrategiaAtaque`.

### 5.2. Módulo `itens.py`

* `Item`: Classe base para todos os objetos que podem ser guardados no inventário.
* `Arma` / `Pocao`: Subclasses de `Item` que adicionam atributos específicos, como `dano` ou `cura`. Demonstram o uso de herança.
* `Inventario`: Uma classe que contém e gerencia uma lista de `Itens`, respeitando um limite de capacidade.

### 5.3. Módulo `factories.py`

* `ItemFactory`: Implementa o padrão Factory Method. Centraliza a criação de diferentes tipos de `Item` em um único lugar.
* `IPersonagemFactory`: A interface para o padrão Abstract Factory. Define os métodos que todas as fábricas de arquétipos de personagem devem implementar.
* `GuerreiroFactory` / `MagoFactory`: Implementações concretas da `IPersonagemFactory`. Cada uma é responsável por criar uma família de objetos relacionados que compõem um arquétipo específico.

### 5.4. Módulo `patterns.py`

* `IBuilderPersonagem` / `BuilderPersonagem`: Implementação do padrão Builder. Oferece uma interface fluente para construir um objeto `Personagem` complexo de forma incremental e controlada.
* `AtaqueFisico` / `AtaqueMagico`: Implementações concretas da `IEstrategiaAtaque`. Cada uma encapsula um algoritmo de ataque diferente, tornando o comportamento de combate do personagem extensível e desacoplado.
