import logging
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .ideas.forms import IdeaForm, CommentForm, VoteForm
from .ideas.models import Idea, Tag, Comment, Vote


logger = logging.getLogger('islideas')
login_url = '/'


class ActionMixin(object):
    # Add message of any level
    def add_message(self, msg, level=messages.INFO):
        messages.add_message(self.request, level, msg)

    # Add success messages for forms evaluated to valid
    def form_valid(self, form):
        if hasattr(self, 'success_msg'):
            self.add_message(self.success_msg, level=messages.SUCCESS)
        return super(ActionMixin, self).form_valid(form)


class TagMixin(object):
    def create_tag_list(self, form):
        tag_ids = []
        for each in form['tags'].value():
            try:
                tag = Tag.objects.get(id=each)
            except:
                try:
                    tag = Tag.objects.get(name=each.lower())
                except:
                    tag = Tag.objects.create(name=each.lower())
                    # self.add_message('{0} was added as a new tag!'.format(
                    #     tag.name), level=messages.SUCCESS)
            tag_ids.append(tag.id)
        return tag_ids


class IndexView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            view = TopIdeaList.as_view()
        else:
            view = LoginView.as_view()
        return view(request, *args, **kwargs)


class LoginView(TemplateView):
    template_name = 'ideas/login.html'


class IdeaList(ActionMixin, LoginRequiredMixin, ListView):
    model = Idea
    template_name = 'ideas/idea_list.html'

    def get_context_data(self, **kwargs):
        context = super(IdeaList, self).get_context_data(**kwargs)
        context['vote_form'] = VoteForm()
        context['user_votes'] = Vote.objects.filter(
            author=self.request.user).values_list('idea_id', flat=True)
        return context


class NewIdeaList(IdeaList):
    ordering = ('-date')


class TopIdeaList(IdeaList):
    ordering = ('-popularity')


class TagList(ListView):
    model = Tag
    template_name = 'ideas/tag_list.html'


class TagDetail(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'ideas/tag.html'

    def get_context_data(self, **kwargs):
        context = super(TagDetail, self).get_context_data(**kwargs)
        context['idea_list'] = Idea.objects.filter(
            tags__name__icontains=self.kwargs['slug'])
        context['vote_form'] = VoteForm()
        context['user_votes'] = Vote.objects.filter(
            author=self.request.user).values_list('idea_id', flat=True)
        return context


class IdeaCreate(ActionMixin, TagMixin, LoginRequiredMixin, CreateView):
    model = Idea
    form_class = IdeaForm

    def get_context_data(self, **kwargs):
        context = super(IdeaCreate, self).get_context_data(**kwargs)
        context['idea_form'] = IdeaForm()
        return context

    def post(self, request, *args, **kwargs):
        idea_form = IdeaForm(request.POST)

        if idea_form.has_changed():
            tag_ids = self.create_tag_list(idea_form)

            # Disable tag field so is_valid can be called
            idea_form.fields['tags'].disabled = True
            if idea_form.is_valid():
                new_idea = idea_form.save(commit=False)
                new_idea.author = request.user
                new_idea.save()

                # Add tag field back into idea
                for each in tag_ids:
                    new_idea.tags.add(each)

                self.add_message(
                    'Your idea was added!',
                    level=messages.SUCCESS)
                return redirect('idea_detail', new_idea.slug)
            else:
                idea_form.fields['tags'].disabled = False
                self.add_message(
                    'Sorry, your idea could not be added.',
                    level=messages.ERROR)
                return render(request, 'ideas/idea_form.html', {
                    'idea_form': idea_form})

        # If only TagForm was added, reload page to display messages
        else:
            return redirect('idea_form')


class IdeaUpdate(ActionMixin, TagMixin, LoginRequiredMixin, UpdateView):
    model = Idea
    form_class = IdeaForm
    template_name_suffix = '_update_form'
    success_url = '/ideas/{slug}'


    def post(self, request, *args, **kwargs):
        # Create form from request data
        form = self.form_class(
            instance=self.get_object(), data=request.POST)
        # Get or create requested tags
        tag_ids = self.create_tag_list(form)

        # Create form without tags
        request_post_copy = request.POST.copy()
        request_post_copy.pop('tags')
        form_clean_tags = self.form_class(
            instance=self.get_object(), data=request_post_copy)

        # Create idea, add author and tags, and save
        if form_clean_tags.is_valid():
            updated_idea = form_clean_tags.save(commit=False)
            updated_idea.author = request.user
            updated_idea.tags = tag_ids
            updated_idea.save()
            self.add_message(
                'Your idea was updated!',
                level=messages.SUCCESS)
            return redirect('idea_detail', updated_idea.slug)
        else:
            self.add_message(
                'Sorry, your idea could not be updated.',
                level=messages.ERROR)
            return redirect('idea_detail', slug=kwargs['slug'])


class IdeaDelete(ActionMixin, LoginRequiredMixin, DeleteView):
    model = Idea

    def get_success_url(self):
        return reverse_lazy('home')


class IdeaDetail(ActionMixin, LoginRequiredMixin, DetailView):
    model = Idea
    form_class = IdeaForm

    def get_context_data(self, **kwargs):
        context = super(IdeaDetail, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['vote_form'] = VoteForm()
        context['user_votes'] = Vote.objects.filter(
            author=self.request.user).values_list('idea_id', flat=True)
        return context

    def post(self, request, *args, **kwargs):
        idea = get_object_or_404(Idea, slug=kwargs['slug'])

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.idea = idea
            new_comment.save()
            self.add_message('Your comment was added!', level=messages.SUCCESS)

        vote_form = VoteForm(request.POST)
        if vote_form.is_valid():
            new_vote = vote_form.save(commit=False)
            # Only save VoteForm data if vote was added
            if new_vote.vote_1:
                new_vote.idea = idea
                new_vote.save()
                self.add_message(
                    'Your vote was tallied!', level=messages.SUCCESS)

        # return redirect('idea_detail', idea.slug,)
        return self.post_success()

    def success(self):
        if self.request.is_ajax():
            response_data = {}
            return JsonResponse(response_data)

    def post_success(self):
        return self.success()


class CommentDelete(ActionMixin, LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        self.add_message("Comment deleted!", level=messages.SUCCESS)
        return reverse_lazy(
            'idea_detail', kwargs={'slug': self.kwargs['idea_slug']})


class CommentUpdate(ActionMixin, LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        self.add_message("Comment edited!", level=messages.SUCCESS)
        return reverse_lazy(
            'idea_detail', kwargs={'slug': self.kwargs['idea_slug']})
