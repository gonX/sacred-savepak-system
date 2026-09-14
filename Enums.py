from enum import Enum

class SacredSaveStruct2Enum(Enum):
    NULL = 0
    ENGINE = 128
    TRIGGERS = 129
    VIEWS = 130
    DESCRIPTOR = 131
    CALENDAR = 139
    INVENTORY = 141
    ITEMS_U = 142 # uncompressed, probably never seen in a finished file
    QUEST_U = 145 # uncompressed
    WEATHER = 146
    PICTURE = 147
    BLOOD = 148
    GENERIC = 149
    PARTICLES = 150 # uncompressed
    MOUSE = 152
    REGIONS = 153
    TEAM = 154
    STATS = 155
    UNK_0x9c = 156 # always 40 value
    UNK_0x9d = 157 # always 0x400 value (all 0 bytes?)
    ITEMS_C = 160 # compressed
    QUEST_C = 161 # compressed
    PARTICLES_C = 162 # compressed
    ENDING_likely = 195 # value 0 if no hero data, and always at end?

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return self.__repr__()
