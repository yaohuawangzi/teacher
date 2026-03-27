import argparse
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--student_id", type=str, required=True, help="班级id")
    args = parser.parse_args()
    print("Hello World!" + args.student_id)

if __name__ == "__main__":
    main()