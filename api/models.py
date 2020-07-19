from django.db import models
from queue import PriorityQueue

# Create your models here.

class Victim(models.Model):
    time_of_death = models.DateTimeField(null=True)
    username = models.CharField(max_length=250)
    age = models.IntegerField()
    difficulty = models.IntegerField()
    priority = models.IntegerField()


class Link(models.Model):
    pre_victim = models.ForeignKey(Victim, related_name='pre_victim', on_delete=models.CASCADE)
    post_victim = models.ForeignKey(Victim, related_name='post_victim', on_delete=models.CASCADE)


class KillerManager(models.Model):

    start_of_work_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(KillerManager, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def process_order(self, target_list):

        victims = Victim.objects.all()
        links = Link.objects.all()
        for x in victims: x.delete()
        for x in links: x.delete()

        per_target_hours = {}
        target_list = sorted(target_list, key=lambda x: int(x['priority']), reverse=True)
        target_orm = []
        for target in target_list:
            new_victim = Victim.objects.create(username = target['username'], age = target['age'],
                          difficulty = target['difficulty'], priority = target['priority'])
            target_orm.append(new_victim)

        for target in target_list:
            pre_victim = Victim.objects.filter(username=target['username']).first()
            post_victim = Victim.objects.filter(username=target['link']).first()
            per_target_hours[target['username']] = int(target['difficulty'])
            if (post_victim == None):
                continue
            if target['link'] not in per_target_hours:
                per_target_hours[target['link']] = int(post_victim.difficulty)
            per_target_hours[target['link']] *= 2 if pre_victim.age >= 40 else 1.5
            Link.objects.create(pre_victim=pre_victim,post_victim=post_victim)

        targets_q = PriorityQueue()
        for target in target_orm:
            link = Link.objects.filter(post_victim = target).first()
            if (link == None):
                targets_q.put([int(target.priority), target])

        order = []

        while (not targets_q.empty()):
            top_target = targets_q.get()
            order.append(top_target[1].username)
            top_target_links = Link.objects.filter(pre_victim=top_target[1])
            for link in top_target_links:
                post_victim = link.post_victim
                link.delete()
                try:
                    Link.objects.get(post_victim=post_victim)
                except models.ObjectDoesNotExist:
                    targets_q.put([int(link.post_victim.priority), link.post_victim])
        total_hours = 0
        for x in order:
            print (x, per_target_hours[x])
        # 2 + (1.5 * 1) + 1 + (2 * 10) + (2 * 3)