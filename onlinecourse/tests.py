from django.test import TestCase
from django.urls import reverse
from .models import Question

class ExamResultTests(TestCase):
    def setUp(self):
        # Create test questions
        self.question1 = Question.objects.create(text="Question 1", correct_answer="A")
        self.question2 = Question.objects.create(text="Question 2", correct_answer="B")
        self.question3 = Question.objects.create(text="Question 3", correct_answer="C")

    def test_exam_pass(self):
        # Simulate user submitting correct answers
        response = self.client.post(reverse('onlinecourse:exam_result'), {
            'answers': ['A', 'B', 'C']
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Congratulations! You passed the exam.")
        self.assertEqual(response.context['score'], 3)
        self.assertTrue(response.context['passed'])

    def test_exam_fail(self):
        # Simulate user submitting incorrect answers
        response = self.client.post(reverse('onlinecourse:exam_result'), {
            'answers': ['A', 'C', 'B']
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, you failed the exam.")
        self.assertEqual(response.context['score'], 1)
        self.assertFalse(response.context['passed'])

    def test_exam_edge_case_all_wrong(self):
        # Simulate user submitting all wrong answers
        response = self.client.post(reverse('onlinecourse:exam_result'), {
            'answers': ['D', 'D', 'D']
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, you failed the exam.")
        self.assertEqual(response.context['score'], 0)
        self.assertFalse(response.context['passed'])

    def test_exam_edge_case_all_correct(self):
        # Simulate user submitting all correct answers
        response = self.client.post(reverse('onlinecourse:exam_result'), {
            'answers': ['A', 'B', 'C']
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Congratulations! You passed the exam.")
        self.assertEqual(response.context['score'], 3)
        self.assertTrue(response.context['passed'])
