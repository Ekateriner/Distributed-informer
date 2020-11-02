from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db.models import signals
from django.dispatch import receiver

from .serializer import (UplinkStat, UplinkStatSerializer, Node, NodeSerializer,
                         NodeIp, NodeIpSerializer, Border, BorderSerializer,
                         Site, SiteSerializer, SiteLatency, SiteLatencySerializer,
                         NodeLatency, NodeLatencySerializer, Service, ServiceSerializer)
from . import dumpdata


class InventarizationView(APIView):

    def get(self, request):
        response = self.cls.objects.all()

        for cur_field, cur_filter in zip(self.fields, self.filters):

            param = request.query_params.get(cur_field)

            if param is not None:
                query_to_field_mapping = {cur_filter: param}
                response.filter(**query_to_field_mapping)

        serializer = self.serializer(response, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NodeIpView(InventarizationView):
    cls = NodeIp
    serializer = NodeIpSerializer

    fields = (
        'node_id',
        'addrtype',
        'addr',
    )

    filters = (
        'node_id',
        'addrtype',
        'addr',
    )


class BorderView(InventarizationView):
    cls = Border
    serializer = BorderSerializer

    fields = (
        'name',
        'interfaces',
        'created_at',
        'updated_at',
        'site_id',
        'stage',
    )

    filters = (
        'name',
        'interfaces',
        'created_at',
        'updated_at',
        'site_id',
        'stage',
    )


class SiteLatencyView(InventarizationView):
    cls = SiteLatency
    serializer = SiteLatencySerializer

    fields = (
        'net',
        'source_id',
        'target_id',
        'last',
        'mean',
        'median',
        'loss',
        'created_at'
        'updated_at',
    )

    filters = ()


class SiteView(InventarizationView):
    cls = Site
    serializer = SiteSerializer

    fields = (
        'qsite_id',
        'name',
        'location',
        'stage',
    )

    filters = ()


class NodeView(InventarizationView):
    cls = Node
    serializer = NodeSerializer

    fields = (
        'name',
        'role',
        'stage',
        'monitored',
        'site_id',
        'essential',
        'hwinfo',
        'health_status',
        'description',
    )

    filters = ()


class NodeLatencyView(InventarizationView):
    cls = NodeLatency
    serializer = NodeLatencySerializer

    fields = (
        'net',
        'source_id',
        'target_id',
        'last',
        'mean',
        'loss',
        'created_at',
        'updated_at',
    )

    filters = ()


class ServiceView(InventarizationView):
    cls = Service
    serializer = ServiceSerializer

    fields = (
        'node_id',
        'type',
        'params',
        'last_state',
        'description',
        'created_at',
        'updated_at',
        'status',
        'last_seen',
        'last_reported',
    )

    filters = ()


class UplinkStatView(InventarizationView):
    cls = UplinkStat
    serializer = UplinkStatSerializer

    fields = (
        'border_id',
        'year',
        'month',
        'data',
    )

    filters = ()


class TagDict(APIView):
    def get(self, request):
        tags = {'node_id': sorted(['stage', 'name', 'role'])}
        submodels = ['node_id']
        submodels_prefix = ['node_']
        sites = Site.objects.all()
        serializer = SiteSerializer(sites, many=True)
        tag_dict = {}
        for data in serializer.data:
            tag_values = {'site_' + k: v for k, v in dict(data).items() if k not in ['id'] + submodels}
            tag_key = ''
            for submodel, prefix in zip(submodels, submodels_prefix):
                tag_values.update(
                    {prefix + k: v for k, v in dict(data[submodel]).items() if k not in ['id'] + tags[submodel]})
                tag_key += ','.join(prefix + tag + '=' + str(data[submodel][tag]) for tag in tags[submodel]) + ','
            tag_dict[tag_key[:-1]] = tag_values

        return Response(tag_dict)


@receiver(signals.post_save)
def dumpdata_post_save(sender, instance, **kwargs):
    dumpdata.dumpdata_post_save(sender, instance, **kwargs)


@receiver(signals.post_delete)
def dumpdata_post_delete(sender, instance, **kwargs):
    dumpdata.dumpdata_post_delete(sender, instance, **kwargs)
