# Excel 계산

사용자가 엑셀 파일을 업로드하면 데이터에 대한 통계 화면을 보여준다.

![main_page](https://user-images.githubusercontent.com/51525202/85220276-1d60fe80-b3e5-11ea-98a1-9c9c78e2704b.PNG)

<br/>

## 학습 내용  

- django admin page
- 회원 가입 구현 및 세션을 사용한 로그인 기능
- file upload
- pandas를 이용한 엑셀 파일 핸들링

<br/>

## admin page

django에서는 DB를 웹 페이지 상에서 쉽게 관리하도록 관리자 페이지를 기본적으로 제공한다.


먼저 admin 페이지에 접속할 계정을 터미널에서 생성한다.

``` sh
python manage.py createsuperuser
```

그리고, admin.py에서 생성한 모델들을 등록해야 한다.


``` python
from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
```

![admin_page](https://user-images.githubusercontent.com/51525202/85220377-eccd9480-b3e5-11ea-8069-f52640f21dae.png)


<br/>


## 회원 가입

회원 가입시 인증 코드를 전송하고 validation check 완료 후에 회원 가입을 마무리한다.  

![verify_code](https://user-images.githubusercontent.com/51525202/85220429-52218580-b3e6-11ea-90c1-7ea09b3236f9.png)

<br/>

## 세션을 사용한 로그인 기능

세션을 사용하기 위해서는 settings.py에 다음을 설정한다.

``` python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions', # set this
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'sendEmail',
    'calculate'
]
```

``` python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware' # set this
]
```

로그인 기능

``` python
def login(request):
    loginEmail = request.POST['loginEmail']
    loginPW = request.POST['loginPW']
    try:
        user = User.objects.get(user_email = loginEmail)
    except:
        return redirect('main_loginFail')
    # 사용자가 입력한 password 암호화
    encoded_loginPW = loginPW.encode()
    encrypted_loginPW = hashlib.sha256(encoded_loginPW).hexdigest()
    if user.user_password == encrypted_loginPW:
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return redirect('main_index')
    else:
        return redirect('main_loginFail')
```

이제 다른 request에서 session check를 하여 필요한 페이지를 노출한다.

<br/>

## file upload

파일을 업로드하기 위해서는 먼저 저장될 경로를 settings.py에 설정해야 한다.

``` python
# Media Files

# user file upload 시 저장될 공간
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# media resource 접근에 대한 prefix 설정
MEDIA_URL = '/media/'
```

file을 데이터베이스에 저장하기 위해서는 FileField를 통한 모델 생성이 필요하다.

``` python
# models.py
from django.db import models

# Create your models here.
class Document(models.Model):
    user_upload_file = models.FileField(upload_to='user_upload_files/%Y%m%d/')
```

<br/>

## pandas

엑셀 파일을 업로드하면 이를 읽어서 적절한 작업을 한다.

``` python
df = pd.read_excel(file, sheet_name='Sheet1', header=0)
```

pandas 대한 자세한 내용은 생략하며, 필요시 아래 사이트를 참조한다.

[pandas](https://pandas.pydata.org/)