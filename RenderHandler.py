from ConfigHandler import ConfigHandler

# Load config file
config = ConfigHandler('config.yaml')

# Assigning variables
grid_size = config.get_value('grid_size')


def render_path(path):
    # Create a path slug and print it
    slug = "-".join(str(p) for p in path)
    print(f"\nPattern: {slug}")

    # Render the pattern grid
    for y in range(grid_size):
        for x in range(grid_size):
            if y * grid_size + x in path:
                print("●", end="")
            else:
                print("○", end="")
        print()

def render_path_steps(path):
    # Render the path steps
    for y in range(grid_size):
        for x in range(grid_size):
            value = y * grid_size + x
            if value in path:
                print(f"{path.index(value) + 1} ", end="")
            else:
                print("· ", end="")
        print()