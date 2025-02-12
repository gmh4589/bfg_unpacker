
class Codec:

    @classmethod
    def codec_list(cls):
        return {key: value for key, value in cls.__dict__.items() if isinstance(value, int)}

    @classmethod
    def codec_indexes(cls):
        return {value: key for key, value in cls.__dict__.items() if isinstance(value, int)}

    @classmethod
    def codec_names(cls):
        return [sorted(key for key, value in cls.__dict__.items() if isinstance(value, int))]
