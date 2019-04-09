from django.shortcuts import render,redirect,HttpResponse
from app01.models import Press,Book,Author
import os
from django.conf import settings

# Create your views here.

def press_list(request):    #查
    ret = Press.objects.all()    #读取数据库中press（出版社）表中虽有内容
    return render(request,'press_list.html',{'ret':ret})


def add_press(request):   #增加
    if request.method =='POST':
        press_name = request.POST.get('press_name')
        Press.objects.create(name=press_name)
        return redirect('/press_list/')
    return render(request,'add_press.html')


def del_press(request):
    press_id = request.GET.get('id')   #获取id
    Press.objects.get(id=press_id).delete()   #删除SQL中的数据
    return redirect('/press_list/')


def edit_press(request):
    press_id = request.GET.get('id')   #获取出版社的id
    press_obj = Press.objects.get(id=press_id)  # 获取 出版社的orm对象
    if request.method == 'POST':   #表单提交
        new_press = request.POST.get('press')     #获得前端的数据
        press_obj.name = new_press       #获取的值修改数据库信息
        press_obj.save()     #把偶想你
        return redirect('/press_list/')   #转到出版社列表
    return render(request,'edit_press.html',{'press_obj': press_obj})   #第一次get请求时候



def book_list(request):
    book_list_obj = Book.objects.all()
    return render(request,'book_list.html',{'book_list_obj':book_list_obj})


def add_book(request):
    request.GET.get('id')
    press_obj = Press.objects.all()

    if request.method =='POST':
        new_name = request.POST.get('add_book_name')
        new_press = request.POST.get('press_id')

        Book.objects.create(name=new_name,press_id=new_press)  #(数据库后台自动形成press_id)
        return redirect('/book_list/')
    return render(request,'add_book.html',{'press_obj':press_obj})



def del_book(request):
    book_id = request.GET.get('id')
    Book.objects.get(id=book_id).delete()
    return redirect('/book_list/')

def edit_book(request):
    book_id = request.GET.get('id')    #获得要编辑输的表ID
    book_obj = Book.objects.get(id=book_id)    #得到要编辑书的ORM对象
    press_list_obj = Press.objects.all()

    if request.method == 'POST':
        new_book = request.POST.get('book_name')
        new_press_id = request.POST.get('press_id')


        book_obj.name = new_book
        # book_obj.press = Press.objects.get(id=new_press_id)
        book_obj.press_id = new_press_id    # *****  外键一定要加上后缀_id(类似于类中的私有属性似的)
        print(book_obj.name,book_obj.press)

        book_obj.save()

        return redirect('/book_list/')

    return render(request,'edit_book.html',{'book_obj':book_obj,'press_list':press_list_obj})


def author_list(request):
    # 2 . 获取作者的ORM对象
    author_obj_list = Author.objects.all()

    #返回一author的网页表
    return render(request,'author_list.html',{'author_obj_list':author_obj_list})   #把所有的作者和书籍展示出来

def add_author(request):
    # 2. 把所有书都展示对用户
    #获取所有的书籍
    book_obj_list = Book.objects.all()

    # 用户提交请求时post
    if request.method =='POST':
        add_author_name = request.POST.get('author_name')   #获取作者名字
        add_book_ids = request.POST.getlist('book_ids')        # 获取作者写的书（一定要用getlist   不然只能获取最后一本书）

        # A = Author.objects.create(name=add_author_name)
        # A.books.set(add_book_ids)

        Author.objects.create(name=add_author_name).books.set(add_book_ids)    #利用ORM把数据写入数据库表中
        return redirect('/author_list/')

    # 1 .第一次返回用户一个页面
    return render(request,'add_author.html',{'book_obj_list':book_obj_list})

def del_author(request):
    # 获得删除对象的id
    del_author_id = request.GET.get('id')

    #删除sql表中的数据
    Author.objects.get(id=del_author_id).delete()

    # 跳转回author_lsit面页
    return redirect('/author_list/')

def edit_author(request):
    # 1.先获取要编辑的id
    edit_id = request.GET.get('id')   #第一次获得要编辑的id
    author_obj = Author.objects.get(id=edit_id)   #获得要编辑表中作者的orm对象
    if request.method =='POST':
        edit_author_name = request.POST.get('author_name')
        edit_book_ids = request.POST.getlist('book_obj_ids')    #拿到数据


        author_obj.name = edit_author_name   #修改作者
        author_obj.save()    #改自己的表要保存下

        author_obj.books.set(edit_book_ids)  #修改第三联系表
        return redirect('/author_list/')
    #第一次返回一个html网页
    # 需要对应的作者，书名
    book_obj_list = Book.objects.all()
    return render(request,'edit_author.html',{'book_obj_list':book_obj_list,'author_obj':author_obj})


def upload(request):
    if request.method == 'POST':   #提交表单是post
        file_obj = request.FILES.get('name')   #获得 文件 对象
        print(file_obj)
        file_name = file_obj.name
        print(file_name)
        if os.path.exists(os.path.join(settings.BASE_DIR,file_name)):
            #分析 OS.path.exists 路径存在为true，不存在未false， 文件名字 拼接 项目路径
            #加起来就是项目路径下彼岸是否存在和我文件重名的文件
            name,suffix = file_name.split('.')
            name += '1'
            file_name = name  + '.' + suffix
        with open(file_name,'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
    #第一次给用户一个界面
    return render(request,'upload.html')

def dalei():
	pass
	
def dalei22():
	pass
