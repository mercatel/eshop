from django import forms

from analysis.models import RatingStar, RatingProduct


class Rating(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(),
        widget=forms.RadioSelect(),
        empty_label=None
    )

    class Meta:
        model = RatingProduct
        fields = ('star',)
