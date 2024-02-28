from uagents import Agent, Context
from negotiation.messages import Proposal, CounterProposal, Acceptance, Reject
from negotiation.new_booking import ParkingRequest

BOB_TARGET_MIN_PRICE = 100.0
BOB_TARGET_MAX_PRICE = 150.0
BOB_TARGET_ITEM = 'ParkingSpot'

bob = Agent(name='bob', seed='bobs super secret seed phrase')
print('Bob address: ', bob.address)

coordinator_address = 'agent1qdke0naa94cn7z5wfsc95vwqc67engqxpv66ctl72h8esqah2km9jnrnjw4'

address_to_name = {
    'agent1qg5a9zvex0gy2amagpvadp6f9kcf8jxa3akrqd09lf8kk2frlxj7q7pu3yt': 'Bob',
    'agentq2rc9ema7vgmrd4athph844e37jd2krnfyuzrtzhf5r0qkm9tequ63pkjue': 'Alice',
    'agent1qdke0naa94cn7z5wfsc95vwqc67engqxpv66ctl72h8esqah2km9jnrnjw4': 'Coordinator',
}


@bob.on_event("startup")
async def start(ctx: Context):
    spot_request = ParkingRequest(spot_id='spot2', agent_address=bob.address) 
    await ctx.send(coordinator_address, spot_request)

@bob.on_message(Proposal)
async def handle_proposal(ctx: Context, sender: str, msg: Proposal):
    sender_name = address_to_name.get(sender, 'Unknown')
    ctx.logger.info(f'Received proposal ({msg.id}) from {sender_name} for {msg.item} at price {msg.price}')

    if msg.item != BOB_TARGET_ITEM:
        await ctx.send(sender, Reject(proposal_id=msg.id, reason='Not interested in that item'))
        return

    if BOB_TARGET_MIN_PRICE <= msg.price < BOB_TARGET_MAX_PRICE:
        await ctx.send(sender, Acceptance(proposal_id=msg.id, item=msg.item, price=msg.price))
    else:
        counter_price = min(max(msg.price, BOB_TARGET_MIN_PRICE), BOB_TARGET_MAX_PRICE)
        await ctx.send(sender, CounterProposal(proposal_id=msg.id, item=msg.item, price=counter_price))
        ctx.logger.info(f'Counterproposal sent to {sender_name} at price {counter_price}')

@bob.on_message(ParkingRequest)
async def handle_parking_request(ctx: Context, sender: str, msg: ParkingRequest):
    spot_id = msg.spot_id
    if spot_id == 'spot2':
        # Respond to negotiation request from the coordinator
        negotiation_id = str(uuid4())
        await ctx.send(sender, Proposal(id=negotiation_id, item="ParkingSpot", price=90))  # Example proposal price

