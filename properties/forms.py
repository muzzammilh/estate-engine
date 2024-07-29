from django import forms

from .models import City, Country, Property, State, SubLocality, Unit


class PropertyForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select Country")
    state = forms.ModelChoiceField(queryset=State.objects.none(), empty_label="Select State")
    city = forms.ModelChoiceField(queryset=City.objects.none(), empty_label="Select City")
    sub_locality = forms.ModelChoiceField(queryset=SubLocality.objects.none(), empty_label="Select Sub Locality", required=False)

    class Meta:
        model = Property
        fields = ['name', 'country', 'state', 'city', 'sub_locality', 'address', 'square_feet', 'description', 'currency']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['state'].queryset = self.instance.country.states.order_by('name')

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.cities.order_by('name')

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['sub_locality'].queryset = SubLocality.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['sub_locality'].queryset = self.instance.city.sub_localities.order_by('name')


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'unit_number',
            'description',
            'num_beds',
            'num_bathrooms',
            'num_kitchens',
            'num_living_rooms',
            'num_stores',
            'is_available_for_rent',
            'rent_per_month'
        ]


class TenantUnitFilterForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, empty_label="All Countries")
    state = forms.ModelChoiceField(queryset=State.objects.none(), required=False, empty_label="All States")
    city = forms.ModelChoiceField(queryset=City.objects.none(), required=False, empty_label="All Cities")
    sub_locality = forms.ModelChoiceField(queryset=SubLocality.objects.none(), required=False, empty_label="All Sub Localities")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['state'].queryset = State.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['sub_locality'].queryset = SubLocality.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass


class TableUnitFilterForm(forms.Form):
    property = forms.ModelChoiceField(queryset=Property.objects.all(), required=False, empty_label="All Properties")
    unit = forms.ModelChoiceField(queryset=Unit.objects.none(), required=False, empty_label="All Units")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TableUnitFilterForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['property'].queryset = Property.objects.filter(owner=user)

        if 'property' in self.data:
            try:
                property_id = int(self.data.get('property'))
                units = Unit.objects.filter(property_id=property_id)
                self.fields['unit'].queryset = units
                self.fields['unit'].choices = [("", "All Units")] + [(unit.id, unit.unit_number) for unit in units]
            except (ValueError, TypeError):
                pass
