# voting_app/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Poll, Choice

def index(request):
    polls = Poll.objects.all()
    data = {'polls': [{'id': poll.id, 'question': poll.question} for poll in polls]}
    return JsonResponse(data)

def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    data = {'id': poll.id, 'question': poll.question, 'choices': [{'id': choice.id, 'choice_text': choice.choice_text} for choice in poll.choice_set.all()]}
    return JsonResponse(data)

def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return JsonResponse({'error': "You didn't select a choice."}, status=400)

    selected_choice.votes += 1
    selected_choice.save()
    
    data = {'success': True}
    return JsonResponse(data)

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    data = {
        'id': poll.id,
        'question': poll.question,
        'results': [{'choice_text': choice.choice_text, 'votes': choice.votes} for choice in poll.choice_set.all()]
    }
    return JsonResponse(data)
