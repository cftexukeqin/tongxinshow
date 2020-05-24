from django.shortcuts import render
from apps.front.models import Data
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from pure_pagination import PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST,require_GET
from django.views.generic import View

from apps.utils.pyecharts_restful import JsonResponse
import db_tools.data.show_data as s_data
from apps.utils import restful
from apps.utils.db_read import read_query

import json
from rest_framework.views import APIView
from pyecharts.charts import Bar, Line, Pie, WordCloud, Graph
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode


# Create your views here.

def index(request):
    all_datas = Data.objects.all()
    page = request.GET.get('page', 1)
    p = Paginator(all_datas, 8, request=request)


    try:
        datas = p.page(page)
    except PageNotAnInteger:
        # 捕获到页码不是整数，返回第一页
        datas = p.page(1)
    except EmptyPage:
        # 页码超出范围，返回最后一页
        datas = p.page(p.num_pages)

    context = {
        'datas':datas
    }
    return render(request, 'front/index.html',context=context)


def search(request):
    year = request.GET.get('year')
    words = request.GET.get("words")
    if year!= "0000":
        if words and words!='None':
            all_datas = Data.objects.filter(year=year,name__icontains=words).all()
        else:
            all_datas = Data.objects.filter(year=year).all()
    else:
        all_datas = Data.objects.filter(name__icontains=words).all()

    page = request.GET.get('page', 1)

    p = Paginator(all_datas, 8, request=request)
    datas = p.page(page)
    context = {
        'datas':datas,
        'words':words,
        'r_year':year
    }
    return render(request, 'front/index.html', context=context)


def document_list(request):
    datas = Data.objects.all()
    page = request.GET.get('page', 1)

    p = Paginator(datas, 8, request=request)
    documents = p.page(page)
    context = {
        'documents': documents,

    }
    return render(request, 'front/list.html', context=context)


def author_bar() -> Bar:
    df = read_query()
    name_list = list(df.name.unique())
 #    name_list = ['移动用户数（百万户）','手机上网总流量（kTB）' ,'移动语音通话总分钟数（百万分钟）', '有线宽带用户数（百万户）',
 # '固定电话用户数（百万户）' ,'固定电话本地语音通话总次数（百万次）' ,'固定电话长途总分钟数（百万分钟）', '经营收入（人民币百万元）',
 # 'test3']
    # jidu1 = df[df['year'] == 2018]['jidu_1']
    title = name_list[0]
    data_2018 = Data.objects.filter(year="2018",name=name_list[0]).first()
    data_2019 = Data.objects.filter(year="2019",name=name_list[0]).first()
    data_2020 = Data.objects.filter(year="2020",name=name_list[0]).first()
    print(name_list[0])
    x = [2018,2019,2020]

    y1 = [data_2018.jidu_1,data_2019.jidu_1,data_2020.jidu_1]
    y2 = [data_2018.jidu_2,data_2019.jidu_2,data_2020.jidu_2]
    y3 = [data_2018.jidu_3,data_2019.jidu_3,data_2020.jidu_3]
    y4 = [data_2018.jidu_4,data_2019.jidu_4,data_2020.jidu_4]



    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("第一季度", y1)
            .add_yaxis("第二季度", y2)
            .add_yaxis("第三季度", y3)
            .add_yaxis("第四季度", y4)
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            legend_opts=opts.LegendOpts(type_="scroll", pos_right="30px", orient="vertical"),
        )
            .dump_options_with_quotes()
    )
    return c


