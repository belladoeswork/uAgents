# from pydantic import UUID4
# from uagents import Model
# from datetime import datetime

# class ParkingSpot(Model):
#     id: UUID4
#     is_free: bool
#     departure_time: int  

# class ParkingStatus(Model):
#     spots: list[ParkingSpot]


# class ParkingRequest(Model):
#     agent_address: str


# class ParkingOffer(Model):
#     id: UUID4
#     is_free: bool
#     departure_time: int

# class ParkingReservation(Model):
#     requester: str
#     id: UUID4


# class PaymentRequest(Model):
#     spot_id: str
#     requester: str

# class ParkingOptions(Model):
#     id: UUID4
#     is_free: bool
#     departure_time: int  


# class ParkingSpot(Model):
#     id: UUID4
#     is_free: bool
#     departure_time: int  


# class ParkingBooked(Model):
#     proposal_id: UUID4
#     item: str
#     price: float
#     booking_id: str 
    
    
# class ParkingBookingRequest(Model):
#     requester: str
#     spot_id: str
#     start_time: datetime
#     end_time: datetime 
    
    
#     # correct add 
    
# class SpotAlreadyBooked(Model):
#     holder: str
#     requester: str
#     spot_id: str
#     start_time: datetime
#     end_time: datetime 
    
# class SpotAlreadyBooked(Model):
#     holder: str
#     requester: str
#     spot_id: str
#     start_time: datetime
#     end_time: datetime 
    
# class ParkingConfirmation(Model):  
#     proposal_id: UUID4
#     spot_id: str
#     holder: str
#     booking_id: str 
#     start_time: datetime
#     end_time: datetime
    
# class NegotiationStart(Model):  
#     spot_id: str
#     negotiation_id: str
    
from pydantic import UUID4
from uagents import Model
from datetime import datetime

class ParkingSpot(Model):
    id: UUID4
    is_free: bool
    departure_time: int
    booked_by: str = None

class ParkingStatus(Model):
    spots: list[ParkingSpot]

class ParkingRequest(Model):
    agent_address: str
    spot_id: str

class ParkingOffer(Model):
    id: UUID4
    is_free: bool
    departure_time: int

class ParkingReservation(Model):
    requester: str
    id: UUID4

class PaymentRequest(Model):
    spot_id: str
    requester: str

class ParkingOptions(Model):
    id: UUID4
    is_free: bool
    departure_time: int  

class ParkingBooked(Model):
    proposal_id: UUID4
    item: str
    price: float
    booking_id: str 

class ParkingBookingRequest(Model):
    requester: str
    spot_id: str
    start_time: datetime
    end_time: datetime 

class SpotAlreadyBooked(Model):
    holder: str
    requester: str
    spot_id: str
    start_time: datetime
    end_time: datetime 

class ParkingConfirmation(Model):  
    proposal_id: UUID4
    spot_id: str
    holder: str
    booking_id: str 
    start_time: datetime
    end_time: datetime

class NegotiationStart(Model):  
    spot_id: str
    negotiation_id: str