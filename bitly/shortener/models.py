from django.db import models

from .utils import (
    create_random_code,
)


class Shortener(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    times_followed = models.PositiveIntegerField(default=0)
    url = models.URLField()
    code = models.CharField(max_length=15, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.create_new_code()

        super().save(*args, **kwargs)

    def update_counter(self):
        self.times_followed += 1
        self.save()

    @classmethod
    def create_new_code(cls):
        while True:
            random_code = create_random_code()
            if not cls.objects.filter(code=random_code).exists():
                return random_code
