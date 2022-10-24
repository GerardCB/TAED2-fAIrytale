from pathlib import Path
import logging
import os
import json
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split

params_path = Path("params.yaml")

with open(params_path, "r") as params_file:
    try:
        params = yaml.safe_load(params_file)
        params = params["prepare"]
    except yaml.YAMLError as exc:
        print(exc)

def main(input_filepath, output_filepath):
    """ Divide Data X_train, X_test, y_train, y_test """
    logger = logging.getLogger(__name__)
    logger.info('Dividing DataSet')

    with open(input_filepath, 'r') as f:
        data = json.load(f)

    df = pd.DataFrame(list(data.items()), columns = ["book_id", "book"])
    df["text"] = [[text for text, url in book] for book in df["book"]]
    df["img"] = [[url for text, url in book] for book in df["book"]]
    #X = [text for book in data.values() for text, url in book]
    #y = [url for book in data.values() for text, url in book]

    X_train, X_test, y_train, y_test = train_test_split(df["text"], df["img"], test_size=params["test_size"], random_state=params["random_state"])

    X_train.to_json(output_filepath + "/Xtrain.json")
    X_test.to_json(output_filepath + "/Xtest.json")
    y_train.to_json(output_filepath + "/ytrain.json")
    y_test.to_json(output_filepath + "/ytest.json")

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    input_filepath = os.path.join(project_dir, "data", "raw.json")
    output_filepath = os.path.join(project_dir, "data")

    main(input_filepath, output_filepath)
