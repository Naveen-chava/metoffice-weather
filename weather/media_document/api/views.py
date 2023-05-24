from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from services.media_document import svc_media_document_process_the_text_file


class DocumentUploadView(generics.GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, **kwargs):
        try:
            svc_media_document_process_the_text_file(request.data)
            return Response(status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IndexError as e:
            return Response(
                {"message": "Corrupted text file. Please ensure that text file is in proper format"},
                status=status.HTTP_400_BAD_REQUEST,
            )
