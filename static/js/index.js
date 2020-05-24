$(function () {

    $(".input input").focus(function () {

        $(this).parent(".input").each(function () {
            $("label", this).css({
                "line-height": "18px",
                "font-size": "18px",
                "font-weight": "100",
                "top": "0px"
            })
            $(".spin", this).css({
                "width": "100%"
            })
        });
    }).blur(function () {
        $(".spin").css({
            "width": "0px"
        })
        if ($(this).val() == "") {
            $(this).parent(".input").each(function () {
                $("label", this).css({
                    "line-height": "60px",
                    "font-size": "24px",
                    "font-weight": "300",
                    "top": "10px"
                })
            });

        }
    });

    $(".button").click(function (e) {
        var pX = e.pageX,
            pY = e.pageY,
            oX = parseInt($(this).offset().left),
            oY = parseInt($(this).offset().top);

        $(this).append('<span class="click-efect x-' + oX + ' y-' + oY + '" style="margin-left:' + (pX - oX) + 'px;margin-top:' + (pY - oY) + 'px;"></span>')
        $('.x-' + oX + '.y-' + oY + '').animate({
            "width": "500px",
            "height": "500px",
            "top": "-250px",
            "left": "-250px",

        }, 600);
        $("button", this).addClass('active');
    })

    $(".alt-2").click(function () {
        if (!$(this).hasClass('material-button')) {
            $(".shape").css({
                "width": "100%",
                "height": "100%",
                "transform": "rotate(0deg)"
            })

            setTimeout(function () {
                $(".overbox").css({
                    "overflow": "initial"
                })
            }, 600)

            $(this).animate({
                "width": "140px",
                "height": "140px"
            }, 500, function () {
                $(".box").removeClass("back");

                $(this).removeClass('active')
            });

            $(".overbox .title").fadeOut(300);
            $(".overbox .input").fadeOut(300);
            $(".overbox .button").fadeOut(300);

            $(".alt-2").addClass('material-buton');
        }

    })

    $(".material-button").click(function () {

        if ($(this).hasClass('material-button')) {
            setTimeout(function () {
                $(".overbox").css({
                    "overflow": "hidden"
                })
                $(".box").addClass("back");
            }, 200)
            $(this).addClass('active').animate({
                "width": "700px",
                "height": "700px"
            });

            setTimeout(function () {
                $(".shape").css({
                    "width": "50%",
                    "height": "50%",
                    "transform": "rotate(45deg)"
                })

                $(".overbox .title").fadeIn(300);
                $(".overbox .input").fadeIn(300);
                $(".overbox .button").fadeIn(300);
            }, 700)

            $(this).removeClass('material-button');

        }

        if ($(".alt-2").hasClass('material-buton')) {
            $(".alt-2").removeClass('material-buton');
            $(".alt-2").addClass('material-button');
        }

    });
    var index = new Index();
    index.run()

});

function Index() {
    var self = this;
}

Index.prototype.ListenSearchEvent = function () {
    var searchBtn = $('#search-btn');
    var searchIdSelect = $("select[name='search-year']");
    searchBtn.click(function (event) {
        year = searchIdSelect.val();
        console.log(year)
        xfzajax.get({
            'url': '/search/',
            'data': {
                'year': year,
            },
            'success': function (result) {
                console.log(result)
            }
        })
    })
}


Index.prototype.ListenAddEvent = function () {
    var addBtn = $("#add-data");
    var titleInput = $("input[name='title']");
    var yearSelect = $("select[name='add-year']");

    var nums1Input = $("input[name='nums1']");
    var nums2Input = $("input[name='nums2']");
    var nums3Input = $("input[name='nums3']");
    var nums4Input = $("input[name='nums4']");

    addBtn.click(function (event) {
        event.preventDefault();
        title = titleInput.val();
        year = yearSelect.val();
        nums1 = nums1Input.val();
        nums2 = nums2Input.val();
        nums3 = nums3Input.val();
        nums4 = nums4Input.val();

        if (!nums1) {
            nums1 = 0
        }
        if (!nums2) {
            nums2 = 0
        }
        if (!nums3) {
            nums3 = 0
        }
        if (!nums4) {
            nums4 = 0
        }
        xfzajax.post({
            'url': '/add/',
            'data': {
                'title': title,
                'year': year,
                'nums1': nums1,
                'nums2': nums2,
                'nums3': nums3,
                'nums4': nums4
            },
            'success': function (result) {
                if (result['code'] === 200){
                    window.location.reload()
                } else {
                    window.messageBox.showError(result['message'])
                }
            },
            'fail':function (err) {
                window.messageBox.showError(err)
            }
        })
    })
};
Index.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");

    deleteBtns.click(function () {
        var btn = $(this);
        var data_id = btn.attr('data-id');
        xfzalert.alertConfirm({
            'text': '您是否要删除这条数据吗？',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/del/',
                    'data': {
                        'data_id': data_id
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            window.location = window.location.href;
                            // window.location.reload()
                        }
                    }
                });
            }
        });
    });
};

Index.prototype.listenEditEvent = function(){

}

Index.prototype.listenSubmitEvent = function () {
    var submitBtn = $("#submit-btn");
    submitBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var pk = btn.attr('data-news-id');

        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();

        var url = '';
        if(pk){
            url = '/cms/edit_news/';
        }else{
            url = '/cms/write_news/';
        }

        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'category': category,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': content,
                'pk': pk
            },
            'success': function (result) {
                if(result['code'] === 200){
                    xfzalert.alertSuccess('恭喜！新闻发表成功！',function () {
                        window.location.reload();
                    });
                }
            }
        });
    });
};

Index.prototype.run = function () {
    var self = this;
    self.ListenAddEvent();
    self.ListenSearchEvent();
    self.listenDeleteEvent();
    self.listenSubmitEvent()
};





