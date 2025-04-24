# core/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (
    render, 
    redirect, 
    get_object_or_404
)
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView, 
    ListView
)
from django_filters.views import FilterView
from .models import Stage, Log
from .filters import StageFilter
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Stage, Log
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import Stage
from .forms import StageForm, LogForm
from cloudinary.uploader import upload
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Log, Like



@login_required
def set_log_status_view(request, stage_pk, status):
    """
    観た／観たい／観れない をボタン押下でセットするビュー
    """
    stage = get_object_or_404(Stage, pk=stage_pk)
    
    # すでにユーザーのLogがあるか確認
    user_log, created = Log.objects.get_or_create(
        user=request.user,
        stage=stage,
        defaults={'status': status}
    )

    if not created:
        # 既にあった場合は status を上書き
        user_log.status = status
        user_log.save()

    # もし 'watched' だったらコメントや評価を入力してもらうため、
    # 新規or既存のLogを Update画面やCreate画面に飛ばすイメージ。
    # 例: まだLogがなかったら CreateView のURLへ、あれば UpdateView へ
    if status == 'watched':
        # すでにLogがある場合 → 更新ページへ
        # なかった場合でも get_or_create で user_log ができてるので、UpdateでOK
        return redirect('log_update', pk=user_log.pk)

    # 'want' や 'cannot' の場合は、そのまま舞台詳細へ戻るだけ
    return redirect('stage_detail', pk=stage.pk)



@login_required
def my_page(request):
    # ユーザーの全ログ
    user_logs = Log.objects.filter(user=request.user).select_related('stage').order_by('-updated_at')

    # それぞれのステータスでフィルタ
    want_logs = user_logs.filter(status='want')
    watched_logs = user_logs.filter(status='watched')
    cannot_logs = user_logs.filter(status='cannot')

    context = {
        'want_logs': want_logs,
        'watched_logs': watched_logs,
        'cannot_logs': cannot_logs,
    }
    return render(request, 'core/my_page.html', context)



class StageListView(FilterView):
    model = Stage
    template_name = 'core/stage_list.html'
    context_object_name = 'stages'
    filterset_class = StageFilter


from django.db.models import Avg

class StageDetailView(DetailView):
    model = Stage
    template_name = 'core/stage_detail.html'
    context_object_name = 'stage'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stage = self.object

        # 1) みんなの観劇ログ(観た＋コメントあり) ←既存
        all_logs = (Log.objects.filter(stage=stage, status='watched')
                    .exclude(comment__isnull=True)
                    .exclude(comment__exact='')
                    .select_related('user')
                    .order_by('-updated_at')
                   )
        context['all_logs'] = all_logs

        # 2) 自分のログ(全部) ←既存
        user = self.request.user
        if user.is_authenticated:
            user_log = Log.objects.filter(stage=stage, user=user).first()
            context['user_log'] = user_log

        # ★ 3) 平均レーティングを計算 (status='watched' が対象なら加える)
        avg_dict = Log.objects.filter(stage=stage, status='watched', rating__isnull=False) \
                              .aggregate(avg_rating=Avg('rating'))
        average_rating = avg_dict['avg_rating']  # 例: 3.5 とか None

        context['average_rating'] = average_rating

        return context


class StageCreateView(LoginRequiredMixin, CreateView):
    model = Stage
    form_class = StageForm
    template_name = 'core/stage_form.html'

    # StageCreateView
    def form_valid(self, form):
        self.object = form.save(commit=False)
        poster_file = form.cleaned_data.get('poster_file')
        if poster_file:
            result = upload(poster_file)
            self.object.poster_url = result['secure_url']
        self.object.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('stage_detail', kwargs={'pk': self.object.pk})

class StageUpdateView(UpdateView):
    model = Stage
    form_class = StageForm
    template_name = 'core/stage_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        poster_file = form.cleaned_data.get('poster_file')
        if poster_file:
            result = upload(poster_file)
            self.object.poster_url = result['secure_url']
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('stage_detail', kwargs={'pk': self.object.pk})


class StageDeleteView(DeleteView):
    model = Stage
    template_name = 'core/stage_delete.html'
    success_url = reverse_lazy('stage_list')
    def test_func(self):
        stage = self.get_object()
        # “作成者 or 管理者”に許可
        # 例: is_staff or is_superuser なら削除可
        #     あるいは stage.created_by == self.request.user
        return (
            self.request.user.is_staff or 
            self.request.user.is_superuser or
            (stage.created_by == self.request.user)
        )


class StageSearchView(FilterView):
    model = Stage
    template_name = 'core/stage_search.html'
    context_object_name = 'stages'  # テンプレート上で使うオブジェクト名
    filterset_class = StageFilter   # 先ほど作成した FilterSet を指定


class LogUpdateView(LoginRequiredMixin, UpdateView):
    model = Log
    form_class = LogForm
    template_name = 'core/log_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('stage_detail', kwargs={'pk': self.object.stage.pk})



class LogDeleteView(LoginRequiredMixin, DeleteView):
    model = Log
    template_name = 'core/log_confirm_delete.html'

    def get_queryset(self):
        # 自分のLogのみ削除可
        return super().get_queryset().filter(user=self.request.user)

    def get_success_url(self):
        # 削除後も同様に StageDetail へ
        return reverse_lazy('stage_detail', kwargs={'pk': self.object.stage.pk})



class LogCreateView(LoginRequiredMixin, CreateView):
    model = Log
    form_class = LogForm
    template_name = 'core/log_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        stage_pk = self.kwargs.get('stage_pk')
        stage = get_object_or_404(Stage, pk=stage_pk)
        form.instance.stage = stage
        return super().form_valid(form)

    def get_success_url(self):
        # 作成後は Stage の詳細ページへ戻る
        stage_pk = self.kwargs.get('stage_pk')
        return reverse_lazy('stage_detail', kwargs={'pk': stage_pk})



from django.shortcuts import render, redirect

def top_view(request):
    if request.user.is_authenticated:
        return redirect('stage_list')  # ログインしていれば /stage/ へ
    else:
        # LP用テンプレートを表示
        return render(request, 'core/top.html')



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, log_id):
    log = get_object_or_404(Log, pk=log_id)
    like_qs = Like.objects.filter(user=request.user, log=log)

    if like_qs.exists():        # 既に押している ⇒ 解除
        like_qs.delete()
        liked = False
    else:                       # まだ押していない ⇒ 追加
        Like.objects.create(user=request.user, log=log)
        liked = True

    return Response({
        'liked': liked,
        'like_count': log.likes.count()
    })