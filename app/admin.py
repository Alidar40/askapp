from django.contrib import admin
from .models import Question, Answer, LikeToQuestion, LikeToAnswer, Tag, Profile

# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(LikeToAnswer)
admin.site.register(LikeToQuestion)
admin.site.register(Tag)
admin.site.register(Profile)
