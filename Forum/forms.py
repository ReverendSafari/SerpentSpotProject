from django import forms
from .models import Thread, Post, PostImage

class NewThreadForm(forms.ModelForm):
      
    message = forms.CharField(
        required=True,  # Explicitly make this field required
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'What are you thinking?'}),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )
    image1 = forms.ImageField(required=False, help_text='Optional image upload')
    image2 = forms.ImageField(required=False, help_text='Optional image upload')
    image3 = forms.ImageField(required=False, help_text='Optional image upload')

    class Meta:
        model = Thread
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(NewThreadForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter thread title'})
        self.fields['title'].widget.attrs['required'] = 'required'
        self.fields['message'].widget.attrs['required'] = 'required'

    def save(self, commit=True):
        thread = super().save(commit=False)
        if commit:
            thread.starter = self.instance.starter
            thread.save()
            post = Post.objects.create(
                message=self.cleaned_data['message'],
                thread=thread,
                created_by=self.instance.starter  # Assuming 'starter' is passed as form instance
            )
            # Save images if provided
            for field_name in ['image1', 'image2', 'image3']:
                image_field = self.cleaned_data.get(field_name)
                if image_field:
                    PostImage.objects.create(post=post, image=image_field)
        return thread

class PostForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5, 
            'placeholder': 'Type your reply here...',
            'maxlength': '4000'  # Ensures HTML5 browser validation
        }),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )
    image = forms.ImageField(required=False, help_text='Optional image upload')  # Add an optional image field

    class Meta:
        model = Post
        fields = ['message']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            # Save the image if provided
            image_field = self.cleaned_data.get('image')
            if image_field:
                PostImage.objects.create(post=post, image=image_field)
        return post
