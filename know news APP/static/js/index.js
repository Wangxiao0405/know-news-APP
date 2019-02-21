$(function () {
    $(".iBox").click(function () {
        $(".meau").slideDown()
        $("body").css("overflow","hidden")
    });
    $(".icon-cuohao1").click(function () {
        $(".meau").slideUp()
        $("body").css("overflow","auto")
    })
    $("#search").click(function () {
        $(".search_yemian").css("display","block")
    });
    $(".icon-fanhui").click(function () {
        $(".search_yemian").css("display","none")
    })
    let time=0;
    $(".camerabox").click(function () {

        time++;
        if (time%2!=0) {
            $(".huiBox").css("display","block")
        }else if(time%2==0){
            $(".huiBox").css("display","none")
        }

    })
    $("nav ul li").click(function () {
        let index=$(this).index()
        $("nav ul a li")
        .css("color","black")
        .eq(index)
        .css("color","red")

    })
    $("footer ul li").click(function () {
        let index=$(this).index()
        $("footer ul li").css("color","black").eq(index).css("color","red")

    })

})