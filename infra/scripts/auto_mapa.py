import os

# Pastas que a automação deve ignorar
IGNORE_DIRS = {'.git', 'venv', 'node_modules', '__pycache__', '.pytest_cache'}

def generate_markdown_tree(startpath):
    tree_lines = []
    for root, dirs, files in os.walk(startpath):
        # Remove diretórios ignorados para não entrar na varredura
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '  ' * level
        folder_name = os.path.basename(root)
        
        if level == 0:
            tree_lines.append(f"* **`{os.path.basename(startpath)}/`** (Raiz do Monorepo)")
        else:
            tree_lines.append(f"{indent}* `{folder_name}/`")
            
        sub_indent = '  ' * (level + 1)
        for f in sorted(files):
            # Ignora arquivos ocultos de sistema ou o próprio script
            if not f.startswith('.') and f != 'auto_mapa.py':
                tree_lines.append(f"{sub_indent}* `{f}`")
                
    return "\n".join(tree_lines)

def update_map_file(repo_path):
    map_path = os.path.join(repo_path, 'mapa_tcc.md')
    tree_content = generate_markdown_tree(repo_path)
    
    content = f"""# Mapa da Estrutura do TCC

Este arquivo é **gerado automaticamente** pelo script `infra/scripts/auto_mapa.py`.
Não edite a árvore manualmente.

## 🌳 Árvore de Diretórios (Formato Markmap)

{tree_content}
"""
    with open(map_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Sucesso: mapa_tcc.md atualizado automaticamente!")

if __name__ == "__main__":
    # Roda o script considerando que ele está 2 níveis abaixo da raiz (infra/scripts/)
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    update_map_file(root_dir)