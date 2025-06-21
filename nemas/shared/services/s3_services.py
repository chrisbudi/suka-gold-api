import boto3
from django.conf import settings


class S3Service:
    def __init__(self):
        aws_s3 = settings.AWS_S3
        # print(settings.AWS_S3, aws_s3)
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_s3["ACCESS_KEY_ID"],
            aws_secret_access_key=aws_s3["SECRET_ACCESS_KEY"],
            region_name=aws_s3["REGION_NAME"],
        )
        self.bucket_name = aws_s3["BUCKET_NAME"]
        self.custom_domain = aws_s3["CUSTOM_DOMAIN"]

    def upload_file(self, file_obj, file_name, content_type=None):
        """
        Upload a file to the S3 bucket.

        :param file_obj: File object to upload
        :param file_name: Name of the file in S3
        :param content_type: MIME type of the file
        :return: Public URL of the uploaded file
        """
        try:
            extra_args = {"ContentType": content_type} if content_type else {}
            self.s3_client.upload_fileobj(
                file_obj, self.bucket_name, file_name, ExtraArgs=extra_args
            )
            return f"https://{self.custom_domain}/{file_name}"
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")
