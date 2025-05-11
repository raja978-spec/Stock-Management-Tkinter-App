from tkinter.font import Font

def CustomFontStyle(font_family="Helvetica", font_size=25,
                    weight='normal'):
    font_style = Font(family=font_family, size=font_size,
                      weight=weight)
    return font_style

background_color = '#cff6f6'