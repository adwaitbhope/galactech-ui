
def reset_current_file(num_files):
    with open('.current_file', 'w') as file:
        file.write(f'{0} {num_files}')

def get_next_file():
    with open('.current_file', 'r') as file:
        current_file, num_files = list(map(int, file.read().split()))

    with open('.current_file', 'w') as file:
        file.write(f'{current_file + 1} {num_files}')

    return (int(current_file) + 1) % num_files

def get_previous_file():
    with open('.current_file', 'r') as file:
        current_file, num_files = list(map(int, file.read().split()))

    with open('.current_file', 'w') as file:
        file.write(f'{current_file - 1} {num_files}')

    return (int(current_file) - 1) % num_files
