from django import forms

class ChooseTextForm(forms.Form):
    def __init__(self, *args, **kwargs):
        chapter = kwargs.pop('chapter')
        verse = kwargs.pop('verse')
        init = kwargs.pop('initial')
        # print verse
        super(ChooseTextForm, self).__init__(*args, **kwargs)
        if init == "":
            self.fields['chapter_choices'] = forms.ChoiceField(choices=chapter,\
                                                           label = 'Chapter',\
                    widget=forms.Select(attrs={'onchange': "findVerse();"}))
        if verse != "":
            self.fields['chapter_choices'] = forms.ChoiceField(choices=chapter,\
                                                           label = 'Chapter',\
                    widget=forms.Select(attrs={'onchange': "findVerse();"}),\
                    initial = init)
            self.fields['verse_choices'] = forms.ChoiceField(choices=verse,\
                                                             label = 'Verse',\
                widget=forms.Select(attrs={'onchange': "showSubmit();"}))
