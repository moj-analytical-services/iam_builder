import argparse
from iam_builder.iam_builder import build_iam_policy

def main(config_path, out_path):
    build_iam_policy(config_path, out_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="path to your yaml/json config")
    parser.add_argument("-o", "--output", help="output_path")
    args = parser.parse_args()
    main(args.config, args.output)