def get_relationship_score(records):
    '''
    According to the call records of the acc_nbr, calculate the relaitonship
    score of each called_nbr.
    Return the relationship score by dictionary, using called_nbr as key.
    :param records: the call records of the acc_nbr
    :return: the relationship score of each called_nbr
    '''
    call_con_list = []
    call_duration_list = []

    for record in records:
        call_con_list.append(record['call_cnt'])
        call_duration_list.append(record['call_duration'])

    call_con_max = max(call_con_list)
    call_duration_max = max(call_duration_list)

    relationship_score_dict = {}
    for record in records:
        other_party = record['called_nbr']
        call_com = record['call_cnt']
        call_duration = record['call_duration']

        relationship_score = (call_com / call_con_max +
                              call_duration / call_duration_max) / 2
        relationship_score_dict[other_party] = relationship_score

    return relationship_score_dict


def get_close_relationship_dict(records, top_num):
    '''
    According to the call records of the acc_nbr, calculate the close
    relationship for the acc_nbr.
    Return the relationship score of each called_nbr in the close relationship
    by dictionary, using called_nbr as key.
    :param records: the call records of the acc_nbr
    :param top_num: the size of contact list to choose close relationship
    :return: the relationship score of each called_nbr in the close relationship
    '''
    relationship_score = get_relationship_score(records)
    relationship_score_sorted_reverse = sorted(
        relationship_score.items(),
        key=lambda x: x[1], reverse=True
    )
    if len(relationship_score_sorted_reverse) < top_num:
        top_num = len(relationship_score_sorted_reverse)

    close_relationship_dict = {}
    for t in relationship_score_sorted_reverse[:top_num]:
        close_relationship_dict[t[0]] = t[1]
    return close_relationship_dict


def get_fraud_score(records, blacklist, top_num):
    '''
    According to the call records of the acc_nbr, calculate the fraud score
    for the acc_nbr.
    Return the fraud_score and the called_nbr list
    in the blacklist and close relationship.
    :param records: the call records of the acc_nbr
    :param blacklist: the existing blacklist
    :param top_num: the size of contact list to calculate fraud_score
    :return: the fraud_score and the called_nbr list in the blacklist and
    close relationship.
    '''
    relationship_score = get_relationship_score(records)
    relationship_score_sorted_reverse = sorted(
        relationship_score.items(),
        key=lambda x: x[1], reverse=True)
    if len(relationship_score_sorted_reverse) < top_num:
        top_num = len(relationship_score_sorted_reverse)

    fraud_score = 0
    close_relationship_in_blacklist = []

    for t in relationship_score_sorted_reverse[:top_num]:
        if t[0] in blacklist:
            fraud_score = fraud_score + t[1]
            close_relationship_in_blacklist.append(t[0])

    if fraud_score > 1:
        fraud_score = 1

    return fraud_score, close_relationship_in_blacklist


def get_gang_pair_score(person1, person2, records_p1, records_p2, blacklist):
    '''
    According to the call records of person1 and person2, calculate the
    relationship score of the pair person1--person2,
    as well as the pair_gang_score.
    Return the pair_score and the pair_gang_score
    :param person1:
    :param person2:
    :param records_p1: the call records of person1
    :param records_p2: the call records of person2
    :param blacklist: the existing blacklist
    :return: the pair_score and the pair_gang_score
    '''
    relationship_score_p1 = get_relationship_score(records_p1)
    relationship_score_p2 = get_relationship_score(records_p2)

    pair_score = 0
    pair_gang_score = 0

    # Direct connection
    if person2 in relationship_score_p1 and person1 in relationship_score_p2:
        pair_score += (relationship_score_p1[person2] +
                       relationship_score_p2[person1]) / 2
        # If person1 or person2 is in the blacklist, group gang score grows.
        pair_gang_score += pair_score * (person1 in blacklist)
        pair_gang_score += pair_score * (person2 in blacklist)

    # Someone in the acc_nbr list can have common contacts,
    # their relationship score are used to calculate gang score.
    common_relation = set(relationship_score_p1.keys()).intersection(
        relationship_score_p2.keys())

    if len(common_relation) != 0:
        # gang pair score are calculated by adding all relationship scores of common contacts
        for p in common_relation:
            common_relation_score = \
                (relationship_score_p1[p] + relationship_score_p2[p]) * 3 / 8
            pair_score += common_relation_score
            # if common contact is in the blacklist, group gang score grows.
            pair_gang_score += common_relation_score * (p in blacklist)

    if pair_score > 1:
        pair_score = 1
    if pair_gang_score > 1:
        pair_gang_score = 1

    return pair_score, pair_gang_score


def get_fraud_detection(records, blacklist, top_num):
    '''
    According to the call records of the acc_nbr, find out whether the acc_nbr
    is fraud or not.
    Return the fraud status and the fraud reason
    :param records: the call records of the acc_nbr
    :param blacklist: the existing blacklist
    :param top_num: the size of contact list to calculate fraud_score
    :return: the fraud status and the fraud reason
    '''
    fraud_score, close_relationship_in_blacklist = \
        get_fraud_score(records, blacklist, top_num)

    fraud_status = fraud_score > 0.005
    if fraud_status:
        fraud_reason = 'The given acc_nbr has close relationship to blacklist: {}'.format(
            close_relationship_in_blacklist)
    else:
        fraud_reason = None

    return fraud_status, fraud_reason
