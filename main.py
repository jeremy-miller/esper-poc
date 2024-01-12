from dataclasses import dataclass as component
from time import sleep

import esper


@component
class Position:
    x: float = 0.0
    y: float = 0.0


@component
class Velocity:
    x: float = 0.0
    y: float = 0.0


class MovementProcessor(esper.Processor):
    def process(self):
        for entity, (velocity, position) in esper.get_components(Velocity, Position):
            position.x += velocity.x
            position.y += velocity.y
            print(f"Entity {entity} has new position ({position.x}, {position.y})")


def test_event_handler():
    print("Received test event")


def main():
    esper.add_processor(MovementProcessor(), priority=3)
    esper.set_handler("test", test_event_handler)
    player = esper.create_entity(Velocity(x=0.9, y=1.2), Position(x=5, y=5))
    print(
        f"Player entity ({player}) has these components: {esper.components_for_entity(player)}"
    )

    while True:
        esper.dispatch_event("test")
        esper.process()
        sleep(1)


if __name__ == "__main__":
    main()
