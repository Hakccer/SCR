from django.db import models
import json
import os
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


def set_image(self, filename):
    return os.path.join("scrolliffy", f"{self.get_posts()}")


class Post(models.Model):
    image = models.ImageField(upload_to=set_image, blank=False)
    description = models.TextField(default="Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium quibusdam corrupti maiores quisquam saepe! Impedit praesentium quaerat corporis officia iusto porro veritatis fugit placeat, in animi suscipit fugiat dolores sunt!Doloremque quod ea nobis, vitae aspernatur quasi tempora cum autem maiores adipisci temporibus mollitia. Libero, ex suscipit dignissimos consequuntur amet beatae, optio nesciunt enim iusto eius inventore. Iure, beatae veritatis.Nihil officiis maxime esse ex eveniet exercitationem. Placeat, accusamus alias quia optio corporis nostrum saepe temporibus odit autem, cumque quisquam facere vero eum nesciunt repellendus modi. Sint at maxime unde?Qui architecto necessitatibus placeat dicta provident aspernatur dolorum minima beatae repellat cumque quia doloremque veritatis ex iste eligendi numquam excepturi ducimus, velit iure possimus ut sequi dolores. Pariatur, beatae iure.Odit a aut harum, placeat doloribus cum? Ad consectetur porro, qui error voluptatem magnam fugit vero repellat aperiam facere ea laboriosam odio obcaecati impedit neque debitis exercitationem cumque reiciendis. Quo.Doloribus numquam incidunt id odio atque aliquid ipsa explicabo repellendus eius quod quibusdam magnam nisi fugit impedit iste est velit, facilis eaque sapiente odit officia, quas quis. Laborum, accusamus adipisci.Magnam labore alias ipsa aliquid ea mollitia, ad rerum voluptate nostrum eos excepturi numquam consequuntur distinctio laboriosam doloremque facere natus corrupti adipisci nulla quidem aut quos! Suscipit esse qui porro.Nihil minima saepe vitae provident natus molestiae odio tenetur obcaecati similique dolorum non harum, mollitia explicabo repellendus vero suscipit praesentium ex. Ullam vero esse ab dicta illo, iste a mollitia.Ea reprehenderit illum consequatur vero quae odio mollitia quo odit ipsa numquam, saepe inventore repellat itaque id minima quis cupiditate eveniet obcaecati a. Dolorum quod quasi laudantium asperiores quaerat quos.Similique quasi necessitatibus iure eveniet officiis quam, harum voluptates laboriosam quidem incidunt, veniam quibusdam minima id. Vitae quos voluptatibus, esse reprehenderit quas itaque neque doloremque sequi nisi explicabo, harum voluptates.")
    likes = models.TextField(default=json.dumps([]))

    def get_posts(self):
        return len(Post.objects.all())


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    user = models.CharField(max_length=200, blank=False)
    time = models.TextField(default=str(datetime.now().strftime("%d/%m/%Y")))
