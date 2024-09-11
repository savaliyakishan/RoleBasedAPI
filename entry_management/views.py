# drf
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# serializer
from entry_management.serializers import EntrySerializer

# model
from entry_management.models import Entry


# create your views here.
class EntryListCreateView(APIView):
    """
    APIView to handle listing and creating Entry objects.
    GET retrieves all entries in reverse chronological order, and POST creates a new entry.
    Returns appropriate status codes and messages based on request success.
    """

    serializer_class = EntrySerializer

    def get(self, request):
        entries = Entry.objects.all().order_by('-created_at')
        serializer = self.serializer_class(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):        
        entry_serializer = self.serializer_class(data=request.data)
        if not entry_serializer.is_valid(raise_exception=True):
            return Response({"success": False, 'message': entry_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        entry_serializer.save()
        return Response({"success": True, 'message': "Entry successfully created."}, status=status.HTTP_200_OK)
    

class EntryUpdateDeleteView(APIView):
    """
    APIView for updating and deleting specific Entry objects based on entry_id.
    PUT updates an existing entry with new data, while DELETE removes the entry from the database.
    Returns appropriate success messages and status codes based on operation outcome.
    """

    serializer_class = EntrySerializer

    def put(self, request, entry_id):
    
        entry_instance = get_object_or_404(Entry, id=entry_id)
        if not entry_instance:
            return Response({"success": True, 'message': "No matching entry found."}, status=status.HTTP_200_OK)

        entry_serializer = self.serializer_class(entry_instance, data=request.data, partial=True)
        if not entry_serializer.is_valid(raise_exception=True):
            return Response({"success": False, "message": "Entry data not updated.", "errors": entry_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        entry_serializer.save()
        
        return Response({"success": True, 'message': 'Entry updated successfully.'}, status=status.HTTP_200_OK)
        
    def delete(self, request, entry_id):

        entry_instance = get_object_or_404(Entry, id=entry_id)
        if not entry_instance:
            return Response({"success": True, 'message': "No matching entry found."}, status=status.HTTP_200_OK)
        entry_instance.delete()

        return Response({"success": True, 'message': 'Entry deleted successfully.'}, status=status.HTTP_200_OK)