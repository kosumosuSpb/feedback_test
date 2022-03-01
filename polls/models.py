from django.db import models


# нужно ли вообще хранить шаблон в БД?
class Template(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    # questions - FK


class Project(models.Model):
    name = models.CharField(max_length=45, unique=True)
    description = models.CharField(max_length=255)
    # question_lists - FK


class QuestionList(models.Model):
    title = models.CharField(max_length=45)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='questions_lists')
    # questions - FK


class Question(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    question_list = models.ForeignKey(QuestionList, on_delete=models.CASCADE, related_name='questions')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='questions')  # надо подумать про каскадное удаление тут
    # answers - FK

    # метод-свойство для определения результатов голосования.
    # Выдаёт среднее арифметическое всех оценок из answers
    @property
    def rating(self):
        rating = self.answers.aggregate(rate=models.Avg('rating'))['rate']
        return round(rating, 1) if rating else None


class Answer(models.Model):
    rating = models.IntegerField(default=0)
    data_time = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
