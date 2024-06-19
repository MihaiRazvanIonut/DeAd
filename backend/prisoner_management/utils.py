def normalise_row(row: dict):
    for key, value in row.items():
        row[key] = str(value)
