from rest_framework import status
from rest_framework.test import APITestCase


# class TestDBTests(APITestCase):
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.url_prefix = '/anti-fraud/test-db/'
#
#    def test_existing_id(self):
#        response = self.client.get('{}?id=1'.format(self.url_prefix))
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        self.assertEqual(
#            response.data,
#            {
#                'acc_nbr': '06b13159e88e97068814a52074c3df1a'
#            }
#        )
#
#    def test_nonexisting_id(self):
#        response = self.client.get('{}?id=100000'.format(self.url_prefix))
#        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#    def test_illegal_id(self):
#        response = self.client.get('{}?id=abc'.format(self.url_prefix))
#        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestBlacklist(APITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_prefix = '/anti-fraud/blacklist/'

    def test_blacklist_get(self):
        response = self.client.get('{}?op_time=201606'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "blacklist": [
                    "7a2ef376620bfca27bf2e3afd91fe4de",
                    "6c371b993deadf64c28da2f77fb40395",
                    "7592dd8e0f0e6e2a092e074d5fca129c",
                    "005f26e3162cfd1eaf1800e8e919f7a4",
                    "0133454645e12b3f39a0b485ccdc60a2",
                    "01737e721796975a6317efb33aa92378",
                    "0202a0d8eeb77f8b78dbb46da59a29a6",
                    "02125a2219b1eb70a561aff0e67c6826",
                    "023564f472ffb2c1d8cb8d36ab874a49",
                    "024d3cd31063bd78a514fe088a5dec5b",
                    "06b13159e88e97068814a52074c3df1a",
                    "0765c04ba0bf083cbf7a79a029a234c2"
                ],
                "op_time": "201606"
            }
        )

    def test_blacklist_post_and_delete(self):
        response = self.client.post(
            '{}?op_time=201606&acc_nbr=dc48b170a561db765bbbeb8ae1475c9f'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                "op_time": "201606",
                "acc_nbr": "dc48b170a561db765bbbeb8ae1475c9f"
            }
        )

        # remove the just posted record
        response = self.client.delete(
            '{}?op_time=201606&acc_nbr=dc48b170a561db765bbbeb8ae1475c9f'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_existing_acc_nbr_post(self):
        response = self.client.post(
            '{}?op_time=201606&acc_nbr=024d3cd31063bd78a514fe088a5dec5b'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonexisting_acc_nbr_delete(self):
        response = self.client.delete(
            '{}?op_time=201606&acc_nbr=dc48b170a561db765bbbeb8ae1475c9f'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_nonexisting_op_time(self):
        response = self.client.get('{}?op_time=201607'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_illegal_op_time(self):
        response = self.client.get('{}?op_time=2016'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestMsisdnBlacklistStatus(APITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_prefix = '/anti-fraud/msisdnBlacklistStatus/'

    def test_acc_nbr_in_blacklist(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr=06b13159e88e97068814a52074c3df1a'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "blacklist_status": True,
                "acc_nbr": "06b13159e88e97068814a52074c3df1a",
                "op_time": "201606"
            }
        )

    def test_acc_nbr_not_in_blacklist(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr=0aed7b1d74eff382561fa2118468e965'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "op_time": "201606",
                "acc_nbr": "0aed7b1d74eff382561fa2118468e965",
                "blacklist_status": False
            }
        )

    def test_nonexisting_op_time(self):
        response = self.client.get(
            '{}?op_time=201607&acc_nbr=06b13159e88e97068814a52074c3df1a'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_illegal_op_time(self):
        response = self.client.get(
            '{}?op_time=2016&acc_nbr=06b13159e88e97068814a52074c3df1a'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonexisting_acc_nbr(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr=6c371b993deadf64c28da2f77fb40395'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_illegal_acc_nbr(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr=abc'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestMsisdnCloseRelationship(APITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_prefix = '/anti-fraud/msisdnCloseRelationship/'

    def test_close_relationship_return_top_5(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr=06b13159e88e97068814a52074c3df1a'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "op_time": "201606",
                "acc_nbr": "06b13159e88e97068814a52074c3df1a",
                "close_relationship": {
                    "43f5bdb56f957b498f5de19a90439eb4": 0.5942028985507246,
                    "0b17ea896d243cda41ab8b83c38a5018": 0.740036231884058,
                    "04a41c98e036facbf35dfc53765f689a": 0.75,
                    "cba32d58b7501b8fbac0c928ca1faa99": 0.5335144927536232,
                    "40ad14c2d77db6c63968e4b65ec45733": 0.6422101449275363
                }
            }
        )

    def test_close_relationship_return_less_than_5(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr=0971e3eefa39b47940582da1887d970a'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "op_time": "201606",
                "acc_nbr": "0971e3eefa39b47940582da1887d970a",
                "close_relationship": {
                    "c14ab09b1b34ea4711f092cdf69fa68a": 0.5619834710743802,
                    "98824c83fca6997831fe4909f7f848c8": 1.0,
                    "91bc41ecbaecb1a6c871142e4b1f66a9": 0.5289256198347108
                }
            }
        )

    def test_nonexisting_op_time(self):
        response = self.client.get(
            '{}?op_time=201607&acc_nbr=06b13159e88e97068814a52074c3df1a'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_illegal_op_time(self):
        response = self.client.get(
            '{}?op_time=2016&acc_nbr=06b13159e88e97068814a52074c3df1a'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonexisting_acc_nbr(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr=6c371b993deadf64c28da2f77fb40395'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_illegal_acc_nbr(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr=abc'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestMsisdnFraudScore(APITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_prefix = '/anti-fraud/msisdnFraudScore/'

    def test_fraud_score_high(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr=06b13159e88e97068814a52074c3df1a'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "fraud_score": 1,
                "op_time": "201606",
                "acc_nbr": "06b13159e88e97068814a52074c3df1a"
            }
        )

    def test_fraud_score_low(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr=c95fdcdbb3cc4a6054d3559bff910548'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "op_time": "201606",
                "acc_nbr": "c95fdcdbb3cc4a6054d3559bff910548",
                "fraud_score": 0.03447488584474886
            }
        )

    def test_nonexisting_op_time(self):
        response = self.client.get(
            '{}?op_time=201607&acc_nbr=06b13159e88e97068814a52074c3df1a'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_illegal_op_time(self):
        response = self.client.get(
            '{}?op_time=2016&acc_nbr=06b13159e88e97068814a52074c3df1a'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonexisting_acc_nbr(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr=6c371b993deadf64c28da2f77fb40395'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_illegal_acc_nbr(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr=abc'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestMsisdnGangDetection(APITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_prefix = '/anti-fraud/msisdnGangDetection/'

    def test_gang_score_1(self):
        response = self.client.get(
            '{}?op_time=201606&acc_nbr_list=07fa6b554cd1c085fa6b0113e0598765&acc_nbr_list=0aed7b1d74eff382561fa2118468e965&acc_nbr_list=1196ef976043129632da6aa17428136b'.format(
                self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "gang_score": 0.006926805915968226,
                "acc_nbr_list": [
                    "07fa6b554cd1c085fa6b0113e0598765",
                    "0aed7b1d74eff382561fa2118468e965",
                    "1196ef976043129632da6aa17428136b"
                ],
                "op_time": "201606",
                "relationship": {
                    "07fa6b554cd1c085fa6b0113e0598765--1196ef976043129632da6aa17428136b": 0.007039173486046447,
                    "07fa6b554cd1c085fa6b0113e0598765--0aed7b1d74eff382561fa2118468e965": 0.006798207358263346,
                    "0aed7b1d74eff382561fa2118468e965--1196ef976043129632da6aa17428136b": 0.006943036903594885
                }
            }
        )


    def test_gang_score_2(self):
        response = self.client.get('{}?op_time=201606&acc_nbr_list=0765c04ba0bf083cbf7a79a029a234c2&acc_nbr_list=07fa6b554cd1c085fa6b0113e0598765'.format(
            self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "gang_score": 0.0,
                "acc_nbr_list": [
                    "0765c04ba0bf083cbf7a79a029a234c2",
                    "07fa6b554cd1c085fa6b0113e0598765"
                ],
                "op_time": "201606",
                "relationship": {
                    "0765c04ba0bf083cbf7a79a029a234c2--07fa6b554cd1c085fa6b0113e0598765": 0
                }
            }
        )

    def test_gang_score_3(self):
        response = self.client.get('{}?op_time=201606&acc_nbr_list=0765c04ba0bf083cbf7a79a029a234c2&acc_nbr_list=0ac49fa735db28e93dc23500b18cae75'.format(
            self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "gang_score": 0.01471022415722453,
                "acc_nbr_list": [
                    "0765c04ba0bf083cbf7a79a029a234c2",
                    "0ac49fa735db28e93dc23500b18cae75"
                ],
                "op_time": "201606",
                "relationship": {
                    "0765c04ba0bf083cbf7a79a029a234c2--0ac49fa735db28e93dc23500b18cae75": 0.01471022415722453
                }
            }
        )

    def test_nonexisting_op_time(self):
        response = self.client.get('{}?op_time=201607&acc_nbr_list=07fa6b554cd1c085fa6b0113e0598765&acc_nbr_list=0aed7b1d74eff382561fa2118468e965&acc_nbr_list=1196ef976043129632da6aa17428136b'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_illegal_op_time(self):
        response = self.client.get('{}?op_time=2016&acc_nbr_list=07fa6b554cd1c085fa6b0113e0598765&acc_nbr_list=0aed7b1d74eff382561fa2118468e965&acc_nbr_list=1196ef976043129632da6aa17428136b'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonexisting_acc_nbr(self):
        response = self.client.get('{}?op_time=201606&acc_nbr_list=0765c04ba0bf083cbf7a79a029a234c2&acc_nbr_list=6c371b993deadf64c28da2f77fb40395'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_illegal_acc_nbr(self):
        response = self.client.get('{}?op_time=201606&acc_nbr_list=abc&acc_nbr_list=0765c04ba0bf083cbf7a79a029a234c2'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_one_acc_nbr(self):
        response = self.client.get('{}?op_time=201606&acc_nbr_list=0765c04ba0bf083cbf7a79a029a234c2'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestMsisdnFraudDetection(APITestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_prefix = '/anti-fraud/msisdnFraudDetection/'

    def test_fraud_true_1(self):
        response = self.client.get('{}?op_time=201606&acc_nbr=06b13159e88e97068814a52074c3df1a'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "acc_nbr": "06b13159e88e97068814a52074c3df1a",
                "op_time": "201606",
                "fraud_reason": "The given acc_nbr is in the blacklist!",
                "fraud_status": True
            }
        )

    def test_fraud_true_2(self):
        response = self.client.get('{}?op_time=201606&acc_nbr=c95fdcdbb3cc4a6054d3559bff910548'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "op_time": "201606",
                "fraud_reason": "The given acc_nbr has close relationship to blacklist: ['7592dd8e0f0e6e2a092e074d5fca129c']",
                "fraud_status": True,
                "acc_nbr": "c95fdcdbb3cc4a6054d3559bff910548"
            }
        )

    def test_fraud_false(self):
        response = self.client.get('{}?op_time=201606&acc_nbr=c7da2df1d4e15e25b9311115d5ebe04c'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "op_time": "201606",
                "fraud_reason": None,
                "fraud_status": False,
                "acc_nbr": "c7da2df1d4e15e25b9311115d5ebe04c"
            }
        )

    def test_nonexisting_op_time(self):
        response = self.client.get('{}?op_time=201607&acc_nbr=06b13159e88e97068814a52074c3df1a'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_illegal_op_time(self):
        response = self.client.get('{}?op_time=2016&acc_nbr=06b13159e88e97068814a52074c3df1a'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonexisting_acc_nbr(self):
        response = self.client.get('{}?op_time=201606&acc_nbr=6c371b993deadf64c28da2f77fb40395'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_illegal_acc_nbr(self):
        response = self.client.get('{}?op_time=201606&acc_nbr=abc'.format(self.url_prefix))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
