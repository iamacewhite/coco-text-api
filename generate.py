import coco_text
import os
ct = coco_text.COCO_Text('../COCO_Text.json')

dataDir='../train2014'
dataType='train2014'
# get all images containing at least one instance of legible text
imgIds = ct.getImgIds(imgIds=ct.train)
# pick one at random
imgs = ct.loadImgs(imgIds)

for img in imgs:
    annIds = ct.getAnnIds(imgIds=img['id'])
    anns = ct.loadAnns(annIds)
    if not os.path.exists(os.path.join('..', 'gt', img['file_name'].split('.')[0]+'.txt')):
        with open(os.path.join('..', 'gt', img['file_name'].split('.')[0]+'.txt'), 'w+') as f:
            for ann in anns:
                if u'utf8_string' in ann:
                    text = ann[u'utf8_string']
                else:
                    text = '###'
                if ann['legibility'] == 'legible':
                    line= ','.join(map(str, ann['polygon'])) + ',' + text + '\n'
                    f.write(line.encode('utf-8'))


