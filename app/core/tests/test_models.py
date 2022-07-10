"""
Test for models
"""
from unittest.mock import patch 

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models



def create_user(email='user@example.com', password='testpassword123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)

def create_area():
    """Create and return a new area"""
    user = create_user(email='user2@example.com')
    return models.Area.objects.create(user=user, name='Area1')


class ModelTest(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is not normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.com','test4@example.com'],
         ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample23')
            self.assertEqual(user.email, expected)

    def test_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_personel(self):
        """Test creating a personel data is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        personel = models.Personel.objects.create(
            user=user,
            full_name='Test User',
            birthday = '1980-01-01'
        )

        self.assertEqual(str(personel), personel.full_name)
    
    def test_create_area(self):
        """Test creating a area is successful."""
        user = create_user()
        area = models.Area.objects.create(user=user, name='Area1')

        self.assertEqual(str(area), area.name)
    
    def test_create_subarea(self):
        """Test creating a sub area is successful."""
        user = create_user()
        area = create_area()
        sub_area = models.SubArea.objects.create (
            user=user,
            name='SubArea1',
            description='description sub area',
            area_id = area
        )

        self.assertEqual(str(sub_area), sub_area.name)
    
    def test_create_audit(self):
        """Test creating non conformity form is successful"""
        user = create_user()
        area = models.Area.objects.create(user=user, name='PJT')
        sub_area = models.SubArea.objects.create(user=user, name='PJT', area_id=area)
        standard = models.Standard.objects.create(user=user)
        nc = models.Audit.objects.create(
            user=user,
            title='nc lab semen',
            audit_date='2022-07-05',
            area=area,
            sub_area=sub_area,
            nc_point='6.1',
            nc_source='Audit Internal',
            description='uraian berkepanjangan',
            verification_note='ada yang tidak lengkap',
            is_verified=False,
            verified_date='2022-07-11',
            cat='mayor'
        )
        nc.standard.add(standard)

        self.assertEqual(str(nc), nc.title)
    
    def test_create_correctiveaction(self):
        """Test creating corrective action form is successful."""
        user = create_user()
        personel = models.Personel.objects.create(user=user)
        area = models.Area.objects.create(user=user, name='PJT')
        sub_area = models.SubArea.objects.create(user=user, name='PJT', area_id=area)
        audit = models.Audit.objects.create(user=user, area=area, sub_area=sub_area, cat='MJ')
        corrective_action = models.Correctiveaction.objects.create(
            user=user,
            cause_analysis='penyebab terbesar adalah dari akarnya sendiri',
            corrective_actions='tindakan perbaikan sudah dilakukan',
            due_date='2022-07-10',
            prepared_by=personel,
            pre_actions='tindakan pencegahan',
            links="http://example.com",
            audit=audit,
        )

        self.assertEqual(str(corrective_action), corrective_action.corrective_actions)
    
    def test_create_standard(self):
        """Test creating a standard is successful"""
        user = create_user()
        standard = models.Standard.objects.create(user=user, name='Standard 1')

        self.assertEqual(str(standard), standard.name)
    
    def test_create_standard_point(self):
        """Test creating a standard point is successful"""
        user = create_user()
        standard = models.Standard.objects.create(user=user, name='Standard 1')
        point = models.Standardpoint.objects.create(user=user, standard_id=standard, name='1.1', description=' Standard 1 Point 1.1')

        self.assertEqual(str(point), point.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating document path"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.audit_corrective_file_path(None, 'example.pdf')

        self.assertEqual(file_path, f'uploads/audit/correctives/{uuid}.pdf')

