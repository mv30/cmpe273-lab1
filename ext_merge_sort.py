import os
from os import listdir

BUFFER_SIZE = 100


def get_output_file_name(start, end, total_length):
    if end-start+1 == total_length:
        return 'output.txt'
    else:
        return 'output_{start}_{end}.txt'.format(start=start, end=end)


def write_elements(curr_file, content_buffer):
    file_content = ''.join(str(content_buffer[i]) + '\n' for i in range(len(content_buffer)))
    curr_file.write(file_content)


def read_element(curr_file, remaining_count):
    read_count = min(remaining_count, BUFFER_SIZE)
    content_buffer = []
    for i in range(read_count):
        line = curr_file.readline().strip()
        content_buffer.append(int(line))
    return content_buffer


def merge(left_partition, right_partition, output_file_name):

    output_file = open(output_file_name, 'a')
    left_file = open(left_partition[0], 'r')
    right_file = open(right_partition[0], 'r')

    left_remaining_count = left_partition[1]
    right_remaining_count = right_partition[1]

    left_buffer = []
    right_buffer = []
    content_buffer = []

    left_pos = 0
    right_pos = 0

    while left_remaining_count > 0 and right_remaining_count > 0:

        if left_pos == len(left_buffer):
            left_buffer = read_element(left_file, left_remaining_count)
            left_pos = 0

        if right_pos == len(right_buffer):
            right_buffer = read_element(right_file, right_remaining_count)
            right_pos = 0

        if left_buffer[left_pos] <= right_buffer[right_pos]:
            content_buffer.append(left_buffer[left_pos])
            left_remaining_count = left_remaining_count - 1
            left_pos = left_pos + 1
        else:
            content_buffer.append(right_buffer[right_pos])
            right_remaining_count = right_remaining_count - 1
            right_pos = right_pos + 1

        if len(content_buffer) == BUFFER_SIZE:
            write_elements(output_file, content_buffer)
            content_buffer = []

    while left_remaining_count > 0:

        if left_pos == len(left_buffer):
            left_buffer = read_element(left_file, left_remaining_count)
            left_pos = 0

        content_buffer.append(left_buffer[left_pos])
        left_remaining_count = left_remaining_count - 1
        left_pos = left_pos + 1

        if len(content_buffer) == BUFFER_SIZE:
            write_elements(output_file, content_buffer)
            content_buffer = []

    while right_remaining_count > 0:

        if right_pos == len(right_buffer):
            right_buffer = read_element(right_file, right_remaining_count)
            right_pos = 0

        content_buffer.append(right_buffer[right_pos])
        right_remaining_count = right_remaining_count - 1
        right_pos = right_pos + 1

        if len(content_buffer) == BUFFER_SIZE:
            write_elements(output_file, content_buffer)
            content_buffer = []

    if len(content_buffer) > 0:
        write_elements(output_file, content_buffer)
        content_buffer = []

    output_file.close()
    left_file.close()
    right_file.close()

    return output_file_name, left_partition[1] + right_partition[1]


def merge_sort(start, end, files_list):

    if start == end:

        curr_file = open(files_list[start], 'r+')
        file_strings = curr_file.readlines()
        curr_file.close()

        file_nums = [int(string_val.strip()) for string_val in file_strings ]
        file_nums.sort()
        sorted_file_content = ''.join([str(file_num) + '\n' for file_num in file_nums ])

        output_file_name = get_output_file_name(start, end, len(files_list))
        output_file = open(output_file_name, 'w+')
        output_file.write(sorted_file_content)
        output_file.close()

        return output_file_name, len(file_nums)

    else:

        mid = (start + end)//2
        output_file_name = get_output_file_name(start, end, len(files_list))

        left_partition = merge_sort(start, mid, files_list)
        right_partition = merge_sort(mid+1, end, files_list)
        combined_partition = merge(left_partition, right_partition, output_file_name)

        os.remove(left_partition[0])
        os.remove(right_partition[0])

        return combined_partition


files_list = ['./input/'+file_name for file_name in listdir('./input') ]
merge_sort(0, len(files_list)-1, files_list)
