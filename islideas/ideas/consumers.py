from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.sessions import channel_session

from .models import Vote, Idea, Comment


# Connected to websocket.connect
@channel_session_user_from_http
def ws_connect(message):
    # # Work out room name from path (ignore slashes)
    # room = message.content['path'].strip("/")
    # # Save room in session and add us to the group
    # message.channel_session['room'] = room
    # Group('chat').add(message.reply_channel)
    pass


# Connected to websocket.receive
@channel_session_user
def ws_message(message):
    msg = message.content.get('text')
    listify_msg = msg.split('/_/')
    action = listify_msg[0]
    idea_id = listify_msg[1]

    if action == 'add_vote:':
        try:
            idea = Idea.objects.get(id=int(idea_id))
            Vote.objects.create(author=message.user, idea=idea)
            resp = {'text': 'vote_success'}
        except Idea.DoesNotExist:
            resp = {'text': 'vote_failure- idea does not exist'}

    elif action == 'remove_vote:':
        Vote.objects.filter(author=message.user, idea_id=idea_id).delete()
        resp = {'text': 'vote_success'}

    elif action == 'add_comment:':
        try:
            description = listify_msg[2]
            idea = Idea.objects.get(id=int(idea_id))
            idea_slug = idea.slug
            new_comment = Comment.objects.create(author=message.user,
                                                 idea=idea,
                                                 description=description)
            listified_comment = ['comment_success:',
                                 str(new_comment.author_name),
                                 new_comment.description,
                                 str(new_comment.date), str(new_comment.id),
                                 idea_slug]
            stringified_comment = '/_/'.join(listified_comment)
            resp = {'text': stringified_comment}
        except Idea.DoesNotExist:
            resp = {'text': 'comment_failure- idea does not exist'}

    else:
        resp = {'text': 'failure'}

    message.reply_channel.send(resp)


# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    pass
