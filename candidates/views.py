from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import CandidateService
from .models import Candidate
from .serializers import CandidateSerializer

class CandidateAPIView(APIView):

    def get(self, request):
        """
        Search candidates by name query string.
        """
        query = request.query_params.get("q", "")
        queryset = Candidate.objects.all()
        filtered = CandidateService.search_candidates(query, queryset)
        serializer = CandidateSerializer(filtered, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new candidate.
        """
        service = CandidateService(data=request.data)
        candidate = service.instance
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        """
        Full update of an existing candidate (requires 'id' in body).
        """
        candidate_id = request.data.get("id")
        if not candidate_id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        service = CandidateService(id=candidate_id)
        updated_candidate = service.update(request.data, partial=False)
        serializer = CandidateSerializer(updated_candidate)
        return Response(serializer.data)

    def patch(self, request):
        """
        Partial update of an existing candidate (requires 'id' in body).
        """
        candidate_id = request.data.get("id")
        if not candidate_id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        service = CandidateService(id=candidate_id)
        updated_candidate = service.update(request.data, partial=True)
        serializer = CandidateSerializer(updated_candidate)
        return Response(serializer.data)

    def delete(self, request):
        """
        Delete an existing candidate (requires 'id' in body).
        """
        candidate_id = request.query_params.get("id")
        if not candidate_id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        service = CandidateService(id=candidate_id)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
