import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render

from boutique.decorators import ajax_required
from messenger.models import Message
from shop.models import Product


@login_required
def inbox(request):
    conversations = Message.get_conversations(user=request.user)
    active_conversation = None
    messages = None
    active_id = None
    if conversations:
        conversation = conversations[0]
        active_conversation = conversation['user'].username
        active_id = conversation['user'].id
        messages = Message.objects.filter(user=request.user,
                                          conversation=conversation['user'])
        messages.update(is_read=True)
        for conversation in conversations:
            if conversation['user'].username == active_conversation:
                conversation['unread'] = 0

    return render(request, 'messenger/inbox.html', {
        'messages': messages,
        'conversations': conversations,
        'activeId': active_id,
        'active': active_conversation
        })


@login_required
def messages(request, username):
    conversations = Message.get_conversations(user=request.user)
    active_conversation = username

    messages = Message.objects.filter(user=request.user,
                                      conversation__username=username)

    context = {
        'username': username,
    }

    inbox_context = {'activeId': messages.first().conversation.id}

    if request.method == 'GET' and not messages:
        return render(request, 'messenger/new.html', context)

    messages.update(is_read=True)
    for conversation in conversations:
        if conversation['user'].username == username:
            conversation['unread'] = 0

    inbox_context['messages'] = messages
    inbox_context['conversations'] = conversations
    inbox_context['active'] = active_conversation
    inbox_context['activeId'] = messages.first().conversation.id

    return render(request, 'messenger/inbox.html', inbox_context)


@login_required
def new(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')

        try:
            to_user = User.objects.get(username=to_user_username)

        except Exception:
            try:
                to_user_username = to_user_username[
                    to_user_username.rfind('(')+1:len(to_user_username)-1]
                to_user = User.objects.get(username=to_user_username)

            except Exception:
                print('new message error')
                return redirect('/messages/new/')

        message = request.POST.get('message')
        if len(message.strip()) == 0:
            return redirect('/messages/new/')

        if from_user != to_user:
            Message.send_message(from_user, to_user, message)
        return redirect('/messages/{0}/'.format(to_user_username))

    else:
        conversations = Message.get_conversations(user=request.user)
        return render(request, 'messenger/new.html',
                      {'conversations': conversations})


@login_required
@ajax_required
def delete(request):
    return HttpResponse()


@login_required
@ajax_required
def send(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = User.objects.get(username=to_user_username)
        message = request.POST.get('message')

        if len(message.strip()) == 0:
            return HttpResponse()
        if from_user != to_user:
            msg = Message.send_message(from_user, to_user, message)
            return render(request, 'messenger/includes/partial_message.html',
                          {'message': msg})

        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@login_required
@ajax_required
def users(request):
    users = User.objects.filter(is_active=True)
    dump = []
    template = '{0} ({1})'
    for user in users:
        if user.profile.get_screen_name() != user.username:
            dump.append(template.format(user.profile.get_screen_name(),
                                        user.username))
        else:
            dump.append(user.username)
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')


@login_required
@ajax_required
def check(request):
    count = Message.objects.filter(user=request.user, is_read=False).count()
    return HttpResponse(count)


@login_required
@ajax_required
def latest(request):
    data = {}
    from_user_id = request.GET.get('from_user')
    if from_user_id:
        from_user = User.objects.get(pk=from_user_id)
        latest = Message.objects.filter(user=request.user, from_user=from_user, is_read=False).last()
        if latest:
            if request.GET.get('is_read'):
                data = {'success': True}
                latest.is_read = True
                latest.save()
            else:
                data = {
                    "message": latest.message,
                    "date": str(latest.date.__format__('%b %m %H:%m')),
                    "user": latest.conversation.username,
                    "picture": latest.conversation.profile.get_picture()
                }
    return HttpResponse(json.dumps(data), content_type='application/json')