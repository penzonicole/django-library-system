from datetime import timedelta, date
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.db.models.functions import TruncMonth
from .models import Livro, Membro, Emprestimo, Autor, Reserva


def lista_livros(request):
    query = request.GET.get('q', '')
    livros = Livro.objects.select_related('autor').all()

    if query:
        livros = livros.filter(
            Q(titulo__icontains=query) |
            Q(autor__nome__icontains=query) |
            Q(isbn__icontains=query)
        )

    livros_mais_emprestados = Livro.objects.annotate(
        total_emprestimos=Count('emprestimo')
    ).order_by('-total_emprestimos')[:5]

    membros = Membro.objects.all()

    return render(request, 'biblioteca/lista_livros.html', {
        'livros': livros,
        'livros_mais_emprestados': livros_mais_emprestados,
        'membros': membros,
        'query': query,
    })


def emprestar_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    membro_id = request.POST.get('membro_id')

    if not membro_id:
        messages.error(request, 'Selecione um membro para continuar.')
        return redirect('lista_livros')

    membro = get_object_or_404(Membro, pk=membro_id)

    # DESAFIO: Limite de Empréstimos Simultâneos (Máximo 3 ativos)
    emprestimos_ativos = Emprestimo.objects.filter(membro=membro, status='ATIVO').count()
    if emprestimos_ativos >= 3:
        messages.error(request, f'O membro "{membro.nome}" já atingiu o limite máximo de 3 empréstimos ativos simultâneos.')
        return redirect('lista_livros')

    if livro.copias_disponiveis <= 0:
        messages.error(request, f'Sem cópias disponíveis. Utilize a opção de reservar o livro.')
        return redirect('lista_livros')

    # Registra o empréstimo
    emprestimo = Emprestimo.objects.create(
        livro=livro,
        membro=membro,
        data_prevista_devolucao=date.today() + timedelta(days=14),
    )
    livro.copias_disponiveis -= 1
    livro.save()

    # DESAFIO: Notificação por E-mail (Aviso do prazo)
    try:
        send_mail(
            subject='Confirmação de Empréstimo - Biblioteca',
            message=f'Olá {membro.nome},\n\nO empréstimo de "{livro.titulo}" foi realizado com sucesso!\nPrazo limite de devolução: {emprestimo.data_prevista_devolucao.strftime("%d/%m/%Y")}.',
            from_email='biblioteca@exemplo.com',
            recipient_list=[membro.email],
            fail_silently=True,
        )
    except Exception:
        pass

    messages.success(request, f'Empréstimo de "{livro.titulo}" registrado para {membro.nome}!')
    return redirect('meus_emprestimos', membro_id=membro.id)


def reservar_livro(request, livro_id):
    """DESAFIO: Reserva de Livro"""
    livro = get_object_or_404(Livro, pk=livro_id)
    membro_id = request.POST.get('membro_id')

    if not membro_id:
        messages.error(request, 'Selecione um membro para criar a reserva.')
        return redirect('lista_livros')

    membro = get_object_or_404(Membro, pk=membro_id)

    Reserva.objects.create(livro=livro, membro=membro)
    messages.success(request, f'Reserva registrada para {membro.nome} na fila do livro "{livro.titulo}".')
    return redirect('lista_livros')


def devolver_livro(request, emprestimo_id):
    """DESAFIO: Devolução e Notificação de Fila de Reserva"""
    emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_id)

    if emprestimo.status != 'DEVOLVIDO':
        emprestimo.data_devolucao = date.today()
        emprestimo.status = 'DEVOLVIDO'
        emprestimo.save()

        emprestimo.livro.copias_disponiveis += 1
        emprestimo.livro.save()

        # Verifica se há fila de reserva para avisar por e-mail
        reserva = Reserva.objects.filter(livro=emprestimo.livro, atendida=False).order_by('data_reserva').first()
        if reserva:
            reserva.atendida = True
            reserva.save()
            try:
                send_mail(
                    subject='Livro Reservado Disponível!',
                    message=f'Olá {reserva.membro.nome},\n\nO livro "{emprestimo.livro.titulo}" foi devolvido e já está disponível para retirada!',
                    from_email='biblioteca@exemplo.com',
                    recipient_list=[reserva.membro.email],
                    fail_silently=True,
                )
            except Exception:
                pass

        messages.success(request, f'Devolução de "{emprestimo.livro.titulo}" registrada.')

    return redirect('meus_emprestimos', membro_id=emprestimo.membro.id)


def meus_emprestimos(request, membro_id):
    membro = get_object_or_404(Membro, pk=membro_id)
    emprestimos = membro.emprestimo_set.all().order_by('-data_emprestimo')
    return render(request, 'biblioteca/meus_emprestimos.html', {
        'membro': membro,
        'emprestimos': emprestimos,
    })


def dashboard_estatisticas(request):
    """DESAFIO: Dashboard de Empréstimos com Agrupamento por Mês"""
    dados_mensais = (
        Emprestimo.objects.annotate(mes=TruncMonth('data_emprestimo'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    labels = [d['mes'].strftime('%b/%Y') for d in dados_mensais if d['mes']]
    valores = [d['total'] for d in dados_mensais]

    return render(request, 'biblioteca/dashboard.html', {
        'chart_labels': labels,
        'chart_valores': valores,
        'total_emprestimos': Emprestimo.objects.count(),
        'total_livros': Livro.objects.count(),
        'total_membros': Membro.objects.count(),
    })