import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MachineForm, MachineSearchForm
from .models import Machine


@login_required
def machine_list(request):
    machines = Machine.objects.all()
    search_form = MachineSearchForm(request.GET or None)

    if search_form.is_valid():
        query = search_form.cleaned_data.get('q')

        if query:
            machines = machines.filter(
                Q(machine_id__icontains=query)
                | Q(machine_name__icontains=query)
                | Q(machine_number__icontains=query)
            )

    context = {
        'machines': machines,
        'search_form': search_form,
        'total_count': machines.count(),
    }
    return render(request, 'machines/machine_list.html', context)


@login_required
def machine_add(request):
    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            machine = form.save()
            messages.success(
                request, f'Machine "{machine.machine_name}" ({machine.machine_id}) added successfully.'
            )
            return redirect('machines:list')
    else:
        form = MachineForm()

    return render(request, 'machines/machine_form.html', {
        'form': form,
        'title': 'Add Machine',
    })


@login_required
def machine_edit(request, pk):
    machine = get_object_or_404(Machine, pk=pk)
    if request.method == 'POST':
        form = MachineForm(request.POST, instance=machine)
        if form.is_valid():
            form.save()
            messages.success(request, f'Machine "{machine.machine_name}" updated successfully.')
            return redirect('machines:list')
    else:
        form = MachineForm(instance=machine)

    return render(request, 'machines/machine_form.html', {
        'form': form,
        'title': 'Edit Machine',
        'machine': machine,
    })


@login_required
def machine_delete(request, pk):
    machine = get_object_or_404(Machine, pk=pk)
    if request.method == 'POST':
        name = f'{machine.machine_name} ({machine.machine_id})'
        machine.delete()
        messages.success(request, f'Machine "{name}" deleted successfully.')
        return redirect('machines:list')

    return render(request, 'machines/machine_confirm_delete.html', {'machine': machine})


@login_required
def export_machines_csv(request):
    machines = Machine.objects.all().order_by('machine_id')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="machine_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['Machine ID', 'Machine Name', 'Machine Number', 'Machine Type', 'Status', 'Created Date'])
    for machine in machines:
        writer.writerow([
            machine.machine_id,
            machine.machine_name,
            machine.machine_number,
            machine.machine_type,
            machine.status,
            machine.created_at.strftime('%Y-%m-%d'),
        ])
    return response
