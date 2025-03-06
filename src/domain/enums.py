from enum import Enum


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    NOT_SPECIFIED = "Not Specified"


class Education(Enum):
    BACHELOR = "Bachelor"
    MASTER = "Master"
    COLLEGE = "College"
    MIDDLE_SCHOOL = "Middle School"
    PHD = "PhD"
    POSTGRADUATE = "Postgraduate"


class TinderPreference(Enum):
    LONG_TERM_PARTNER = "Long-term partner"
    LONG_OR_SHORT_TERM_1 = "Long or short-term"
    LONG_OR_SHORT_TERM_2 = "Long or short-term"
    JUST_FOR_FUN = "Just for fun"
    FIND_FRIENDS = "Find friends"
    STILL_DECIDING = "Still deciding"


class ZodiacSign(Enum):
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"


class ChildrenPreference(Enum):
    WANT = "Я хочу детей"
    DO_NOT_WANT = "Я не хочу детей"
    HAVE_AND_WANT_MORE = "У меня есть дети и хочу ещё"
    HAVE_AND_NOT_WANT_MORE = "У меня есть дети, но больше не хочу"
    UNDECIDED = "Пока не знаю"
