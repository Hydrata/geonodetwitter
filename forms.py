from django.forms import Form, ModelForm
from models import HashtagStatus


class HashtagStatusForm(ModelForm):
    class Meta:
        model = HashtagStatus
        fields = ['hashtag']
