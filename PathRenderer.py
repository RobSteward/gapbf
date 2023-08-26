from ConfigHandler import ConfigHandler

# Load config file
config = ConfigHandler('config.yaml')
grid_size = config.grid_size

def render_path(path):
    rows = []
    # Create a path slug and print it
    slug = "-".join(str(p) for p in path)

    # Render the pattern grid
    for y in range(grid_size):
        row = []
        for x in range(grid_size):
            if y * grid_size + x in path:
                row.append("●")
            else:
                row.append("○")
        rows.append("".join(row))
    return rows

def render_path_steps(path):
    rows = []
    # Render the path steps
    for y in range(grid_size):
        row = []
        for x in range(grid_size):
            value = y * grid_size + x
            if value in path:
                row.append(f"{path.index(value) + 1}")
            else:
                row.append("·")
        rows.append(" ".join(row))
    return rows