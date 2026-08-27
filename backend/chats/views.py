from django.http import HttpResponse

# Create your views here.
def chat_view(request):
    return HttpResponse("Running chats")