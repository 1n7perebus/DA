from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.conf import settings

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.utils import timezone

from django.db.models import *
from .forms import *
from .models import *

def index(request):
    dreams = Dreams.objects.all()
    recent_submission = False
    #json_data = None
        
    if request.method == "POST":
        ip_address = request.META.get('REMOTE_ADDR')
        print("IP Address:", ip_address)  
        # CHANGE THIS BEFORE DEPLOYMENT
        recent_submission = Dreams.objects.filter(ip_address=ip_address, submission_time__gte=timezone.now() - timezone.timedelta(seconds=1)).exists()
        #recent_submission = Dreams.objects.filter(ip_address=ip_address, submission_time__gte=timezone.now() - timezone.timedelta(days=1)).exists()
        print("Recent Submission:", recent_submission)  
        dream_form = DreamForm(request.POST)
        
        if dream_form.is_valid() and not recent_submission:
            dream_post = dream_form.save(commit=False)
            
            dream_post.ip_address = ip_address
            sender = dream_post.email 
        
            dream_post.save()
            '''
            from_email = 'dreamanalytica@outlook.com'
            to_email = 'dreamanalytica08@gmail.com'
            
            subject = "New Dream Submission"
            context = {
                "name": dream_post.name,
                "mbti_type": dream_post.mbti_type,
                "email": dream_post.email,
                "phone": dream_post.phone,
                "title": dream_post.title,
                "dream": dream_post.dream,
                "pub": dream_post.pub, 
            }

            html_message = render_to_string("dreamapp/email_templates/dream_submission.html", context)
            plain_message = strip_tags(html_message)
            # Send the email
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=from_email,
                to=[to_email, sender],
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)
            '''
            '''
            pub_str = dream_post.pub.strftime('%Y-%m-%d %H:%M:%S') if dream_post.pub else None

            dream_data = {
                'id': str(dream_post.id),
                'ip_address': dream_post.ip_address,
                'submission_time': dream_post.submission_time.strftime('%Y-%m-%d %H:%M:%S'),
                'name': dream_post.name,
                'mbti_type': dream_post.mbti_type,
                'email': dream_post.email,
                'phone': str(dream_post.phone),
                'title': dream_post.title,
                'dream': dream_post.dream,
                'active': dream_post.active,
                'pub': pub_str,
            }
            
            json_data = json.dumps(dream_data)

            file_path = os.path.join(os.getcwd(), f"{dream_post.id}.json")

            with open(file_path, 'w') as file:
                file.write(json_data)
            # Store the JSON data in Firebase storage
            storage.child("dreams").child(f"{dream_post.id}.json").put(file_path)
            '''
            return HttpResponseRedirect("dreams")
        else:
            print("Form is not valid or recent submission exists")  
            print("Form errors:", dream_form.errors)
            print("Submitted data:", request.POST)

    else:
        dream_form = DreamForm()

    mbti_choices = DreamForm.MBTI_CHOICES

    return render(request, "dreamapp/index.html", context={"dreams": dreams,
                                                             "dream_form": dream_form,
                                                             "recent_submission": recent_submission,
                                                             "mbti_choices": mbti_choices,})
   

def dreams(request):
    all_json_data = []
    dreams_with_replies = []
    dreams = Dreams.objects.all()
    for dream in dreams:
        replies = Reply.objects.filter(dream=dream)
        dreams_with_replies.append({'dream': dream, 'replies': replies})


    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            try:
                dream_id = request.POST.get('dream_id')
                dream_instance = get_object_or_404(Dreams, id=dream_id)
                print(f"Dream Instance: {dream_instance}")  
            except Exception as e:
                print(f"Error retrieving Dream: {e}")  
                dream_instance = None

            if dream_instance:
                print("Saving Reply...") 

                reply = reply_form.save(commit=False)
                reply.dream = dream_instance
                reply.reply = request.POST.get('reply')
                reply.pub = timezone.now()
                reply.save()

                print("Reply saved successfully!")  

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        reply_form = ReplyForm()

    return render(request, "dreamapp/dreams.html", context={
        "dreams_with_replies": dreams_with_replies,
        "dreams": dreams,
        "reply_form": reply_form,
        "all_json_data": all_json_data,
    })


    '''
    if dreams.exists():
        for dream_post in dreams:
            file_path = f"dreams/{dream_post.id}.json"
            # Get the download URL for the file from Firebase Storage
            download_url = storage.child(file_path).get_url(None)
            # Make an HTTP GET request to the download URL
            response = requests.get(download_url)
            # Check if the request was successful
            if response.status_code == 200:
                # Read the JSON data from the response
                json_data = response.json()
                # Append the JSON data to the list
                all_json_data.append(json_data)
            else:
                print(f"Error: Unable to fetch JSON data for dream ID {dream_post.id} from Firebase Storage. Status code: {response.status_code}")
    else:
        print("No dreams found.")
    '''
