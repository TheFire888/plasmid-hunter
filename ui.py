from config import *

class Text:
    FONT = "pixeled"
    SIZE = 10
    COLOR = "white"

    @staticmethod
    def draw(screen, content, **kwargs):
        if "fontname" not in kwargs: kwargs["fontname"] = Text.FONT
        if "fontsize" not in kwargs: kwargs["fontsize"] = Text.SIZE
        if "color" not in kwargs: kwargs["color"] = Text.COLOR
        screen.draw.text(str(content), **kwargs)

    @staticmethod
    def draw_textbox(screen, content, rect, **kwargs):
        if "fontname" not in kwargs: kwargs["fontname"] = Text.FONT
        if "color" not in kwargs: kwargs["color"] = Text.COLOR
        screen.draw.textbox(str(content), rect, **kwargs)
