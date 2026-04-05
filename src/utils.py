from typing import List, Optional
from src.aeroplane import Aeroplane


def filter_aeroplanes_by_country(aeroplanes: List[Aeroplane], country: str) -> List[Aeroplane]:
    """Фильтрация самолетов по стране регистрации"""
    if not country:
        return aeroplanes
    country_lower = country.lower()
    return [a for a in aeroplanes if a.origin_country.lower() == country_lower]


def filter_aeroplanes_by_altitude(aeroplanes: List[Aeroplane],
                                  min_altitude: Optional[float] = None,
                                  max_altitude: Optional[float] = None) -> List[Aeroplane]:
    """Фильтрация самолетов по диапазону высот"""
    result = aeroplanes

    if min_altitude is not None:
        result = [a for a in result if a.altitude is not None and a.altitude >= min_altitude]

    if max_altitude is not None:
        result = [a for a in result if a.altitude is not None and a.altitude <= max_altitude]

    return result


def sort_aeroplanes_by_altitude(aeroplanes: List[Aeroplane], reverse: bool = False) -> List[Aeroplane]:
    """Сортировка самолетов по высоте"""
    # Фильтруем самолеты с неизвестной высотой в конец
    with_altitude = [a for a in aeroplanes if a.altitude is not None]
    without_altitude = [a for a in aeroplanes if a.altitude is None]

    with_altitude.sort(reverse=reverse)

    if reverse:
        return with_altitude + without_altitude
    else:
        return without_altitude + with_altitude


def get_top_aeroplanes(aeroplanes: List[Aeroplane], top_n: int) -> List[Aeroplane]:
    """Получение топ N самолетов"""
    return aeroplanes[:top_n]


def parse_altitude_range(altitude_range: str) -> tuple:
    """Парсинг диапазона высот из строки вида '10000-20000'"""
    try:
        parts = altitude_range.split('-')
        if len(parts) == 2:
            min_alt = float(parts[0].strip())
            max_alt = float(parts[1].strip())
            return min_alt, max_alt
        elif len(parts) == 1:
            alt = float(parts[0].strip())
            return alt, alt
    except (ValueError, AttributeError):
        pass
    return None, None


def print_aeroplanes(aeroplanes: List[Aeroplane]) -> None:
    """Вывод информации о самолетах в консоль"""
    if not aeroplanes:
        print("✈️ Самолеты не найдены")
        return

    print(f"\n{'=' * 60}")
    print(f"📊 Найдено самолетов: {len(aeroplanes)}")
    print(f"{'=' * 60}\n")

    for i, aeroplane in enumerate(aeroplanes, 1):
        print(f"{i}. {aeroplane}")

    print(f"\n{'=' * 60}")
