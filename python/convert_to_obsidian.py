import os
import pathlib
import signal
import shutil
from markitdown import MarkItDown

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

def convert_files():
    markitdown = MarkItDown()
    signal.signal(signal.SIGALRM, timeout_handler)
    
    source_to_dest = {
        "/run/media/weinne/2ba8e106-fce3-4215-a5f6-d97c5872dfb9/Syncthing/weinne/01_ministerio/aulas_e_estudos": "/home/weinne/Obsidian/obsidian-vault/01_ministerio/aulas_e_estudos",
        "/run/media/weinne/2ba8e106-fce3-4215-a5f6-d97c5872dfb9/Syncthing/weinne/02_academico_biblioteca/cursos": "/home/weinne/Obsidian/obsidian-vault/02_academico_biblioteca/cursos"
    }
    
    supported_extensions = {".docx", ".pptx", ".pdf", ".xlsx", ".zip", ".html"}
    
    for src_root, dest_root in source_to_dest.items():
        if not os.path.exists(src_root):
            continue
            
        print(f"Sincronizando: {src_root}")
        src_root_path = pathlib.Path(src_root)
        dest_root_path = pathlib.Path(dest_root)

        # --- FASE 1: Atualizações e Novos Arquivos ---
        for root, dirs, files in os.walk(src_root):
            for file in files:
                file_path = pathlib.Path(root) / file
                extension = file_path.suffix.lower()
                
                if extension in supported_extensions:
                    relative_path = file_path.relative_to(src_root_path)
                    dest_path = dest_root_path / relative_path.with_suffix(".md")
                    
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Verifica se precisa converter (se não existe ou se a origem é mais nova)
                    needs_conversion = False
                    if not dest_path.exists():
                        needs_conversion = True
                    else:
                        if file_path.stat().st_mtime > dest_path.stat().st_mtime:
                            needs_conversion = True
                    
                    if needs_conversion:
                        print(f"Convertendo/Atualizando: {relative_path}")
                        try:
                            signal.alarm(30)
                            try:
                                result = markitdown.convert(str(file_path))
                                with open(dest_path, "w", encoding="utf-8") as f:
                                    f.write(result.text_content)
                            finally:
                                signal.alarm(0)
                        except TimeoutException:
                            print(f"Erro: Timeout em {file_path}")
                        except Exception as e:
                            print(f"Erro ao converter {file_path}: {e}")

        # --- FASE 2: Remoção de arquivos que não existem mais na origem ---
        if dest_root_path.exists():
            for root, dirs, files in os.walk(dest_root, topdown=False):
                dest_current_dir = pathlib.Path(root)
                
                for file in files:
                    if file.endswith(".md"):
                        dest_file_path = dest_current_dir / file
                        rel_to_dest = dest_file_path.relative_to(dest_root_path)
                        
                        # Tenta encontrar o arquivo original com qualquer uma das extensões suportadas
                        found_original = False
                        for ext in supported_extensions:
                            original_candidate = src_root_path / rel_to_dest.with_suffix(ext)
                            if original_candidate.exists():
                                found_original = True
                                break
                        
                        if not found_original:
                            print(f"Removendo órfão: {rel_to_dest}")
                            dest_file_path.unlink()

                # Remove pastas vazias no destino
                if not os.listdir(root) and dest_current_dir != dest_root_path:
                    print(f"Removendo pasta vazia: {dest_current_dir.relative_to(dest_root_path)}")
                    os.rmdir(root)

if __name__ == "__main__":
    convert_files()
