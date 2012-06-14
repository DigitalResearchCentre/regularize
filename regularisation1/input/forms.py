from django import forms
# import django_tables2 as tables

REGULARIZATION_CHOICES = (
    ('all_places', 'All witnesses, all places'),
    ('this_block', 'All witnesses, this block'),
    ('this_word', 'All witnesses, this word'),
    ('other', 'Other ...'),
)

class WitnessInputForm(forms.Form):
    witness_a = forms.CharField(label = 'Witness A',\
                                initial='The black cat',\
        widget=forms.TextInput(attrs={'size':'100'}))
    witness_b = forms.CharField(label = 'Witness B',\
                                initial='The black and white cat',\
        widget=forms.TextInput(attrs={'size':'100'}))
    witness_c = forms.CharField(label = 'Witness C',\
                                initial='The black and green cat',\
        widget=forms.TextInput(attrs={'size':'100'}))
    witness_d = forms.CharField(label = 'Witness D',\
                                initial='The black very special cat',\
        widget=forms.TextInput(attrs={'size':'100'}))
    witness_e = forms.CharField(label = 'Witness E',\
                                initial='The black not very special cat',\
        widget=forms.TextInput(attrs={'size':'100'}))
        
class RegularizationForm(forms.Form):
    reg_area = forms.CharField(\
                                widget=forms.TextInput(attrs={'size':'100',\
                                    'onclick': "determineClick();",}),\
                                    #'ondblclick': "selectToken();",}),\
                                    #'onclick': "selectNew();",}),\
                                required=False,\
                                label = 'Collation')
                                #w idget=forms.Select(attrs = {'onclick': "alert('foo !');",}))
    reg_this = forms.CharField(\
                                widget=forms.TextInput(attrs={'size':'100'}),\
                                required=False,\
                                label = 'Regularize This')
    reg_to = forms.CharField(\
                                widget=forms.TextInput(attrs={'size':'100'}),\
                                required=False,\
                                label = 'To This')
    reg_choices = forms.ChoiceField(choices=REGULARIZATION_CHOICES,\
                            required=False)

# class ContactForm(forms.Form):
#     # regularization_choices = forms.ChoiceField(choices=REGULARISATION_CHOICES)
#     cc_myself = forms.BooleanField(required=False)
#     # # message = forms.CharField() <--- only a single line
#     # message = forms.CharField(widget=forms.Textarea(), initial="Replace with your feedback")
#     # sender = forms.EmailField(required=False)

    
