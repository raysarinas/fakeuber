# 4 - POST RIDE REQUESTS
# 5 - SEARCH AND DELETE RIDE requests

def postRequest(conn):
    '''
    The member should be able to post a ride request by providing a date,
    a pick up location code, a drop off location code, and the amount willing
    to pay per seat. The request rid is set by your system to a unique number
    and the email is set to the email address of the member.
    '''
    # TAKE date, pickup code, dropoff code and amount willing to pay
    # as input from USER.
    # need to assign that value with a unique request RID
        # could just use an incrementer so every new one is just +1 from
        # previous request posted or just whatever
    # set email to email address of member
    pass

def seadelRequest(conn):
    '''
    The member should be able to see all his/her ride requests and be able
    to delete any of them. Also the member should be able to provide a
    location code or a city and see a listing of all requests with a pickup
    location matching the location code or the city entered. If there are more
    than 5 matches, at most 5 matches will be shown at a time. The member
    should be able to select a request and message the posting member, for
    example asking the member to check out a ride.
    '''
    # display / query ride requests RELATED TO member (i.e. EMAIL)
    # match the query thing with member email
    # INPUT: location code or city and then QUERY and list all requests with
        # pickup location matching INPUT
    # SHOW AT MOST 5 MATCHES
    # SCROLL THROUGH NEXT PAGE????
    # BE ABLE TO MESSAGE THE POSTING MEMBER WTF
    pass
