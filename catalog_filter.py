# This code will remove the entries correspoding to the bad images obtained from image_filter.py

import os
import json
img_path = './raw/data/images/bad'
catalog_path = './raw/data'

''' Example of an entry in catalog file
{"_index": 999, "_session_id": "22-08-13_0", "_timestamp_ms": 1660396688209,
"cam/image_array": "999_cam_image_array_.jpg",
"user/angle": -0.8926728650143272, "user/mode": "user", "user/throttle": 0.65}
'''

cat_list = []

# form a list of indexes of the bad images
for file in os.scandir(img_path):
    index = file.name.split('_')[0]
    if(index == '.DS'):  # skip the last line
        continue
    index = int(index)
    cat_list.append(index)

cat_list.sort()
l = len(cat_list)
i = 0
cat_no = 0
    
while i < l:
    path = f'./raw/data/catalog_{cat_no}.catalog'
    with open(path, 'r') as file:
        data = file.readlines()
        remove = []
        print(len(data))
        while i < l and cat_list[i] // 1000 == cat_no:
            print(i, cat_list[i])
            entry = data[cat_list[i] % 1000]
            # add to waitlist to remove
            remove.append(entry)
            #next entry
            i += 1
        # removing bad entries
        for rmv_entry in rmv:
            data.remove(rmv_entry)
            
    file.close()
    with open(path, 'w') as file:
        file.writelines(data)
    file.close()
            
    if i >= l:
        break

    # Finding the correct catalog file, 1000 entries per file
    cat_no = cat_list[i] // 1000
