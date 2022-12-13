import datetime
import warnings
import dateparser
import ipaddress
import random
from random import randint
from schwifty import IBAN
from email_validator import validate_email, EmailNotValidError

"""
Anon Helper/Callback methods to use in the change argument of the Anon-Clas 
"""


def ch_postal_code(postal_code: str, pc_len: int = 5, len_check: bool = True, change_last_n: int = 1,
                   change_with: str = "0") -> str:
    """
    Change helper/callback function to use in the change argument of the Anon-Class.

    Args:
        postal_code (str): postal code to process
        pc_len (int): length of the postal code.
            Defaults to 5
        len_check (bool): should the length of the postal code be checked?
            Defaults to True
        change_last_n (int):

        change_with (str):

    Returns:

    """
    # just opt out if None was provided
    if postal_code is None:
        return None

    change_last_n = abs(change_last_n)
    len_ok = True if not len_check else len(postal_code) == pc_len
    ret = postal_code
    if len_ok:
        try:
            ret = postal_code[:-change_last_n]
            # duplicate the "change_with" string * "change_last_n"-times to fill up the cut off characters
            ret = ret + ''.join(change_with * change_last_n)
        except:
            warnings.warn("An error occurred while processing the postalcode-string '" + postal_code +
                          "'. Please review the given parameters in combination with the given string and try again." +
                          "The initially given string will be returned")
    else:
        warnings.warn("The length check (len == " + str(pc_len) + ")  for the postalcode-string '" + postal_code +
                      "'. was not successful. The initially given string will be returned")
    return ret


def ch_datetime(date: object, return_unix_timestamp: bool = False,
                year_replace: int = None, month_replace: int = None, day_replace: int = None,
                hour_replace: int = None, minute_replace: int = None, second_replace: int = None,
                save_parse_mode: bool = True, save_parse_overwrite: str = "#ANONYMIZED_COULD_NOT_PARSE"):
    """
    Parses the given date/timestamp string or unix timestamp and replaces parts of the timestamp with the specified
    replace parameters for anonymization purpose.

    Args:
        date (str): date(time) represented as string.
            The function can even process human readable date strings like '21 July 2013' or '1 min ago'
            through the 'dateparser'-package (https://pypi.org/project/dateparser/)
        return_unix_timestamp (bool, optional): If true, a unix timestamp, seconds since epoch (1970) is returned
            Defaults to False,
        year_replace (int, optional): Value to replace the current year. 
            Has to be >= 1970 if 'return_unix_timestamp' == True, otherwise a random year is choosen between 1970:today().
            Defaults to None 
        month_replace (int, optional): Value to replace the current month.
            Defaults to None, 
        day_replace (int, optional): Value to replace the current day.
            Defaults to None,
        hour_replace (int, optional): Value to replace the current hour.
            Defaults to None
        minute_replace (int, optional): Value to replace the current minute.
            Defaults to None, 
        second_replace (int, optional): Value to replace the current second.
            Defaults to None
        save_parse_mode (bool, optional): If true and a date can not be parsed it get´s overwritten with 'save_parse_overwrite'
        save_parse_overwrite (str, optional): Overwrite-value if the parsing of a date fails and 'save_parse_mode' = True

    Returns:
        [datetime.datetime; int]
        if return_unix_timestamp is True:
            int
        else:
            datetime.datetime
    """

    # check if a number was supplied and convert it to a string
    try:
        date / 1
        date = str(date)
        wasNumber = True
    except:
        wasNumber = False

    # check if the year fits for a unix timestamp. If not, choose a random year between 1970 and todays year.
    if year_replace is not None and year_replace < 1970 and return_unix_timestamp:
        year_today = datetime.date.today().year
        year_replace = randint(1970, datetime.date.today().year)
        warnings.warn(
            "The parameter 'year_replace' can´t be smaller than 1970 for a unix timestamp." +
            "The random year " + str(year_replace) + " was choosen between 1970 and " + str(year_today))

    def early_return():
        # if save_parse_mode is True, overwrite the date value on error, else return it without modification
        if save_parse_mode:
            warnings.warn("The given date " + date if date else "" + " could not be parsed, the overwrite value " +
                          save_parse_overwrite + " will be returned.")
            ts = save_parse_overwrite
        else:
            warnings.warn("The given date " + date if date else "" + " could not be parsed, the original value is returned.")
            ts = date
        return ts

    # try to parse the date
    try:
        ts = dateparser.parse(date)
    except:
        return early_return()

    # just opt out if None was provided
    if ts is None:
        return early_return()

    # assing the own value of the timestamp to the replace params if none is provided
    year_replace = ts.year if year_replace is None else year_replace
    month_replace = ts.month if month_replace is None else month_replace
    day_replace = ts.day if day_replace is None else day_replace
    hour_replace = ts.hour if hour_replace is None else hour_replace
    minute_replace = ts.minute if minute_replace is None else minute_replace
    second_replace = ts.second if second_replace is None else second_replace

    # replace the given parts
    ts = ts.replace(year=year_replace, month=month_replace, day=day_replace,
                    hour=hour_replace, minute=minute_replace, second=second_replace)
    # Return a datetime-object or int(unix timestamp in millisenconds since epoch)
    ret = ts if not return_unix_timestamp else _unix_timestamp_epoch(ts)

    return ret


