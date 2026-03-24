import argparse
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--class_id", type=str, required=True, help="班级id")
    args = parser.parse_args()
    return "Hello World!" + args.class_id