def orginize_bar() -> Bar:
    #    name_list = ['移动用户数（百万户）','手机上网总流量（kTB）' ,'移动语音通话总分钟数（百万分钟）', '有线宽带用户数（百万户）',
    # '固定电话用户数（百万户）' ,'固定电话本地语音通话总次数（百万次）' ,'固定电话长途总分钟数（百万分钟）', '经营收入（人民币百万元）',
    # 'test3']
    df = read_query()
    name_list = list(df.name.unique())
    title = name_list[2]
    data_2018 = Data.objects.filter(year="2018", name=name_list[2]).first()
    data_2019 = Data.objects.filter(year="2019", name=name_list[2]).first()

    x = ['第一季度', '第二季度', '第三季度', '第四季度']
    y1 = [data_2018.jidu_1,data_2018.jidu_2,data_2018.jidu_3,data_2018.jidu_4]
    y2 = [data_2019.jidu_1,data_2019.jidu_2,data_2019.jidu_3,data_2019.jidu_4]

    line2 = (
        Line(

        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
            .add_xaxis(x)
            .add_yaxis(
            series_name="2018年",
            stack="总量",
            y_axis= y1,
            label_opts=opts.LabelOpts(is_show=True),
        )
            .add_yaxis(
            series_name="2019年",
            stack="总量",
            y_axis=y2,
            label_opts=opts.LabelOpts(is_show=True),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            legend_opts=opts.LegendOpts(type_="scroll", pos_right="30px", orient="vertical"),
        )
            # 设置 boundary_gap 的时候一定要放在最后一个配置项里, 不然会被覆盖
            .dump_options_with_quotes()
    )
    return line2


def year_line():
    #    name_list = ['移动用户数（百万户）','手机上网总流量（kTB）' ,'移动语音通话总分钟数（百万分钟）', '有线宽带用户数（百万户）',
    # '固定电话用户数（百万户）' ,'固定电话本地语音通话总次数（百万次）' ,'固定电话长途总分钟数（百万分钟）', '经营收入（人民币百万元）',
    # 'test3']
    df = read_query()
    name_list = list(df.name.unique())
    title = name_list[1]
    data_2018 = Data.objects.filter(year="2018", name=name_list[1]).first()
    data_2019 = Data.objects.filter(year="2019", name=name_list[1]).first()

    x = ['第一季度', '第二季度', '第三季度', '第四季度']
    y1 = [data_2018.jidu_1,data_2018.jidu_2,data_2018.jidu_3,data_2018.jidu_4]
    y2 = [data_2019.jidu_1,data_2019.jidu_2,data_2019.jidu_3,data_2019.jidu_4]

    line2 = (
        Line(

        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
            .add_xaxis(x)
            .add_yaxis(
            series_name="2018年",
            stack="总量",
            y_axis= y1,
            label_opts=opts.LabelOpts(is_show=True),
        )
            .add_yaxis(
            series_name="2019年",
            stack="总量",
            y_axis=y2,
            label_opts=opts.LabelOpts(is_show=True),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            legend_opts=opts.LegendOpts(type_="scroll", pos_right="30px", orient="vertical"),
        )
            # 设置 boundary_gap 的时候一定要放在最后一个配置项里, 不然会被覆盖
            .dump_options_with_quotes()
    )
    return line2


def cishu_pie():
    #    name_list = ['移动用户数（百万户）','手机上网总流量（kTB）' ,'移动语音通话总分钟数（百万分钟）', '有线宽带用户数（百万户）',
    # '固定电话用户数（百万户）' ,'固定电话本地语音通话总次数（百万次）' ,'固定电话长途总分钟数（百万分钟）', '经营收入（人民币百万元）',
    # 'test3']
    df = read_query()
    name_list = list(df.name.unique())
    title = name_list[5]
    data_2018 = Data.objects.filter(year="2018", name=name_list[5]).first()
    data_2019 = Data.objects.filter(year="2019", name=name_list[5]).first()
    # data_2020 = Data.objects.filter(year="2020", name=name_list[5]).first()
    print(name_list[0])
    x = [2018, 2019, 2020]

    y1 = [data_2018.jidu_1, data_2018.jidu_2, data_2018.jidu_3,data_2018.jidu_4]
    y2 = [data_2019.jidu_1, data_2019.jidu_2, data_2019.jidu_3,data_2019.jidu_4]


    v = ['第一季度','第二季度','第三季度','第四季度']
    c = (
        Pie()
            .add(
            "2018年",
            [list(z) for z in zip(v, y1)],
            radius=["30%", "75%"],
            center=["25%", "50%"],
            rosetype="radius",
            label_opts=opts.LabelOpts(is_show=True),
        )
            .add(
            "2019年",
            [list(z) for z in zip(v, y2)],
            radius=["30%", "75%"],
            center=["75%", "50%"],
            rosetype="area",
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            legend_opts=opts.LegendOpts(type_="scroll", pos_right="30px", orient="vertical"),
        )
            .dump_options_with_quotes()
    )
    return c
def minute_pie():
    #    name_list = ['移动用户数（百万户）','手机上网总流量（kTB）' ,'移动语音通话总分钟数（百万分钟）', '有线宽带用户数（百万户）',
    # '固定电话用户数（百万户）' ,'固定电话本地语音通话总次数（百万次）' ,'固定电话长途总分钟数（百万分钟）', '经营收入（人民币百万元）',
    # 'test3']
    df = read_query()
    name_list = list(df.name.unique())
    title = name_list[6]
    data_2018 = Data.objects.filter(year="2018", name=name_list[6]).first()
    data_2019 = Data.objects.filter(year="2019", name=name_list[6]).first()
    # data_2020 = Data.objects.filter(year="2020", name=name_list[5]).first()
    print(name_list[0])
    x = [2018, 2019, 2020]

    y1 = [data_2018.jidu_1, data_2018.jidu_2, data_2018.jidu_3,data_2018.jidu_4]
    y2 = [data_2019.jidu_1, data_2019.jidu_2, data_2018.jidu_3,data_2019.jidu_4]


    v = ['第一季度','第二季度','第三季度','第四季度']
    c = (
        Pie()
            .add(
            "2018年",
            [list(z) for z in zip(v, y1)],
            radius=["30%", "75%"],
            center=["25%", "50%"],
            label_opts=opts.LabelOpts(is_show=True),
        )
            .add(
            "2019年",
            [list(z) for z in zip(v, y2)],
            radius=["30%", "75%"],
            center=["75%", "50%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            legend_opts=opts.LegendOpts(type_="scroll", pos_right="30px", orient="vertical"),
        )
            .dump_options_with_quotes()
    )
    return c

def qikan_bar() -> Bar:
    df = read_query()
    name_list = list(df.name.unique())
    #    name_list = ['移动用户数（百万户）','手机上网总流量（kTB）' ,'移动语音通话总分钟数（百万分钟）', '有线宽带用户数（百万户）',
    # '固定电话用户数（百万户）' ,'固定电话本地语音通话总次数（百万次）' ,'固定电话长途总分钟数（百万分钟）', '经营收入（人民币百万元）',
    # 'test3']
    # jidu1 = df[df['year'] == 2018]['jidu_1']
    title = name_list[3]
    data_2018 = Data.objects.filter(year="2018", name=name_list[3]).first()
    data_2019 = Data.objects.filter(year="2019", name=name_list[3]).first()
    data_2020 = Data.objects.filter(year="2020", name=name_list[3]).first()
    print(name_list[0])
    x = [2018, 2019, 2020]

    y1 = [data_2018.jidu_1, data_2019.jidu_1, data_2020.jidu_1]
    y2 = [data_2018.jidu_2, data_2019.jidu_2, data_2020.jidu_2]
    y3 = [data_2018.jidu_3, data_2019.jidu_3, data_2020.jidu_3]
    y4 = [data_2018.jidu_4, data_2019.jidu_4, data_2020.jidu_4]

    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("第一季度", y1)
            .add_yaxis("第二季度", y2)
            .add_yaxis("第三季度", y3)
            .add_yaxis("第四季度", y4)

            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            toolbox_opts=opts.ToolboxOpts(),
            legend_opts=opts.LegendOpts(is_show=True),
        )
            .dump_options_with_quotes()
    )
    return c



def wordshow():
    #    name_list = ['移动用户数（百万户）','手机上网总流量（kTB）' ,'移动语音通话总分钟数（百万分钟）', '有线宽带用户数（百万户）',
    # '固定电话用户数（百万户）' ,'固定电话本地语音通话总次数（百万次）' ,'固定电话长途总分钟数（百万分钟）', '经营收入（人民币百万元）',
    # 'test3']
    df = read_query()
    name_list = list(df.name.unique())
    title = name_list[4]
    data_2018 = Data.objects.filter(year="2018", name=name_list[4]).first()
    data_2019 = Data.objects.filter(year="2019", name=name_list[4]).first()

    x = ['第一季度', '第二季度', '第三季度', '第四季度']
    y1 = [data_2018.jidu_1, data_2018.jidu_2, data_2018.jidu_3, data_2018.jidu_4]
    y2 = [data_2019.jidu_1, data_2019.jidu_2, data_2019.jidu_3, data_2019.jidu_4]

    line2 = (
        Line(

        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
            .add_xaxis(x)
            .add_yaxis(
            series_name="2018年",
            stack="总量",
            y_axis=y1,
            label_opts=opts.LabelOpts(is_show=True),
        )
            .add_yaxis(
            series_name="2019年",
            stack="总量",
            y_axis=y2,
            label_opts=opts.LabelOpts(is_show=True),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            legend_opts=opts.LegendOpts(type_="scroll", pos_right="30px", orient="vertical"),
        )
            # 设置 boundary_gap 的时候一定要放在最后一个配置项里, 不然会被覆盖
            .dump_options_with_quotes()
    )
    return line2


def relation():
    df = read_query()
    name_list = list(df.name.unique())
    #    name_list = ['移动用户数（百万户）','手机上网总流量（kTB）' ,'移动语音通话总分钟数（百万分钟）', '有线宽带用户数（百万户）',
    # '固定电话用户数（百万户）' ,'固定电话本地语音通话总次数（百万次）' ,'固定电话长途总分钟数（百万分钟）', '经营收入（人民币百万元）',
    # 'test3']
    # jidu1 = df[df['year'] == 2018]['jidu_1']
    title = name_list[7]
    data_2018 = Data.objects.filter(year="2018", name=name_list[7]).first()
    data_2019 = Data.objects.filter(year="2019", name=name_list[7]).first()
    data_2020 = Data.objects.filter(year="2020", name=name_list[7]).first()
    print(name_list[0])
    x = [2018, 2019, 2020]

    y1 = [data_2018.jidu_1, data_2019.jidu_1, data_2020.jidu_1]
    y2 = [data_2018.jidu_2, data_2019.jidu_2, data_2020.jidu_2]
    y3 = [data_2018.jidu_3, data_2019.jidu_3, data_2020.jidu_3]
    y4 = [data_2018.jidu_4, data_2019.jidu_4, data_2020.jidu_4]

    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("第一季度", y1)
            .add_yaxis("第二季度", y2)
            .add_yaxis("第三季度", y3)
            .add_yaxis("第四季度", y4)

            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            toolbox_opts=opts.ToolboxOpts(),
            legend_opts=opts.LegendOpts(is_show=True),
        )
            .dump_options_with_quotes()
    )
    return c


class AuthorChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(author_bar()))


class OrginiseChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(orginize_bar()))


class YearChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(year_line()))


class XuekeChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(cishu_pie()))


class QikanChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(qikan_bar()))


class CatChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(minute_pie()))


class WordChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(wordshow()))


class RelationChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(relation()))

@method_decorator([login_required(login_url='/user/login/'),],name='dispatch')
class ShowView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open("./templates/front/show.html", encoding="utf-8").read())


@require_POST
def adddata(request):
    title = request.POST.get("title")
    year = request.POST.get('year')

    exsited = Data.objects.filter(name=title).first()
    if not  exsited:
        nums1 = float(request.POST.get("nums1", 0))
        nums2 = float(request.POST.get("nums2", 0))
        nums3 = float(request.POST.get("nums3", 0))
        nums4 = float(request.POST.get("nums4", 0))
        data = Data(name=title, year=year, jidu_1=nums1, jidu_2=nums2, jidu_3=nums3, jidu_4=nums4)
        data.save()
        return restful.ok()
    else:
        return restful.paramserror(message="该数据名称已存在！")




@require_POST
def delete_data(request):
    data_id = request.POST.get('data_id')
    print("data_id",data_id)
    Data.objects.filter(pk=data_id).delete()
    return restful.ok()


def test(request):
    data = Data.objects.filter(year='2018',name='移动用户数（百万户）').first()
    print(data.name,data.jidu_2)
    return restful.ok()


# class EditNewsView(View):
#     def get(self,request):
#         news_id = request.GET.get('news_id')
#         news = Data.objects.get(pk=news_id)
#         context = {
#             'news': news,
#         }
#         return render(request,'cms/write_news.html',context=context)
#
#     def post(self,request):
#         title = form.cleaned_data.get('title')
#         desc = form.cleaned_data.get('desc')
#         thumbnail = form.cleaned_data.get('thumbnail')
#         content = form.cleaned_data.get('content')
#         category_id = form.cleaned_data.get('category')
#         pk = form.cleaned_data.get("pk")
#         category = NewsCategory.objects.get(pk=category_id)
#         News.objects.filter(pk=pk).update(title=title,desc=desc,thumbnail=thumbnail,content=content,category=category)
#         return restful.ok()
#         else:
#             return restful.params_error(message=form.get_errors())