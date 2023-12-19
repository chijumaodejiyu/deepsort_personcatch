def list_bboxes2dict_bboxes(list_bboxes: list) -> dict:
    """
    将list_bboxes转化为{id:(x1, y1, x2, y2),...}格式的字典
    """
    dict_bboxes = {}

    for item_bbox in list_bboxes:
        x1, y1, x2, y2, lbl, id_ = item_bbox
        dict_bboxes[str(id)] = (x1, y1, x2, y2, lbl, id_)
    return dict_bboxes
