# Scripts de Organização e Conversão

Este diretório contém ferramentas para manutenção, indexação e conversão de documentos do acervo pessoal.

## Estrutura de Pastas (Proposta)

- **python/**: Scripts em Python (Conversão para Obsidian).
- **node/**: Scripts em Node.js (Indexação de conteúdo).
- **shell/**: Scripts Bash (Organização de arquivos).
- **data/**: Arquivos de dados (Índices JSON, categorizações).
- **logs/**: Registros de execuções anteriores.

---

## Scripts Principais

### 1. Conversor para Obsidian (`python/convert_to_obsidian.py`)
Converte documentos (`.docx`, `.pdf`, `.pptx`, etc.) em arquivos Markdown para uso no Obsidian, mantendo a estrutura de pastas.

**Como rodar:**
```bash
cd scripts/python
source venv_markitdown/bin/activate
python convert_to_obsidian.py
```

### 2. Indexador de Arquivos (`node/indexer.js`)
Gera um arquivo `index.json` em `scripts/data/` com o conteúdo (snippet) de todos os arquivos para facilitar buscas globais.

**Como rodar:**
```bash
cd scripts/node
npm install  # Caso seja a primeira vez
node indexer.js
```

### 3. Organização de Arquivos (`shell/organize.sh`)
Script em lote que move arquivos baseados em regras pré-definidas para as pastas corretas (`01_Ministerio`, `02_Academico`, etc.).

**Como rodar:**
```bash
# Simulação (Dry-run)
./scripts/shell/organize.sh true

# Execução real
./scripts/shell/organize.sh
```

---

## Manutenção

Para adicionar novas dependências Node:
```bash
cd scripts/node
npm install <pacote>
```

Para atualizar o ambiente Python:
```bash
cd scripts/python
pip install --upgrade markitdown
```
