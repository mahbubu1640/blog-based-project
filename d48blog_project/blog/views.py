#from curses.ascii import EM
from email import message
from webbrowser import get
from django.shortcuts import get_object_or_404, redirect, render
from blog.models import Post
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.
from blog.forms import Signupform

def post_list_view(request):
    post_list=Post.objects.all()
    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',{'post_list':post_list})



from django.views.generic import ListView
from blog.forms import CommentForm
class PostListView(ListView):
    model=Post
    paginate_by=1


    
def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
    status='published',
    publish__year=year,
    publish__month=month,
    publish__day=day,)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()

    return render(request,'blog/post_detail.html',{'post':post,'form':form,'csubmit':csubmit})
def get_absolute_url(self):
    return reverse('post_detail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])

from django.core.mail import send_mail
from blog.forms import EmailSendForm

def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject='{}({}) recommends you to read"{}"'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message='Read Post At:\n {}\n\n{}\'s Comments:\n{}'.format('post_url',cd['name'],cd['comments'])
            send_mail(subject,'message','4020alam@gmail.com',[cd['to']])
            send=True
    else:
        form=EmailSendForm()
    return render(request,'blog/sharebymail.html',{'form':form,'post':post})


def premium_view(request):
    return render(request,'blog/premium.html')

def logout_view(request):
    return render(request,'blog/logout.html')

def contact_view(request):
    return render(request,'blog/contact.html')

def signup_view(request):
    form = Signupform()
    if request.method == 'POST':
        form = Signupform(request.POST)
        user = form.save()
        user.set_password(user.password)
        user.save()
        return redirect('/accounts/login')
    return render(request,'blog/signup.html',{'form':form})