def ch_ipv4(ip: str, ip_check: bool = True, change_parts: list = [3], assign_rand_num: bool = True,
            change_with: str = "0") -> str:
    """
    Replaces parts - specified in "change_parts" - of an ip-address with the given "change_with" value
    :param ip: (str) ip adresse to parse/anonymize.
    :param ip_check: (bool, optional)
        Should this ip address be validated if it is really an ip?
        If the check is false the value will be returned without anonymization.
        Defaults to True.
    :param change_parts: (list, optional)
        Can contain values between 0 and 3, parts of the ip address to change.
        Defaults to [3].
    :param assign_rand_num: (bool, optional)
        If true, assignes a random number between 0 and 255 to the specified parts.
        Defaults to True.
    :param change_with: (str, optional)
        Change the under "change_parts" specified parts with this value if "assign_rand_num" = False.
        Defaults to 0.

    :return: (str
    """

    # check if it´s an valid ip adress
    if ip_check:
        try:
            # try to parse it
            ipaddress.ip_address(ip)
        except ValueError as ve:
            warnings.warn("The given ip adresse '" + ip if ip else "" + "' is not an valid ip. The original value will be returned")
            return ip

    ip_list: list = ip.split(".")

    for part in change_parts:
        # check if a valid part is specified
        if 0 <= part <= 3:
            # random number of replacement
            if assign_rand_num:
                replacement = random.randint(0, 255)
            else:
                replacement = change_with
            # try to replace it
            try:
                ip_list[part] = replacement
            except Exception as e:
                warnings.warn("The part '" + part + "' of the given ip '" + ip +
                              "' could not be replaced. Error: " + str(e))
        else:
            warnings.warn("The specified part " + str(part) + " is not valid. Valid are values between 0 - 3.")

    # concat the list of integers back together to the anon ip string
    ret = ".".join(str(x) for x in ip_list)

    return ret


def ch_iban(iban: str, overwrite_acccount: str = "0123456789") -> str:
    """
    Remove the account from the iban.
    Based on python library schwifty, currently only works with german IBANs.
    :param iban: iban code
        Gets validated. If not valid, returns the IBAN without anonymization.
    :param overwrite_acccount: (str, optional) Value to overwrite the account
        Defaults to 0123456789.
        Should be numeric and 10 digits long.
    :return: (str)
        anon iban.
    """
    # check the provided overwrite account
    if len(overwrite_acccount) != 10:
        warnings.warn("The provided overwrite_account should be of length 10 but is: " + str(len(overwrite_acccount)))
    if not overwrite_acccount.isdigit():
        warnings.warn("The provided overwrite_account should only consist of digits, but is: " + overwrite_acccount)

    # check if it´s an valid iban
    try:
        _iban = IBAN(iban)
    except ValueError as ve:
        warnings.warn("The iban '" + iban + "' is not valid. The original value will be returned.")
        return iban
    # bring together the parts of the iban
    anon_iban = _iban.country_code + _iban.checksum_digits + _iban.bank_code + overwrite_acccount
    return anon_iban


def ch_email(email: str, overwrite_local_part: str = "anonymized") -> str:
    """
    changes the local part of a valid e-mail adress to overwrite_local_part and returns it.
    :param email: email adress
    :param overwrite_local_part: overwrite value for the local part.
    (email: info@lv1871.de; info is the local part and @lv1871 is the domain)
    :return: (str)
        anonymized e-mail
    """
    try:
        valid_email = validate_email(email)
    except EmailNotValidError as e:
        warnings.warn("The provided e-mail '" + email + "' is not valid. The original value will be returned.")
        return email

    anon_email = overwrite_local_part + "@" + valid_email["domain"]
    return anon_email


def _unix_timestamp_epoch(dt: datetime.datetime) -> int:
    """
    Returns an unix timestamp in milliseconds since epoch format

    Args:
        dt (datetime.datetime): timestamp to process

    Returns:
        (int): Millisenconds since epoch.
    """
    return int(dt.timestamp())