import json

file_path = r'c:\Users\jenil\OneDrive\Desktop\Machine learning\AI-Ops\triage\notebooks\05_evaluation.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        source = cell.get('source', [])
        for i, line in enumerate(source):
            if 'questions, answers, contexts , ground_truth = [], [], [], []' in line:
                source[i] = line.replace('ground_truth', 'ground_truths')
        cell['source'] = source

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
    
print("Notebook fixed.")
