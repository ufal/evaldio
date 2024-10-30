from statistics import mean, median
import sys

for line in sys.stdin:
    line = line.rstrip()
    file_id, *rest = line.split("\t")
    if not rest:
        print(line)
        continue
    time_range_annots = [tuple([float(time) for time in time_range.split("-")]) for time_range in rest[0].split(" ")]
    # the split for an annotation is an average between the boundaries of the range
    time_split_annots = [mean(time_range) for time_range in time_range_annots]
    # the final split is a median of the splits over all annotations
    time_split = median(time_split_annots)
    print("\t".join([file_id, f"{time_split:.2f}"]))


