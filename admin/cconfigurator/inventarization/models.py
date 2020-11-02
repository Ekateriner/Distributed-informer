from django.db import models


class Node(models.Model):
    name = models.CharField(max_length=100)
    role = models.IntegerField()
    stage = models.IntegerField()
    monitored = models.BooleanField()
    essential = models.BooleanField()
    hwinfo = models.TextField()
    health_status = models.IntegerField()
    description = models.CharField(max_length=100)

    @staticmethod
    def model_name():
        return "node"


class NodeLatency(models.Model):
    net = models.IntegerField()
    source_id = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='source')
    target_id = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='target')
    last = models.FloatField()
    loss = models.FloatField()
    mean = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Service(models.Model):
    node_id = models.ForeignKey(Node, on_delete=models.CASCADE)
    type = models.IntegerField()
    params = models.TextField()
    last_state = models.TextField()
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    status = models.IntegerField()
    last_seen = models.DateTimeField()
    last_reported = models.DateTimeField()


class NodeIp(models.Model):
    node_id = models.ForeignKey(Node, on_delete=models.CASCADE)
    addrType = models.IntegerField()
    addr = models.CharField(max_length=100)


class Site(models.Model):
    node_id = models.ForeignKey(Node, on_delete=models.CASCADE)
    qsite_id = models.IntegerField()
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    stage = models.IntegerField()

    @staticmethod
    def model_name():
        return "site"


class Border(models.Model):
    name = models.CharField(max_length=100)
    interfaces = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)
    stage = models.IntegerField()


class UplinkStat(models.Model):
    border_id = models.ForeignKey(Border, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    data = models.TextField()


class SiteLatency(models.Model):
    net = models.IntegerField()
    source_id = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='source')
    target_id = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='target')
    last = models.FloatField()
    loss = models.FloatField()
    mean = models.FloatField()
    median = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()