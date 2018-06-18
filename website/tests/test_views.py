from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from website.models import *
from website.forms import *

class HomeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data"""
        user = User.objects.create_user("johndoe", "johndoe@example.com", "johndoe")
        category = FossCategory.objects.create(name="TestCategory", email="category@example.com")
        FossCategory.objects.create(name="TestCategory2", email="category2@example.com")
        Question.objects.create(user=user, category=category, title="TestQuestion")
        Question.objects.create(user=user, category=category, title="TestQuestion 2", is_spam=True)

    def test_view_url_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/templates/index.html')

    def test_view_context_questions(self):
        response = self.client.get(reverse('website:home'))
        question_id = Question.objects.get(title="TestQuestion").id
        self.assertTrue('questions' in response.context)
        self.assertQuerysetEqual(response.context['questions'],
                                    ['<Question: {0} - TestCategory -  - TestQuestion - johndoe>'.format(question_id)])

    def test_view_context_categories(self):
        response = self.client.get(reverse('website:home'))
        self.assertTrue('categories' in response.context)
        self.assertQuerysetEqual(response.context['categories'],
                                    ['<FossCategory: TestCategory>', '<FossCategory: TestCategory2>'])

class QuestionsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up test data"""
        user = User.objects.create_user("johndoe", "johndoe@example.com", "johndoe")
        category = FossCategory.objects.create(name="TestCategory", email="category@example.com")
        Question.objects.create(user=user, category=category, title="TestQuestion")
        Question.objects.create(user=user, category=category, title="TestQuestion 2", is_spam=True)

    def test_view_url_at_desired_location(self):
        response = self.client.get('/questions/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('website:questions'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('website:questions'))
        self.assertTemplateUsed(response, 'website/templates/questions.html')

    def test_view_context_questions(self):
        response = self.client.get(reverse('website:home'))
        question_id = Question.objects.get(title="TestQuestion").id
        self.assertTrue('questions' in response.context)
        self.assertQuerysetEqual(response.context['questions'],
                                    ['<Question: {0} - TestCategory -  - TestQuestion - johndoe>'.format(question_id)])

class GetQuestionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Create sample data"""
        user = User.objects.create_user("johndoe", "johndoe@example.com", "johndoe")
        category = FossCategory.objects.create(name="TestCategory", email="category@example.com")
        question = Question.objects.create(user=user, category=category, title="TestQuestion",\
                                            sub_category="TestSubCategory", num_votes=1)
        answer = Answer.objects.create(question=question, uid=user.id, body="TestAnswer")
        Answer.objects.create(question=question, uid=user.id, body="TestAnswer 2", is_spam=True)
        AnswerComment.objects.create(answer=answer, uid=user.id, body="TestAnswerComment")

    def test_view_url_at_desired_location(self):
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.get('/question/{0}/'.format(question_id))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.get(reverse('website:get_question', args=(question_id,)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.get(reverse('website:get_question', args=(question_id,)))
        self.assertTemplateUsed(response, 'website/templates/get-question.html')

    def test_view_context_question(self):
        question = Question.objects.get(title="TestQuestion")
        response = self.client.get(reverse('website:get_question', args=(question.id,)))
        self.assertTrue('question' in response.context)
        self.assertEqual(response.context['question'], question)

    def test_view_context_ans_count(self):
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.get(reverse('website:get_question', args=(question_id,)))
        self.assertTrue('ans_count' in response.context)
        self.assertEqual(response.context['ans_count'], 1)

    def test_view_context_sub_category(self):
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.get(reverse('website:get_question', args=(question_id,)))
        self.assertTrue('sub_category' in response.context)
        self.assertEqual(response.context['sub_category'], True)

    def test_view_context_main_list(self):
        question_id = Question.objects.get(title="TestQuestion").id
        answer = Answer.objects.get(body = "TestAnswer")
        response = self.client.get(reverse('website:get_question', args=(question_id,)))
        self.assertTrue('main_list' in response.context)
        self.assertEqual(response.context['main_list'], [(answer, [0,0,0])])

    def test_view_context_form(self):
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.get(reverse('website:get_question', args=(question_id,)))
        self.assertTrue('form' in response.context)
        self.assertIsInstance(response.context['form'], AnswerQuestionForm)

    def test_view_context_thisUserUpvote(self):
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.get(reverse('website:get_question', args=(question_id,)))
        self.assertTrue('thisUserUpvote' in response.context)
        self.assertEqual(response.context['thisUserUpvote'], 0)

    def test_view_context_thisUserDownvote(self):
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.get(reverse('website:get_question', args=(question_id,)))
        self.assertTrue('thisUserDownvote' in response.context)
        self.assertEqual(response.context['thisUserDownvote'], 0)

    def test_view_context_net_count(self):
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.get(reverse('website:get_question', args=(question_id,)))
        self.assertTrue('net_count' in response.context)
        self.assertEqual(response.context['net_count'], 1)

class QuestionAnswerViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Create sample data"""
        user = User.objects.create_user("johndoe", "johndoe@example.com", "johndoe")
        User.objects.create_user("johndoe2", "johndoe2@example.com", password="johndoe2")
        category = FossCategory.objects.create(name="TestCategory", email="category@example.com")
        Question.objects.create(user=user, category=category, title="TestQuestion")

    def test_view_redirect_if_not_logged_in(self):
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.get(reverse('website:question_answer', args=(question_id,)))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_view_url_loads_with_correct_template(self):
        self.client.login(username='johndoe', password='johndoe')
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.get('/question-answer/{0}/'.format(question_id))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('website:question_answer', args=(question_id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/templates/get-question.html')

    def test_view_post_no_answer(self):
        self.client.login(username='johndoe', password='johndoe')
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.post(reverse('website:question_answer', args=(question_id,)),\
                                        {'question': question_id})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Answer field required')

    def test_view_post_too_short_body(self):
        self.client.login(username='johndoe', password='johndoe')
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.post(reverse('website:question_answer', args=(question_id,)),\
                                    {'body': 'TooShort', 'question': question_id})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Body should be minimum 12 characters long')

    def test_view_post_body_only_spaces(self):
        self.client.login(username='johndoe', password='johndoe')
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.post(reverse('website:question_answer', args=(question_id,)),\
                                    {'body': '        &nbsp;          ', 'question': question_id})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Body cannot be only spaces')

    def test_view_post_body_only_tags(self):
        self.client.login(username='johndoe', password='johndoe')
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.post(reverse('website:question_answer', args=(question_id,)),\
                                    {'body': '<p><div></div></p>        ', 'question': question_id})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Body cannot be only tags')

    def test_view_post_notification_created(self):
        self.client.login(username='johndoe2', password='johndoe2')
        question_id = Question.objects.get(title="TestQuestion").id
        self.client.post(reverse('website:question_answer', args=(question_id,)),\
                                    {'body': 'Test question body', 'question': question_id})
        try:
            user_id = User.objects.get(username='johndoe').id
            Notification.objects.get(uid=user_id, qid=question_id)
        except:
            self.fail('Notification object not created.')

    def test_view_post_valid_data(self):
        self.client.login(username='johndoe', password='johndoe')
        question_id = Question.objects.get(title="TestQuestion").id
        response = self.client.post(reverse('website:question_answer', args=(question_id,)),\
                                    {'body': 'Test question body', 'question': question_id})
        self.assertRedirects(response, reverse('website:get_question', args=(question_id,)))
    
class AnswerCommentViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Create sample data"""
        user = User.objects.create_user("johndoe", "johndoe@example.com", "johndoe")
        user2 = User.objects.create_user("johndoe2", "johndoe2@example.com", "johndoe2")
        user3 = User.objects.create_user("johndoe3", "johndoe3@example.com", "johndoe3")
        category = FossCategory.objects.create(name="TestCategory", email="category@example.com")
        question = Question.objects.create(user=user, category=category, title="TestQuestion")
        answer = Answer.objects.create(question=question, uid=user.id, body="TestAnswer")
        AnswerComment.objects.create(answer=answer, uid=user3.id, body="TestAnswerComment")

    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('website:answer_comment'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_view_does_not_load(self):
        self.client.login(username='johndoe', password='johndoe')
        response = self.client.get(reverse('website:answer_comment'), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_view_post_body_only_spaces(self):
        self.client.login(username='johndoe', password='johndoe')
        answer_id = Answer.objects.get(body="TestAnswer").id
        response = self.client.post(reverse('website:answer_comment'),\
                                    {'body': '        &nbsp;          ', 'answer_id': answer_id})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Body cannot be only spaces')

    def test_view_post_body_only_tags(self):
        self.client.login(username='johndoe', password='johndoe')
        answer_id = Answer.objects.get(body="TestAnswer").id
        response = self.client.post(reverse('website:answer_comment'),\
                                    {'body': '<p><div></div></p>     ', 'answer_id': answer_id})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Body cannot be only tags')

    def test_view_post_notification_created_answer_creator(self):
        self.client.login(username='johndoe2', password='johndoe2')
        answer = Answer.objects.get(body="TestAnswer")
        self.client.post(reverse('website:answer_comment'),\
                                    {'body': 'Test Answer comment', 'answer_id': answer.id})
        try:
            user_id = User.objects.get(username='johndoe').id
            Notification.objects.get(uid=user_id, qid=answer.question.id, aid=answer.id)
        except:
            self.fail('Notification not created for answer creator.')

    def test_view_post_notification_created_comment_creators(self):
        self.client.login(username='johndoe2', password='johndoe2')
        answer = Answer.objects.get(body="TestAnswer")
        self.client.post(reverse('website:answer_comment'),\
                                    {'body': 'Test Answer comment', 'answer_id': answer.id})
        try:
            user_id = User.objects.get(username='johndoe3').id
            Notification.objects.get(uid=user_id, qid=answer.question.id, aid=answer.id)
        except:
            self.fail('Notification not created for comment creators.')

    def test_view_post_valid_data(self):
        self.client.login(username='johndoe', password='johndoe')
        answer = Answer.objects.get(body="TestAnswer")
        response = self.client.post(reverse('website:answer_comment'),\
                                    {'body': 'Test Answer comment', 'answer_id': answer.id})
        self.assertRedirects(response, reverse('website:get_question', args=(answer.question.id, )))

class NewQuestionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Create sample data"""
        user = User.objects.create_user("johndoe", "johndoe@example.com", "johndoe")
        category = FossCategory.objects.create(name="TestCategory", email="category@example.com")
        Question.objects.create(user=user, category=category, title="TestQuestion")

    def test_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('website:new_question'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_view_url_loads_with_correct_template(self):
        self.client.login(username='johndoe', password='johndoe')
        response = self.client.get('/new-question/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('website:new_question'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/templates/new-question.html')

    def test_view_post_no_category(self):
        self.client.login(username='johndoe', password='johndoe')
        response = self.client.post(reverse('website:new_question'),\
                                    {'title': 'Test question title', 'body': 'Test question body',\
                                    'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'category', 'Select a category')

    def test_view_post_no_title(self):
        self.client.login(username='johndoe', password='johndoe')
        category = FossCategory.objects.get(name='TestCategory')
        response = self.client.post(reverse('website:new_question'),\
                                    {'category': category.id, 'body': 'Test question body',\
                                    'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'Title field required')

    def test_view_post_no_body(self):
        self.client.login(username='johndoe', password='johndoe')
        category = FossCategory.objects.get(name='TestCategory')
        response = self.client.post(reverse('website:new_question'),\
                                    {'category': category.id, 'title': 'Test question title',\
                                    'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Question field required')

    def test_view_post_title_only_spaces(self):
        self.client.login(username='johndoe', password='johndoe')
        category = FossCategory.objects.get(name='TestCategory')
        response = self.client.post(reverse('website:new_question'),\
                                    {'category': category.id, 'title': '  &nbsp;             ',\
                                    'body': 'Test question body', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'Title cannot be only spaces')

    def test_view_post_title_only_tags(self):
        self.client.login(username='johndoe', password='johndoe')
        category = FossCategory.objects.get(name='TestCategory')
        response = self.client.post(reverse('website:new_question'),\
                                    {'category': category.id, 'title': '<p><div></div></p>',\
                                    'body': 'Test question body', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'Title cannot be only tags')

    def test_view_post_title_too_short(self):
        self.client.login(username='johndoe', password='johndoe')
        category = FossCategory.objects.get(name='TestCategory')
        response = self.client.post(reverse('website:new_question'),\
                                    {'category': category.id, 'title': 'TooShort',\
                                    'body': 'Test question body', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'Title should be longer than 12 characters')

    def test_view_post_title_already_exists(self):
        self.client.login(username='johndoe', password='johndoe')
        category = FossCategory.objects.get(name='TestCategory')
        response = self.client.post(reverse('website:new_question'),\
                                    {'category': category.id, 'title': 'TestQuestion',\
                                    'body': 'Test question body', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'This title already exists')

    def test_view_post_body_only_spaces(self):
        self.client.login(username='johndoe', password='johndoe')
        category = FossCategory.objects.get(name='TestCategory')
        response = self.client.post(reverse('website:new_question'),\
                                    {'category': category.id, 'title': 'Test question title',\
                                    'body': '           &nbsp;     ', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Body cannot be only spaces')

    def test_view_post_body_only_tags(self):
        self.client.login(username='johndoe', password='johndoe')
        category = FossCategory.objects.get(name='TestCategory')
        response = self.client.post(reverse('website:new_question'),\
                                    {'category': category.id, 'body': '<p><div></div></p>',\
                                    'title': 'Test question title', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Body cannot be only tags')

    def test_view_post_body_too_short(self):
        self.client.login(username='johndoe', password='johndoe')
        category = FossCategory.objects.get(name='TestCategory')
        response = self.client.post(reverse('website:new_question'),\
                                    {'category': category.id, 'body': 'TooShort',\
                                    'title': 'Test question title', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Body should be minimum 12 characters long')

    def test_view_post_spam_question(self):
        self.client.login(username='johndoe', password='johndoe')
        category = FossCategory.objects.get(name='TestCategory')
        response = self.client.post(reverse('website:new_question'),\
                                    {'category': category.id, 'body': 'swiss replica watches buy',\
                                    'title': 'Test question title', 'tutorial':  None})
        self.assertRedirects(response, reverse('website:home'))

    def test_view_post_valid_data(self):
        self.client.login(username='johndoe', password='johndoe')
        category = FossCategory.objects.get(name='TestCategory')
        response = self.client.post(reverse('website:new_question'),\
                                    {'category': category.id, 'body': 'Test question body',\
                                    'title': 'Test question title', 'tutorial':  None})
        question_id = Question.objects.get(title='Test question title').id
        self.assertRedirects(response, reverse('website:get_question', args=(question_id, )))

    def test_view_get_context(self):
        self.client.login(username='johndoe', password='johndoe')
        response = self.client.get(reverse('website:new_question'))
        self.assertTrue('category' in response.context)
        self.assertTrue('form' in response.context)
        self.assertIsInstance(response.context['form'], NewQuestionForm)

    def test_view_post_context_when_form_error(self):
        self.client.login(username='johndoe', password='johndoe')
        category = FossCategory.objects.get(name='TestCategory')
        response = self.client.post(reverse('website:new_question'),\
                                    {'category': category.id, 'body': 'TooShort',\
                                    'title': 'Test question title', 'tutorial':  None})
        self.assertTrue('category' in response.context)
        self.assertEqual(int(response.context['category']), category.id)
        self.assertTrue('tutorial' in response.context)
        self.assertEqual(response.context['tutorial'], 'None')
        self.assertTrue('form' in response.context)
        self.assertIsInstance(response.context['form'], NewQuestionForm)

class EditQuestionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Create sample data"""
        user = User.objects.create_user("johndoe", "johndoe@example.com", "johndoe")
        user2 = User.objects.create_user("johndoe2", "johndoe2@example.com", "johndoe2")
        category = FossCategory.objects.create(name="TestCategory", email="category@example.com")
        FossCategory.objects.create(name="TestCategory2", email="category2@example.com")
        Question.objects.create(user=user, category=category, title="TestQuestion")

    def test_view_redirect_if_not_logged_in(self):
        question_id = Question.objects.get(title='TestQuestion').id
        response = self.client.get(reverse('website:edit_question', args=(question_id, )))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_view_url_loads_with_correct_template(self):
        self.client.login(username='johndoe', password='johndoe')
        question_id = Question.objects.get(title='TestQuestion').id
        response = self.client.get('/question/edit/{0}/'.format(question_id))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('website:edit_question', args=(question_id, )))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/templates/edit-question.html')

    def test_view_redirects_when_not_authorized(self):
        self.client.login(username='johndoe2', password='johndoe2')
        question_id = Question.objects.get(title='TestQuestion').id
        response = self.client.get(reverse('website:edit_question', args=(question_id, )))
        self.assertContains(response, "Not authorized to edit question.")

    def test_view_post_no_category(self):
        self.client.login(username='johndoe', password='johndoe')
        question_id = Question.objects.get(title='TestQuestion').id
        response = self.client.post(reverse('website:edit_question', args=(question_id, )),\
                                    {'title': 'Test question title', 'body': 'Test question body',\
                                    'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'category', 'Select a category')

    def test_view_post_no_title(self):
        self.client.login(username='johndoe', password='johndoe')
        question = Question.objects.get(title='TestQuestion')
        response = self.client.post(reverse('website:edit_question', args=(question.id, )),\
                                    {'category': question.category.id, 'body': 'Test question body',\
                                    'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'Title field required')

    def test_view_post_no_body(self):
        self.client.login(username='johndoe', password='johndoe')
        question = Question.objects.get(title='TestQuestion')
        response = self.client.post(reverse('website:edit_question', args=(question.id, )),\
                                    {'category': question.category.id, 'title': 'Test question title',\
                                    'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Question field required')

    def test_view_post_title_only_spaces(self):
        self.client.login(username='johndoe', password='johndoe')
        question = Question.objects.get(title='TestQuestion')
        response = self.client.post(reverse('website:edit_question', args=(question.id, )),\
                                    {'category': question.category.id, 'title': '  &nbsp;             ',\
                                    'body': 'Test question body', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'Title cannot be only spaces')

    def test_view_post_title_only_tags(self):
        self.client.login(username='johndoe', password='johndoe')
        question = Question.objects.get(title='TestQuestion')
        response = self.client.post(reverse('website:edit_question', args=(question.id, )),\
                                    {'category': question.category.id, 'title': '<p><div></div></p>',\
                                    'body': 'Test question body', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'Title cannot be only tags')

    def test_view_post_title_too_short(self):
        self.client.login(username='johndoe', password='johndoe')
        question = Question.objects.get(title='TestQuestion')
        response = self.client.post(reverse('website:edit_question', args=(question.id, )),\
                                    {'category': question.category.id, 'title': 'TooShort',\
                                    'body': 'Test question body', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'Title should be longer than 12 characters')

    def test_view_post_body_only_spaces(self):
        self.client.login(username='johndoe', password='johndoe')
        question = Question.objects.get(title='TestQuestion')
        response = self.client.post(reverse('website:edit_question', args=(question.id, )),\
                                    {'category': question.category.id, 'title': 'Test question title',\
                                    'body': '           &nbsp;     ', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Body cannot be only spaces')

    def test_view_post_body_only_tags(self):
        self.client.login(username='johndoe', password='johndoe')
        question = Question.objects.get(title='TestQuestion')
        response = self.client.post(reverse('website:edit_question', args=(question.id, )),\
                                    {'category': question.category.id, 'body': '<p><div></div></p>',\
                                    'title': 'Test question title', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Body cannot be only tags')

    def test_view_post_body_too_short(self):
        self.client.login(username='johndoe', password='johndoe')
        question = Question.objects.get(title='TestQuestion')
        response = self.client.post(reverse('website:edit_question', args=(question.id, )),\
                                    {'category': question.category.id, 'body': 'TooShort',\
                                    'title': 'Test question title', 'tutorial':  None})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'body', 'Body should be minimum 12 characters long')

    def test_view_post_title_exists_allowed(self):
        self.client.login(username='johndoe', password='johndoe')
        question = Question.objects.get(title='TestQuestion')
        response = self.client.post(reverse('website:edit_question', args=(question.id, )),\
                                    {'category': question.category.id, 'title': 'TestQuestion',\
                                    'body': 'Test question body', 'tutorial':  None})
        self.assertRedirects(response, reverse('website:get_question', args=(question.id, )))

    def test_view_post_mark_spam(self):
        self.client.login(username='johndoe', password='johndoe')
        question = Question.objects.get(title='TestQuestion')
        response = self.client.post(reverse('website:edit_question', args=(question.id, )),\
                                    {'category': question.category.id, 'title': 'TestQuestion',\
                                    'body': 'Test question body', 'tutorial':  None, 'is_spam': True})
        self.assertRedirects(response, reverse('website:home'))

    def test_view_post_mark_spam_moderator_activated(self):
        settings.MODERATOR_ACTIVATED = True
        self.client.login(username='johndoe', password='johndoe')
        question = Question.objects.get(title='TestQuestion')
        response = self.client.post(reverse('website:edit_question', args=(question.id, )),\
                                    {'category': question.category.id, 'title': 'TestQuestion',\
                                    'body': 'Test question body', 'tutorial':  None, 'is_spam': True})
        self.assertRedirects(response, reverse('website:get_question', args=(question.id, )))
        settings.MODERATOR_ACTIVATED = False

    def test_view_get_context(self):
        self.client.login(username='johndoe', password='johndoe')
        question_id = Question.objects.get(title='TestQuestion').id
        response = self.client.get(reverse('website:edit_question', args=(question_id, )))
        self.assertTrue('form' in response.context)
        self.assertIsInstance(response.context['form'], NewQuestionForm)

    def test_view_post_context_when_form_error(self):
        self.client.login(username='johndoe', password='johndoe')
        question = Question.objects.get(title='TestQuestion')
        response = self.client.post(reverse('website:edit_question', args=(question.id, )),\
                                    {'category': question.category.id, 'body': 'TooShort',\
                                    'title': 'Test question title', 'tutorial':  None})
        self.assertTrue('category' in response.context)
        self.assertEqual(int(response.context['category']), question.category.id)
        self.assertTrue('tutorial' in response.context)
        self.assertEqual(response.context['tutorial'], 'None')
        self.assertTrue('form' in response.context)
        self.assertIsInstance(response.context['form'], NewQuestionForm)

    def test_view_post_change_data(self):
        settings.MODERATOR_ACTIVATED = True
        self.client.login(username='johndoe', password='johndoe')
        question_id = Question.objects.get(title='TestQuestion').id
        category = FossCategory.objects.get(name='TestCategory2')
        response = self.client.post(reverse('website:edit_question', args=(question_id, )),\
                                    {'category': category.id, 'title': 'Test question title',\
                                    'body': 'Test question body changed', 'tutorial':  'TestTutorial',\
                                    'is_spam': True})
        self.assertRedirects(response, reverse('website:get_question', args=(question_id, )))
        settings.MODERATOR_ACTIVATED = False
        question = Question.objects.get(id = question_id)
        self.assertEqual(question.category, category)
        self.assertEqual(question.title, 'Test question title')
        self.assertEqual(question.body, 'Test question body changed')
        self.assertEqual(question.sub_category, 'TestTutorial')
        self.assertTrue(question.is_spam)

    