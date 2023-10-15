from typing import List, Callable
import re


def print_nested_dict(d: dict, indent_size: int = 0) -> None:
    """Print a nested dict.

    If a dict value is a dict, print the key and call the function recursively.
    Otherwise, print the key and the value.
    Indent increase by the depth of the recursion.

    Parameters
    ----------
    d : dict
        The nested dict
    indent_size : int, optional
        The indent size, by default 0

    Examples
    --------
    >>> test_dict = {
    ... "foo" : "fooo",
    ... "doink" : {"soo": "huyji"}
    ... }
    >>> print_nested_dict(test_dict)
    foo : fooo
    doink:
       soo : huyji
    """
    tab_value: str = "   "
    for key, value in d.items():
        if isinstance(value, dict):
            print(tab_value * indent_size + key + ": ")
            print_nested_dict(value, indent_size=indent_size + 1)

        else:
            print(tab_value * indent_size + key + " : " + str(value))


PATTERN_AVAILABLE_YEARS = r"(?<=/year=)\d+(?<!/)"
AVAILABALE_TIMES = ["year", "month", "day"]


def get_system_date_times(web_page: str, kind: str = "year") -> List[int]:
    """Get the available years for the data.

    Parameters
    ----------
    web_page : str
        The web page of S3 bucket.
    kind: str, optional
        The kind of data we want, by default "year".

    Returns
    -------
    List[int]
        The list of the retrieved times..

    Examples
    --------
    >>> get_system_date_times("foo/test/temps/year=20/sk")
    [20]
    """

    assert kind in AVAILABALE_TIMES, "The requested time must be in " + str(
        AVAILABALE_TIMES
    )
    pattern_available_time = rf"(?<=/{kind}=)\d+(?<!/)"

    available_times: List[str] = re.findall(pattern_available_time, web_page)
    available_times = [int(x) for x in available_times]
    return available_times


convert_date: Callable[[int], str] = lambda x: x if x >= 10 else "0" + str(x)
data_url_csv: Callable[
    [int, int, int, int], str
] = (
    lambda system_id, year, month, day: f"https://oedi-data-lake.s3.amazonaws.com/pvdaq/csv/pvdata/system_id={system_id}/year={year}/month={month}/day={day}/system_{system_id}__date_{year}_{convert_date(month)}_{convert_date(day)}.csv"
)
