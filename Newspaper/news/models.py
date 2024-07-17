from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.validators import MinValueValidator

# Create your models here.

class Author(models.Model):
	authorUser = models.OneToOneField(User, on_delete=models.DO_NOTHING)
	ratingAuthor = models.SmallIntegerField(default=0)

	def update_rating(self):
		postRat = self.post_set.aggregate(postRating=Sum('rating'))
		pRat = 0
		pRat += postRat.get('postRating')
		# pRat += Post.rating

		commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
		cRat = 0
		cRat += commentRat.get('commentRating')

		self.ratingAuthor = pRat * 3 + cRat
		self.save()

class Category(models.Model):
	name = models.CharField(max_length=64, unique=True)

class Post(models.Model):
	NEWS = 'NW'
	ARTICLE = 'AR'
	CATEGORY_CHOICE = [
		(NEWS, "Новость"),
		(ARTICLE, "Статья"),
	]
	title = models.CharField(max_length=128)
	text = models.TextField()
	dateCreation = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICE, default=NEWS)
	postCategory = models.ManyToManyField(Category, through='PostCategory')
	rating = models.SmallIntegerField(default=0)

	def like(self):
		self.rating += 1
		self.save()

	def dislike(self):
		self.rating -= 1
		self.save()

	# def true_rating(self):
	# 	if self.rating < -10:
	# 		return self.rating == -10
	# 	elif self.rating > 10:
	# 		return self.rating == 10

	def preview(self):
		return self.text[0:123] + "..."

class Comment(models.Model):
	text = models.TextField()
	dateCreation = models.DateTimeField(auto_now_add=True)
	commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
	commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.SmallIntegerField(default=0)

	def like(self):
		self.rating += 1
		self.save()

	def dislike(self):
		self.rating -= 1
		self.save()

	# def true_rating(self):
	# 	if self.rating < -10:
	# 		return self.rating == -10
	# 	elif self.rating > 10:
	# 		return self.rating == 10

class PostCategory(models.Model):
	postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
	categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

