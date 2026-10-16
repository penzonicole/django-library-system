# 📚 Projeto 2 — Sistema de Biblioteca (Django ORM Avançado)

Um sistema completo de gestão de biblioteca desenvolvido em Django 5+, demonstrando consultas avançadas com o Django ORM, agregações, buscas dinâmicas com `Q` e funcionalidades complexas de empréstimo/reserva.

---

## 🚀 Funcionalidades & Destaques

- **Dashboard com Agregações ORM**: Métricas calculadas via ORM (`Count`, `Avg`) exibindo total de livros, empréstimos ativos e média de avaliações.
- **Consultas & Filtros Dinâmicos**: Busca por Título, Autor ou ISBN com `Q` objects e filtragem por Categoria.
- **Relacionamentos Avançados**:
  - `ForeignKey` (Autor e Leitor)
  - `ManyToManyField` (Categorias)
- **Desafios Extras Implementados**:
  - ⭐ **Sistema de Avaliação (Rating)**: Nota de 1 a 5 estrelas por livro.
  - 💰 **Cálculo de Multa por Atraso**: R$ 2,00/dia calculado automaticamente via `@property`.
  - 🔖 **Sistema de Reserva**: Permite solicitar reservas para livros sem exemplares disponíveis.

---

## 🛠️ Passo a Passo da Construção do Projeto

1. **Setup Inicial**: Criação do ambiente virtual `venv`, instalação do Django/Pillow e inicialização do app `biblioteca`.
2. **Modelagem ORM**: Construção de `Autor`, `Categoria`, `Livro`, `Emprestimo` e `Reserva`.
3. **Migrações e Admin**: Criação das tabelas no banco de dados e configuração do painel de administração customizado.
4. **Views Avançadas**: Implementação do Dashboard e do Acervo com buscas inteligentes.
5. **Interface do Usuário**: Criação dos templates com Bootstrap 5 integrando o fluxo de dados.

---

## 🐛 Relatório de Dificuldades Encontradas & Errata

Durante a construção do backend, foram contornados e resolvidos os seguintes pontos:

1. **Configuração do Interpretador Python (Pylance Import Error)**:
   - *Problema*: VS Code apresentando avisos de `could not be resolved from source`.
   - *Solução*: Seleção explícita do interpretador `./venv/bin/python`.
2. **Cálculo Dinâmico de Multas sem Duplicação de Dados**:
   - *Problema*: Evitar salvar valores estáticos de multas no banco que poderiam ficar desatualizados.
   - *Solução*: Utilização da `@property` `valor_multa` no model `Emprestimo` comparando `data_devolucao_prevista` com a data atual (`timezone.now().date()`).

---

## 🖥️ Fluxo de Funcionamento da Aplicação

1. **`/` (Dashboard)**: Visualização rápida de métricas do sistema e livros recentes.
2. **`/livros/` (Acervo)**: Interface com campo de busca e seletor de categorias.
3. **`/livros/<id>/` (Detalhes)**: Exibição completa das informações do livro e disponibilidade.
4. **`/admin/` (Painel Administrativo)**: Gestão de autores, livros, empréstimos e reservas.

---

## 🌟 Diferenciais & Funcionalidades Avançadas

- **Ações no Admin (`Admin Actions`)**: Devolução rápida de exemplares em lote direto pelo painel de controle.
- **Relatório Impresso / PDF**: Emissão do acervo completo pronto para impressão ou exportação em PDF.
- **Suíte de Testes Automatizados**: Validação das regras de negócio principais executada via `python manage.py test`.