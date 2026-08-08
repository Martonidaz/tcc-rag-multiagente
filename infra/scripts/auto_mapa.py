import os
import re

# Pastas que a automação deve ignorar
IGNORE_DIRS = {'.git', 'venv', 'node_modules', '__pycache__', '.pytest_cache'}

def sanitize_id(name):
    """Remove caracteres especiais para criar IDs válidos no Mermaid."""
    return re.sub(r'[^a-zA-Z0-9]', '', name)

def generate_markdown_tree(startpath):
    """Gera a árvore em formato de lista aninhada (Markmap)."""
    tree_lines = []
    for root, dirs, files in os.walk(startpath):
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
            if not f.startswith('.') and f != 'auto_mapa.py':
                tree_lines.append(f"{sub_indent}* `{f}`")
                
    return "\n".join(tree_lines)

def generate_mermaid_graph(startpath):
    """Gera o grafo visual arquitetural (Mermaid.js)."""
    lines = ["```mermaid", "graph TD"]
    root_name = os.path.basename(startpath)
    root_id = sanitize_id(root_name) or "Root"
    
    lines.append(f"    {root_id}[{root_name}]")
    
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        level = root.replace(startpath, '').count(os.sep)
        
        # Limita a profundidade do Mermaid (Nível 1) para o gráfico não virar um labirinto ilegível
        if level >= 1:
            dirs[:] = []
            continue
            
        parent_name = os.path.basename(root)
        parent_id = sanitize_id(parent_name) if level > 0 else root_id
        
        for d in dirs:
            child_id = sanitize_id(d) + str(level)
            lines.append(f"    {parent_id} --> {child_id}[{d}]")
            
        for f in sorted(files):
            if not f.startswith('.') and f != 'auto_mapa.py':
                child_id = sanitize_id(f) + "f" + str(level)
                lines.append(f"    {parent_id} --> {child_id}({f})")
                
    lines.append("```")
    return "\n".join(lines)

def update_map_file(repo_path):
    """Consolida os dois modelos em um único arquivo Markdown."""
    map_path = os.path.join(repo_path, 'mapa_tcc.md')
    tree_content = generate_markdown_tree(repo_path)
    mermaid_content = generate_mermaid_graph(repo_path)
    
    content = f"""# Mapa da Estrutura do TCC

Este arquivo é **gerado automaticamente** pelo script `infra/scripts/auto_mapa.py`.
Não edite a árvore manualmente.

## 🌳 Árvore de Diretórios (Formato Markmap / Universal)

{tree_content}

---

## 📊 Grafo Arquitetural (Formato Mermaid)
*No GitHub, o bloco abaixo é renderizado automaticamente como um diagrama visual, focado na arquitetura de alto nível.*

{mermaid_content}
"""
    with open(map_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Sucesso: mapa_tcc.md atualizado com árvore Markmap e grafo visual Mermaid!")

if __name__ == "__main__":
    # Roda o script considerando que ele está 2 níveis abaixo da raiz (infra/scripts/)
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    update_map_file(root_dir)