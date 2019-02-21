$(function () {
    $("nav ul li").click(function () {
        let index=$(this).index()
        $("nav ul li").removeClass("select").eq(index).addClass("select")
        $("main .xxk").css({"z-index":"5","display":"none"}).eq(index).css({"z-index":"10","display":"block"})
    })
})