import random
import re

MAC_PREFIXES = [
    '00:1A:79',  # Magnum Semiconductors Ltd (MAG box manufacturer) - Most common
    '00:2A:01',
    '00:1B:79',
    '00:2A:79',
    '00:A1:79',
    'D4:CF:F9',
    '33:44:CF',
    '10:27:BE',
    'A0:BB:3E',
    '55:93:EA',
    '04:D6:AA',
    '11:33:01',
    '00:1C:19',
    '1A:00:6A',
    '1A:00:FB'
]

MAC_REGEX = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
MAC_EXTRACT_REGEX = re.compile(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})')

class MacGenerator:
    @staticmethod
    def normalize_mac(mac: str) -> str:
        mac = mac.upper().replace('-', ':')
        return re.sub(r'[^0-9A-F:]', '', mac)

    @staticmethod
    def normalize_prefix(prefix: str) -> str:
        normalized = prefix.upper().replace('-', ':')
        parts = normalized.split(':')
        if len(parts) != 3 or not all(re.match(r'^[0-9A-F]{2}$', p) for p in parts):
            raise ValueError(f"Invalid MAC prefix: {prefix}. Expected format: XX:XX:XX")
        return normalized

    @staticmethod
    def is_valid_mac(mac: str) -> bool:
        return bool(MAC_REGEX.match(mac))

    @staticmethod
    def mac_to_number(mac: str) -> int:
        normalized = MacGenerator.normalize_mac(mac)
        parts = normalized.split(':')
        if len(parts) != 6:
            raise ValueError(f"Invalid MAC address: {mac}")
        
        result = 0
        for part in parts:
            result = result * 256 + int(part, 16)
        return result

    @staticmethod
    def number_to_mac(num: int) -> str:
        parts = []
        for i in range(5, -1, -1):
            byte = (num >> (i * 8)) & 0xFF
            parts.append(f"{byte:02X}")
        return ':'.join(parts)

    @staticmethod
    def generate_random_mac(prefix: str = '00:1A:79') -> str:
        normalized_prefix = MacGenerator.normalize_prefix(prefix)
        suffix = ':'.join(f"{random.randint(0, 255):02X}" for _ in range(3))
        return f"{normalized_prefix}:{suffix}"

    @staticmethod
    def generate_random(prefix: str = '00:1A:79', count: int = 1) -> list:
        normalized_prefix = MacGenerator.normalize_prefix(prefix)
        generated = set()
        attempts = 0
        max_attempts = count * 10
        
        while len(generated) < count and attempts < max_attempts:
            attempts += 1
            mac = MacGenerator.generate_random_mac(normalized_prefix)
            generated.add(mac)
            
        return list(generated)

    @staticmethod
    def generate_sequential(start: str, end: str) -> list:
        start_num = MacGenerator.mac_to_number(start)
        end_num = MacGenerator.mac_to_number(end)

        if start_num > end_num:
            raise ValueError("Start MAC must be less than or equal to end MAC")

        max_range = 1000000
        range_size = end_num - start_num + 1

        if range_size > max_range:
            raise ValueError(f"Range too large: {range_size} MACs. Maximum allowed: {max_range}")

        return [MacGenerator.number_to_mac(i) for i in range(start_num, end_num + 1)]

    @staticmethod
    def parse_imported_macs(input_text: str) -> list:
        macs = set()
        # Split by newlines, commas, semicolons
        lines = re.split(r'[\n,;]+', input_text)
        
        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue
                
            match = MAC_EXTRACT_REGEX.search(trimmed)
            if match:
                mac = match.group(0)
                if MacGenerator.is_valid_mac(mac):
                    macs.add(MacGenerator.normalize_mac(mac))
                    
        return list(macs)

    @staticmethod
    def get_default_prefixes() -> list:
        prefix_info = {
            '00:1A:79': 'Magnum Semiconductors Ltd (MAG boxes)',
            '00:2A:01': 'STB Device',
            '00:1B:79': 'Magnum Semiconductors Ltd',
            '00:2A:79': 'STB Device',
            '00:A1:79': 'STB Device',
            'D4:CF:F9': 'STB Device',
            '10:27:BE': 'STB Device',
            'A0:BB:3E': 'STB Device',
            '04:D6:AA': 'STB Device',
            '00:1C:19': 'STB Device'
        }
        
        return [{"prefix": p, "name": prefix_info.get(p, "STB Device")} for p in MAC_PREFIXES]
