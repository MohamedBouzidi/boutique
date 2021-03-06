import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render

from boutique.decorators import ajax_required
from messenger.forms import AttachementForm
from messenger.models import Message, Attachement, Notification
from shop.models import Product


def get_products(user_id):
    return Product.objects.filter(boutique__owner__user__pk=user_id)[:3] or Product.objects.all()[:3]

def get_messages(from_user, to_user, last=0, count=5):
    if isinstance(to_user, User):
        messages =  Message.objects.filter(user=from_user, conversation=to_user)
    else:
        messages =  Message.objects.filter(user=from_user, conversation__id=to_user)

    messages_count = messages.count()

    last = messages_count - last

    if last <= 0:
        return None
    elif 0 <= last <= count:
        return messages[:last]

    print('last is ', last, ' | count is ', messages_count)

    return messages[last-count:last]

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
        messages = get_messages(request.user, conversation['user'])
        for message in messages:
            message.is_read = True
            message.save()
        for conversation in conversations:
            if conversation['user'].username == active_conversation:
                conversation['unread'] = 0

    return render(request, 'messenger/inbox.html', {
        'messages': messages,
        'conversations': conversations,
        'activeId': active_id,
        'active': active_conversation,
        'products': get_products(active_id)
    })


@login_required
def messages(request, username):
    conversations = Message.get_conversations(user=request.user)
    active_conversation = username
    active_id = User.objects.get(username=username).id

    messages = get_messages(request.user, active_id)

    context = {
        'username': username,
        'products': get_products(active_id)
    }
    inbox_context = {}

    if request.method == 'GET' and not messages:
        return render(request, 'messenger/new.html', context)

    for message in messages:
        message.is_read = True
        message.save()
    for conversation in conversations:
        if conversation['user'].username == username:
            conversation['unread'] = 0

    inbox_context['messages'] = messages
    inbox_context['conversations'] = conversations
    inbox_context['active'] = active_conversation
    inbox_context['activeId'] = active_id
    inbox_context['products'] = get_products(active_id)

    return render(request, 'messenger/inbox.html', inbox_context)


@login_required
def messages_ajax(request):
    if request.method == 'GET':
        user_id = request.GET.get('userId')
        messages = None
        if not not user_id:
            conversation = User.objects.get(pk=user_id)
            messages = get_messages(request.user, conversation)
            context = {
                'activeId': user_id,
                'active': conversation.username,
                'products': get_products(user_id),
                'messages': messages
            }
    return render(request, 'messenger/includes/conversation.html', context)


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
def send(request):
    if request.method == 'POST':
        msg = None
        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = User.objects.get(username=to_user_username)
        message = request.POST.get('message')

        if len(message.strip()) == 0:
            return HttpResponse()

        if from_user != to_user:
            form = AttachementForm(request.POST, request.FILES)

            if form.is_valid():
                obj = form.save(commit=False)
                msg = Message.send_message(from_user, to_user, message, attachement=obj)
                obj.message = msg
                print(msg.attachement)
                obj.save()
                
                dub = obj
                dub.id = None
                dub.message = Message.objects.last()
                dub.save()
            else:
                msg = Message.send_message(from_user, to_user, message)
                print('form is invalid')

        return render(request, 'messenger/includes/partial_message.html', {'message': msg})
    else:
        print('This is a bad request inside send view')
        return HttpResponseBadRequest()


@login_required
@ajax_required
def send_product(request):
    msg = None
    if request.method == 'POST':
        from_user = request.user
        to_user_id = request.POST.get('to')
        to_user = User.objects.get(pk=to_user_id)

        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)

        if product and from_user != to_user:
            msg = Message.send_message(from_user, to_user, product=product)

    return render(request, 'messenger/includes/partial_message.html', {'message': msg})


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
def user_messages(request, user_id):
    if request.method == 'GET':
        last = int(request.GET.get('last'))
        count = int(request.GET.get('count'))
        messages = get_messages(from_user=request.user, to_user=user_id, last=last, count=count)
        return render(request, 'messenger/includes/partial_messages_list.html', {'messages': messages})
    else:
        return HttpResponse()


@login_required
@ajax_required
def check(request):
    count = Message.objects.filter(user=request.user, is_read=False).count()
    return HttpResponse(count)


@login_required
@ajax_required
def latest(request):
    latest = None
    from_user_id = request.GET.get('from_user')
    if from_user_id:
        from_user = User.objects.get(pk=from_user_id)
        latest = Message.objects.filter(user=request.user, from_user=from_user, is_read=False).last()
        if latest:
            if request.GET.get('is_read'):
                data = {'success': True}
                latest.is_read = True
                latest.save()
    return render(request, 'messenger/includes/partial_message.html', {'message': latest})


@login_required
@ajax_required
def notification(request):
    if request.method == 'GET':
        if request.GET.get('unread'):
            notifications = request.user.profile.get_unread_notifications()
        else:
            notifications = request.user.profile.get_all_notifications()

        if notifications:
            notifications = notifications[:3]
        return render(request, 'messenger/includes/notification_list.html', {'notifications': notifications})
    else:
        return HttpResponse('post notification')


@login_required
@ajax_required
def notification_count(request):
    if request.method == 'GET':
        data = request.user.profile.get_unread_notifications()
        print(data)
        if data:
            return HttpResponse(json.dumps(data.count()), content_type='application/json')
        return HttpResponse()
    else:
        request.user.profile.read_all_notifications()
        return HttpResponse(json.dumps(0), content_type='application/json')


@login_required
def notifications(request):
    return render(request, 'messenger/notifications.html', 
        {'notifications': request.user.profile.get_all_notifications()})