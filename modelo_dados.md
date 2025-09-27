# Modelo de Dados – Web App de Treinos

## Tabelas Principais

### 1. muscle_groups
- id (serial, PK)
- name (string, único)

### 2. exercises
- id (serial, PK)
- name (string, único)

### 2b. exercise_muscle_groups (nova tabela para relação many-to-many)
- id (serial, PK)
- exercise_id (FK → exercises.id)
- muscle_group_id (FK → muscle_groups.id)

### 3. sessions
- id (serial, PK)
- session_date (timestamp)
- created_at (timestamp)

### 4. session_exercises
- id (serial, PK)
- session_id (FK → sessions.id)
- exercise_id (FK → exercises.id)

### 5. sets
- id (serial, PK)
- session_exercise_id (FK → session_exercises.id)
- set_number (int)
- weight (float)
- reps (int, opcional)
- created_at (timestamp)

---

## Relações
- Um exercício pode pertencer a vários grupos musculares (relação many-to-many).
- Uma sessão pode ter vários exercícios.
- Cada exercício numa sessão pode ter vários sets (com carga e reps).

---

## Notas
- A tabela `users` pode ser adicionada no futuro para multi-utilizador.
- O campo `reps` é opcional, caso queiras registar repetições por set.
- O campo `created_at` pode ser útil para auditoria e ordenação.

Se quiseres o SQL para criar estas tabelas, avisa!
