from django import forms
from board.models import Post, Answer, Comment

class PostForm(forms.ModelForm):
    area = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Post
        fields = ['subject', 'content']
        labels = {
            'subject' : '제목',
            'content' : '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content' : '내용',
        }

class AreaForm(forms.Form):
    area1 = forms.CharField()
    area2 = forms.CharField()
    area3 = forms.CharField()