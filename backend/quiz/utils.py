from itertools import groupby

def transform_array_by_id(arr):
    sorted_array = sorted(arr, key=lambda x: x['id'])
    grouped_array = [list(group) for key, group in groupby(sorted_array, key=lambda x: x['id'])]
    return grouped_array

# Example usage
original_array = [
    {'id': 3, 'text': 'text'},
    {'id': 1, 'text': 'text'},
    {'id': 2, 'text': 'text'},
    {'id': 4, 'text': 'text'},
    {'id': 2, 'text': 'text'},
    {'id': 3, 'text': 'text'},
    {'id': 4, 'text': 'text'},
]
transformed_array = transform_array_by_id(original_array)

for i in transformed_array:
    print(i)
