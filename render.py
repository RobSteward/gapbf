from config import GRID_SIZE

def render_path(path):
    # Create a path slug and print it
    slug = "-".join(str(p) for p in path)
    print(f"\nPattern: {slug}")

    # Render the pattern grid
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if y * GRID_SIZE + x in path:
                print("●", end="")
            else:
                print("○", end="")
        print()

def render_path_steps(path):
    # Render the path steps
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            value = y * GRID_SIZE + x
            if value in path:
                print(f"{path.index(value) + 1} ", end="")
            else:
                print("· ", end="")
        print()