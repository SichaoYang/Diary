#!/usr/bin/env python3
from log_processing_utils import process_log
from glob import glob
from os import path

if __name__ == '__main__':
    # The last raw log may have been updated after the last aggregation, so it should be aggregated again.
    start_date: int = int(path.splitext(path.basename(glob("../logs/*.txt")[-1]))[0])
    end_date: int = int(path.splitext(path.basename(glob("../logs/raw/*.csv")[-1]))[0])
    for date in range(start_date, end_date + 1):
        process_log(date)
