from django.urls import path
from . import views

app_name = 'first_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('questionhub/', views.QuestionhubView.as_view(), name='questionhub'),
    path('questionhub/<int:question_id>', views.question, name='question'),
    path('newquestion/', views.newquestion, name ='newquestion'),
    path('newanswer/<int:question_id>', views.newanswer, name='newanswer'),
    path('editanswer/<int:answer_id>', views.editanswer, name='editanswer'),
    path('deleteanswer/<int:answer_id>', views.deleteanswer, name='deleteanswer'),
]
