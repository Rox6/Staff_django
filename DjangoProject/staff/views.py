from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from staff.models import Mitarbeiter
from staff.forms import Staff_form


def staff_list(request):
    mitarbeiter = Mitarbeiter.objects.all()
    return render(request, 'staff/list.html', {'mitarbeiter': mitarbeiter})

def staff_create(request):
    if request.method == 'POST':
        form = Staff_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mitarbeiter erfolgreich gespeichert.')
            return redirect('staff_list')
    else:
        form = Staff_form()
    return render(request, 'staff/form.html', {'form': form})


def staff_update(request, pk):
    mitarbeiter = get_object_or_404(Mitarbeiter, pk=pk)
    if request.method == 'POST':
        form = Staff_form(request.POST, instance=mitarbeiter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mitarbeiter erfolgreich aktualisiert.')
            return redirect('staff_list')
    else:
        form = Staff_form(instance=mitarbeiter)
    return render(request, 'staff/form.html', {'form': form})

def staff_delete(request, pk):
    mitarbeiter = get_object_or_404(Mitarbeiter, pk=pk)
    if request.method == 'POST':
        mitarbeiter.delete()
        messages.success(request, 'Mitarbeiter erfolgreich gelöscht.')
        return redirect('staff_list')
    return render(request, 'staff/confirm_delete.html', {'mitarbeiter': mitarbeiter})