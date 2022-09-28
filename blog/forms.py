from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		exclude = ["post"]
	
		labels = {
			"user_name" : "Your Name",
			"user_email" : "Your Email",
			"user_comment" : "Your Comment",
		}
		error_messages = {
			"user_name" : {
				"required" : "Name Field Must Be Filled !!",
			},
			"user_comment" : {
				"required" : "Comment Field Must Be Filled !!"
			}
		}