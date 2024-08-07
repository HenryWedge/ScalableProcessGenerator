import random as rd
from typing import List


class OutlierCategory:
    POINT_OUTLIER = "POINT_OUTLIER"
    CONTEXTUAL_OUTLIERS = "CONTEXTUAL_OUTLIERS"
    SUBSEQUENCE_OUTLIERS = "SUBSEQUENCE_OUTLIERS"


class BgColors:
    HEADER: str = '\033[95m'
    OKBLUE: str = '\033[94m'
    OKCYAN: str = '\033[96m'
    OKGREEN: str = '\033[92m'
    WARNING: str = '\033[93m'
    FAIL: str = '\033[91m'
    ENDC: str = '\033[0m'
    BOLD: str = '\033[1m'
    UNDERLINE: str = '\033[4m'


def print_color(message: str, color: str, end=None) -> None:
    if end is not None:
        print(f"{color}{message}{BgColors.ENDC}", end=end)
    else:
        print(f"{color}{message}{BgColors.ENDC}")


def fisher_yates_shuffle(lst: List[any], start=0, end=None):
    """
    Shuffle a portion of the given list using the Fisher-Yates algorithm.
    If `end` is not provided, shuffle from `start` to the end of the list.
    """
    if end is None:
        end = len(lst)
    for i in range(end - 1, start, -1):
        j = rd.randint(start, i)
        lst[i], lst[j] = lst[j], lst[i]
    return lst
