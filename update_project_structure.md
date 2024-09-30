import os

def generate_project_structure():
    project_structure = "# Cấu trúc dự án VoiceTyping\n\n"
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py') and file != 'update_project_structure.py':
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path)
                project_structure += f"## {relative_path}\n```python\n"
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    project_structure += f.read()
                
                project_structure += "\n```\n\n"
    
    with open('project_structure.md', 'w', encoding='utf-8') as f:
        f.write(project_structure)

if __name__ == "__main__":
    generate_project_structure()
