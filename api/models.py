import datetime
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.db import models
from queue import PriorityQueue


class Contract(models.Model):
    payed = models.BooleanField(default=False)
    amount = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment_time = models.DateTimeField(null=True)

    def append_victim(self, victim):
        ContractToVictim.objects.create(contract=self, victim=victim)

    def get_victim_list(self):
        contract_to_victims = ContractToVictim.objects.filter(contract=self)
        victim_list = []
        for x in contract_to_victims:
            victim_list.append(x.victim)
        return victim_list

    def pay(self, amount):
        res = {}
        res['result'] = 'failed'
        res['comment'] = ''
        if (self.payed):
            res['comment'] = 'already payed'
        elif (self.amount == None):
            res['comment'] = 'no amount yet'
            return res
        elif (amount == self.amount):
            res['result'] = 'success'
            self.payed = True
            self.payment_time = datetime.datetime.now()
            self.save()
        elif (amount < self.amount):
            res['comment'] = 'not enough credit'
        elif (amount > self.amount):
            res['comment'] = 'too much credit'
        return res


class Victim(models.Model):
    time_of_death = models.DateTimeField(null=True)
    username = models.CharField(max_length=250, unique=True)
    age = models.IntegerField()
    difficulty = models.IntegerField()
    priority = models.IntegerField()

    def __str__(self):
        return self.username

class ContractToVictim(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    victim = models.ForeignKey(Victim, on_delete=models.CASCADE)

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

    def process_order(self, target_list, user):

        contract = Contract.objects.create(user=user)
        per_target_hours = {}
        target_list = sorted(target_list, key=lambda x: int(x['priority']), reverse=True)
        target_orm = []
        for target in target_list:
            try:
                user = User.objects.get(username=target['username'])
                res = {'result': 'failed', 'reason': 'cant process own client'}
                return res
            except models.ObjectDoesNotExist:
                if (Victim.objects.filter(username=target['username']).first() != None):
                            return {'result': 'failed', 'reason': 'recheck the targets, it contains targets which where murdered or duplicates'}
                new_victim = Victim.objects.create(username = target['username'], age = int(target['age']),
                              difficulty = int(target['difficulty']), priority = int(target['priority']))
                target_orm.append(new_victim)
                contract.append_victim(new_victim)
        was_multiplied = {}
        for target in target_list:
            pre_victim = Victim.objects.filter(username=target['username']).first()
            post_victim = Victim.objects.filter(username=target['link']).first()
            if (target['username'] not in per_target_hours):
                per_target_hours[target['username']] = int(target['difficulty'])
            if (post_victim == None):
                continue
            if target['link'] not in per_target_hours:
                per_target_hours[target['link']] = int(post_victim.difficulty)
            if (target['link'] not in was_multiplied):
                per_target_hours[target['link']] *= 2 if post_victim.age >= 40 else 1.5
                was_multiplied[target['link']] = True
            Link.objects.create(pre_victim=pre_victim,post_victim=post_victim)

        # here I'm just using PriorityQueue to every time get target with most priority

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
        start_date = self.start_of_work_time
        total_hours = 0
        for x in order:
            total_hours += per_target_hours[x]
            current_time = self.start_of_work_time
            current_time += datetime.timedelta(hours=per_target_hours[x])
            killed_target = Victim.objects.get(username=x)
            killed_target.time_of_death = current_time
            killed_target.save()
            self.start_of_work_time = current_time
            self.save()
        end_date = self.start_of_work_time
        order_response = {
            'start_date': start_date,
            'end_date': end_date,
            'order': order,
            'hours': total_hours
        }
        amount = len(target_orm) * 10 * total_hours
        contract.amount = amount
        contract.save()
        print (total_hours)
        return order_response
