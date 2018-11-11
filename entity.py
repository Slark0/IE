import copy


class Entity(object):

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

    class EntityMentionExtent(object):

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

    class EntityMentionHead(object):

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

    class EntityMention(object):

        def __init__(self):
            self.__id = None
            self.__type = None
            self.__role = None
            self.__extent = None
            self.__head = None

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

        @property
        def head(self):
            return self.__head

        @head.setter
        def head(self, value):
            self.__head = copy.deepcopy(value)

    def __init__(self):
        self.__id = None
        self.__type = None
        self.__subtype = None
        self.__class = None
        self.__entity_mention = []

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
    def ec1ass(self):
        return self.__class

    @ec1ass.setter
    def ec1ass(self, value):
        self.__class = value

    @property
    def entity_mention(self):
        return self.__entity_mention

    @entity_mention.setter
    def entity_mention(self, value):
        self.__entity_mention = copy.deepcopy(value)

    def __str__(self):
        return "entity:id:%s, type:%s, subtype:%s, class:%s\n entity_mention:%s" \
                % (self.__id, self.__type, self.__subtype, self.__class, self.__entity_mention)




