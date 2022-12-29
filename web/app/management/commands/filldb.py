from random import choice
from itertools import islice
from django.core.management.base import BaseCommand
from ...models import *
from faker import Faker

faker = Faker()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-u", "--users", type=int)
        parser.add_argument("-t", "--tags", type=int)
        parser.add_argument("-q", "--questions", type=int)
        parser.add_argument("-a", "--answers", type=int)
        parser.add_argument("-lq", "--likes_question", type=int)
        parser.add_argument("-la", "--likes_answer", type=int)
        parser.add_argument("-all", "--all", type=int)

    def handle(self, *args, **options):
        num_of_users = options["users"]
        num_of_questions = options["questions"]
        num_of_answers = options["answers"]
        num_of_tags = options["tags"]
        num_of_likes_on_question = options["likes_question"]
        num_of_likes_on_answer = options["likes_answer"]
        num = options["all"]

        if num:
            self.fill_users(num * 10)
            self.fill_tags(num * 10)
            self.fill_questions(num * 100)
            self.fill_answers(num * 1000)
            self.fill_likes_on_question(num * 2000)
            self.fill_likes_on_answer(num * 2000)
        if num_of_tags:
            self.fill_tags(num_of_tags * 10)
        if num_of_users:
            self.fill_users(num_of_users * 10)
        if num_of_questions:
            self.fill_questions(num_of_questions * 100)
        if num_of_answers:
            self.fill_answers(num_of_answers * 1000)
        if num_of_likes_on_question:
            self.fill_likes_on_question(num_of_likes_on_question * 2000)
        if num_of_likes_on_answer:
            self.fill_likes_on_answer(num_of_likes_on_answer * 2000)

    def fill_questions(self, n):
        users = list(
            Profile.objects.values_list(
                "id", flat=True
            )
        )
        tags = list(
            Tag.objects.values_list(
                "id", flat=True
            )
        )

        for i in range(n):
            question = Question.objects.create(author_id=choice(users),
                                               title=faker.sentence()[:128],
                                               text=". ".join(faker.sentences(faker.random_int(min=2, max=5))),
                                               date=faker.date_between("-100d", "today"))
            tag1 = choice(tags)
            tag2 = choice(tags)
            while tag1 == tag2:
                tag2 = choice(tags)
            question.tags.add(tag1)
            question.tags.add(tag2)

    def fill_answers(self, n):
        questions = list(
            Question.objects.values_list(
                "id", flat=True
            )
        )
        users = list(
            Profile.objects.values_list(
                "id", flat=True
            )
        )
        answers = []

        for i in range(n):
            answer = Answer(question_id=choice(questions),
                            author_id=choice(users),
                            text=". ".join(faker.sentences(faker.random_int(min=2, max=5))))
            answers.append(answer)

        batch_size = 100000
        while True:
            batch = list(islice(answers, batch_size))
            del answers[:batch_size]
            if not batch:
                break
            Answer.objects.bulk_create(batch, batch_size)

    def fill_users(self, n):
        usernames = set()

        while len(usernames) != n:
            usernames.add(faker.user_name() + str(faker.random.randint(0, 1000000)))

        for name in usernames:
            # user = User.objects.create_user(username=name, password=faker.password(), email=faker.email())
            user = User.objects.create_user(username=name, password='asdf', email=faker.email())
            Profile.objects.create(user=user, login=faker.name())

    def fill_tags(self, n):
        for i in range(n):
            Tag.objects.create(name=faker.word(), rating=faker.random.randint(0, 255))

    def fill_likes_on_question(self, n):
        questions = list(
            Question.objects.values_list(
                "id", flat=True
            )
        )
        users = list(
            Profile.objects.values_list(
                "id", flat=True
            )
        )
        likes = []
        for i in range(n):
            like = LikeToQuestion(question_id=choice(questions), user_id=choice(users),
                                  is_liked=faker.random.randint(-1, 1))
            question = Question.objects.get(id=like.question_id)
            question.rating += like.is_liked
            question.save()
            likes.append(like)

        batch_size = 100000
        while True:
            batch = list(islice(likes, batch_size))
            del likes[:batch_size]
            if not batch:
                break
            LikeToQuestion.objects.bulk_create(batch, batch_size)

    def fill_likes_on_answer(self, n):
        answers = list(
            Answer.objects.values_list(
                "id", flat=True
            )
        )
        users = list(
            Profile.objects.values_list(
                "id", flat=True
            )
        )
        likes = []
        for i in range(n):
            like = LikeToAnswer(answer_id=choice(answers), user_id=choice(users),
                                is_liked=faker.random.randint(-1, 1))
            answer = Answer.objects.get(id=like.answer_id)
            answer.rating += like.is_liked
            answer.save()
            likes.append(like)

        batch_size = 10000
        while True:
            batch = list(islice(likes, batch_size))
            del likes[:batch_size]
            if not batch:
                break
            LikeToAnswer.objects.bulk_create(batch, batch_size)
