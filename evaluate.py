import coco_text
import os, json, sys
import coco_evaluation
ct = coco_text.COCO_Text('../COCO_Text.json')
test_path = sys.argv[1]
dataDir='../train2014'
dataType='train2014'
test = []
print "test path: {}".format(test_path)
imgIds = []
for txt in os.listdir(test_path):
    if 'txt' in txt:
        im_id = int(txt.split('_')[-1].replace('.txt', ''))
        with open(os.path.join(test_path, txt)) as f:
            content = f.readlines()
        imgIds.append(im_id)
        for line in content:
            line = map(int, line.split(',')[:8])
            x_axis = [line[0], line[2], line[4], line[6]]
            y_axis = [line[1], line[3], line[5], line[7]]
            x_coord = min(x_axis)
            y_coord = min(y_axis)
            width = max(x_axis) - min(x_axis)
            height = max(y_axis) - min(y_axis)
            test.append({
                "image_id": im_id,
                "bbox": [x_coord, y_coord, width, height]
                })

print len(test)
os.system('touch results.json')
json.dump(test, open('results.json', 'w'))

our_results = ct.loadRes('results.json')
our_detections = coco_evaluation.getDetections(ct, our_results, imgIds=imgIds, detection_threshold=0.5)
print our_detections.keys()
print 'True positives have a ground truth id and an evaluation id: ', len(our_detections['true_positives'])
print 'False positives only have an evaluation id: ', len(our_detections['false_positives'])
print 'True negatives only have a ground truth id: ', len(our_detections['false_negatives'])
print "precision: {}".format(len(our_detections['true_positives']) / float(len(our_detections['true_positives']) + len(our_detections['false_positives'])))
print "recall: {}".format(len(our_detections['true_positives']) / float(len(our_detections['true_positives']) + len(our_detections['false_negatives'])))
