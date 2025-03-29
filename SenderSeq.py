class __SenderSeq:
    def __init__(self):
        self.__seq_num = 0

    def increment(self) -> bytes:
        self.__seq_num = (self.__seq_num + 1) % 256
        return self.__seq_num.to_bytes(1, "big")

    def get_seq_num(self) -> bytes:
        return self.__seq_num.to_bytes(1, "big")

    def get_and_then_increment(self) -> bytes:
        current_seq = self.__seq_num
        self.increment()
        return current_seq.to_bytes(1, "big")

SenderSeq = __SenderSeq()