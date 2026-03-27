import argparse
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--class_id", type=str, required=True, help="班级id")
    args = parser.parse_args()
    print("Hello World!" + args.class_id)

if __name__ == "__main__":
    main()