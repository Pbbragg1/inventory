from model import (Base, Session, inventory, engine)


if __name__ == "__main__":
    Base.metadata.create_all(engine)