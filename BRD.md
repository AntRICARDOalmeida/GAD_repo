# Business Requirements Document (BRD)

## Web App de Registo e Análise de Treinos

### 1. Objetivo
Desenvolver uma aplicação web pessoal para registo, consulta e análise de treinos de musculação, permitindo acompanhar o volume de treino por grupo muscular e o progresso de carga em cada exercício ao longo do tempo. O armazenamento dos dados será feito numa base de dados Supabase.

---

### 2. Página Principal (Dashboard)
- Exibir um dashboard com dados analíticos sobre o volume de treino (número de sets) por grupo muscular na última semana.
- Visualização gráfica (ex: gráfico de barras ou pizza) do volume semanal por grupo muscular.
- Destaques de tendências ou variações em relação à semana anterior (opcional).

---

### 3. Use Cases Principais

#### 3.1. Registo de Exercícios
- Inserir novos exercícios, especificando:
  - Nome do exercício
  - Grupo muscular principal trabalhado

#### 3.2. Registo de Sessões de Treino
- Adicionar uma nova sessão de treino, guardando:
  - Data e hora da sessão
  - Lista de exercícios realizados na sessão
    - Para cada exercício: número de sets, carga utilizada em cada set

#### 3.3. Consulta e Análise de Dados
- Visualizar tabela de exercícios registados, incluindo:
  - Nome do exercício
  - Grupo muscular
  - Carga máxima atual (última carga utilizada)
- Consultar histórico de cargas por exercício:
  - Gráfico/tabela mostrando evolução da carga ao longo do tempo para cada exercício
- Visualizar volume de treino por grupo muscular ao longo do tempo:
  - Gráficos/tabelas analíticas (ex: volume semanal/mensal por grupo muscular)

---

### 4. Funcionalidades Detalhadas

#### 4.1. Gestão de Exercícios
- Adicionar, editar e remover exercícios
- Associar cada exercício a um grupo muscular

#### 4.2. Gestão de Sessões de Treino
- Adicionar nova sessão com data/hora
- Selecionar exercícios realizados na sessão
- Para cada exercício:
  - Inserir número de sets
  - Inserir carga utilizada em cada set

#### 4.3. Consulta e Análise
- Listagem de exercícios com carga máxima atual
- Consulta do histórico de cargas por exercício (tabela e/ou gráfico)
- Visualização do volume de treino por grupo muscular ao longo do tempo

---

### 5. Requisitos Técnicos

- Framework: Streamlit (Python)
- Base de dados: Supabase (PostgreSQL)
- Interface intuitiva e responsiva
- Possibilidade de exportar dados (CSV/Excel) para backup ou análise externa

---

### 6. Futuras Expansões (Opcional)
- Suporte a múltiplos utilizadores
- Integração com dispositivos de tracking (ex: smartwatches)
- Notificações ou sugestões de treino

---

### 7. Considerações Finais
- O foco inicial é a usabilidade pessoal e a simplicidade
- O sistema deve ser facilmente extensível para novas funcionalidades
