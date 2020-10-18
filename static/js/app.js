(function ($) {
    var trailer = "null";
    var baseUrl;
    var baseUrl = $("body").attr("alt");

    function getCookie(t) {
        for (var e = t + "=", i = decodeURIComponent(document.cookie).split(";"), a = 0; a < i.length; a++) {
            for (var s = i[a];
                 " " == s.charAt(0);) s = s.substring(1);
            if (0 == s.indexOf(e)) return s.substring(e.length, s.length)
        }
        return ""
    }

    function setCookie(t, e, i) {
        var a = new Date;
        a.setTime(a.getTime() + 24 * i * 60 * 60 * 1e3);
        var s = "expires=" + a.toUTCString();
        document.cookie = t + "=" + e + ";" + s + ";path=/"
    }

    baseUrl = $("body").attr("alt");
    $(".alert-home>button").on("click", function () {
        $(this).parent().fadeOut()
    }), $(".gplay-box>span").on("click", function () {
        $(".gplay-box").hide(), setCookie("gplay", "true", 10)
    }), "" == getCookie("gplay") && $(".gplay-box").fadeIn(), $(document).ready(function () {
        $(".menu-left-btn").on("click", function () {
            $(".sidebar").toggleClass("active-sidebar"), $(".close-menu-left-btn").show()
        }), $(".close-menu-left-btn").on("click", function () {
            $(".sidebar").toggleClass("active-sidebar"), $(".close-menu-left-btn").hide()
        })
    }), setTimeout(function () {
        $("#paypal-form-pay").submit()
    }, 2e3), setTimeout(function () {
        $(".alert-home").fadeOut()
    }, 3e3);
    var t = "none",
        e = "none",
        i = "none",
        a = "none";
    $(".btn-fav").on("click", function () {
        var t = $(this).attr("alt"),
            e = $(this);
        e.html("<i class='fas fa-circle-notch fa-spin'></i>");
        var i = {
            id: t,
            type: "poster"
        };
        $.ajax({
            type: "post",
            data: i,
            url: baseUrl + "/ajax/mylist/add.html",
            success: function (t) {
                200 == t && e.html("<i class='fa fa-heart'></i>"), 202 == t && e.html("<i class='far fa-heart'></i>")
            }
        })
    }), $(".search-btn").on("click", function () {
        $(".search-form").show()
    }), $(".search-btn-close").on("click", function () {
        $(".search-form").hide()
    }), $(".btn-fav-channel").on("click", function () {
        var t = $(this).attr("alt"),
            e = $(this);
        e.html("<i class='fas fa-circle-notch fa-spin'></i>");
        var i = {
            id: t,
            type: "channel"
        };
        $.ajax({
            type: "post",
            data: i,
            url: baseUrl + "/ajax/mylist/add.html",
            success: function (t) {
                200 == t && e.html("<i class='fa fa-heart'></i>"), 202 == t && e.html("<i class='far fa-heart'></i>")
            }
        })
    }), $(".pack").on("click", function () {
        $(".pack").removeClass("active"), $(this).addClass("active"), e = $(this).attr("alt"), i = $(this).find("span").html(), a = $(this).find("h5").html(), $(this).attr("id"), $("#selected_pack h5").html(a), $("#selected_pack span.price-step-1").html(i), $(".error-plan").hide()
    }), $(".payment").on("click", function () {
        t = $(this).attr("alt"), $(".payment").removeClass("active"), $(this).addClass("active"), $(".error-method").hide()
    }), $("#go-to-pay").on("click", function () {
        "none" == t ? $(".error-method").show() : ($(".error-method").hide(), $("#form_payment_step").submit())
    }), $(".file-input").on("click", function () {
        $(this).prev().on("click",)
    }), $("input[type=file]").change(function () {
        $(this).next().addClass("active")
    }), $("#go-payment-method").on("click", function () {
        "none" == e ? $(".error-plan").show() : ($(".error-plan").hide(), $("#payment-method").show(), $("#subscribe-plan").hide())
    }), $(".movie-subtitles").on("click", function () {
        var t = $(this);
        $(this).html("<i class='fas fa-circle-notch fa-spin'></i> Subtitles"), $(".serie-dialog>.login-box .notif-title").html("<span class='fa fa-cc'></span> " + $(this).attr("data-title") + " -  Subtitles");
        var e = $(this).attr("data-id");
        return $.ajax({
            url: baseUrl + "/ajax/movie/subtitles/" + e + ".html",
            success: function (e) {
                $(".box-content").html(e), $(".serie-dialog").show(), t.html("<i class='fa fa-cc'></i> Subtitles")
            }
        }), !1
    }), $(document).on("click", ".movie-downloads", function () {
        var t = $(this);
        $(this).html("<i class='fas fa-circle-notch fa-spin'></i> Download"), $(".serie-dialog>.login-box .notif-title").html("<span class='fa fa-download'></span> " + $(this).attr("data-title") + " -  Download ");
        var e = $(this).attr("data-id");
        return $.ajax({
            url: baseUrl + "/ajax/movie/downloads/" + e + ".html",
            success: function (e) {
                $(".box-content").html(e), $(".serie-dialog").show(), t.html("<i class='fa fa-download'></i> Download")
            }
        }), !1
    }), $(document).on("click", ".episode-subtitles", function () {
        var t = $(this);
        $(this).html("<i class='fas fa-circle-notch fa-spin'></i>"), $(".serie-dialog>.login-box .notif-title").html("<span class='fa fa-cc'></span> " + $(this).attr("data-title") + " - Subtitles");
        var e = $(this).attr("data-id");
        return $.ajax({
            url: baseUrl + "/ajax/serie/subtitles/" + e + ".html",
            success: function (e) {
                $(".box-content").html(e), $(".serie-dialog").show(), t.html("<i class='fa fa-cc'></i>")
            }
        }), !1
    }), $(document).on("click", ".episode-download", function () {
        var t = $(this);
        $(this).html("<i class='fas fa-circle-notch fa-spin'></i>"), $(".serie-dialog>.login-box .notif-title").html("<span class='fa fa-download'></span> " + $(this).attr("data-title") + "  Download");
        var e = $(this).attr("data-id");
        return $.ajax({
            url: baseUrl + "/ajax/serie/downloads/" + e + ".html",
            success: function (e) {
                $(".box-content").html(e), $(".serie-dialog").show(), t.html("<i class='fa fa-download'></i>")
            }
        }), !1
    }), $(".flix-carousel .next_btn").on("click", function () {
        $(this).nextAll(".flix-scroll-x").animate({
            scrollLeft: $(this).nextAll(".flix-scroll-x").scrollLeft() + $(this).nextAll(".flix-scroll-x").width() - 50
        }, 200)
    }), $(".flix-carousel .prev_btn").on("click", function () {
        $(this).nextAll(".flix-scroll-x").animate({
            scrollLeft: $(this).nextAll(".flix-scroll-x").scrollLeft() - $(this).nextAll(".flix-scroll-x").width() - 50
        }, 200)
    }), $("#subtitles-btn").on("click", function () {
        $(".subtitles-table").slideToggle(), $(".downloads-table").show() && $(".downloads-table").hide()
    }), $("#downloads-btn").on("click", function () {
        $(".downloads-table").slideToggle(), $(".subtitles-table").show() && $(".subtitles-table").hide()
    }), $("#trailer-btn").on("click", function () {
        "null" == trailer && (trailer = $(".trailer-video").attr("alt")), $(".trailer-video").html("<div class='embed-responsive embed-responsive-16by9'><iframe width='560' height='315' src='https://www.youtube.com/embed/" + trailer + "' frameborder='0' allow='ccelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe></div>"), $(".trailer-video").fadeIn()
    }), $(".trailer-video").on("click", function () {
        $(this).fadeOut(), $(".trailer-video").html("")
    }), $("#share-btn").on("click", function () {
        $(".share-buttons").slideToggle()
    })

    var rating = 1;

    function setRate(t) {
        rating = t
    }

    function rate(t) {
        var e = $("#rate-input").attr("alt"),
            i = $(".input-review").val(),
            a = {
                id: e,
                rating: rating,
                review: i,
                type: t
            };
        $(".submit-review").hide(), $(".loading-review").css("display", "block"), $.ajax({
            type: "post",
            data: a,
            url: baseUrl + "/ajax/rating/add.html",
            success: function (t) {
                $(".input-review").val(""), $(".submit-review").show(), $(".loading-review").css("display", "none"), $(".success-review").show()
            },
            fail: function () {
                $(".input-review").val(""), $(".submit-review").show(), $(".loading-review").css("display", "none"), $(".error-review").show(), setTimeout(function () {
                    $(".error-review").fadeOut()
                }, 2e3)
            },
            error: function (t) {
                $(".input-review").val(""), $(".submit-review").show(), $(".loading-review").hide(), $(".error-review").show(), setTimeout(function () {
                    $(".error-review").fadeOut()
                }, 2e3)
            }
        })
    }

    $("#star5").on("click", function () {
        setRate(5)
    }), $("#star4").on("click", function () {
        setRate(4)
    }), $("#star3").on("click", function () {
        setRate(3)
    }), $("#star2").on("click", function () {
        setRate(2)
    }), $("#star1").on("click", function () {
        setRate(1)
    }), $(".review-write").on("click", function (t) {
        t.stopPropagation()
    }), $("#darkmode").on("click", function () {
        $("body").addClass("dark-mode"), $("body").removeClass("light-mode"), $(this).hide(), $("#lightmode").show();
        $.ajax({
            data: {
                theme: "dark"
            },
            type: "post",
            url: baseUrl + "/ajax/theme/",
            success: function (t) {
            }
        })
    }), $("#lightmode").on("click", function () {
        $("body").addClass("light-mode"), $("body").removeClass("dark-mode"), $(this).hide(), $("#darkmode").show();
        $.ajax({
            data: {
                theme: "light"
            },
            type: "post",
            url: baseUrl + "/ajax/theme/",
            success: function (t) {
            }
        })
    }), $(".open-login").on("click", function () {
        return $(".login-full").show(), !1
    }), $(".notif-close").on("click", function () {
        $(".login-full").hide(), $(".serie-dialog").hide()
    }), $(".submit-review").on("click", function () {
        rate($(this).attr("type"))
    }), $(".submit-comment").on("click", function () {
        var t = $(".input-comment").val(),
            e = $(".input-comment").attr("alt"),
            i = {
                id: $(this).attr("alt"),
                comment: t,
                type: e
            };
        $(this).hide(), $(".loading-comment").show(), $.ajax({
            type: "post",
            data: i,
            url: baseUrl + "/ajax/comment/add.html",
            success: function (t) {
                var e = jQuery.parseJSON(t);
                $(".input-comment").val(""), $(".comment-list").append("<div class='comment-item'><a title='View profile' href='#'' class='avatar-thumb'><img alt='Mrigank_Gurudatt profile' src=" + e.image + "></a><div class='comment-text'><a>" + e.user + "</a><span class='float-right'><i class='fa fa-clock-o'></i> " + e.created + "</span><p>" + e.content + "</p></div></div>"), $(".comment-list").scrollTop($(".comment-list")[0].scrollHeight), $(".success-comment").show(), setTimeout(function () {
                    $(".success-comment").fadeOut()
                }, 2e3), $(".submit-comment").show(), $(".loading-comment").hide()
            },
            fail: function () {
                $(".input-comment").val(""), $(".submit-comment").show(), $(".loading-comment").hide(), $(".error-comment").show(), setTimeout(function () {
                    $(".error-comment").fadeOut()
                }, 2e3)
            },
            error: function (t) {
                $(".input-comment").val(""), $(".submit-comment").show(), $(".loading-comment").hide(), $(".error-comment").show(), setTimeout(function () {
                    $(".error-comment").fadeOut()
                }, 2e3)
            }
        })
    }), $(".season-btn").on("click", function () {
        var t = $(this).attr("alt");
        $(".season-btn-selected").html($(this).html()), $(".season-btn-selected").html($(this).html()), $(".serie-episodes-loading").show(), $(".serie-episodes").hide(), $.ajax({
            url: baseUrl + "/ajax/episodes/" + t + ".html",
            success: function (t) {
                $(".serie-episodes-loading").hide(), $(".serie-episodes").show(), $(".serie-episodes").html(t)
            }
        })
    }), $(function () {
        $(".flix-scroll-x").scroll(function () {
            var t = $(this).outerWidth(),
                e = $(this)[0].scrollWidth,
                i = $(this).scrollLeft();
            e - t === i ? $(this).prevAll(".next_btn").hide() : $(this).prevAll(".next_btn").show(), 0 === i ? $(this).prevAll(".prev_btn").hide() : $(this).prevAll(".prev_btn").show()
        })
    }), $("#myCarousel").carousel({
        interval: 3e3
    }), $(".carousel .carousel-item").each(function () {
        var t = $(this).next();
        t.length || (t = $(this).siblings(":first")), t.children(":first-child").clone().appendTo($(this));
        for (var e = 0; e < 4; e++) (t = t.next()).length || (t = $(this).siblings(":first")), t.children(":first-child").clone().appendTo($(this))
    });
})(jQuery);