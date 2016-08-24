from rest_framework import serializers

# class TestDBSerializer(serializers.Serializer):
#     id = serializers.IntegerField()


class OpTimeSerializer(serializers.Serializer):
    op_time = serializers.CharField(min_length=6, max_length=6)


class BlacklistSerializer(serializers.Serializer):
    op_time = serializers.CharField(min_length=6, max_length=6)
    acc_nbr = serializers.CharField(min_length=32, max_length=32)


# class MsisdnBlacklistStatusSerializer(serializers.Serializer):
#     op_time = serializers.CharField(min_length=6, max_length=6)
#     acc_nbr = serializers.CharField(min_length=32, max_length=32)


class MsisdnCloseRelationshipSerializer(serializers.Serializer):
    op_time = serializers.CharField(min_length=6, max_length=6)
    acc_nbr = serializers.CharField(min_length=32, max_length=32)


class MsisdnFraudScoreSerializer(serializers.Serializer):
    op_time = serializers.CharField(min_length=6, max_length=6)
    acc_nbr = serializers.CharField(min_length=32, max_length=32)


class MsisdnGangDetectionSerializer(serializers.Serializer):
    op_time = serializers.CharField(min_length=6, max_length=6)
    acc_nbr_list = serializers.ListField(
        child=serializers.CharField(min_length=32, max_length=32)
    )


class MsisdnFraudDetectionSerializer(serializers.Serializer):
    op_time = serializers.CharField(min_length=6, max_length=6)
    acc_nbr = serializers.CharField(min_length=32, max_length=32)
    # acc_nbr_list = serializers.ListField(
    #     child=serializers.CharField(min_length=32, max_length=32)
    # )


