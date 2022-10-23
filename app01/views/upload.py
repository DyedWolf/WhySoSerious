from django.shortcuts import render,HttpResponse


def upload_list(request):
    if request.method == 'GET':
        return render(request, "upload_list.html")
    # print(request.FILES)
    # {'avatar': [<InMemoryUploadedFile: ABD337FD-6095-4208-A273-689499A6F808.jpeg (image/jpeg)>]}>
    file_object = request.FILES.get("avatar")

    f = open(file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse("...")
