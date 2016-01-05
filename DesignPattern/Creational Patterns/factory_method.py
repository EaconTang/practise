# coding=utf-8
"""
delegate a specialized function/method to create instances

http://ginstrom.com/scribbles/2007/10/08/design-patterns-python-style/

We don't need our factory products to have a common base class in order to give them a common type,
but we can if we want to in order to share functionality.

In this example, we have a factory function called get_localizer,
which returns the appropriate localizer class depending on the language name we pass to it.
"""

class EnToCh:
    def __init__(self):
        self.dictionary = dict(dog='狗',cat='猫',pig='猪')

    def translate(self, word):
        try:
            return self.dictionary[word]
        except KeyError:
            print 'Translator do not know!'


class ChToEn:
    def __init__(self):
        self.dictionary = {
            '狗': 'dog',
            '猫': 'cat',
            '猪': 'pig'
        }

    def translate(self,word):
        try:
            return self.dictionary[word]
        except KeyError:
            print 'Translator do not know!'


def get_localizer(language):
    translator = {
        'english': ChToEn,
        'chinese': EnToCh
    }
    try:
        return translator[language.lower()]()
    except KeyError:
        print 'Language not support!'


if __name__ == '__main__':
    ch = get_localizer('Chinese')
    en = get_localizer('english')
    jp = get_localizer('JApanese')
    print ch.translate('pig')
    print en.translate('猪')
