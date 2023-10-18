from django.shortcuts import render, redirect
from .models import Tweet, Follow
from django.contrib.auth.decorators import login_required

@login_required
def tweet_create(request):
    if request.method == 'POST':
        content = request.POST['content']
        tweet = Tweet.objects.create(user=request.user, content=content)
        tweet.save()
        return redirect('feed')

@login_required
def feed(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    following_ids = list(following_ids) + [request.user.id]
    tweets = Tweet.objects.filter(user_id__in=following_ids).order_by('-timestamp')
    return render(request, 'feed.html', {'tweets': tweets})
