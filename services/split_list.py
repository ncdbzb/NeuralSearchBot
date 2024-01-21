def split_list(input_list: list, max_elements: int) -> list[list]:
    result = []
    current_sublist = []

    for item in input_list:
        current_sublist.append(item)

        if len(current_sublist) == max_elements:
            result.append(current_sublist)
            current_sublist = []

    if current_sublist:
        result.append(current_sublist)

    return result
