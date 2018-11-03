# 291miniproject1
painnnnnnnnnnnnnnnnnnnnnnnnnnn

### Login Screen
The first screen of your system should provide options for members to login and for new members to register. Existing members should be able to login using a valid email and password, denoted with email and pwd in table members. After a login, all unseen messages of the member will be displayed, and the status of the messages will be set to seen (i.e, the seen column is set to 'y'). Unregistered members should be able to sign up by providing a unique email, a name, a phone, and a password. Proper messages should be given if the provided email is not unique. After a successful login or signup, members should be able to perform the subsequent operations (possibly chosen from a menu) as discussed next.

Members should be able to logout and there must be also an option to exit the program.

### System Functionalities
Members should be able to perform all of the following tasks. All string matches must be case-insensitive (e.g., edmonton will match Edmonton, EDMONTON, edmontoN and edmonton).

#### 1 - Offer a ride.
The member should be able to offer rides by providing a date, the number of seats offered, the price per seat, a luggage description, a source location, and a destination location. The member should have the option of adding a car number and any set of enroute locations. For locations (including source, destination and enroute), the member should be able to provide a keyword, which can be a location code. If the keyword is not a location code, your system should return all locations that have the keyword as a substring in city, province or address fields. If there are more than 5 matching locations, at most 5 matches will be shown at a time, letting the member select a location or see more matches. If a car number is entered, your system must ensure that the car belongs to the member. Your system should automatically assign a unique ride number (rno) to the ride and set the member as the driver of the ride.

#### 2 - Search for rides.

The member should be able to enter 1-3 location keywords and retrieve all rides that match all keywords. A ride matches a keyword if the keyword matches one of the locations source, destination, or enroute. Also a location matches a keyword if the keyword is either the location code or a substring of the city, the province, or the address fields of the location. For each matching ride, all information about the ride (from the rides table) and car details (if any) will be displayed. If there are more than 5 matches, at most 5 will be shown at a time, and the member is provided an option to see more. The member should be able to select a ride and message the member posting the ride that h/she wants to book seats on that ride.

#### 3 - Book members or cancel bookings.

The member should be able to list all bookings on rides s/he offers and cancel any booking. For any booking that is cancelled (i.e. being deleted from the booking table), a proper message should be sent to the member whose booking is cancelled. Also the member should be able to book other members on the rides they offer. Your system should list all rides the member offers with the number of available seats for each ride (i.e., seats that are not booked). If there are more than 5 matching rides, at most 5 will be shown at a time, and the member will have the option to see more. The member should be able to select a ride and book a member for that ride by entering the member email, the number of seats booked, the cost per seat, and pickup and drop off location codes. Your system should assign a unique booking number (bno) to the booking. Your system should give a warning if a ride is being overbooked (i.e. the number of seats booked exceeds the number of seats offered), but will allow overbooking if the member confirms it. After a successful booking, a proper message should be sent to the other member that s/he is booked on the ride.

#### 4 - Post ride requests.

The member should be able to post a ride request by providing a date, a pick up location code, a drop off location code, and the amount willing to pay per seat. The request rid is set by your system to a unique number and the email is set to the email address of the member.

#### 5 - Search and delete ride requests.

The member should be able to see all his/her ride requests and be able to delete any of them. Also the member should be able to provide a location code or a city and see a listing of all requests with a pickup location matching the location code or the city entered. If there are more than 5 matches, at most 5 matches will be shown at a time. The member should be able to select a request and message the posting member, for example asking the member to check out a ride.

### SQL INJECTION?
Groups of size 3 must counter SQL injection attacks and make the password non-visible at the time of typing.
