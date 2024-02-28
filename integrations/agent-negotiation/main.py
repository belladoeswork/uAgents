from uagents import Bureau

from negotiation.bob import bob
from negotiation.alice import alice
from negotiation.coordinator import coordinator

bureau = Bureau()
bureau.add(alice)
bureau.add(bob)
bureau.add(coordinator)


if __name__ == '__main__':
    bureau.run()
