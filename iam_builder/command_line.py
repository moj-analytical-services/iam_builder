import argparse
import yaml
import json

from iam_builder.iam_builder import build_iam_policy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="path to your yaml/json config")
    parser.add_argument("-o", "--output", help="output_path")
    args = parser.parse_args()

    config_path = args.config
    output_path = args.output

    # Assume config is a yaml file if not json
    with open(config_path, 'r') as f:
        if config_path.endswith('.json'):
            config = json.load(f)
        else:
            config = yaml.load(f, Loader=yaml.FullLoader)
    
    iam = build_iam_policy(config)

    with open(output_path, "w+") as outfile:
        json.dump(iam, outfile, indent=4, separators=(',', ': '))

if __name__ == "__main__":
    main()
