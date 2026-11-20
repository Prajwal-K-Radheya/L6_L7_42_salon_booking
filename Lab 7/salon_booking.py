import math


def parse_booking(text):
    """Parse 'service:minutes' -> (Service, float). Raises ValueError on bad input."""
    if not isinstance(text, str):
        raise ValueError("input must be a string")
    parts = text.split(':')
    if len(parts) != 2:
        raise ValueError("expected format service:minutes")
    service, minutes = parts
    service = service.strip()
    if not service:
        raise ValueError("service name is empty")
    try:
        value = float(minutes)
    except ValueError:
        raise ValueError("minutes must be a number")
    if not math.isfinite(value) or value < 0:
        raise ValueError("minutes must be a finite non-negative number")
    return service.title(), value


def duration_average(durations_csv):
    """Average (integer floor) of comma separated durations. Raises ValueError on bad input."""
    if not isinstance(durations_csv, str):
        raise ValueError("input must be a string")
    try:
        values = [int(r) for r in durations_csv.split(',')]
    except ValueError:
        raise ValueError("durations must be integers separated by commas")
    if not values:
        raise ValueError("no durations given")
    return sum(values) // len(values)


def payable_bill(text):
    """Parse 'bill|discount' -> payable amount incl. 18% tax. Raises ValueError on bad input."""
    if not isinstance(text, str):
        raise ValueError("input must be a string")
    parts = text.split('|')
    if len(parts) != 2:
        raise ValueError("expected format bill|discount")
    try:
        bill, discount = float(parts[0]), float(parts[1])
    except ValueError:
        raise ValueError("bill and discount must be numbers")
    if not (math.isfinite(bill) and math.isfinite(discount)):
        raise ValueError("bill and discount must be finite")
    total = bill * 1.18 - discount
    if not math.isfinite(total):
        raise ValueError("amount out of range")
    return max(total, 0)
def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter service:duration in min (e.g. haircut:45): ")
    result = parse_booking(user_input)
    print("Service and Duration:", result)

    print("\n==== Running duration_average ====")
    user_input = input("Enter durations as CSV (e.g. 30,45,60): ")
    result = duration_average(user_input)
    print("Average Duration:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 800|100): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result)

if __name__ == "__main__":
    main()
