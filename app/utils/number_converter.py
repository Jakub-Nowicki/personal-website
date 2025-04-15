def convert_to_decimal(number_str, base):
    """
    Convert a number from a given base to decimal.

    Args:
        number_str (str): The number to convert as a string
        base (int): The base of the input number (2-16)

    Returns:
        str: The decimal representation of the number

    Raises:
        ValueError: If the input contains invalid digits for the given base
    """
    if not 2 <= base <= 16:
        raise ValueError(f"Base must be between 2 and 16, got {base}")

    # Handle empty input
    if not number_str:
        return ""

    # Handle negative numbers
    is_negative = number_str.startswith('-')
    if is_negative:
        number_str = number_str[1:]

    # Handle decimal points
    if '.' in number_str:
        integer_part, fractional_part = number_str.split('.')
    else:
        integer_part, fractional_part = number_str, ""

    # Validate each digit
    valid_digits = "0123456789ABCDEF"[:base]
    for digit in integer_part.upper() + fractional_part.upper():
        if digit not in valid_digits:
            raise ValueError(f"Invalid digit '{digit}' for base {base}")

    # Convert integer part
    decimal_value = 0
    for digit in integer_part.upper():
        decimal_value = decimal_value * base + valid_digits.index(digit)

    # Convert fractional part if present
    if fractional_part:
        fraction_value = 0
        power = base
        for digit in fractional_part.upper():
            fraction_value += valid_digits.index(digit) / power
            power *= base
        decimal_value += fraction_value

    # Apply sign if negative
    if is_negative:
        decimal_value = -decimal_value

    # Format result based on whether it's an integer or has fractional part
    if fractional_part:
        return str(decimal_value)
    else:
        return str(int(decimal_value))


def convert_from_decimal(decimal_str, base):
    """
    Convert a decimal number to the specified base.

    Args:
        decimal_str (str): The decimal number to convert as a string
        base (int): The target base (2-16)

    Returns:
        str: The number represented in the target base

    Raises:
        ValueError: If the input is not a valid decimal number or base is invalid
    """
    if not 2 <= base <= 16:
        raise ValueError(f"Base must be between 2 and 16, got {base}")

    # Handle empty input
    if not decimal_str:
        return ""

    # Handle negative numbers
    is_negative = decimal_str.startswith('-')
    if is_negative:
        decimal_str = decimal_str[1:]

    # Handle decimal points
    if '.' in decimal_str:
        integer_part, fractional_part = decimal_str.split('.')
    else:
        integer_part, fractional_part = decimal_str, ""

    try:
        # Convert integer part
        integer_value = int(integer_part)
        digits = "0123456789ABCDEF"

        # Handle zero case
        if integer_value == 0:
            result = "0"
        else:
            result = ""
            while integer_value > 0:
                result = digits[integer_value % base] + result
                integer_value //= base

        # Convert fractional part if present
        if fractional_part:
            fractional_value = float("0." + fractional_part)
            if fractional_value > 0:
                result += "."
                # Limit precision to avoid infinite loops
                precision = 10
                for _ in range(precision):
                    fractional_value *= base
                    digit = int(fractional_value)
                    result += digits[digit]
                    fractional_value -= digit
                    if fractional_value == 0:
                        break

        # Apply sign if negative
        if is_negative:
            result = "-" + result

        return result

    except ValueError:
        raise ValueError(f"Invalid decimal number: {decimal_str}")


def convert_between_bases(number_str, from_base, to_base):
    # Validate bases
    if not 2 <= from_base <= 16:
        raise ValueError(f"Source base must be between 2 and 16, got {from_base}")
    if not 2 <= to_base <= 16:
        raise ValueError(f"Target base must be between 2 and 16, got {to_base}")

    # Handle special case: same base
    if from_base == to_base:
        # Still validate the input
        valid_digits = "0123456789ABCDEF"[:from_base]
        clean_number = number_str.upper().replace('-', '').replace('.', '')
        for digit in clean_number:
            if digit not in valid_digits:
                raise ValueError(f"Invalid digit '{digit}' for base {from_base}")
        return number_str

    # First convert to decimal
    decimal = convert_to_decimal(number_str, from_base)

    # Then convert to target base
    return convert_from_decimal(decimal, to_base)