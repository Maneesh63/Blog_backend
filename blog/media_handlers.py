from django.core.exceptions import ValidationError
from root.settings import SUPABASE_S3_STORAGE

class S3Handler:

    @classmethod
    def upload_file_to_s3(cls, bucket="blog", file_bytes=None, file_path=None, file_options=None, delete=False):
        try:

            response = SUPABASE_S3_STORAGE.storage.from_(bucket).upload(
                path=file_path,
                file=file_bytes,
                file_options=file_options or {}
            )

            print("Upload response:", response)

            public_url = (
                SUPABASE_S3_STORAGE
                .storage
                .from_(bucket)
                .get_public_url(file_path)
            )

            return public_url

        except Exception as e:
            print("UPLOAD ERROR:", repr(e))
            print("ERROR TYPE:", type(e))

            if hasattr(e, "response"):
                print("STATUS:", e.response.status_code)
                print("HEADERS:", e.response.headers)
                print("BODY:", e.response.text)

            import traceback
            traceback.print_exc()

            raise ValidationError({
                "detail": "Failed to upload file.",
                "error": str(e)
            })