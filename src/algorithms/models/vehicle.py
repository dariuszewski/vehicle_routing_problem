
class Vehicle:
    def __init__(self, number) -> None:
        self.number = str(number).zfill(3)
        self.routes = []
    
    def add_route(self, route):
        self.routes.append(route)

if __name__ == "__main__":
    v = Vehicle(1)
    print(v.number)