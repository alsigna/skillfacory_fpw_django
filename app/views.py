from urllib import response
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
import re
from collections import Counter
import json


class Index(View):
    def get(self, request: HttpRequest) -> HttpRequest:
        answer = request.COOKIES.get("answer")
        if answer:
            answer = json.loads(answer)
        return render(
            request=request,
            template_name="app/index.html",
            context={"result": answer},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        response = redirect(reverse("index"))

        if "upload_file" in request.POST:
            f = request.FILES.get("sent_file")
            if f is not None:
                lines = f.file.read().decode()
                words = re.findall(r"\w+", lines.lower())
                response.set_cookie("words", json.dumps(Counter(words)))
                answer = "файл загружен"
            else:
                answer = "укажите файл"
        elif "get_word_count" in request.POST:
            words = json.loads(request.COOKIES.get("words") or '""')
            word = request.POST.get("word_count")
            if words == "" or words is None:
                answer = "сначала загрузите файл"
            elif word == "" or word is None:
                answer = "укажите слово для поиска"
            elif word in words:
                answer = f"количество слова '{word}' равно {words[word]}"
            else:
                answer = f"слово '{word}' не встречается"

        elif "clear_cache" in request.POST:
            response.delete_cookie("words")
            answer = "кеш очищен"

        response.set_cookie("answer", json.dumps(answer))
        return response
