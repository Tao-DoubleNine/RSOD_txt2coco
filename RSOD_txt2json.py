import json
import os
from PIL import Image

if __name__ == '__main__':
    image_dir = ''
    anno_dir = ''
    json_save_path = ''
    class_id = {'aircraft': 1, 'oiltank': 2, 'overpass': 3, 'playground': 4}
    write_json_context = dict()  # 写入.json文件的大字典
    write_json_context['info'] = {'description': '', 'year': 2023, 'contributor': '',
                                  'date_created': '2023-02-06'}
    write_json_context['licenses'] = [{'id': None, 'name': None}]
    write_json_context['categories'] = [{"supercategory": "RSOD", "id": 1, "name": "aircraft"},
                                        {"supercategory": "RSOD", "id": 2, "name": "oiltank"},
                                        {"supercategory": "RSOD", "id": 3, "name": "overpass"},
                                        {"supercategory": "RSOD", "id": 4, "name": "playground"}]

    write_json_context['images'] = []
    write_json_context['annotations'] = []
    image_id_init = 0
    box_id = 0
    image_file_list = os.listdir(image_dir)
    for i, image_file in enumerate(image_file_list):
        image_path = os.path.join(image_dir, image_file)
        image = Image.open(image_path)
        w, h = image.size
        img_context = {'id': image_id_init + i, 'file_name': image_file, 'height': h, 'width': w}
        write_json_context['images'].append(img_context)

        txt_name = str(image_file.split('.')[0]) + '.txt'
        txt_file = os.path.join(anno_dir, txt_name)

        with open(txt_file) as f:
            lines = f.readlines()

        for j, line in enumerate(lines):
            img_name, class_name, xmin, ymin, xmax, ymax = line.strip().split()

            assert (int(xmax) > int(xmin)), "xmax <= xmin, {}".format(line)
            assert (int(ymax) > int(ymin)), "ymax <= ymin, {}".format(line)

            o_width = abs(int(xmax) - int(xmin))

            o_height = abs(int(ymax) - int(ymin))

            bbox_context = {}
            box_id += 1
            bbox_context['id'] = box_id
            
            bbox_context['image_id'] = image_id_init + i
            bbox_context['category_id'] = class_id[class_name]
            bbox_context['iscrowd'] = 0
            bbox_context['area'] = o_width * o_height
            bbox_context['bbox'] = [abs(int(xmin)), abs(int(ymin)), o_width, o_height]
            bbox_context['segmentation'] = []
            write_json_context['annotations'].append(bbox_context)
    name = os.path.join(json_save_path, 'instances_train2017.json')

    with open(name, 'w') as fw:
        json.dump(write_json_context, fw, indent=2)
