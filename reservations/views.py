from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ReservationForm


def reservation_create(request):

    if request.method == "POST":
        form = ReservationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Votre demande a bien été envoyée. "
                "Miss Digital vous contactera prochainement."
            )

            return redirect("reservation")

    else:
        form = ReservationForm()

    return render(
        request,
        "reservations/reservation.html",
        {"form": form},
    )