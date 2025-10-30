(function(root, factory) {
  	if (typeof define === 'function' && define.amd) {
            define(['moment', 'jquery', 'exports'], 
            function(momentjs, $, exports) {
		      root.daterangepicker = factory(root, exports, momentjs, $);
		    });
		} else if (typeof exports !== 'undefined') {
      	var momentjs = require('moment');
      	var jQuery = (typeof window != 'undefined') ? window.jQuery: undefined; 
      	if (!jQuery) {
          try {
              jQuery = require('jquery');
              if (!jQuery.fn) jQuery.fn = {};
          } catch(err) {
              if (!jQuery) throw new Error('jQuery dependency not found');
          }
      }
    factory(root, exports, momentjs, jQuery);
  // 最后，作为一个浏览器全局。
  } else {
    root.daterangepicker = factory(root, {}, 
        root.moment || moment, (root.jQuery || root.Zepto || root.ender || root.$));
  }
} (this || {},
    function(root, daterangepicker, moment, $) { 
    //服务器上不存在“this”
    var DateRangePicker = function(element, options, cb) {
        //选项的默认设置
        this.parentEl = 'body';
        this.element = $(element);
        this.startDate = moment().startOf('day');
        this.endDate = moment().endOf('day');
        this.minDate = true; 
        this.maxDate = true; 
        this.dateLimit = false;
        this.autoApply = false;
        this.singleDatePicker = false;
        this.showDropdowns = true;
        this.showWeekNumbers = false;
        this.showISOWeekNumbers = false;
        this.timePicker = false;
        this.timePicker24Hour = false;
        this.timePickerIncrement = 1;
        this.timePickerSeconds = false;
        this.linkedCalendars = true;
        this.autoUpdateInput = true;
        this.alwaysShowCalendars = false;
        this.ranges = {};
        this.opens = 'right';
        if (this.element.hasClass('pull-right')) this.opens = 'left';
        this.drops = 'down';
        if (this.element.hasClass('dropup')) this.drops = 'up';
        this.buttonClasses = 'btn btn-sm';
        this.applyClass = 'btn-success';
        this.cancelClass = 'btn-default';
        this.locale = {
            format: 'YYYY/MM/DD',
            separator: ' - ',
            applyLabel: '确定',
            cancelLabel: '取消',
            resetLabel: '重置',
            weekLabel: 'W',
            customRangeLabel: '自定义',
            daysOfWeek: moment.weekdaysMin(),
            monthNames: moment.monthsShort(),
            firstDay: moment.localeData().firstDayOfWeek(),
            daysOfWeek:["日","一","二","三","四","五","六"],
            monthNames: ["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"]
        };
        this.callback = function() {};
        //一些状态信息
        this.isShowing = false;
        this.leftCalendar = {};
        this.rightCalendar = {};
        //来自用户的自定义选项
        if (typeof options !== 'object' || options === null) options = {};
        //允许使用数据属性设置选项
        //数据api选项将被自定义javascript选项覆盖
        options = $.extend(this.element.data(), options);
        //选择器UI的html模板
        if (typeof options.template !== 'string' && !(options.template instanceof $))
            options.template = '<div class="daterangepicker dropdown-menu">' +
                                    '<div class="ranges">' +
                                    '</div>' +
                                    '<div class="calendar left">' +
                                    	'<div class="prev_year">  <img src="zuojian2.png" border="0" width="16" style=" margin-top:7px" /> </div>'+
                                        '<div class="calendar-table">' +
                                        '</div>' +
                                    '</div>' +
                                    '<div class="calendar right">' +
                                    		'<div class="prev_month"> <img src="youjian2.png" border="0" width="16" style=" margin-top:7px" /> </div>'+
                                        '<div class="calendar-table"></div>' +
                                    '</div>' +
                                    '<div class="calendar calendar_1">' +
                                        '<div class="daterangepicker_input">' +
                                            '<input class="input-mini" type="text" name="daterangepicker_start" value="" />' +
                                            '<div class="calendar-time">' +
                                                '<div></div>'+
                                                '<i class="fa fa-clock-o glyphicon glyphicon-time"></i>' +
                                            '</div>' +
                                        '</div>' +
                                    '</div>' +
                                    '<div class="calendar calendar_2">' +
                                        '<div class="daterangepicker_input">' +
                                            '<input class="input-mini" type="text" name="daterangepicker_end" value="" />' +
                                            '<div class="calendar-time">' +
                                                '<div></div>' +
                                                '<i class="fa fa-clock-o glyphicon glyphicon-time"></i>' +
                                            '</div>' +
                                        '</div>' +
                                    '</div>' +
                                    '<div class="ranges ranges_1">' +
                                        '<div class="range_inputs">' +
                                            '<button class="applyBtn" disabled="disabled" type="button"></button> <button class="cancelBtn" type="button"></button> <button class="resetBtn" type="button"></button>' +
                                        '</div>' +
                                    '</div>' +
                                    '<div class="line_date"></div>'+
                                    '<div class="line_date_2"></div>'+
                                    '<div class="all">全部日期</div>'+
                                '</div>';
        this.parentEl = (options.parentEl && $(options.parentEl).length) ? $(options.parentEl) : $(this.parentEl);
        this.container = $(options.template).appendTo(this.parentEl);
        // 处理所有可能覆盖默认值的选项 
        if (typeof options.locale === 'object') {
            if (typeof options.locale.format === 'string') this.locale.format = options.locale.format;
            if (typeof options.locale.separator === 'string') this.locale.separator = options.locale.separator;
            if (typeof options.locale.daysOfWeek === 'object') this.locale.daysOfWeek = options.locale.daysOfWeek.slice();
            if (typeof options.locale.monthNames === 'object') this.locale.monthNames = options.locale.monthNames.slice();
            if (typeof options.locale.firstDay === 'number') this.locale.firstDay = options.locale.firstDay; 
            if (typeof options.locale.applyLabel === 'string') this.locale.applyLabel = options.locale.applyLabel;
            if (typeof options.locale.cancelLabel === 'string') this.locale.cancelLabel = options.locale.cancelLabel;
            if (typeof options.locale.resetLabel === 'string') this.locale.resetLabel = options.locale.resetLabel;
            if (typeof options.locale.weekLabel === 'string') this.locale.weekLabel = options.locale.weekLabel;
            if (typeof options.locale.customRangeLabel === 'string') this.locale.customRangeLabel = options.locale.customRangeLabel;
        }
        if (typeof options.startDate === 'string') this.startDate = moment(options.startDate, this.locale.format);
        if (typeof options.endDate === 'string') this.endDate = moment(options.endDate, this.locale.format);
        if (typeof options.minDate === 'string') this.minDate = moment(options.minDate, this.locale.format);
        if (typeof options.maxDate === 'string') this.maxDate = moment(options.maxDate, this.locale.format);
        if (typeof options.startDate === 'object') this.startDate = moment(options.startDate);
        if (typeof options.endDate === 'object') this.endDate = moment(options.endDate);
        if (typeof options.minDate === 'object') this.minDate = moment(options.minDate);
        if (typeof options.maxDate === 'object') this.maxDate = moment(options.maxDate);
        if (this.minDate && this.startDate.isBefore(this.minDate)) this.startDate = this.minDate.clone();
        // 检查不正确的选项
        if (this.maxDate && this.endDate.isAfter(this.maxDate)) this.endDate = this.maxDate.clone();
        if (typeof options.applyClass === 'string') this.applyClass = options.applyClass;
        if (typeof options.cancelClass === 'string') this.cancelClass = options.cancelClass;
        if (typeof options.dateLimit === 'object') this.dateLimit = options.dateLimit;
        if (typeof options.opens === 'string') this.opens = options.opens;
        if (typeof options.drops === 'string') this.drops = options.drops;
        if (typeof options.showWeekNumbers === 'boolean') this.showWeekNumbers = options.showWeekNumbers;
        if (typeof options.showISOWeekNumbers === 'boolean') this.showISOWeekNumbers = options.showISOWeekNumbers;
        if (typeof options.buttonClasses === 'string') this.buttonClasses = options.buttonClasses;
        if (typeof options.buttonClasses === 'object') this.buttonClasses = options.buttonClasses.join(' ');
        if (typeof options.showDropdowns === 'boolean') this.showDropdowns = options.showDropdowns;
        if (typeof options.singleDatePicker === 'boolean') {
            this.singleDatePicker = options.singleDatePicker;
            if (this.singleDatePicker) this.endDate = this.startDate.clone();
        }
        if (typeof options.timePicker === 'boolean') this.timePicker = options.timePicker;
        if (typeof options.timePickerSeconds === 'boolean') this.timePickerSeconds = options.timePickerSeconds;
        if (typeof options.timePickerIncrement === 'number') this.timePickerIncrement = options.timePickerIncrement;
        if (typeof options.timePicker24Hour === 'boolean') this.timePicker24Hour = options.timePicker24Hour;
        if (typeof options.autoApply === 'boolean') this.autoApply = options.autoApply;
        if (typeof options.autoUpdateInput === 'boolean') this.autoUpdateInput = options.autoUpdateInput;
        if (typeof options.linkedCalendars === 'boolean') this.linkedCalendars = options.linkedCalendars;
        if (typeof options.isInvalidDate === 'function') this.isInvalidDate = options.isInvalidDate;
        if (typeof options.alwaysShowCalendars === 'boolean') this.alwaysShowCalendars = options.alwaysShowCalendars;
        // 将日期名称顺序更新为firstDay
        if (this.locale.firstDay != 0) {
            var iterator = this.locale.firstDay;
            while (iterator > 0) {
                this.locale.daysOfWeek.push(this.locale.daysOfWeek.shift());
                iterator--;
            }
        }
        var start, end, range;
        //如果没有设置开始/结束日期，请检查输入元素是否包含初始值
        if (typeof options.startDate === 'undefined' && typeof options.endDate === 'undefined') {
            if ($(this.element).is('input[type=text]')) {
                var val = $(this.element).val(),
                    split = val.split(this.locale.separator);
                start = end = null;
                if (split.length == 2) {
                    start = moment(split[0], this.locale.format);
                    end = moment(split[1], this.locale.format);
                } else if (this.singleDatePicker && val !== "") {
                    start = moment(val, this.locale.format);
                    end = moment(val, this.locale.format);
                }
                if (start !== null && end !== null) {
                    this.setStartDate(start);
                    this.setEndDate(end);
                }
            }
        }
        if (typeof options.ranges === 'object') {
            for (range in options.ranges) {
                if (typeof options.ranges[range][0] === 'string') start = moment(options.ranges[range][0], this.locale.format);
                else start = moment(options.ranges[range][0]);
                if (typeof options.ranges[range][1] === 'string') end = moment(options.ranges[range][1], this.locale.format);
                else end = moment(options.ranges[range][1]);
                //如果开始或结束日期超过了minDate或dateLimit允许的日期
                //选项，将范围缩短到允许的周期。
                if (this.minDate && start.isBefore(this.minDate)) start = this.minDate.clone();
                var maxDate = this.maxDate;
                if (this.dateLimit && start.clone().add(this.dateLimit).isAfter(maxDate)) maxDate = start.clone().add(this.dateLimit);
                if (maxDate && end.isAfter(maxDate)) end = maxDate.clone();
                //如果范围的结束在最小值之前或范围的开始是
                //在最大值之后，根本不显示此范围选项。
                if ((this.minDate && end.isBefore(this.minDate)) || (maxDate && start.isAfter(maxDate))) continue;
                //字符范围支持unicode名称。
                var elem = document.createElement('textarea');
                elem.innerHTML = range;
                var rangeHtml = elem.value;
                this.ranges[rangeHtml] = [start, end];
            }
            var list = '<ul>';
            for (range in this.ranges) {
                list += '<li>' + range + '</li>';
            }
//          list += '<li>' + this.locale.customRangeLabel + '</li>';
            list += '</ul>';
            this.container.find('.ranges').prepend(list);
        }
        if (typeof cb === 'function') {
            this.callback = cb;
        }
        if (!this.timePicker) {
            this.startDate = this.startDate.startOf('day');
            this.endDate = this.endDate.endOf('day');
            this.container.find('.calendar-time').hide();
        }
        //暂时不能一起使用
        if (this.timePicker && this.autoApply) this.autoApply = false;
        if (this.autoApply && typeof options.ranges !== 'object') {
            this.container.find('.ranges').hide();
        } else if (this.autoApply) {
            this.container.find('.applyBtn, .cancelBtn, .resetBtn').addClass('hide');
        }
        if (this.singleDatePicker) {
            this.container.addClass('single');
            this.container.find('.calendar.left').addClass('single');
            this.container.find('.calendar.left').show();
            this.container.find('.calendar.right').hide();
            this.container.find('.daterangepicker_input input, .daterangepicker_input i').hide();
            if (!this.timePicker) {
                this.container.find('.ranges').hide();
            }
        }
        if ((typeof options.ranges === 'undefined' && !this.singleDatePicker) || this.alwaysShowCalendars) {
            this.container.addClass('show-calendar');
        }
        this.container.addClass('opens' + this.opens);
        //如果向右打开，则交换预定义范围的位置
        if (typeof options.ranges !== 'undefined' && this.opens == 'right') {
            var ranges = this.container.find('.ranges');
            var html = ranges.clone();
            ranges.remove();
            this.container.find('.calendar.left').parent().prepend(html);
        }
        //将CSS类和标签应用于按钮
        this.container.find('.applyBtn, .cancelBtn, .resetBtn').addClass(this.buttonClasses);
        if (this.applyClass.length) this.container.find('.applyBtn').addClass(this.applyClass);
        if (this.cancelClass.length) this.container.find('.cancelBtn').addClass(this.cancelClass);
        this.container.find('.applyBtn').html(this.locale.applyLabel);
        this.container.find('.cancelBtn').html(this.locale.cancelLabel);
        this.container.find('.resetBtn').html(this.locale.resetLabel);
        //  事件监听器 
        this.container.find('.calendar')
            .on('click.daterangepicker', '.prev', $.proxy(this.clickPrev, this))
            .on('click.daterangepicker', '.next', $.proxy(this.clickNext, this))
            .on('click.daterangepicker', '.prev_year', $.proxy(this.clickPrevYear, this))
            .on('click.daterangepicker', '.prev_month', $.proxy(this.clickNextYear, this))
            .on('click.daterangepicker', 'td.available', $.proxy(this.clickDate, this))
            .on('mouseenter.daterangepicker', 'td.available', $.proxy(this.hoverDate, this))
            // .on('mouseleave.daterangepicker', 'td.available', $.proxy(this.updateFormInputs, this))
            .on('change.daterangepicker', 'select.yearselect', $.proxy(this.monthOrYearChanged, this))
            .on('change.daterangepicker', 'select.monthselect', $.proxy(this.monthOrYearChanged, this))
            .on('change.daterangepicker', 'select.hourselect,select.minuteselect,select.secondselect,select.ampmselect', $.proxy(this.timeChanged, this))
            .on('click.daterangepicker', '.daterangepicker_input input', $.proxy(this.showCalendars, this))
            //.on('keyup.daterangepicker', '.daterangepicker_input input', $.proxy(this.formInputsChanged, this))
            .on('change.daterangepicker', '.daterangepicker_input input', $.proxy(this.formInputsChanged, this));
        this.container.find('.ranges')
            .on('click.daterangepicker', 'button.applyBtn', $.proxy(this.clickApply, this))
            .on('click.daterangepicker', 'button.cancelBtn', $.proxy(this.clickCancel, this))
            .on('click.daterangepicker', 'button.resetBtn', $.proxy(this.clickReset, this))
            .on('click.daterangepicker', 'li', $.proxy(this.clickRange, this))
//            .on('mouseenter.daterangepicker', 'li', $.proxy(this.hoverRange, this))
//            .on('mouseleave.daterangepicker', 'li', $.proxy(this.updateFormInputs, this));
        if (this.element.is('input')) {
            this.element.on({
                'click.daterangepicker': $.proxy(this.show, this),
                'focus.daterangepicker': $.proxy(this.show, this),
                'keyup.daterangepicker': $.proxy(this.elementChanged, this),
                'keydown.daterangepicker': $.proxy(this.keydown, this)
            });
        } else {
            this.element.on('click.daterangepicker', $.proxy(this.toggle, this));
        }
        // 如果附加到文本输入，请设置初始值
        if (this.element.is('input') && !this.singleDatePicker && this.autoUpdateInput) {
            this.element.val(this.startDate.format(this.locale.format) + this.locale.separator + this.endDate.format(this.locale.format));
            this.element.trigger('change');
        } else if (this.element.is('input') && this.autoUpdateInput) {
            this.element.val(this.startDate.format(this.locale.format));
            this.element.trigger('change');
        }
    };
    DateRangePicker.prototype = {
        constructor: DateRangePicker,
        setStartDate: function(startDate) {
     		//console.log('我是第1个方法');
            if (typeof startDate === 'string') this.startDate = moment(startDate, this.locale.format);
            if (typeof startDate === 'object') this.startDate = moment(startDate);
            if (!this.timePicker) this.startDate = this.startDate.startOf('day');
            if (this.timePicker && this.timePickerIncrement) this.startDate.minute(Math.round(this.startDate.minute() / this.timePickerIncrement) * this.timePickerIncrement);
            if (this.minDate && this.startDate.isBefore(this.minDate)) this.startDate = this.minDate;
            if (this.maxDate && this.startDate.isAfter(this.maxDate)) this.startDate = this.maxDate;
            if (!this.isShowing) this.updateElement();
            this.updateMonthsInView();
        },
        setEndDate: function(endDate) {
        	//console.log('我是第2个方法');
            if (typeof endDate === 'string') this.endDate = moment(endDate, this.locale.format);
            if (typeof endDate === 'object') this.endDate = moment(endDate);
            if (!this.timePicker) this.endDate = this.endDate.endOf('day');
            if (this.timePicker && this.timePickerIncrement) this.endDate.minute(Math.round(this.endDate.minute() / this.timePickerIncrement) * this.timePickerIncrement);
            if (this.endDate.isBefore(this.startDate)) this.endDate = this.startDate.clone();
            if (this.maxDate && this.endDate.isAfter(this.maxDate)) this.endDate = this.maxDate;
            if (this.dateLimit && this.startDate.clone().add(this.dateLimit).isBefore(this.endDate)) this.endDate = this.startDate.clone().add(this.dateLimit);
            this.previousRightTime = this.endDate.clone();
            if (!this.isShowing) this.updateElement();
            this.updateMonthsInView();
        },
        isInvalidDate: function() {
            return false;
        },
        updateView: function() {
        	//页面点击显示日历后的第三个方法，
       		//console.log('我是第3个方法');
            if (this.timePicker) {
                this.renderTimePicker('left');
                this.renderTimePicker('right');
                if (!this.endDate) {
                    this.container.find('.right .calendar-time select').attr('disabled', 'disabled').addClass('disabled');
                } else {
                    this.container.find('.right .calendar-time select').removeAttr('disabled').removeClass('disabled');
                }
            }
            if (this.endDate) {
                this.container.find('input[name="daterangepicker_end"]').removeClass('active');
                this.container.find('input[name="daterangepicker_start"]').addClass('active');
            } else {
                this.container.find('input[name="daterangepicker_end"]').addClass('active');
                this.container.find('input[name="daterangepicker_start"]').removeClass('active');
            }
            this.updateMonthsInView();
            this.updateCalendars();
            this.updateFormInputs();
        },
        updateMonthsInView: function() {
        	//页面点击显示日历后的第四个方法，如果有结束日期，或者没有结束日期
       		//console.log('我是第4个方法');
            if (this.endDate) {
                //如果两个日期都已可见，则不执行任何操作
                if (!this.singleDatePicker && this.leftCalendar.month && this.rightCalendar.month && (this.startDate.format('YYYY-MM') == this.leftCalendar.month.format('YYYY-MM') || this.startDate.format('YYYY-MM') == this.rightCalendar.month.format('YYYY-MM')) && (this.endDate.format('YYYY-MM') == this.leftCalendar.month.format('YYYY-MM') || this.endDate.format('YYYY-MM') == this.rightCalendar.month.format('YYYY-MM'))) {
                    return;
                }
                this.leftCalendar.month = this.startDate.clone().date(2);
                if (!this.linkedCalendars && (this.endDate.month() != this.startDate.month() || this.endDate.year() != this.startDate.year())) {
                    this.rightCalendar.month = this.endDate.clone().date(2);
                } else {
                    this.rightCalendar.month = this.startDate.clone().date(2).add(1, 'month');
                }
            } else {
                if (this.leftCalendar.month.format('YYYY-MM') != this.startDate.format('YYYY-MM') && this.rightCalendar.month.format('YYYY-MM') != this.startDate.format('YYYY-MM')) {
                    this.leftCalendar.month = this.startDate.clone().date(2);
                    this.rightCalendar.month = this.startDate.clone().date(2).add(1, 'month');
                }
            }
        },
        updateCalendars: function() {
        	//是否显示小时
        	//console.log('我是第5个方法');
            if (this.timePicker) {
                var hour, minute, second;
                if (this.endDate) {
                    hour = parseInt(this.container.find('.left .hourselect').val(), 10);
                    minute = parseInt(this.container.find('.left .minuteselect').val(), 10);
                    second = this.timePickerSeconds ? parseInt(this.container.find('.left .secondselect').val(), 10) : 0;
                    if (!this.timePicker24Hour) {
                        var ampm = this.container.find('.left .ampmselect').val();
                        if (ampm === 'PM' && hour < 12) hour += 12;
                        if (ampm === 'AM' && hour === 12) hour = 0;
                    }
                } else {
                    hour = parseInt(this.container.find('.right .hourselect').val(), 10);
                    minute = parseInt(this.container.find('.right .minuteselect').val(), 10);
                    second = this.timePickerSeconds ? parseInt(this.container.find('.right .secondselect').val(), 10) : 0;
                    if (!this.timePicker24Hour) {
                        var ampm = this.container.find('.right .ampmselect').val();
                        if (ampm === 'PM' && hour < 12) hour += 12;
                        if (ampm === 'AM' && hour === 12) hour = 0;
                    }
                }
                this.leftCalendar.month.hour(hour).minute(minute).second(second);
                this.rightCalendar.month.hour(hour).minute(minute).second(second);
            }
            this.renderCalendar('left');
            this.renderCalendar('right');
            //突出显示与当前开始日期和结束日期匹配的任何预定义范围
            this.container.find('.ranges li').removeClass('active');
            if (this.endDate == null) return;
            this.calculateChosenLabel();
        },
        renderCalendar: function(side) {
        	//页面初始怎么显示，显示选择哪个日期
        	//console.log('我是第6个方法');
            //构建将填充日历的日期矩阵
            var calendar = side == 'left' ? this.leftCalendar: this.rightCalendar;
            var month = calendar.month.month();
            var year = calendar.month.year();
            var hour = calendar.month.hour();
            var minute = calendar.month.minute();
            var second = calendar.month.second();
            var daysInMonth = moment([year, month]).daysInMonth();
            var firstDay = moment([year, month, 1]);
            var lastDay = moment([year, month, daysInMonth]);
            var lastMonth = moment(firstDay).subtract(1, 'month').month();
            var lastYear = moment(firstDay).subtract(1, 'month').year();
            var daysInLastMonth = moment([lastYear, lastMonth]).daysInMonth();
            var dayOfWeek = firstDay.day();
            //初始化日历的6行x 7列数组
            var calendar = [];
            calendar.firstDay = firstDay;
            calendar.lastDay = lastDay;
            for (var i = 0; i < 6; i++) {
                calendar[i] = [];
            } 
            //用日期对象填充日历
            var startDay = daysInLastMonth - dayOfWeek + this.locale.firstDay + 1;
            if (startDay > daysInLastMonth) startDay -= 7;
            if (dayOfWeek == this.locale.firstDay) startDay = daysInLastMonth - 6;
            var curDate = moment([lastYear, lastMonth, startDay, 12, minute, second]);
            var col, row;
            for (var i = 0, col = 0, row = 0; i < 42; i++, col++, curDate = moment(curDate).add(24, 'hour')) {
                if (i > 0 && col % 7 === 0) {
                    col = 0;
                    row++;
                }
                calendar[row][col] = curDate.clone().hour(hour).minute(minute).second(second);
                curDate.hour(12);
                if (this.minDate && calendar[row][col].format('YYYY/MM/DD') == this.minDate.format('YYYY/MM/DD') && calendar[row][col].isBefore(this.minDate) && side == 'left') {
                    calendar[row][col] = this.minDate.clone();
                }
                if (this.maxDate && calendar[row][col].format('YYYY/MM/DD') == this.maxDate.format('YYYY/MM/DD') && calendar[row][col].isAfter(this.maxDate) && side == 'right') {
                    calendar[row][col] = this.maxDate.clone();
                }
            }
            //使日历对象可用于hoverDate/clickDate
            if (side == 'left') {
                this.leftCalendar.calendar = calendar;
            } else {
                this.rightCalendar.calendar = calendar;
            }
            var minDate = side == 'left' ? this.minDate: this.startDate;
            var maxDate = this.maxDate;
            var selected = side == 'left' ? this.startDate: this.endDate;
            var html = '<table class="table-condensed">';
            html += '<thead>';
            html += '<tr>';
            if (this.showWeekNumbers || this.showISOWeekNumbers) html += '<th></th>';
            if ((!minDate || minDate.isBefore(calendar.firstDay)) && (!this.linkedCalendars || side == 'left')) {
                html += '<th class="prev available"> <img src="zuojian.png" border="0" width="16" /> </th>';
            } else {
                html += '<th></th>';
            }	
			var dateHtml = calendar[1][1].format("YYYY") +'年' + calendar[1][1].format("MM") + '月';
            if (this.showDropdowns) { 
                
                var currentMonth = calendar[1][1].month();
                var currentYear = calendar[1][1].year();   
                var maxYear = (maxDate && maxDate.year()) || (currentYear + 4); 
                var minYear = (minDate && minDate.year()) || (currentYear - 10); 
                var inMinYear = currentYear == minYear;
                var inMaxYear = currentYear == maxYear;

                var monthHtml = '<select class="monthselect">'; 
                for (var m = 0; m < 12; m++) {  
                    monthHtml += "<option value='" + m + "'" + (m === currentMonth ? " selected='selected'": "") + ">" + this.locale.monthNames[m] + "</option>";
                    
                    // if ((!inMinYear || m >= minDate.month()) && (!inMaxYear || m <= maxDate.month())) {
                    //     monthHtml += "<option value='" + m + "'" + (m === currentMonth ? " selected='selected'": "") + ">" + this.locale.monthNames[m] + "</option>";
                    // } else { 
                    //     monthHtml += "<option value='" + m + "'" + (m === currentMonth ? " selected='selected'": "") + " disabled='disabled'>" + this.locale.monthNames[m] + "</option>";  
                    // }
                }
                monthHtml += "</select>";
                var yearHtml = '<select class="yearselect">';
                
                var myDatehan = new Date;
                var yearhan = myDatehan.getFullYear();  
                var maxyearhan =  yearhan + 1; 
                for (var y = 2017; y <= maxyearhan; y++) {
                    yearHtml += '<option value="' + y + '"' + (y === currentYear ? ' selected="selected"': '') + '>' + y + '</option>';
                }
                yearHtml += '</select>';
                dateHtml = yearHtml + monthHtml;
            }
            html += '<th colspan="5" class="month">' + dateHtml + '</th>';
            if ((!maxDate || maxDate.isAfter(calendar.lastDay)) && (!this.linkedCalendars || side == 'right' || this.singleDatePicker)) {
                html += '<th class="next available"> <img src="youjian.png" border="0" width="16" /> </th>';
            } else {
                html += '<th></th>';
            }
            html += '</tr>';
            html += '<tr>';
            if (this.showWeekNumbers || this.showISOWeekNumbers) html += '<th class="week">' + this.locale.weekLabel + '</th>';
            $.each(this.locale.daysOfWeek, 
                function(index, dayOfWeek) {
                html += '<th>' + dayOfWeek + '</th>';
            });
            html += '</tr>';
            html += '</thead>';
            html += '<tbody>';
            //调整maxDate以反映dateLimit设置，以便
            //灰色显示超出日期限制的结束日期
            if (this.endDate == null && this.dateLimit) {
                var maxLimit = this.startDate.clone().add(this.dateLimit).endOf('day');
                if (!maxDate || maxLimit.isBefore(maxDate)) {
                    maxDate = maxLimit;
                }
            }
            for (var row = 0; row < 6; row++) {
                html += '<tr>';
                // 添加周数
                if (this.showWeekNumbers) html += '<td class="week">' + calendar[row][0].week() + '</td>';
                else if (this.showISOWeekNumbers) html += '<td class="week">' + calendar[row][0].isoWeek() + '</td>';
                for (var col = 0; col < 7; col++) {
                    var classes = [];
                    //突出显示今天的日期
                    if (calendar[row][col].isSame(new Date(), "day")) classes.push('today');
                    //突出周末 
                    if (calendar[row][col].isoWeekday() > 5) classes.push('weekend');
                    //灰色显示此日历开始和结束时显示的其他月份的日期
                    if (calendar[row][col].month() != calendar[1][1].month()) classes.push('off');
                    //不允许在最小日期之前选择日期
                    if (this.minDate && calendar[row][col].isBefore(this.minDate, 'day')) classes.push('off', 'disabled');
                    //不允许在最大日期之后选择日期
                    if (maxDate && calendar[row][col].isAfter(maxDate, 'day')) classes.push('off', 'disabled');
                    //如果自定义函数确定日期无效，则不允许选择日期
                    if (this.isInvalidDate(calendar[row][col])) classes.push('off', 'disabled');
                    //突出显示当前选定的开始日期
                    if (calendar[row][col].format('YYYY/MM/DD') == this.startDate.format('YYYY/MM/DD')) classes.push('active', 'start-date');
                    //突出显示当前选定的结束日期
                    if (this.endDate != null && calendar[row][col].format('YYYY/MM/DD') == this.endDate.format('YYYY/MM/DD')) classes.push('active', 'end-date');
                    //突出显示选定日期之间的日期
                    if (this.endDate != null && calendar[row][col] > this.startDate && calendar[row][col] < this.endDate) classes.push('in-range');
                    var cname = '', 
                    disabled = false;
                    for (var i = 0; i < classes.length; i++) {
                        cname += classes[i] + ' ';
                        if (classes[i] == 'disabled') disabled = true;
                    }
                    if (!disabled) cname += 'available';
                    html += '<td class="' + cname.replace(/^\s+|\s+$/g, '') + '" data-title="' + 'r' + row + 'c' + col + '">' + calendar[row][col].date() + '</td>';
                }
                html += '</tr>';
            }
            html += '</tbody>';
            html += '</table>';
            this.container.find('.calendar.' + side + ' .calendar-table').html(html);
        },
        renderTimePicker: function(side) {
            //console.log('我是第7个方法');
            var html, selected, minDate, maxDate = this.maxDate;
            if (this.dateLimit && (!this.maxDate || this.startDate.clone().add(this.dateLimit).isAfter(this.maxDate))) maxDate = this.startDate.clone().add(this.dateLimit);
            if (side == 'left') {
                selected = this.startDate.clone();
                minDate = this.minDate;
            } else if (side == 'right') {
                selected = this.endDate ? this.endDate.clone() : this.previousRightTime.clone();
                minDate = this.startDate;
                //保留已选择的时间
                var timeSelector = this.container.find('.calendar.right .calendar-time div');
                if (timeSelector.html() != '') {
                    selected.hour(timeSelector.find('.hourselect option:selected').val() || selected.hour());
                    selected.minute(timeSelector.find('.minuteselect option:selected').val() || selected.minute());
                    selected.second(timeSelector.find('.secondselect option:selected').val() || selected.second());
                    if (!this.timePicker24Hour) {
                        var ampm = timeSelector.find('.ampmselect option:selected').val();
                        if (ampm === 'PM' && selected.hour() < 12) selected.hour(selected.hour() + 12);
                        if (ampm === 'AM' && selected.hour() === 12) selected.hour(0);
                    }
                    if (selected.isBefore(this.startDate)) selected = this.startDate.clone(); 
                    if (selected.isAfter(maxDate)) selected = maxDate.clone();
                }
            }
            // hours
            html = '<select class="hourselect">';
            var start = this.timePicker24Hour ? 0 : 1;
            var end = this.timePicker24Hour ? 23 : 12;
            for (var i = start; i <= end; i++) {
                var i_in_24 = i;
                if (!this.timePicker24Hour) i_in_24 = selected.hour() >= 12 ? (i == 12 ? 12 : i + 12) : (i == 12 ? 0 : i);
                var time = selected.clone().hour(i_in_24);
                var disabled = false;
                if (minDate && time.minute(59).isBefore(minDate)) disabled = true;
                if (maxDate && time.minute(0).isAfter(maxDate)) disabled = true;
                if (i_in_24 == selected.hour() && !disabled) {
                    html += '<option value="' + i + '" selected="selected">' + i + '</option>';
                } else if (disabled) {
                    html += '<option value="' + i + '" disabled="disabled" class="disabled">' + i + '</option>';
                } else {
                    html += '<option value="' + i + '">' + i + '</option>';
                }
            }
            html += '</select> ';
            // minutes
            html += ': <select class="minuteselect">';
            for (var i = 0; i < 60; i += this.timePickerIncrement) {
                var padded = i < 10 ? '0' + i: i;
                var time = selected.clone().minute(i);
                var disabled = false;
                if (minDate && time.second(59).isBefore(minDate)) disabled = true;
                if (maxDate && time.second(0).isAfter(maxDate)) disabled = true;
                if (selected.minute() == i && !disabled) {
                    html += '<option value="' + i + '" selected="selected">' + padded + '</option>';
                } else if (disabled) {
                    html += '<option value="' + i + '" disabled="disabled" class="disabled">' + padded + '</option>';
                } else {
                    html += '<option value="' + i + '">' + padded + '</option>';
                }
            }
            html += '</select> ';
            // seconds
            if (this.timePickerSeconds) {
                html += ': <select class="secondselect">';
                for (var i = 0; i < 60; i++) {
                    var padded = i < 10 ? '0' + i: i;
                    var time = selected.clone().second(i);
                    var disabled = false;
                    if (minDate && time.isBefore(minDate)) disabled = true; 
                    if (maxDate && time.isAfter(maxDate)) disabled = true;
                    if (selected.second() == i && !disabled) {
                        html += '<option value="' + i + '" selected="selected">' + padded + '</option>';
                    } else if (disabled) {
                        html += '<option value="' + i + '" disabled="disabled" class="disabled">' + padded + '</option>';
                    } else {
                        html += '<option value="' + i + '">' + padded + '</option>';
                    }
                }
                html += '</select> ';
            }
            // AM/PM
            if (!this.timePicker24Hour) {
                html += '<select class="ampmselect">';
                var am_html = '';
                var pm_html = '';
                if (minDate && selected.clone().hour(12).minute(0).second(0).isBefore(minDate)) am_html = ' disabled="disabled" class="disabled"';
                if (maxDate && selected.clone().hour(0).minute(0).second(0).isAfter(maxDate)) pm_html = ' disabled="disabled" class="disabled"';
                if (selected.hour() >= 12) {
                    html += '<option value="AM"' + am_html + '>AM</option><option value="PM" selected="selected"' + pm_html + '>PM</option>';
                } else {
                    html += '<option value="AM" selected="selected"' + am_html + '>AM</option><option value="PM"' + pm_html + '>PM</option>';
                }
                html += '</select>';
            }
            this.container.find('.calendar.' + side + ' .calendar-time div').html(html);
        },
        updateFormInputs: function() {
        	//console.log('我是第8个方法');
			//当上面的日历文本输入有焦点时忽略鼠标移动
            // if (this.container.find('input[name=daterangepicker_start]').is(":focus") || this.container.find('input[name=daterangepicker_end]').is(":focus"))
         //     return;
            this.container.find('input[name=daterangepicker_start]').val(this.startDate.format(this.locale.format));
            this.container.find('input[name=daterangepicker_end]').val(this.startDate.format(this.locale.format));
            if (this.endDate) this.container.find('input[name=daterangepicker_end]').val(this.endDate.format(this.locale.format));
            if (this.singleDatePicker || (this.endDate && (this.startDate.isBefore(this.endDate) || this.startDate.isSame(this.endDate)))) {
                this.container.find('button.applyBtn').removeAttr('disabled');
            } else {
            	this.container.find('button.applyBtn').removeAttr('disabled');
                //this.container.find('button.applyBtn').attr('disabled', 'disabled');
            }
        },
        move: function() {
        	//console.log('我是第9个方法');
            var parentOffset = { 
                top: 0, 
                left: 0 
            },
                containerTop;
            var parentRightEdge = $(window).width();
            if (!this.parentEl.is('body')) {
                parentOffset = {
                    top: this.parentEl.offset().top - this.parentEl.scrollTop(),
                    left: this.parentEl.offset().left - this.parentEl.scrollLeft()
                };
                parentRightEdge = this.parentEl[0].clientWidth + this.parentEl.offset().left;
            }
            if (this.drops == 'up') containerTop = this.element.offset().top - this.container.outerHeight() - parentOffset.top;
            else containerTop = this.element.offset().top + this.element.outerHeight() - parentOffset.top;
            this.container[this.drops == 'up' ? 'addClass' : 'removeClass']('dropup');
            if (this.opens == 'left') {
                this.container.css({
                    top: containerTop,
                    right: parentRightEdge - this.element.offset().left - this.element.outerWidth(),
                    left: 'auto'
                });
                if (this.container.offset().left < 0) {
                    this.container.css({
                        right: 'auto',
                        left: 9
                    });
                }
            } else if (this.opens == 'center') {
                this.container.css({
                    top: containerTop,
                    left: this.element.offset().left - parentOffset.left + this.element.outerWidth() / 2 - this.container.outerWidth() / 2,
                    right: 'auto'
                });
                if (this.container.offset().left < 0) {
                    this.container.css({
                        right: 'auto',
                        left: 9
                    });
                }
            } else {
                this.container.css({
                    top: containerTop,
                    left: this.element.offset().left - parentOffset.left,
                    right: 'auto'
                });
                if (this.container.offset().left + this.container.outerWidth() > $(window).width()) {
                    this.container.css({
                        left: 'auto',
                        right: 0
                    });
                }
            }
        },
        show: function(e) {
       	    //console.log('我是第10个方法');
        	//第二个，如果页面没有显示，第二个方法进这，让日历显示
            if (this.isShowing) return;
            // 创建一个对这个datepicker实例私有的click代理，用于解除绑定
            this._outsideClickProxy = $.proxy(function(e) { 
                this.outsideClick(e); 
            }, this);
            $(document).on('mousedown.daterangepicker', this._outsideClickProxy)
              .on('touchend.daterangepicker', this._outsideClickProxy)
              .on('click.daterangepicker', '[data-toggle=dropdown]', this._outsideClickProxy)
              .on('focusin.daterangepicker', this._outsideClickProxy);
            $(window).on('resize.daterangepicker', $.proxy(function(e) { 
                this.move(e); 
            }, this));
			//console.log('当我选择完以后再次点击日历开始'+this.startDate)
			//console.log('当我选择完以后再次点击日历结束'+this.endDate.clone)
            this.oldStartDate = this.startDate.clone();
            //this.oldEndDate = this.endDate.clone();
            //this.previousRightTime = this.endDate.clone();
            this.updateView();
            this.container.show();
            this.move();
            this.element.trigger('show.daterangepicker', this);
            this.isShowing = true;
            if ($('#daterange-btn span').html() == '全部') {
                $('.calendar').find('.active').removeClass('active');
                $('.calendar').find('.in-range').removeClass('in-range');
            }
        },
        hide: function(e) {
        	//console.log('我是第11个方法');
            if (!this.isShowing) {
            	return
            };
            //日期选择不完整，还原为上一个值
            //这个判断是只选择了一个日子
            if (this.startDate && !this.endDate) {
             	//console.log('现在是单日子')
            	$('#daterange-btn span').html(this.container.find('input[name=daterangepicker_start]').val());
          	    //this.startDate = Date.parse(new Date(this.container.find('input[name=daterangepicker_start]').val()))
          	    //this.endDate = Date.parse(new Date(this.container.find('input[name=daterangepicker_end]').val()));
         	    this.callback(this.startDate, this.endDate, this.chosenLabel);
            	this.updateElement();
	            $(document).off('.daterangepicker');
	            $(window).off('.daterangepicker');
	            this.container.remove();
	            this.element.trigger('hide.daterangepicker', this);
	            this.isShowing = false;
            } else {
                //如果选择了新的日期范围，请调用用户回调函数
	            if (!this.startDate.isSame(this.oldStartDate) || !this.endDate.isSame(this.oldEndDate)) {
	                this.callback(this.startDate, this.endDate, this.chosenLabel);
	            }
	            //如果选取器附加到文本输入，请更新它
	            this.updateElement();
	            $(document).off('.daterangepicker');
	            $(window).off('.daterangepicker');
	            this.container.remove();
	            this.element.trigger('hide.daterangepicker', this);
	            this.isShowing = false;
            }
        },
        toggle: function(e) {
        	//点击后先进这个方法，判断是否显示，显示则隐藏，隐藏则显示
        	//console.log('我是第12个方法');
            if (this.isShowing) {
                this.hide();
            } else {
                this.show();
            }
        },
        outsideClick: function(e) {
        	//console.log('我是第13个方法');
            var target = $(e.target);
            //如果在DateRangePicker/button之外的任何位置单击页面
            //它自己就会隐藏
            // ie模式对话框修复
            if (
                e.type == "focusin" || target.closest(this.element).length || target.closest(this.container).length || target.closest('.calendar-table').length) return;
            this.hide();
        },
        showCalendars: function() {
        	//console.log('我是第14个方法');
            this.container.addClass('show-calendar');
            this.move();
            this.element.trigger('showCalendar.daterangepicker', this);
        },
        hideCalendars: function() {
        	//console.log('我是第15个方法');
            this.container.removeClass('show-calendar');
            this.element.trigger('hideCalendar.daterangepicker', this);
        },
        hoverRange: function(e) {
        	//console.log('我是第16个方法');
        	//鼠标滑过每个td
            //当上面的日历文本输入有焦点时忽略鼠标移动
            if (this.container.find('input[name=daterangepicker_start]').is(":focus") || this.container.find('input[name=daterangepicker_end]').is(":focus")) return;
            var label = e.target.innerHTML;
            if (label == this.locale.customRangeLabel) {
                this.updateView();
            } else {
//              var dates = this.ranges[label];
//              this.container.find('input[name=daterangepicker_start]').val(dates[0].format(this.locale.format));
//              this.container.find('input[name=daterangepicker_end]').val(dates[1].format(this.locale.format));
            }
        },
        clickRange: function(e) {
        	//console.log('我是第17个方法');
            var label = e.target.innerHTML;
            this.chosenLabel = label;
            if (label == this.locale.customRangeLabel) {
                this.showCalendars();
            } else {
                var dates = this.ranges[label];
                this.startDate = dates[0];
                this.endDate = dates[1];
                if (!this.timePicker) {
                  this.startDate.startOf('day');
                  this.endDate.endOf('day');
                }
                if (!this.alwaysShowCalendars) {
                	//点击的时候不隐藏日历
                    //this.hideCalendars();
              	    //this.clickApply();
                    this.setStartDate(this.startDate);
                    this.setEndDate(this.endDate);
                    this.updateCalendars();
          		    //this.formInputsChanged(this)
                    this.renderCalendar('left');
                    this.renderCalendar('right');
                    if (label == '全部') {
                        $('.daterangepicker .all').css('display', 'block');
                        $('.calendar').find('.active').removeClass('active');
                        $('.calendar').find('.in-range').removeClass('in-range');
                    } else {
                        $('.daterangepicker .all').css('display', 'none');
                    }
                    this.updateFormInputs();
				}
            }
        },
        clickPrev: function(e) {
        	//console.log('我是第18个方法');
            var cal = $(e.target).parents('.calendar');
            if (cal.hasClass('left')) {
                this.leftCalendar.month.subtract(1, 'month');
                if (this.linkedCalendars) {
                    this.rightCalendar.month.subtract(1, 'month');
                 }
            } else {
                this.rightCalendar.month.subtract(1, 'month');
            } 
            this.updateCalendars();
        },
        clickNext: function(e) {
            //console.log('我是第19个方法');
            var cal = $(e.target).parents('.calendar');
            if (cal.hasClass('left')) {
                this.leftCalendar.month.add(1, 'month');
            } else {
                this.rightCalendar.month.add(1, 'month');
                if (this.linkedCalendars) this.leftCalendar.month.add(1, 'month');
            }  
            this.updateCalendars();
        },
        clickPrevYear: function(e) {
            //点击显示上一年的当前月份
            var myDatehan = new Date;
            var yearhan = myDatehan.getFullYear(); 
            var minyearhan =  2017; 
            var maxyearhan =  yearhan + 1; 
            var cal = $(e.target).parents('.calendar');
            var leftimg = this.leftCalendar.month.year() 
            cal.next(".calendar.right").children(".prev_month").css({"cursor":"pointer","opacity":"1"}) 
            if(minyearhan < leftimg && leftimg <= maxyearhan) {    
                $(e.target).parent().css({"cursor":"pointer","opacity":"1"})
                if (cal.hasClass('left')) {
                    this.leftCalendar.month.subtract(1, 'year');
                    if (this.linkedCalendars) { this.rightCalendar.month.subtract(1, 'year'); }
                } else {
                    this.rightCalendar.month.subtract(1, 'year');
                }
            }else{
                this.leftCalendar.month.year(2017);
                $(e.target).parent(".prev_year").css({"cursor":"not-allowed","opacity":"0.5"})
                
            }

            this.updateCalendars();
        },
		clickNextYear: function(e) {
            //点击显示下一年的当前月份  
            var myDatehan = new Date;
            var yearhan = myDatehan.getFullYear(); 
            var minyearhan =  2017; 
            var maxyearhan =  yearhan + 1 ;  
            var cal = $(e.target).parents('.calendar'); 
            var rightimg = this.rightCalendar.month.year()
            cal.prev(".calendar.left").children(".prev_year").css({"cursor":"pointer","opacity":"1"})
            if(minyearhan <= rightimg && rightimg < maxyearhan) { 
                $(e.target).parent(".prev_month").css({"cursor":"pointer","opacity":"1"} )
                if (cal.hasClass('left')) {
                    this.leftCalendar.month.add(1, 'year');
                } else { 
                    this.rightCalendar.month.add(1, 'year');
                    if (this.linkedCalendars) this.leftCalendar.month.add(1, 'year');  
                } 
            }else{
                this.rightCalendar.month.year(maxyearhan);
                $(e.target).parent(".prev_month").css({"cursor":"not-allowed","opacity":"0.5"})
            } 
            this.updateCalendars();
		},
        hoverDate: function(e) {
//      	//console.log('我是第20个方法');
            //当上面的日历文本输入有焦点时忽略鼠标移动
//          if (this.container.find('input[name=daterangepicker_start]').is(":focus") || this.container.find('input[name=daterangepicker_end]').is(":focus"))
//              return;
//          //ignore dates that can't be selected
//          if (!$(e.target).hasClass('available')) return;
//          //have the text inputs above calendars reflect the date being hovered over
//          var title = $(e.target).attr('data-title');
//          var row = title.substr(1, 1);
//          var col = title.substr(3, 1);
//          var cal = $(e.target).parents('.calendar');
//          var date = cal.hasClass('left') ? this.leftCalendar.calendar[row][col] : this.rightCalendar.calendar[row][col];
//          if (this.endDate) {
////              this.container.find('input[name=daterangepicker_start]').val(date.format(this.locale.format));
//          } else {
////              this.container.find('input[name=daterangepicker_end]').val(date.format(this.locale.format));
//          }
//          //highlight the dates between the start date and the date being hovered as a potential end date
//          var leftCalendar = this.leftCalendar;
//          var rightCalendar = this.rightCalendar;
//          var startDate = this.startDate;
//          if (!this.endDate) {
//              this.container.find('.calendar td').each(function(index, el) {
//                  //skip week numbers, only look at dates
//                  if ($(el).hasClass('week')) return;
//                  var title = $(el).attr('data-title');
//                  var row = title.substr(1, 1);
//                  var col = title.substr(3, 1);
//                  var cal = $(el).parents('.calendar');
//                  var dt = cal.hasClass('left') ? leftCalendar.calendar[row][col] : rightCalendar.calendar[row][col];
//                  if (dt.isAfter(startDate) && dt.isBefore(date)) {
//                      $(el).addClass('in-range');
//                  } else {
//                      $(el).removeClass('in-range');
//                  }
//
//              });
//          }
        }, 
        clickDate: function(e) {
            if (!$(e.target).hasClass('available')) return;
            var title = $(e.target).attr('data-title');
            var row = title.substr(1, 1);
            var col = title.substr(3, 1);
            var cal = $(e.target).parents('.calendar');
            var date = cal.hasClass('left') ? this.leftCalendar.calendar[row][col] : this.rightCalendar.calendar[row][col];
            //此函数需要执行以下操作：
            //*交替选择范围的开始日期和结束日期，
            //*如果启用时间选择器，则将选择框中的小时/分钟/秒应用于单击的日期
            //*如果启用了自动应用，并且选择了结束日期，则应用所选内容
            //*如果单日期选取器模式，且时间选取器未启用，请立即应用选择
            if (this.endDate || date.isBefore(this.startDate, 'day')) {
                if (this.timePicker) {
                    var hour = parseInt(this.container.find('.left .hourselect').val(), 10);
                    if (!this.timePicker24Hour) {
                        var ampm = this.container.find('.left .ampmselect').val();
                        if (ampm === 'PM' && hour < 12) hour += 12;
                        if (ampm === 'AM' && hour === 12) hour = 0;
                    }
                    var minute = parseInt(this.container.find('.left .minuteselect').val(), 10);
                    var second = this.timePickerSeconds ? parseInt(this.container.find('.left .secondselect').val(), 10) : 0;
                    date = date.clone().hour(hour).minute(minute).second(second);
                }
                this.endDate = null;
                this.setStartDate(date.clone());
            } else if (!this.endDate && date.isBefore(this.startDate)) {
                this.setEndDate(this.startDate.clone());
            } else {
                if (this.timePicker) {
                    var hour = parseInt(this.container.find('.right .hourselect').val(), 10);
                    if (!this.timePicker24Hour) {
                        var ampm = this.container.find('.right .ampmselect').val();
                        if (ampm === 'PM' && hour < 12) hour += 12;
                        if (ampm === 'AM' && hour === 12) hour = 0;
                    }
                    var minute = parseInt(this.container.find('.right .minuteselect').val(), 10);
                    var second = this.timePickerSeconds ? parseInt(this.container.find('.right .secondselect').val(), 10) : 0;
                    date = date.clone().hour(hour).minute(minute).second(second);
                }
                this.setEndDate(date.clone());
                if (this.autoApply) {
                  this.calculateChosenLabel();
                  this.clickApply();
                }
            }
            if (this.singleDatePicker) {
                this.setEndDate(this.startDate);
                if (!this.timePicker) this.clickApply();
            }
            this.updateView();
        },
        calculateChosenLabel: function() {
            //console.log('我是第22个方法');
            //判断页面显示自定义哪个
          var customRange = true;
          var i = 0;
          for (var range in this.ranges) {
              if (this.timePicker) {
                  if (this.startDate.isSame(this.ranges[range][0]) && this.endDate.isSame(this.ranges[range][1])) {
                      customRange = false;
                      this.chosenLabel = this.container.find('.ranges li:eq(' + i + ')').addClass('active').html();
                      break;
                  }
              } else {
                  if (this.startDate.format('YYYY/MM/DD') == this.ranges[range][0].format('YYYY/MM/DD') && this.endDate.format('YYYY/MM/DD') == this.ranges[range][1].format('YYYY/MM/DD')) {
                      customRange = false;
                      this.chosenLabel = this.container.find('.ranges li:eq(' + i + ')').addClass('active').html();
                      break;
                  }
              }
              i++;
          }
          if (customRange) {
              this.chosenLabel = this.container.find('.ranges li:last').addClass('active').html();
              this.showCalendars();
          }
        },
        clickApply: function(e) {
      	    //console.log('我是第23个方法');
            this.element.trigger('apply.daterangepicker', this);
            this.hide();
        },
        clickCancel: function(e) {
      		//console.log('我是第24个方法');
            this.element.trigger('cancel.daterangepicker', this);
            this.updateElement();
            $(document).off('.daterangepicker');
            $(window).off('.daterangepicker');
            this.container.remove();
            this.element.trigger('hide.daterangepicker', this);
            this.isShowing = false;
        },
        monthOrYearChanged: function(e) {
            //console.log('我是第25个方法'); 
            var isLeft = $(e.target).closest('.calendar').hasClass('left'),
                leftOrRight = isLeft ? 'left': 'right',
                cal = this.container.find('.calendar.' + leftOrRight);
            var month = parseInt(cal.find('.monthselect').val(), 10);
            var year = cal.find('.yearselect').val(); 
            var myDatehan = new Date;
            var yearhan = myDatehan.getFullYear();  
            var maxyearhan =  yearhan + 1 ; 
            if(year > 2017 &&  year < maxyearhan){
                $(e.target).parents(".calendar.left").find(".prev_year").css({"cursor":"pointer","opacity":"1"})
                $(e.target).parents(".calendar.right").find(".prev_month").css({"cursor":"pointer","opacity":"1"})
            } 
            // if (!isLeft) { 
            //     this.rightCalendar.month.month(month).year(year);
            //     if (year < this.startDate.year() || (year == this.startDate.year() && month < this.startDate.month())) {
            //         month = this.startDate.month();
            //         year = this.startDate.year(); 
            //     } 
            // } 
            if (!isLeft) { 
                this.leftCalendar.month.month(month).year(year);
                if (this.linkedCalendars) this.rightCalendar.month = this.leftCalendar.month.clone().subtract(1, 'month'); 
            } else {
                this.rightCalendar.month.month(month).year(year); 
                if (this.linkedCalendars) this.leftCalendar.month = this.rightCalendar.month.clone().add(1, 'month');
            }
            
            if (this.minDate) {
                if (year < this.minDate.year() || (year == this.minDate.year() && month < this.minDate.month())) {
                    month = this.minDate.month();
                    year = this.minDate.year();
                }
            }
            if (this.maxDate) {
                if (year > this.maxDate.year() || (year == this.maxDate.year() && month > this.maxDate.month())) {
                    month = this.maxDate.month();
                    year = this.maxDate.year();
                }
            }
            if (isLeft) { 
                this.leftCalendar.month.month(month).year(year);
                if (this.linkedCalendars) this.rightCalendar.month = this.leftCalendar.month.clone().add(1, 'month'); 
            } else {
                this.rightCalendar.month.month(month).year(year); 
                if (this.linkedCalendars) this.leftCalendar.month = this.rightCalendar.month.clone().subtract(1, 'month');
            }
            this.updateCalendars();
        },
        timeChanged: function(e) {
         	//console.log('我是第26个方法');
            var cal = $(e.target).closest('.calendar'),
                isLeft = cal.hasClass('left');
            var hour = parseInt(cal.find('.hourselect').val(), 10);
            var minute = parseInt(cal.find('.minuteselect').val(), 10);
            var second = this.timePickerSeconds ? parseInt(cal.find('.secondselect').val(), 10) : 0;
            if (!this.timePicker24Hour) {
                var ampm = cal.find('.ampmselect').val();
                if (ampm === 'PM' && hour < 12) hour += 12;
                if (ampm === 'AM' && hour === 12) hour = 0;
            }
            if (isLeft) {
                var start = this.startDate.clone();
                start.hour(hour);
                start.minute(minute);
                start.second(second);
                this.setStartDate(start);
                if (this.singleDatePicker) {
                    this.endDate = this.startDate.clone();
                } else if (this.endDate && this.endDate.format('YYYY/MM/DD') == start.format('YYYY/MM/DD') && this.endDate.isBefore(start)) {
                    this.setEndDate(start.clone());
                }
            } else if (this.endDate) {
                var end = this.endDate.clone();
                end.hour(hour);
                end.minute(minute);
                end.second(second);
                this.setEndDate(end);
            }
            this.updateCalendars();
            this.updateFormInputs();
            this.renderTimePicker('left');
            this.renderTimePicker('right');
        },
        formInputsChanged: function(e) {
            //console.log('我是第27个方法');
            var isRight = $(e.target).closest('.calendar').hasClass('right');
            var start = moment(this.container.find('input[name="daterangepicker_start"]').val(), this.locale.format);
            var end = moment(this.container.find('input[name="daterangepicker_end"]').val(), this.locale.format);
            if (start.isValid() && end.isValid()) {
                if (isRight && end.isBefore(start)) start = end.clone();
                this.setStartDate(start);
                this.setEndDate(end);
                if (isRight) {
                    this.container.find('input[name="daterangepicker_start"]').val(this.startDate.format(this.locale.format));
                } else {
                    this.container.find('input[name="daterangepicker_end"]').val(this.endDate.format(this.locale.format));
                }
            }
            this.updateCalendars();
            if (this.timePicker) {
                this.renderTimePicker('left');
                this.renderTimePicker('right');
            }
        },
        elementChanged: function() {
            //console.log('我是第28个方法');
            if (!this.element.is('input')) return;
            if (!this.element.val().length) return;
            if (this.element.val().length < this.locale.format.length) return;
            var dateString = this.element.val().split(this.locale.separator),
                start = null,
                end = null;
            if (dateString.length === 2) {
                start = moment(dateString[0], this.locale.format);
                end = moment(dateString[1], this.locale.format);
            }
            if (this.singleDatePicker || start === null || end === null) {
                start = moment(this.element.val(), this.locale.format);
                end = start;
            }
            if (!start.isValid() || !end.isValid()) return;
            this.setStartDate(start);
            this.setEndDate(end);
            this.updateView();
        },
        keydown: function(e) {
            if ((e.keyCode === 9) || (e.keyCode === 13)) {
                this.hide();
            }
        },
        updateElement: function() {
            if (this.element.is('input') && !this.singleDatePicker && this.autoUpdateInput) {
                if(!this.endDate){
                    this.endDate = this.startDate;
                }
                this.element.val(this.startDate.format(this.locale.format) + this.locale.separator + this.endDate.format(this.locale.format));
                this.element.trigger('change');
            } else if (this.element.is('input') && this.autoUpdateInput) {
                this.element.val(this.startDate.format(this.locale.format));
                this.element.trigger('change');
            }
        },
        remove: function() {
            this.container.remove();
            this.element.off('.daterangepicker');
            this.element.removeData();
        },
        clickReset: function(e) {  
            $(document).off('.daterangepicker'); 
            $(window).off('.daterangepicker'); 
            this.element.trigger('cancel.daterangepicker', this);
            // this.updateElement(); 
            this.element.val("") 
            this.container.remove(); 
            this.element.trigger('hide.daterangepicker', this);
            this.isShowing = false;
        } 
    };
    $.fn.daterangepicker = function(options, callback) {
        this.each(function() {
            var el = $(this);
            if (el.data('daterangepicker')) el.data('daterangepicker').remove();
            el.data('daterangepicker', new DateRangePicker(el, options, callback));
        });
        return this;
    };
    return DateRangePicker;
}));







