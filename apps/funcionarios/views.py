from django.contrib.auth.models import User
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView
from apps.funcionarios.models import Funcionario
from django.views.generic import (ListView,
                                  UpdateView,
                                  DeleteView,
                                  CreateView)


class FuncionarioList(ListView):
    model = Funcionario

    def get_queryset(self):
        empresa_logada = self.request.user.funcionario.empresa
        queryset = Funcionario.objects.filter(empresa=empresa_logada)
        return(queryset)


class FuncionarioEdit(UpdateView):
    model = Funcionario
    fields = ['nome', 'departamentos']


class FuncionarioDelete(DeleteView):
    model = Funcionario
    success_url = reverse_lazy('funcionarios:list_funcionarios')


class FuncionarioCreate(CreateView):
    model = Funcionario
    fields = ['nome', 'departamentos']

    def form_valid(self, form):
        funcionario = form.save(commit=False)
        username = (funcionario.nome.split(' ')[0] +
                    funcionario.nome.split(' ')[1])
        funcionario.empresa = self.request.user.funcionario.empresa
        funcionario.user = User.objects.create(username=username)
        funcionario.save()
        return super(FuncionarioCreate, self).form_valid(form)
