from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse

from django.db.models import *
from .forms import *
from .models import *

# Checklist
# Add Sections
# Advertising Goodgle Adsense 
# Payment Mothod
# Adjust Submission Time

def index(request):
    return render(request, "dreamapp/index.html", context={})



def consult(request):
    dreams = Dreams.objects.all()
    recent_submission = False
    #json_data = None
        
    if request.method == "POST":
        ip_address = request.META.get('REMOTE_ADDR')
        #recent_submission = Dreams.objects.filter(ip_address=ip_address, submission_time__gte=timezone.now() - timedelta(days=1)).exists()

        recent_submission = Dreams.objects.filter(ip_address=ip_address, submission_time__gte=timezone.now() - timedelta(seconds=1)).exists()
        
        if recent_submission:
            # Calculate the remaining wait time before resubmitting
            last_submission_time = Dreams.objects.filter(ip_address=ip_address).latest('submission_time').submission_time
            current_time = timezone.now()
            time_difference = current_time - last_submission_time
            wait_time = timedelta(days=1) - time_difference

            messages.error(request, f"You have already submitted the form. Please wait {wait_time} before resubmitting.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        dream_form = DreamForm(request.POST)
        if dream_form.is_valid() and not recent_submission:
            dream_post = dream_form.save(commit=False)
            dream_post.ip_address = ip_address
            sender = dream_post.email 
            dream_post.save()

            from_email = 'dreamanalytica@outlook.com'
            to_email = 'dreamanalytica08@gmail.com'
            
            subject = "New Dream Submission"
            context = {
                "name": dream_post.name,
                "mbti_type": dream_post.mbti_type,
                "email": dream_post.email,
                "title": dream_post.title,
                "dream": dream_post.dream,
                "scale": dream_post.scale,
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
            email.send(fail_silently=True)
            

            return HttpResponseRedirect(reverse('main:dreams'))
        else:
            messages.error(request, "Invalid form data. Please check the entered information.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    else:
        dream_form = DreamForm()

    mbti_choices = DreamForm.MBTI_CHOICES
    return render(request, "dreamapp/consult.html", context={"dreams": dreams,
                                                             "dream_form": dream_form,
                                                             "recent_submission": recent_submission,
                                                             "mbti_choices": mbti_choices})



def dreams(request):
    dreams_with_replies = []
    dreams = Dreams.objects.all()
    reply_form = ReplyForm()

    average_scale = dreams.aggregate(Avg('scale'))['scale__avg']

    if average_scale is not None:
        if average_scale > 6:
            health_status = "healthy"
            health_color = "teal-green"
        elif average_scale < 4:
            health_status = "unhealthy"
            health_color = "maroon-red"
        else:
            health_status = "neutral"
            health_color = "neutral-color"
    else:
        health_status = "No data available"
        health_color = "neutral-color"

    if request.method == 'POST':
        ip_address = request.META.get('REMOTE_ADDR')
        reply_form = ReplyForm(request.POST)

        # Check if the user has submitted a reply in the last 24 hours
        recent_submission = Share.objects.filter(ip_address=ip_address, submission_time__gte=timezone.now() - timedelta(days=1)).exists()

        if recent_submission:
            last_submission_time = Share.objects.filter(ip_address=ip_address).latest('submission_time').submission_time
            current_time = timezone.now()
            time_difference = current_time - last_submission_time
            wait_time = timedelta(days=1) - time_difference

            messages.error(request, f"You have already submitted the form. Please wait {wait_time} before resubmitting.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        elif reply_form.is_valid():
            dream_email = request.POST.get('dream_email')
            try:
                dream_instance = get_object_or_404(Dreams, email=dream_email)
                reply = reply_form.save(commit=False)
                reply.dream = dream_instance
                reply.reply = request.POST.get('reply')
                reply.pub = timezone.now()
                reply.save()

                # Log success
                print("Reply saved successfully!")  

                # Record the submission
                Share.objects.create(ip_address=ip_address, submission_time=timezone.now())

                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except Dreams.DoesNotExist:
                messages.error(request, "Dream not found. Please check the email address.")
            except Exception as e:
                print(f"Error: {e}")
                messages.error(request, "An error occurred. Please try again later.")
            
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Invalid form data. Please check the entered information.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    for dream in dreams:
        replies = Reply.objects.filter(dream=dream)
        dreams_with_replies.append({'dream': dream, 'replies': replies})

    return render(request, "dreamapp/dreams.html", {
        "dreams_with_replies": dreams_with_replies,
        "dreams": dreams,
        "reply_form": reply_form,
        "average_scale": average_scale,
        "health_status": health_status,
        "health_color": health_color,
    })

def analyticalPsychology(request):
    return render(request, "dreamapp/analyticalPsychology.html")

def anima(request):
    return render(request, "dreamapp/anima.html")

def animus(request):
    return render(request, "dreamapp/animus.html")


def typology(request):
    return render(request, "dreamapp/typology.html")

def error(request):
    return render(request, "dreamapp/error.html")

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
    