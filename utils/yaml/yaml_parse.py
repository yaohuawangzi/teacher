import yaml

def load_soul(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soul_data = yaml.safe_load(f)
    return soul_data

def main():
    file_path = 'souls/zh/zh_soul.yaml'
    soul_data = load_soul(file_path)
    print(soul_data)
