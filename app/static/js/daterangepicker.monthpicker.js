// /**
//  * 基于Date Range Picker的月份选择器扩展
//  * github：https://github.com/RidingACodeToStray/daterangepicker-monthrangepicker
//  * @param {起始时间} s 
//  * @param {终止时间} e 
//  * @param {最外层的div对象} classDom $('.s-timeRange')
//  * @param {内层的input对象} idDom $('.s-timePicker')
//  * @param {显示时间格式} sformat 
//  * @param {是否显示日历} showCalendars 
//  * @param {配置默认可选的时间范围} ranges 
//  * @param {是否展示自定义范围} scrl 
//  * @param {是否使用月份选择器} monthRange 
//  */   
var today = new Date(); 
var year=today.getFullYear();//本年的年份
var month=today.getMonth()+1;//本月的月份
var orderDate = year+'-'+month;  //现在的年份和月份

function datePicker(s,e,classDom,idDom,sformat,showCalendars,ranges,scrl,monthRange){
    if (!ranges) {
        ranges = {
            '今天': [moment(), moment()],
            '昨天': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            '近7天': [moment().subtract(6, 'days'), moment()],
            '近30天': [moment().subtract(29, 'days'), moment()],
            '本月': [moment().startOf('month'), moment().endOf('month')],
            '上月': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }
    var start = s || moment();
    var end = e || moment();
 
    function cb(start, end) {
        idDom.html(start.format(sformat) + " - " + end.format(sformat));  
    }
    idDom.val(start.format(sformat) + " ~ " + end.format(sformat))   
    
    classDom.daterangepicker({
            minDate:"2017-01",
            maxDate:orderDate,
            locale: {
                format: sformat,
                separator: '~',
                applyLabel: "应用",
                cancelLabel: "取消",
                resetLabel: "重置",
            },
            alwaysShowCalendars: showCalendars,
            showDropdowns: true,
            startDate: moment(),
            showCustomRangeLabel: scrl,
            endDate: moment(),
            opens: "right",
            ranges: 'ranges', 
    },cb);  
    cb(start, end); 
    
    if(monthRange){ 
        //修改日期选择器 
        $('div.calendar.left,div.calendar.right').empty().html('<div class="s-cal newdatamonth"><div class="s-calTitle"><div class="s-calLastYear"></div><div class="yearnum"><select></select></div><div class="s-calNextYear"></div></div><ul class="s-calMonth"><li data-month="01">一月</li><li data-month="02">二月</li><li data-month="03">三月</li><li data-month="04">四月</li><li data-month="05">五月</li><li data-month="06">六月</li><li data-month="07">七月</li><li data-month="08">八月</li><li data-month="09">九月</li><li data-month="10">十月</li><li data-month="11">十一月</li><li data-month="12">十二月</li></ul></div>');

        for (var y = 2017; y <= year; y++) {
            yearHtml = '<option value="' + y + '">' + y + '</option>'; 
            $('.s-calTitle .yearnum select').append(yearHtml) 
        }  
        var timePickerDom = idDom,
            sYearView = $($('.s-calTitle .yearnum select')[0]),
            eYearView = $($('.s-calTitle .yearnum select')[1]),
            monthViewLis = $('.s-calMonth > li'),
            sMonthViewLis = $($('.s-cal')[0]).find('.s-calMonth > li'),
            eMonthViewLis = $($('.s-cal')[1]).find('.s-calMonth > li'),
            tabs = $('div.daterangepicker > div.ranges'),
            tabs2 = $('div.daterangepicker > div.ranges.ranges_1'); 
        //缓存日期
        var tempSYear,
            tempEyear,
            tempSMonth,
            tempEMonth;
        //变换日历视图修改样式
        function changeView(isAngle){
            var currentSYear = sYearView.val();
            var currentEYear = eYearView.val();
            var isAngle = false;
            eMonthViewLis.removeClass('disabled');
            if(isAngle){
                //年份不一致判断
                if(currentSYear > currentEYear){ eMonthViewLis.addClass('disabled'); }
                if(currentSYear < currentEYear){ eMonthViewLis.removeClass('disabled'); }
                if(currentSYear == tempSYear){ sMonthViewLis.eq(tempSMonth).addClass('onFocus'); }
                if(currentEYear == tempEyear){ eMonthViewLis.eq(tempEMonth).addClass('onFocus'); } 
            }else{
                if(tempSMonth > tempEMonth){
                    //如果选中起始月份较大，则将日期赋值为起始月份  
                    if(currentSYear == currentEYear){
                        eMonthViewLis.removeClass('onFocus ');
                        eMonthViewLis.eq(tempSMonth).addClass('onFocus ');   
                    } 
                    putRangeDate();
                }
                eMonthViewLis.each(function(index){
                    if((index) == Number(tempSMonth)){ return false; }
                    $(this).addClass('disabled'); 
                    if(currentSYear < currentEYear){ eMonthViewLis.removeClass('disabled'); }
                    if(currentSYear > currentEYear){ eMonthViewLis.addClass('disabled'); }
                })
            }   
        }
        $('.s-cal').find(".s-calMonth > li").removeClass('onFocus light_colour')
        $('.s-cal').find(".s-calMonth > li.active").addClass('onFocus')
        $($('.s-cal')[1]).find(".s-calMonth > li.onFocus").prevAll().addClass("disabled") 
 
        //生成日期
        function putRangeDate(){ 
            var sYearDate = $($('.s-cal')[0]).find('.s-calTitle .yearnum select').val();
            var sMonthDate = $($('.s-cal')[0]).find('.s-calMonth > li.onFocus').data('month');
            var eYearDate = $($('.s-cal')[1]).find('.s-calTitle .yearnum select').val();
            var eMonthDate = $($('.s-cal')[1]).find('.s-calMonth > li.onFocus').data('month');
            tempSYear = sYearDate;
            tempEyear = eYearDate;
            tempSMonth = Number(sMonthDate) - 1;
            tempEMonth = Number(eMonthDate) - 1;
            timePickerDom.val(sYearDate+'-'+sMonthDate+'~'+eYearDate+'-'+eMonthDate); 
            $(".newdatamonth").parents(".daterangepicker").find(".calendar_1 input").val(sYearDate+'-'+sMonthDate)
            $(".newdatamonth").parents(".daterangepicker").find(".calendar_2 input").val(eYearDate+'-'+eMonthDate)
            $($('.s-cal')[0]).find(".s-calMonth > li.onFocus").nextAll().addClass("light_colour") 
            $($('.s-cal')[0]).find(".s-calMonth > li.onFocus").prevAll().removeClass("light_colour") 
            $($('.s-cal')[1]).find(".s-calMonth > li.onFocus").prevAll().addClass("light_colour") 
            $($('.s-cal')[1]).find(".s-calMonth > li.onFocus").nextAll().removeClass("light_colour") 
            if(sYearView.val() == eYearView.val()){
                $($('.s-cal')[1]).find(".s-calMonth > li.onFocus").nextAll().each(function(){
                   var attrNUM = $(this).attr("data-month") 
                   $($('.s-cal')[0]).find(".s-calMonth > li[data-month ='"+attrNUM+"' ]").removeClass("light_colour")
               })
            } 
            changeView();  
        }
        
        //给View赋值样式
        function putDateView(sy,ey,sm,em){      
            sy && sYearView.val(sy);//赋值起始年份
            ey && eYearView.val(ey);//赋值终止年份    
            sm && sMonthViewLis.eq(sm).addClass('onFocus active');//高亮起始月份
            em && eMonthViewLis.eq(em).addClass('onFocus active'); //高亮终止月份 
        }
        //取日期给View赋值样式
        function getRangeDate(){  
            var datePeriod = timePickerDom.text().split(' - ');
            var sDate = datePeriod[0].split('-'); //起始年月
            var eDate = datePeriod[1].split('-'); //终止年月
            tempSYear = sDate[0];
            tempEyear = eDate[0];
            tempSMonth = Number(sDate[1]) - 1;
            tempEMonth = Number(eDate[1]) - 1; 
            putDateView(tempSYear,tempEyear,tempSMonth,tempEMonth);  
        } 
        getRangeDate(); 
        changeView();
        
        //前一年
        $('.s-calLastYear').click(function(e){ 
            $(e.target).nextAll('.s-calNextYear').css({"cursor":"pointer","opacity":"1"}) 
            var startDateDom = $(e.target).next('.yearnum').children("select"); 
            console.log($(e.target).attr("class"))
            if(startDateDom.val()  <=  2018){
                startDateDom.val(2017) 
                $(this).css({"cursor":"not-allowed","opacity":"0.5"}) 
            }else{  
                startDateDom.val(Number(startDateDom.val()) - 1)
                $(this).css({"cursor":"pointer","opacity":"1"}) 
            } 
            // $(this).parents('.s-cal').find('.s-calMonth > li').removeClass('onFocus light_colour');
            changeView(true);
        })
        //后一年
        $('.s-calNextYear').click(function(e){ 
            $(e.target).prevAll('.s-calLastYear').css({"cursor":"pointer","opacity":"1"}) 
            var startDateDom = $(e.target).prev('.yearnum').children("select"); 
            console.log($(e.target).attr("class"))
            if(startDateDom.val()  >=  ( year - 1 )){
                startDateDom.val(year)
                $(this).css({"cursor":"not-allowed","opacity":"0.5"}) 
            }else{  
                startDateDom.val(Number(startDateDom.val()) + 1) 
                $(this).css({"cursor":"pointer","opacity":"1"})
            } 
            // $(this).parents('.s-cal').find('.s-calMonth > li').removeClass('onFocus light_colour');
            changeView(true); 
        })
        //选中月份
        monthViewLis.click(function(){
            tabs.removeClass('active'); 
            // lastTab.addClass('active');
            //两个if处理使用箭头移动导致都没有选中月份的情况
            if(!sMonthViewLis.hasClass('onFocus')){
                sMonthViewLis.eq(0).addClass('onFocus');
            }
            if(!eMonthViewLis.hasClass('onFocus')){
                eMonthViewLis.eq(0).addClass('onFocus');
            }
            $(this).parents('.s-cal').find('.s-calMonth > li').removeClass('onFocus');
            $(this).addClass('onFocus');
            putRangeDate();
        }) 

        //下拉选择年份
        $('.s-calTitle .yearnum select').click(function(){
            changeView()
            putRangeDate()
            if($(this).val() == 2017){
                $(this).parent().prev().css({"cursor":"not-allowed","opacity":"0.5"})
            }else{
                $(this).parent().prev().css({"cursor":"pointer","opacity":"1"})
            } 
            if($(this).val() == year){
                $(this).parent().next().css({"cursor":"not-allowed","opacity":"0.5"})
            }else{
                $(this).parent().next().css({"cursor":"pointer","opacity":"1"})
            } 
        }) 
        
        tabs.hide();
        tabs2.show(); 

        //给月份段选择器添加单独的class
        $(".newdatamonth").parents(".daterangepicker").addClass("monthpicker") ;   

        // 获取右下角input输入框的内容赋值给时间框
        function timefu(){
            var sYearDate = $($('.s-cal')[0]).find('.s-calTitle .yearnum select').val();
            var sMonthDate = $($('.s-cal')[0]).find('.s-calMonth > li.onFocus').data('month');
            var eYearDate = $($('.s-cal')[1]).find('.s-calTitle .yearnum select').val();
            var eMonthDate = $($('.s-cal')[1]).find('.s-calMonth > li.onFocus').data('month');
            timePickerDom.val(sYearDate+'-'+sMonthDate+'~'+eYearDate+'-'+eMonthDate); 
        }
 
        // 底部左边input输入 失去焦点和按下回车
        function tianjia(e){
            var gshdata =  e.val().replace(/[^0-9]/ig,""); 
            var monthnum6 = gshdata.substring(4, 6)  
            var monthnum4 = gshdata.substring(0, 4)
            var twomonth = $($('.s-cal')[1]).find(".s-calMonth > li.onFocus").attr("data-month")
            $($('.s-calTitle .yearnum select')[0]).val(monthnum4) 
            $($('.s-cal')[0]).find(".s-calMonth > li[data-month ='"+monthnum6+"' ]").addClass("onFocus light_colour").siblings().removeClass("onFocus light_colour")
            $($('.s-cal')[0]).find(".s-calMonth > li.onFocus").nextAll().addClass("light_colour").removeClass("active")
            $($('.s-cal')[0]).find(".s-calMonth > li.onFocus").prevAll().removeClass("light_colour").removeClass("active")  
            $($('.s-cal')[1]).find(".s-calMonth > li.onFocus").removeClass("active")

            // 如果两边年份相等
            if( Number(monthnum4) == Number($($('.s-calTitle .yearnum select')[1]).val())){
                changeView()  
                $($('.s-cal')[1]).find(".s-calMonth > li[data-month ='"+monthnum6+"' ]").addClass("light_colour").removeClass("disabled ").nextAll().removeClass("disabled ").addClass("light_colour")
                $($('.s-cal')[1]).find(".s-calMonth > li[data-month ='"+monthnum6+"' ]").prevAll().removeClass("light_colour").addClass("disabled ")
                $($('.s-cal')[1]).find(".s-calMonth > li.onFocus").nextAll().removeClass("light_colour") 
                $($('.s-cal')[0]).find(".s-calMonth > li[data-month ='"+twomonth+"' ]").nextAll().removeClass("light_colour") 
            }else{ 
                $($('.s-cal')[1]).find(".s-calMonth > li").removeClass("disabled") 
                $($('.s-cal')[1]).find(".s-calMonth > li.onFocus").prevAll().addClass("light_colour") 
            } 

            // 判断输入的年份  五段  
            if( Number(monthnum4) == 2017){
                $($('.s-calTitle .yearnum select')[0]).parent().prev().css({"cursor":"not-allowed","opacity":"0.5"})
            }else if(Number(monthnum4) == year){
                $($('.s-calTitle .yearnum select')[0]).parent().next().css({"cursor":"not-allowed","opacity":"0.5"})
            }else if(Number(monthnum4) < 2017){ 
                e.val( 2017 + "-" + e.val().substring(5, 7))  
                $($('.s-calTitle .yearnum select')[0]).val(2017).parent().prev().css({"cursor":"not-allowed","opacity":"0.5"})
            }else if(Number(monthnum4) > year){
                e.val( year + "-" + e.val().substring(5, 7))  
                $($('.s-calTitle .yearnum select')[0]).val(year).parent().next().css({"cursor":"not-allowed","opacity":"0.5"}) 
            }else{
                $($('.s-calTitle .yearnum select')[0]).parent().siblings().css({"cursor":"pointer","opacity":"1"}) 
            } 
            timefu()
        } 

        // 底部右边input输入 失去焦点和按下回车
        function tianjia2(e){
            var gshdata =  e.val().replace(/[^0-9]/ig,""); 
            var monthnum6 = gshdata.substring(4, 6)  
            var monthnum4 = gshdata.substring(0, 4)
            var twomonth = $($('.s-cal')[0]).find(".s-calMonth > li.onFocus").attr("data-month")
            $($('.s-calTitle .yearnum select')[1]).val(monthnum4)
            $($('.s-cal')[1]).find(".s-calMonth > li[data-month ='"+monthnum6+"' ]").addClass("onFocus light_colour").siblings().removeClass("onFocus active") 
            $($('.s-cal')[1]).find(".s-calMonth > li.onFocus").prevAll().addClass("light_colour")
            $($('.s-cal')[1]).find(".s-calMonth > li.onFocus").nextAll().removeClass("light_colour")
            // 如果两边年份相等
            if( Number(monthnum4) == Number($($('.s-calTitle .yearnum select')[0]).val())){ 
                $($('.s-cal')[0]).find(".s-calMonth > li[data-month ='"+monthnum6+"' ]").nextAll().removeClass("light_colour") 
                $($('.s-cal')[1]).find(".s-calMonth > li[data-month ='"+twomonth+"' ]").prevAll().removeClass("light_colour").addClass("disabled") 
            }  

            // 判断输入的年份  五段  
            if( Number(monthnum4) == 2017){
                $($('.s-calTitle .yearnum select')[1]).parent().prev().css({"cursor":"not-allowed","opacity":"0.5"})
            }else if(Number(monthnum4) == year){
                $($('.s-calTitle .yearnum select')[1]).parent().next().css({"cursor":"not-allowed","opacity":"0.5"})
            }else if(Number(monthnum4) < 2017){
                e.val( 2017 + "-" + e.val().substring(5, 7))  
                $($('.s-calTitle .yearnum select')[1]).val(2017).parent().prev().css({"cursor":"not-allowed","opacity":"0.5"})
            }else if(Number(monthnum4) > year){
                e.val( year + "-" + e.val().substring(5, 7))  
                $($('.s-calTitle .yearnum select')[1]).val(year).parent().next().css({"cursor":"not-allowed","opacity":"0.5"}) 
            }else{
                $($('.s-calTitle .yearnum select')[1]).parent().siblings().css({"cursor":"pointer","opacity":"1"})  
            }  
            timefu() 
        } 

        // 底部左边input  
        $(".monthpicker").find(".calendar_1").children().children("input").blur(function(){  
            tianjia($(this))
        })
        $(".monthpicker").find(".calendar_1").children().children("input").keydown(function(){ 
            if(event.keyCode==13){ 
                tianjia($(this))
            } 
             
        }) 
        // 底部右边input  
        $(".monthpicker").find(".calendar_2").children().children("input").blur(function(){ 
            tianjia2($(this))  
        })
        $(".monthpicker").find(".calendar_2").children().children("input").keydown(function(){ 
            if(event.keyCode==13){ 
                tianjia($(this))
            } 
        }) 

         
        //重置按钮按下
        $(".monthpicker").find(".resetBtn").click(function(){
            idDom.val("")
        })   
    }
}; 