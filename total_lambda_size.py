import boto3
import botostubs
import glob
import os
import requests
import sys
import shutil
import tempfile
import zipfile

from hurry.filesize import size


def get_size_total(temp_dir):
    zip_files = glob.glob(os.path.join(temp_dir, "*.zip"))
    all_size = 0
    for zip in zip_files:
        total_size = 0
        zip_file = zipfile.ZipFile(zip)
        for file in zip_file.namelist():
            total_size += zip_file.getinfo(name=file).file_size

        all_size += total_size
        human_size = size(total_size)
        print(f"{ zip }: { human_size }")

    print(f"Total: { size(all_size) }")


def main(lambda_name):

    temp_dir = tempfile.mkdtemp()
    client = boto3.client("lambda", region_name="us-east-1")  # type: botostubs.LAMBDA
    lambda_info = client.get_function(
        FunctionName=lambda_name
    )

    response = requests.get(lambda_info["Code"]["Location"])
    with open(os.path.join(temp_dir, f"{ lambda_name }.zip"), "wb") as f:
        f.write(response.content)

    for layer in lambda_info["Configuration"]["Layers"]:
        layer_arn = layer["Arn"].split(":")
        layer_name = layer_arn[6]
        layer_version = layer_arn[7]
        layer_info = client.get_layer_version(
            LayerName=layer_name,
            VersionNumber=int(layer_version)
        )
        response = requests.get(layer_info["Content"]["Location"])
        with open(os.path.join(temp_dir, f"{ layer_name }.zip"), "wb") as f:
            f.write(response.content)

    get_size_total(temp_dir)
    shutil.rmtree(temp_dir)


if __name__ == "__main__":
    lambda_name = sys.argv[1]
    main(lambda_name=lambda_name)