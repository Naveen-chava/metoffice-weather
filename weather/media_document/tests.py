from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from common.constants import Region, Parameter


class DocumentUploadAPI(APITestCase):
    def setUp(self):
        file_name = "media_document/sample_docs/England_MinTemp.txt"

        with open(file_name, "rb") as file:
            self.file_content = file.read()

        self.uploaded_file = SimpleUploadedFile("file_name", self.file_content)
        self.url = reverse("media_document:handler-document-upload")

    def test_upload_document(self):
        request_data = {
            "file_name": self.uploaded_file,
            "region": Region.get_string_for_value(Region.ENGLAND.value),
            "parameter": Parameter.get_string_for_value(Parameter.MIN_TEMP.value),
        }

        response = self.client.post(self.url, request_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_document_missing_file_name_in_request_data(self):
        request_data = {
            # "file_name": self.uploaded_file, # not using file_name to get the error
            "region": Region.get_string_for_value(Region.ENGLAND.value),
            "parameter": Parameter.get_string_for_value(Parameter.MIN_TEMP.value),
        }

        response = self.client.post(self.url, request_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Missing file_name")

    def test_upload_document_missing_region_in_request_data(self):
        request_data = {
            "file_name": self.uploaded_file,
            # "region": Region.get_string_for_value(Region.ENGLAND.value), # not using region to get the error
            "parameter": Parameter.get_string_for_value(Parameter.MIN_TEMP.value),
        }

        response = self.client.post(self.url, request_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Missing region")

    def test_upload_document_missing_parameter_in_request_data(self):
        request_data = {
            "file_name": self.uploaded_file,
            "region": Region.get_string_for_value(Region.ENGLAND.value),
            # "parameter": Parameter.get_string_for_value(Parameter.MIN_TEMP.value), # not using parameter to get the error
        }

        response = self.client.post(self.url, request_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Missing parameter")
