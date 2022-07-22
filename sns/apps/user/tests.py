import json

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import BlacklistedToken, OutstandingToken

from apps.user.models import User

# Create your tests here.


class UserSignUpTest(APITestCase):
    """회원가입 테스트

    Writer: 조병민
    Date: 2022-07-21

    """

    def setUp(self):
        self.data = {
            'email': 'testAdmin@gamil.com',
            'nickname': 'testAdmin',
            'introduce': 'test',
            'password': 'abcdABC123!',
        }
        self.user = User.objects.create_user(**self.data)

    def test_success_user_signup(self):
        """정상적인 회원가입

        [성공] status_code = 200
        [응답] {'detail': 'success, user sign-up'}
        """
        data = {'email': 'testuser@gmail.com', 'nickname': 'testuser', 'introduce': 'hello', 'password': 'abcdABC123!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.json(), {'detail': 'success, user sign-up'})

    def test_failure_user_signup_password(self):
        """잘못된 형식의 비밀번호를 입력받았을 때

        [실패] status_code = 400
        [응답] {'detail': 'inaccurate password'}
        """
        data = {'email': 'testuser@gmail.com', 'nickname': 'testuser', 'introduce': 'hello', 'password': 'abcdABC1'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'detail': 'inaccurate password'})

    def test_failure_user_signup_email(self):
        """이미 가입되어있는 이메일을 입력 받았을때

        [실패] status_code = 400
        [응답] {'detail': 'existed email'}
        """
        data = {
            'email': 'testAdmin@gamil.com',
            'nickname': 'testuser',
            'introduce': 'hello',
            'password': 'abcdABC123!',
        }

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['user의 email은/는 이미 존재합니다.']})

    def test_failure_user_signup_nickname(self):
        """nickname을 입력받지 않았을때

        [실패] status_code = 400
        [응답] {'detail': 'existed email'}
        """
        data = {'email': 'testuser@gmail.com', 'nickname': '', 'introduce': 'hello', 'password': 'abcdABC123!'}

        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'nickname': ['이 필드는 blank일 수 없습니다.']})


class UserSignInTest(APITestCase):
    """로그인 - JWT 발급 테스트

    Writer: 조병민
    Date: 2022-07-21

    """

    def setUp(self):
        self.data = {
            'email': 'testAdmin@gamil.com',
            'nickname': 'testAdmin',
            'introduce': 'test',
            'password': 'abcdABC123!',
        }
        self.user = User.objects.create_user(**self.data)

    def test_success_signing(self):
        """로그인 성공

        [성공] status_code = 200
        """
        data = {'email': 'testAdmin@gamil.com', 'password': 'abcdABC123!'}

        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        user = User.objects.get(email='testAdmin@gamil.com')
        token = OutstandingToken.objects.filter(user=user).all()[1]

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(token.token, response.data['refresh'])

    def test_failure_signin_password(self):
        """로그인 실패 - 비빌먼호 오입력

        [실패] status_code = 400
        """
        data = {'email': 'testAdmin@gamil.com', 'password': 'A123a12aaa3!123'}

        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_sucess_signout_refreshtoken(self):
        """로그아웃 성공

        [성공] status_code = 200
        """
        data = {'email': 'testAdmin@gamil.com', 'password': 'abcdABC123!'}

        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        '''header 추가 시 주의 사항

        1. HTTP_ 접두사를 꼭 붙여야 한다.
        2. header 명은 대문자로 작성해야한다.
        '''
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        response = self.client.post(
            '/users/signout',
            data=json.dumps({'refresh': f'{refresh_token}'}),
            content_type='application/json',
            **headers,
        )

        user = User.objects.get(email='testAdmin@gamil.com')
        black_token = BlacklistedToken.objects.filter(token__user=user).order_by('-blacklisted_at').first().token.token

        self.assertEqual(response.status_code, 200)
        self.assertEqual(refresh_token, black_token)

    def test_failure_signout_header_accesshtoken(self):
        """로그아웃 실패 - 잘못된 토큰

        [실패] status_code = 401
        """
        data = {'email': 'testAdmin@gamil.com', 'password': 'abcdABC123!'}

        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        '''header 추가 시 주의 사항

        1. HTTP_ 접두사를 꼭 붙여야 한다.
        2. header 명은 대문자로 작성해야한다.
        '''
        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}false"}
        response = self.client.post(
            '/users/signout',
            data=json.dumps({'refresh': f'{refresh_token}'}),
            content_type='application/json',
            **headers,
        )

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['messages'][0]['token_class'], 'AccessToken')
        self.assertEqual(response.data['code'], 'token_not_valid')


class UserUpdateTest(APITestCase):
    """유저 수정 테스트

    Writer: 조병민
    Date: 2022-07-21

    """

    def setUp(self):
        self.data = {
            'email': 'testAdmin@gamil.com',
            'nickname': 'testAdmin',
            'introduce': 'test info',
            'password': 'abcdABC123!',
        }
        self.user = User.objects.create_user(**self.data)

    def test_success_user_update_nickname_introduce(self):
        """유저 업데이트 성공

        [성공] status_code = 202
        """
        data = {'email': 'testAdmin@gamil.com', 'password': 'abcdABC123!'}

        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        '''header 추가 시 주의 사항

        1. HTTP_ 접두사를 꼭 붙여야 한다.
        2. header 명은 대문자로 작성해야한다.
        '''

        data = {'nickname': 'testtest', 'introduce': 'modified intro', 'password': 'abcdABC123!'}

        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        response = self.client.patch(
            '/users/update',
            data=json.dumps(data),
            content_type='application/json',
            **headers,
        )

        user = User.objects.filter(email='testAdmin@gamil.com').first()
        self.assertEqual(response.status_code, HTTP_202_ACCEPTED)
        self.assertEqual(user.nickname, 'testtest')
        self.assertEqual(user.introduce, 'modified intro')

    def test_failure_user_update_nickname(self):
        """유저 업데이트 실패 - introduce null

        [실패] status_code = 400
        """
        data = {'email': 'testAdmin@gamil.com', 'password': 'abcdABC123!'}

        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        data = {'nickname': 'testtest', 'introduce': None, 'password': 'abcdABC123!'}

        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        response = self.client.patch(
            '/users/update',
            data=json.dumps(data),
            content_type='application/json',
            **headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_failure_user_update_introduce(self):
        """유저 업데이트 실패 - nickname null

        [실패] status_code = 400
        """
        data = {'email': 'testAdmin@gamil.com', 'password': 'abcdABC123!'}

        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        data = {'nickname': '', 'introduce': 'modified intro', 'password': 'abcdABC123!'}

        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
        response = self.client.patch(
            '/users/update',
            data=json.dumps(data),
            content_type='application/json',
            **headers,
        )

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_failure_user_update_token(self):
        """유저 업데이트 실패 - 잘못된 토큰

        [성공] status_code = 401
        """
        data = {'email': 'testAdmin@gamil.com', 'password': 'abcdABC123!'}

        response = self.client.post('/users/signin', data=json.dumps(data), content_type='application/json')
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        data = {'nickname': 'testtest', 'introduce': 'modified intro', 'password': 'abcdABC123!'}

        headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token} failure"}
        response = self.client.patch(
            '/users/update',
            data=json.dumps(data),
            content_type='application/json',
            **headers,
        )

        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
