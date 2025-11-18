from backend.app.main import app

def list_routes():
    print("\n🚀 FastAPI Registered Endpoints:\n")
    for route in app.routes:
        methods = ', '.join(route.methods)
        name = route.name
        path = route.path
        print(f"{methods:20} | {path:40} | {name}")

if __name__ == "__main__":
    list_routes()
