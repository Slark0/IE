import copy


class Event(object):

    class EventArgument(object):

        def __init__(self):
            self.__refid = None
            self.__role = None

        @property
        def refid(self):
            return self.__refid

        @refid.setter
        def refid(self, value):
            self.__refid = value

        @property
        def role(self):
            return self.__role

        @role.setter
        def role(self, value):
            self.__role = value

    class CharSeq(object):
        def __init__(self):
            self.__start = None
            self.__end = None

        @property
        def start(self):
            return self.__start

        @start.setter
        def start(self, value):
            self.__start = value

        @property
        def end(self):
            return self.__end

        @end.setter
        def end(self, value):
            self.__end = value

        def __str__(self):
            return "charseq : start:%s, end:%s" % (self.__start, self.__end)

    class EventMentionExtent(object):

        def __init__(self):
            self.__charseq = None
            self.__value = None

        @property
        def charseq(self):
            return self.__charseq

        @charseq.setter
        def charseq(self, value):
            self.__charseq = copy.deepcopy(value)

        @property
        def value(self):
            return self.__value

        @value.setter
        def value(self, value):
            self.__value = value

        def __str__(self):
            return "extent:%s, value:%s" % (self.__charseq, self.__value)

    class EventMentionLdcScope(object):

        def __init__(self):
            self.__charseq = None
            self.__value = None

        @property
        def charseq(self):
            return self.__charseq

        @charseq.setter
        def charseq(self, value):
            self.__charseq = value

        @property
        def value(self):
            return self.__value

        @value.setter
        def value(self, value):
            self.__value = value

    class EventMentionAnchor(object):

        def __init__(self):
            self.__charseq = None
            self.__value = None

        @property
        def charseq(self):
            return self.__charseq

        @charseq.setter
        def charseq(self, value):
            self.__charseq = value

        @property
        def value(self):
            return self.__value

        @value.setter
        def value(self, value):
            self.__value = value

    class EventMentionArgument(object):

        def __init__(self):
            self.__refid = None
            self.__role = None
            self.__extent = None

        @property
        def refid(self):
            return self.__refid

        @refid.setter
        def refid(self, value):
            self.__refid = value

        @property
        def role(self):
            return self.__role

        @role.setter
        def role(self, value):
            self.__role = value

        @property
        def extent(self):
            return self.__extent

        @extent.setter
        def extent(self, value):
            self.__extent = copy.deepcopy(value)

    def __init__(self):
        self.__id = None
        self.__type = None
        self.__subtype = None
        self.__modality = None
        self.__polarity = None
        self.__genericity = None
        self.__tense = None
        self.__event_argument_list = []
        self.__event_mention_list = []

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def subtype(self):
        return self.__subtype

    @subtype.setter
    def subtype(self, value):
        self.__subtype = value

    @property
    def modality(self):
        return self.__modality

    @modality.setter
    def modality(self, value):
        self.__modality = value

    @property
    def polarity(self):
        return self.__polarity

    @polarity.setter
    def polarity(self, value):
        self.__polarity = value

    @property
    def genericity(self):
        return self.__genericity

    @genericity.setter
    def genericity(self, value):
        self.__genericity = value

    @property
    def tense(self):
        return self.__tense

    @tense.setter
    def tense(self, value):
        self.__tense = value

    @property
    def event_argument_list(self):
        return self.__event_argument_list

    @event_argument_list.setter
    def event_argument_list(self, value):
        self.__event_argument_list.extend(value)

    @property
    def event_mention_list(self):
        return self.__event_mention_list

    @event_mention_list.setter
    def event_mention_list(self, value):
        self.__event_mention_list.extend(value)









