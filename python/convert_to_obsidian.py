import os
import pathlib
import signal
import shutil
from markitdown import MarkItDown
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

def convert_files():
    markitdown = MarkItDown()
    signal.signal(signal.SIGALRM, timeout_handler)
    
    # Busca caminhos do .env ou usa valores padrão vazios
    source_dirs = os.getenv("SOURCE_DIRS", "").split(",")
    dest_dirs = os.getenv("DEST_DIRS", "").split(",")
    
    if not source_dirs or not dest_dirs or len(source_dirs) != len(dest_dirs):
        print("Erro: Verifique se SOURCE_DIRS e DEST_DIRS estão configurados corretamente no .env")
        return

    source_to_dest = dict(zip([s.strip() for s in source_dirs], [d.strip() for d in dest_dirs]))
    
    supported_extensions = {".docx", ".pptx", ".pdf", ".xlsx", ".zip", ".html"}
    
    for src_root, dest_root in source_to_dest.items():
        if not src_root: continue
        if not os.path.exists(src_root):
            print(f"Aviso: Caminho de origem não encontrado: {src_root}")
            continue

        src_root_path = pathlib.Path(src_root)
        dest_root_path = pathlib.Path(dest_root)

        for root, dirs, files in os.walk(src_root):
            current_dir = pathlib.Path(root)
            relative_path = current_dir.relative_to(src_root_path)
            dest_current_dir = dest_root_path / relative_path

            for file in files:
                file_path = current_dir / file
                ext = file_path.suffix.lower()

                if ext in supported_extensions:
                    dest_file_path = (dest_current_dir / file).with_suffix(".md")
                    
                    if dest_file_path.exists():
                        continue
                    
                    dest_current_dir.mkdir(parents=True, exist_ok=True)
                    
                    print(f"Convertendo: {file}")
                    signal.alarm(30)
                    try:
                        result = markitdown.convert(str(file_path))
                        with open(dest_file_path, "w", encoding="utf-8") as f:
                            f.write(result.text_content)
                    except TimeoutException:
                        print(f"Timeout ao converter {file}")
                    except Exception as e:
                        print(f"Erro ao converter {file}: {e}")
                    finally:
                        signal.alarm(0)

if __name__ == "__main__":
    convert_files()
