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
Index.prototype.ListenUpperSearchBtn = function () {
    var upperBtn = $("#upper-show");
    var simpleBox = $('#simple-box');
    var upperBox = $(".upper-box");
    upperBtn.click(function (event) {
        upperBox.show();
        simpleBox.hide();
    })
};

Index.prototype.ListenAddEvent = function () {
    var addBtn = $("#add-data")
    var titleInput = $("input[name='title']");
    var yearSelect = $("input[name='year']");

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
                window.location.reload()
            }
        })
    })
}

Index.prototype.run = function () {
    var self = this;
    self.ListenAddEvent();
    self.ListenSearchEvent()
};





