from django.contrib import admin
from .models import Task  # Taskモデルをmodels.pyからインポート

admin.site.register(Task)  # 管理サイトにTaskモデルを登録