from django import forms
from blogapp.models import Comment, Post, Reply

class CommentForm(forms.ModelForm):
    parent_comment = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    text = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your comment here'}),
        label='',  # Explicitly set label to an empty string
    )

    class Meta:
        model = Comment
        fields = ('text', 'parent_comment')
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image1', 'image2','image3','image4', 'image5','image6', 'image7', 'tags', 'categories')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the content'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'rows': 4, 'cols': 40, 'class': 'form-control', 'placeholder': 'Write your reply here'}),
        }
