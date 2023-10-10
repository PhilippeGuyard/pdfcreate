import boto3
import uuid
import subprocess
import os


def generate_unique_filename(extension="pdf"):
    return f"{uuid.uuid4().hex}.{extension}"


def create_pdf(
    input_html_path, output_pdf_path, wkhtmltopdf_path="/opt/bin/wkhtmltopdf"
):
    with open(input_html_path, "w") as f:
        f.write("<h1>Hello, world!</h1>")
    subprocess.run([wkhtmltopdf_path, input_html_path, output_pdf_path])


def upload_to_s3(file_path, bucket_name, object_name=None):
    s3_client = boto3.client("s3")
    if object_name is None:
        object_name = os.path.basename(file_path)
    s3_client.upload_file(file_path, bucket_name, object_name)


def lambda_handler(event, context):
    unique_filename = generate_unique_filename()

    input_html_path = "/tmp/input.html"
    output_pdf_path = f"/tmp/{unique_filename}"

    create_pdf(input_html_path, output_pdf_path)

    bucket_name = os.environ.get("PDF_BUCKET_NAME")

    upload_to_s3(output_pdf_path, bucket_name)

    return {
        "statusCode": 200,
        "body": f"PDF {unique_filename} created and uploaded to S3.",
    }
