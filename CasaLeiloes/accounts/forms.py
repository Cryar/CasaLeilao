from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Client, Leiloes
from django import forms
from django.contrib.postgres.fields import ArrayField
from multiupload.fields import MultiFileField

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

            # Create the corresponding Client instance
            client = Client(user=user.id, username=user.username, password=user.password)
            client.save(using='mongodb')  # Save to MongoDB database
        return user

class LoginForm(AuthenticationForm):
    # No need to define fields as they are inherited from AuthenticationForm
    pass

class AddItemForm(forms.Form):
    item_name = forms.CharField(label='Item Name', max_length=100)
    item_description = forms.CharField(label='Item Description', widget=forms.Textarea)
    item_images = MultiFileField(label='Item Images')
    item_lot = forms.IntegerField(label='item_lot', required= False)
    
class AlterProduto(forms.Form):
    new_name = forms.CharField(
        label='New Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required= False
    )
    new_description = forms.CharField(
        label='New Description',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required= False
    )
    new_image = MultiFileField(
        label='New Image',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        required= False
    )
    new_lot = forms.IntegerField(
        label='New Lot',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required= False
    )
    deleted_image = MultiFileField(
       label='deleted_image',
       widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control-file'}), 
       required= False
    )
    

class LeiloesForm(forms.ModelForm):
    class Meta:
        model = Leiloes
        fields = '__all__'


class BidForm(forms.Form):
    bid_amount = forms.DecimalField(max_digits=10, decimal_places=2)