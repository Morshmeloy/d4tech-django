"""Forms for the core application."""
from django import forms

INPUT_CSS = (
    "border-input placeholder:text-muted-foreground flex h-9 w-full min-w-0"
    " rounded-md border bg-transparent px-3 py-1 text-base shadow-xs"
    " transition-[color,box-shadow] outline-none focus-visible:border-ring"
    " focus-visible:ring-ring/50 focus-visible:ring-[3px] md:text-sm"
)
TEXTAREA_CSS = (
    "border-input placeholder:text-muted-foreground focus-visible:border-ring"
    " focus-visible:ring-ring/50 flex min-h-16 w-full rounded-md border"
    " bg-transparent px-3 py-2 text-base shadow-xs"
    " transition-[color,box-shadow] outline-none focus-visible:ring-[3px]"
    " md:text-sm"
)


class ContactForm(forms.Form):
    """Contact form with validation."""

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Иван Иванов",
            "class": INPUT_CSS,
            "id": "name",
        }),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "ivan@example.com",
            "class": INPUT_CSS,
            "id": "email",
        }),
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "placeholder": "Тема вашего сообщения",
            "class": INPUT_CSS,
            "id": "subject",
        }),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Введите ваше сообщение здесь...",
            "rows": 5,
            "class": TEXTAREA_CSS,
            "id": "message",
        }),
    )
