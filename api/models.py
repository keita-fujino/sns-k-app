from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# avatarのupload先
def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id) + str(instance.nickName) + str(".") + str(ext)])

# postのupload先
def upload_post_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['posts', str(instance.postedUser.id) + str(instance.title) + str(".") + str(ext)])
    
# UserManagerの作成（BaseUserManagerを承継）
class UserManager(BaseUserManager):
  # Userの登録
  def create_user(self, email, password=None):
    #emailの入力がなかったときの設定
    if not email:
      raise ValueError('Emailアドレスを入力してください')

    user = self.model(email=self.normalize_email(email))
    user.set_password(password)
    user.save(using=self._db)

    return user

  # superuserの設定→emailの登録を設定
  def create_superuser(self, email, password):
    
    # 設定したcreate_userでuser登録するように設定（引数はemailとpassword）
    user = self.create_user(email, password)
    user.is_staff = True
    user.is_superuser = True #superuserであることを示す
    user.save(using= self._db)

    return user

#Userモデルの作成（AbstractBaseUserとPermissionsMixinを承継）
class User(AbstractBaseUser, PermissionsMixin):

  email = models.EmailField(
    max_length=250,
    unique=True
  )
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'

  def __str__(self):
    return self.email

# profileの設定
class Profile(models.Model):
  userName = models.CharField(max_length=50)
  userProfile = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    related_name='userProfile',
    on_delete=models.CASCADE
  )
  created_at = models.DateTimeField(auto_now_add=True)
  img = models.ImageField(
    blank=True,
    null=True,
    upload_to = upload_avatar_path
  )

  def __str__(self):
      return self.userName

class Post(models.Model):
    title = models.CharField(max_length=100)
    #postを投稿したUserの結びつけ
    postedUser = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      related_name='postedUser',
      on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(
      blank=True,
      null=True,
      upload_to=upload_post_path
    )
    liked = models.ManyToManyField(
      settings.AUTH_USER_MODEL,
      related_name='いいね',
      blank=True
    )

    def __str__(self):
        return self.title

# Commentモデル
class Comment(models.Model):
  text = models.CharField(max_length=100)
  #commentをしたUserの結びつけ
  commentedUser = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='commentedUser',
    on_delete=models.CASCADE
  )
  post = models.ForeignKey(
    Post,
    on_delete=models.CASCADE
  )

  def __str__(self):
    return self.text