from uuid import uuid4
from uagents import Agent, Context
from negotiation.messages import Acceptance, CounterProposal, Proposal, Reject
from negotiation.new_booking import ParkingSpot, ParkingRequest, NegotiationStart, SpotAlreadyBooked

coordinator = Agent(name='coordinator', seed='coordinators super secret seed phrase')
print('Coordinator address: ', coordinator.address)

# Example parking spots
parking_spots = {
    'spot1': ParkingSpot(id=str(uuid4()), spot_id='spot1', is_free=True, departure_time=0),
    'spot2': ParkingSpot(id=str(uuid4()), spot_id='spot2', is_free=False, departure_time=123456789, booked_by='agent1qg5a9zvex0gy2amagpvadp6f9kcf8jxa3akrqd09lf8kk2frlxj7q7pu3yt'),
}

# Mapping from addresses to names
address_to_name = {
    'agent1qg5a9zvex0gy2amagpvadp6f9kcf8jxa3akrqd09lf8kk2frlxj7q7pu3yt': 'Bob',
    'agent1q2rc9ema7vgmrd4athph844e37jd2krnfyuzrtzhf5r0qkm9tequ63pkjue': 'Alice',
    'agent1qdke0naa94cn7z5wfsc95vwqc67engqxpv66ctl72h8esqah2km9jnrnjw4': 'Coordinator',
}

@coordinator.on_message(Proposal)
async def handle_proposal(ctx: Context, sender: str, msg: Proposal):
    sender_name = address_to_name.get(sender, 'Unknown')
    ctx.logger.info(f'Received proposal ({msg.id}) from {sender_name} for {msg.item} at price {msg.price}')

    negotiation = negotiations.get(msg.id)
    if negotiation:
        recipient = negotiation.get('buyer' if sender == negotiation.get('seller') else 'seller')
        if recipient:
            await ctx.send(recipient, msg)
            
            
# Dictionary to keep track of ongoing negotiations
negotiations = {}

@coordinator.on_message(ParkingRequest)
async def handle_parking_request(ctx: Context, sender: str, msg: ParkingRequest):
    spot_id = msg.spot_id
    requested_spot = parking_spots.get(spot_id)

    if requested_spot is None:
        await ctx.send(sender, Reject(proposal_id=str(uuid4()), reason=f"No parking spot with id {spot_id}"))
        return

    if requested_spot.is_free:
        negotiation_id = str(uuid4())
        negotiations[negotiation_id] = {'buyer': sender, 'spot_id': spot_id}
        await ctx.send(sender, Acceptance(proposal_id=negotiation_id, item="ParkingSpot", price=0))
        requested_spot.is_free = False
        requested_spot.booked_by = sender
    else:
        negotiation_id = str(uuid4())
        negotiations[negotiation_id] = {'buyer': sender, 'seller': requested_spot.booked_by, 'spot_id': spot_id}
        await ctx.send(requested_spot.booked_by, Proposal(id=negotiation_id, item="ParkingSpot", price=100))

@coordinator.on_message(CounterProposal)
async def handle_counter_proposal(ctx: Context, sender: str, msg: CounterProposal):
    sender_name = address_to_name.get(sender, 'Unknown')
    ctx.logger.info(f'Received counterproposal ({msg.proposal_id}) from {sender_name} for {msg.item} at price {msg.price}')

    negotiation = negotiations.get(msg.proposal_id)
    if negotiation:
        recipient = negotiation.get('buyer' if sender == negotiation.get('seller') else 'seller')
        if recipient:
            await ctx.send(recipient, msg)

@coordinator.on_message(Acceptance)
async def handle_acceptance(ctx: Context, sender: str, msg: Acceptance):
    negotiation = negotiations.pop(msg.proposal_id, None)
    if negotiation:
        # Notify both parties of acceptance
        await ctx.send(negotiation['seller'], msg)
        await ctx.send(negotiation['buyer'], msg)
        # Update parking spot status if necessary
        spot_id = negotiation.get('spot_id')
        if spot_id:
            spot = parking_spots.get(spot_id)
            if spot:
                spot.is_free = False
                spot.booked_by = negotiation['buyer']
