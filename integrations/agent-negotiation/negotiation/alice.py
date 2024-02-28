import asyncio

from uuid import uuid4

from uagents import Agent, Context
from negotiation.messages import Acceptance, CounterProposal, Proposal, Reject
from negotiation.new_booking import ParkingRequest, NegotiationStart, SpotAlreadyBooked

ALICE_TARGET_MIN_PRICE = 60.0
ALICE_TARGET_MAX_PRICE = 110.0
ALICE_TARGET_ITEM = 'ParkingSpot'

alice = Agent(name='alice', seed='alices super secret seed phrase')
print('Alice address: ', alice.address)

coordinator_address = 'agent1qdke0naa94cn7z5wfsc95vwqc67engqxpv66ctl72h8esqah2km9jnrnjw4'

@alice.on_message(Acceptance)
async def handle_acceptance(ctx: Context, sender: str, msg: Acceptance):
    ctx.logger.info(f'({msg.proposal_id}) accepted at price {msg.price}')

@alice.on_message(Reject)
async def handle_reject(ctx: Context, sender: str, msg: Reject):
    ctx.logger.info(f'({msg.proposal_id}) rejected because {msg.reason}')

@alice.on_message(CounterProposal)
async def handle_counter_proposal(ctx: Context, sender: str, msg: CounterProposal):
    ctx.logger.info(f'({msg.proposal_id}) counter offer for {msg.price}')
    # evaluate the counter proposal
    next_price = ((msg.price - ALICE_TARGET_MIN_PRICE) // 2) + ALICE_TARGET_MIN_PRICE
    # attempt to negotiate down
    await ctx.send(
        coordinator_address,
        CounterProposal(
            proposal_id=msg.proposal_id,
            item=ALICE_TARGET_ITEM,
            price=next_price,
        )
    )

@alice.on_interval(10)
async def on_interval(ctx: Context):
    proposal_id = uuid4()
    starting_price = ALICE_TARGET_MIN_PRICE
    ctx.logger.info(f'({proposal_id}) proposing at price {starting_price}')
    # send the proposal to the coordinator
    await ctx.send(
        coordinator_address,
        Proposal(
            id=proposal_id,
            item=ALICE_TARGET_ITEM,
            price=starting_price
        )
    )



@alice.on_event("startup")
async def start(ctx: Context):
    spot_request = ParkingRequest(spot_id='spot2', agent_address=alice.address) 
    await ctx.send(coordinator_address, spot_request)
    


# @alice.on_message(SpotAlreadyBooked)
# async def handle_spot_already_booked(ctx: Context, sender: str, msg: SpotAlreadyBooked):
#     print(f"Received message that spot {msg.spot_id} is already booked by {msg.holder}")

@alice.on_message(SpotAlreadyBooked)
async def handle_spot_already_booked(ctx: Context, sender: str, msg: SpotAlreadyBooked):
    # initiates negotiation for spot2
    negotiation_id = str(uuid4())
    await ctx.send(sender, Proposal(id=negotiation_id, item="ParkingSpot", price=90))


@alice.on_message(NegotiationStart)
async def handle_negotiation_start(ctx: Context, sender: str, msg: NegotiationStart):
    print(f"Negotiation started for spot {msg.spot_id}, negotiation ID: {msg.negotiation_id}")
    await ctx.send(coordinator_address, Proposal(id=msg.negotiation_id, item="ParkingSpot", price=ALICE_TARGET_MIN_PRICE))


