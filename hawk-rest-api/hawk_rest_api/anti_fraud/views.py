from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from msa.views import LoggedAPIView

from .models import CdmaThjwqSummary201606, Blacklist
from .func import *
from .serializers import *

CLOSE_RELATIONSHIP_TOP_NUM = 5
FRAUD_SCORE_TOP_NUM = 50
#FRAUD_DETECTION_TOP_NUM = 50


class MsisdnBlacklist(LoggedAPIView):
    permission_classes = (AllowAny,)
    # serializer_class = OpTimeSerializer

    def get(self, request, format=None):
        # Get request data
        #serializer = self.serializer_class(data=request.GET)
        serializer = OpTimeSerializer(data=request.GET)
        if not serializer.is_valid(raise_exception=False):
            return Response({'error': 'Wrong input format.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        op_time = data['op_time']

        # Get blacklist
        blacklist = list(Blacklist.objects.filter(
            op_time=op_time).values_list('acc_nbr', flat=True))

        if len(blacklist) == 0:
            return Response({'error': 'Record does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            result = {'op_time': op_time,
                      'blacklist': blacklist}

        return Response(result)

    def post(self, request, format=None):
        # Get request data
        serializer = BlacklistSerializer(data=request.GET)
        if not serializer.is_valid(raise_exception=False):
            return Response({'error': 'Wrong input format.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        op_time = data['op_time']
        acc_nbr = data['acc_nbr']

        # Check whether the acc_nbr exists or not
        is_exist = Blacklist.objects.filter(
            op_time=op_time, acc_nbr=acc_nbr).exists()
        if is_exist:
            return Response(
                {'error': 'The acc_nbr already exists in blacklist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user = Blacklist(op_time=op_time, acc_nbr=acc_nbr)
            user.save()

        return Response(data, status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        # Get request data
        serializer = BlacklistSerializer(data=request.GET)
        if not serializer.is_valid(raise_exception=False):
            return Response({'error': 'Wrong input format.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        op_time = data['op_time']
        acc_nbr = data['acc_nbr']

        # Check whether the acc_nbr exists or not
        is_exist = Blacklist.objects.filter(
            op_time=op_time, acc_nbr=acc_nbr).exists()
        if not is_exist:
            return Response(
                {'error': 'The acc_nbr does not exist in blacklist.'},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            blacklist = Blacklist.objects.get(op_time=op_time, acc_nbr=acc_nbr)
            blacklist.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MsisdnBlacklistStatus(LoggedAPIView):
    permission_classes = (AllowAny,)
    # serializer_class = MsisdnBlacklistStatusSerializer
    serializer_class = BlacklistSerializer

    def get(self, request, format=None):
        # Get request data
        serializer = self.serializer_class(data=request.GET)
        if not serializer.is_valid(raise_exception=False):
            return Response({'error': 'Wrong input format.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        op_time = data['op_time']
        acc_nbr = data['acc_nbr']

        # Get blacklist status
        blacklist = list(Blacklist.objects.filter(
            op_time=op_time).values_list('acc_nbr', flat=True))

        records = CdmaThjwqSummary201606.objects.filter(
            op_time=op_time, acc_nbr=acc_nbr).values()

        if len(records) == 0:
            return Response({'error': 'Record does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            result = {'op_time': op_time,
                      'acc_nbr': acc_nbr,
                      'blacklist_status': acc_nbr in blacklist}

        return Response(result)


class MsisdnCloseRelationship(LoggedAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MsisdnCloseRelationshipSerializer

    def get(self, request, format=None):
        # Get request data
        serializer = self.serializer_class(data=request.GET)
        if not serializer.is_valid(raise_exception=False):
            return Response({'error': 'Wrong input format.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        op_time = data['op_time']
        acc_nbr = data['acc_nbr']

        # Get close relationship score
        records = CdmaThjwqSummary201606.objects.filter(
            op_time=op_time, acc_nbr=acc_nbr).values()

        if len(records) == 0:
            return Response({'error': 'Record does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)

        else:
            close_relationship_dict = \
                get_close_relationship_dict(records, CLOSE_RELATIONSHIP_TOP_NUM)

            result = {
                'op_time': op_time,
                'acc_nbr': acc_nbr,
                'close_relationship': close_relationship_dict
            }

        return Response(result)


class MsisdnFraudScore(LoggedAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MsisdnFraudScoreSerializer

    def get(self, request, format=None):
        # Get request data
        serializer = self.serializer_class(data=request.GET)
        if not serializer.is_valid(raise_exception=False):
            return Response({'error': 'Wrong input format.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        op_time = data['op_time']
        acc_nbr = data['acc_nbr']

        # Get fraud score
        records = CdmaThjwqSummary201606.objects.filter(
            op_time=op_time, acc_nbr=acc_nbr).values()

        blacklist = list(Blacklist.objects.filter(
            op_time=op_time).values_list('acc_nbr', flat=True))

        if len(records) == 0:
            return Response({'error': 'Record does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            if acc_nbr in blacklist:
                fraud_score = 1
            else:
                fraud_score, close_relationship_in_blacklist = get_fraud_score(
                    records, blacklist, FRAUD_SCORE_TOP_NUM)

            result = {
                'op_time': op_time,
                'acc_nbr': acc_nbr,
                'fraud_score': fraud_score
            }

        return Response(result)


class MsisdnGangDetection(LoggedAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MsisdnGangDetectionSerializer

    def get(self, request, format=None):
        # Get request data
        serializer = self.serializer_class(data=request.GET)
        if not serializer.is_valid(raise_exception=False):
            return Response({'error': 'Wrong input format.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        op_time = data['op_time']
        acc_nbr_list = data['acc_nbr_list']

        if len(acc_nbr_list) < 2:
            return Response({'error': 'A valid acc_nbr list is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        blacklist = list(
            Blacklist.objects.filter(
                op_time=op_time).values_list('acc_nbr', flat=True)
        )

        # Get gang score
        gang_score = 0
        pair_dict = {}
        gang_size = len(acc_nbr_list)

        for i in range(gang_size):
            person1 = acc_nbr_list[i]
            for j in range((i + 1), gang_size):
                person2 = acc_nbr_list[j]
                records_p1 = CdmaThjwqSummary201606.objects.filter(
                    op_time=op_time, acc_nbr=person1).values()
                records_p2 = CdmaThjwqSummary201606.objects.filter(
                    op_time=op_time, acc_nbr=person2).values()

                # if anyone in the acc_nbr list cannot be found in db, response 404
                if len(records_p1) == 0 or len(records_p2) == 0:
                    return Response({'error': 'Record does not exist.'},
                                    status=status.HTTP_404_NOT_FOUND)
                else:
                    pair = person1 + '--' + person2
                    pair_score, pair_gang_score = get_gang_pair_score(
                        person1, person2, records_p1, records_p2, blacklist)
                    pair_dict[pair] = pair_score
                    gang_score += pair_gang_score

        gang_score /= len(pair_dict.keys())

        result = {
            'op_time': op_time,
            'acc_nbr_list': acc_nbr_list,
            'gang_score': gang_score,
            'relationship': pair_dict
        }

        return Response(result)


class MsisdnFraudDetection(LoggedAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MsisdnFraudDetectionSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(data=request.GET)
        if not serializer.is_valid(raise_exception=False):
            return Response({'error': 'Wrong input format.'},
                            status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        op_time = data['op_time']
        acc_nbr = data['acc_nbr']

        records = CdmaThjwqSummary201606.objects.filter(
            op_time=op_time, acc_nbr=acc_nbr).values()

        blacklist = list(Blacklist.objects.filter(
            op_time=op_time).values_list('acc_nbr', flat=True))

        if len(records) == 0:
            return Response({'error': 'Record does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            if acc_nbr in blacklist:
                fraud_status = True
                fraud_reason = 'The given acc_nbr is in the blacklist!'
            else:
                fraud_status, fraud_reason = \
                get_fraud_detection(records, blacklist, FRAUD_SCORE_TOP_NUM)

            result = {
                'op_time': op_time,
                'acc_nbr': acc_nbr,
                'fraud_status': fraud_status,
                'fraud_reason': fraud_reason
            }

        return Response(result)
