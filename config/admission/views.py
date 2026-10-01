from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services.rag_service import AdmissionRAGService


class AdmissionChatView(APIView):

    def post(self, request):

        query = request.data.get("query")

        print(query)
        if not query:
            return Response(
                {
                    "error": "Query is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serviceOBJ = AdmissionRAGService()
        answer = serviceOBJ.ask(query)
        print(answer)
        return Response(
            {
                "answer": answer
            }
        )