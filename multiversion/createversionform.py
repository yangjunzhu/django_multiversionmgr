from django import forms


class CreateVersionForm(forms.Form):
    software = forms.CharField()
    version = forms.CharField()

    def clean_software(self):
        software = self.clean_data.get('software', '')
        #if 0 >= software.length():
        if 1:
            raise forms.ValidationError("Not enough words!")
        return software
