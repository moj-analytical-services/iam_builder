import argparse
from iam_builder.iam_builder import build_iam_policy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="path to your yaml/json config")
    parser.add_argument("-o", "--output", help="output_path")
    args = parser.parse_args()
    build_iam_policy(args.config, args.output)

if __name__ == "__main__":
    main()