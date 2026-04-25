#!/bin/bash

# Script de Organização de Arquivos (Exemplo para Portfólio)
# Este script move arquivos baseados em regras de extensão e padrões de nome.

cd "$(dirname "$0")/../.."

DRY_RUN=${1:-false}

function move_file() {
  local src="$1"
  local dest="$2"
  
  if [ ! -f "$src" ]; then
    return # Pula se o arquivo não existir
  fi

  if [ "$DRY_RUN" = "true" ]; then
    echo "[DRY-RUN] mv \"$src\" \"$dest/\""
  else
    mkdir -p "$dest"
    mv -v "$src" "$dest/" 2>/dev/null || echo "Erro ao mover: $src"
  fi
}

echo "Iniciando organização... (Dry-run: $DRY_RUN)"

# --- EXEMPLOS DE REGRAS DE ORGANIZAÇÃO ---

# 1. Organizar PDFs e documentos por tipo
# move_file "meu_livro.pdf" "02_Academico_Biblioteca/Livros"
# move_file "relatorio_mensal.docx" "03_Profissional/Relatorios"

# 2. Organizar arquivos soltos na raiz (Exemplo)
# for f in *.pdf; do move_file "$f" "99_Diversos/PDFs_Soltos"; done

echo "Organização concluída."
