def get_list_from_set(set_data):
    created_list = []
    for set_object in set_data:
        created_list.append(list(set_object)[1])
    return created_list

def get_data_dict(request, fields):
    task_dict = {}
    for field in fields:
        task_dict[field] = request.POST.get(field, None)
    print task_dict    
    return task_dict    