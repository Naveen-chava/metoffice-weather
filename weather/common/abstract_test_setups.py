from django.core.files.uploadedfile import SimpleUploadedFile

from common.constants import Region, Parameter
from services.media_document import svc_media_document_process_the_text_file


class AbstractTestSetup:
    def _upload_document(self):
        file_name = "media_document/sample_docs/England_MinTemp.txt"

        with open(file_name, "rb") as file:
            self.file_content = file.read()

        self.uploaded_file = SimpleUploadedFile("file_name", self.file_content)

        request_data = {
            "file_name": self.uploaded_file,
            "region": Region.get_string_for_value(Region.ENGLAND.value),
            "parameter": Parameter.get_string_for_value(Parameter.MIN_TEMP.value),
        }

        svc_media_document_process_the_text_file(request_data)
