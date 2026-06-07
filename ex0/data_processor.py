#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_processor.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: fanilran <fanilran@student.42.fr>            +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/03 14:16:30 by fanilran            #+#    #+#            #
#   Updated: 2026/06/07 05:43:55 by fanilran           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self.storage: list[tuple[int, str]] = []
        self.rank = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        try:
            if not self.storage:
                raise IndexError("No data available")
            return self.storage.pop(0)
        except Exception as e:
            print(e)
            return (404, "[NOT FOUND] No data found")


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        elif isinstance(data, list) and all(isinstance(d, (int, float))
                                            for d in data):
            return True
        return False

    def ingest(self, data: Any) -> None:
        try:
            if not self.validate(data):
                raise Exception("Incorrect numerical data")
            elif isinstance(data, list):
                for d in data:
                    self.storage.append((self.rank, str(d)))
                    self.rank += 1
            else:
                self.storage.append((self.rank, str(data)))
                self.rank += 1
        except Exception as e:
            print(f"Got exception: {e}")


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        elif isinstance(data, list) and all(isinstance(d, str)
                                            for d in data):
            return True
        return False

    def ingest(self, data: Any) -> None:
        try:
            if not self.validate(data):
                raise Exception("Incorrect string data")
            elif isinstance(data, list):
                for d in data:
                    self.storage.append((self.rank, str(d)))
                    self.rank += 1
            else:
                self.storage.append((self.rank, str(data)))
                self.rank += 1
        except Exception as e:
            print(f"Got exception: {e}")


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def valid_dict(data: dict[str, str]) -> bool:
        return isinstance(data, dict) and all(
            (isinstance(k, str) and (k == "log_level" or k == "log_message"))
            and isinstance(v, str) for k, v in data.items()
        ) and len(data) == 2 and "log_level" in data and "log_message" in data

    @staticmethod
    def dict_to_str(data: dict[str, str]) -> str:
        return ': '.join(list(data.values()))

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return self.valid_dict(data)

        elif isinstance(data, list):
            return all(self.valid_dict(d) for d in data)

        return False

    def ingest(self, data: Any) -> Any:
        try:
            if not self.validate(data):
                raise Exception("Incorrect log data")

            elif isinstance(data, list):
                for d in data:
                    self.storage.append((self.rank, self.dict_to_str(d)))
                    self.rank += 1

            else:
                self.storage.append((self.rank, self.dict_to_str(data)))
                self.rank += 1
        except Exception as e:
            print(e)


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")
    print("==Test Numeric Processor...")
    num_proc = NumericProcessor()
    res = num_proc.validate(42)
    res1 = num_proc.validate("Hello")
    print(f"Trying to validate input '42': {res}")
    print(f"Trying to validate input 'Hello':{res1}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    num_proc.ingest("foo")

    test_num = [1, 2, 3, 4, 5]
    print(f"Processing data: {test_num}")
    print("Exctracting 3 values...")
    num_proc.ingest(test_num)
    if num_proc.validate(test_num):
        for _ in range(3):
            out = num_proc.output()
            print(f"Numeric value {out[0]} = {out[1]}")

    text_proc = TextProcessor()
    print("\n==Testing Text Processor...")
    res = text_proc.validate(42)
    print(f"Trying to validate input '42': {res}")
    test_text = ["Hello", "Nexus", "World"]
    print(f"Processing data: {test_text}")
    print("Extracting 1 value...")
    text_proc.ingest(test_text)

    if text_proc.validate(test_text):
        for _ in range(1):
            out = text_proc.output()
            print(f"Text value {out[0]}: {out[1]}")

    log_proc = LogProcessor()
    print("\n==Testing Log Processor...")

    test_log = [{'log_level': 'NOTICE', 'log_message': 'Connection to server'},
                {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}]

    print(f"Trying to validate input 'Hello': {log_proc.validate('Hello')}")
    print(f"Trying to validate a valid list {test_log} : "
          f"{log_proc.validate(test_log)}")
    print(f"Trying to validate an invalid list ['f', 072331, 'v']: "
          f"{log_proc.validate(['f', 072331, 'v'])}")
    print("Test invalid ingestion of int '072331' without prior validation:")
    log_proc.ingest(072331)

    print(f"Processing data: {test_log}")
    print("Extracting 2 value...")
    log_proc.ingest(test_log)
    if log_proc.validate(test_log):
        for _ in range(2):
            out = log_proc.output()
            print(f"Log value {out[0]} = {out[1]}")
