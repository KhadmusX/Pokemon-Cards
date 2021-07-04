def object_to_dict(object_data):
    if (type(object_data).__name__ == 'list'):
        return_data = [f.__dict__ for f in object_data]
        for element in return_data:
            element.pop('_sa_instance_state', None)
    else:
        return_data = object_data.__dict__
        return_data.pop('_sa_instance_state', None)

    return return_data