
        document.addEventListener('DOMContentLoaded', function () {
            const modal = new bootstrap.Modal(document.getElementById('mprogressModal'));
            const timelineModal = new bootstrap.Modal(document.getElementById('timelineModal'));

            document.querySelectorAll('.edit-link, .edit-button').forEach(function (element) {
                element.addEventListener('click', function (event) {
                    event.preventDefault();
                    const id = this.getAttribute('data-id');
                    console.log("id", id)
                    const accountStatus = parseInt(this.getAttribute('data-account-status'));
                    const description = this.getAttribute('data-description');
                    console.log("description", description);
                    const history_hdescription = this.getAttribute('data-history-description');

                    // 检查 description 是否为 null 或 undefined
                    if (description === 'None' || description == '') {
                        console.log("ifdescription", description);
                        console.log(typeof description);
                        document.getElementById('remark').value = '';
                    } else {
                        document.getElementById('remark').innerHTML = description;
                    }


                    document.getElementById('id').value = id;


                    // Filter the options based on accountStatus
                    const progressStateSelect = document.getElementById('progress_state');
                    progressStateSelect.innerHTML = '';  // 清空现有选项

                    // 重新添加所有原始选项
                    const originalOptions = [
                        {value: '1', text: '初步沟通'},
                        {value: '3', text: '直连'},
                        {value: '4', text: '转售后'},
                        // {#{value: '5', text: '试用期间'},#}
                        // {#{value: '6', text: '到期付费'}#}
                    ];

                    originalOptions.forEach(option => {
                        const opt = document.createElement('option');
                        opt.value = option.value;
                        opt.textContent = option.text;
                        progressStateSelect.appendChild(opt);
                    });


                    const options = Array.from(progressStateSelect.options);
                    console.log("options", options)
                    progressStateSelect.innerHTML = '';  // Clear existing options
                    clonedOption = null;


                    options.forEach(option => {

                        console.log("option.value", option.value)
                        if (parseInt(option.value) >= (parseInt(accountStatus)) || option.value === '') {
                            const clonedOption = option.cloneNode(true);
                            console.log("clonedOption", clonedOption)
                            progressStateSelect.appendChild(clonedOption);
                        }

                    });

                    // Set the selected value
                    console.log("accountStatus", accountStatus);
                    progressStateSelect.value = accountStatus;

                    modal.show();


                });
            });

            document.querySelectorAll('.timeline-link').forEach(function (element) {
                element.addEventListener('click', function (event) {
                    event.preventDefault();
                    const stepOneContent = this.getAttribute('data-step_one');
                    // {#const steptwoContent = this.getAttribute('data-step_two');#}
                    const stepthreeContent = this.getAttribute('data-step_three');
                    const stepfourContent = this.getAttribute('data-step_four');
                    // {#const stepfiveContent = this.getAttribute('data-step_five');#}
                    // {#const stepsixContent = this.getAttribute('data-step_six');#}

                    const stepOneContent_g = stepOneContent !== 'None' ? `<span style="color: blue;">初步沟通</span>   ---------------------------------------<br><br>${stepOneContent}` : `<span style="color: blue;">初步沟通</span>------------------------------------------<br><br>`
                    // {#const steptwoContent_g = steptwoContent !== 'None' ? `<span style="color: blue;">注册</span>------------------------------<br><br>${steptwoContent}` : `<span style="color: blue;">注册</span>------------------------------<br><br>`#}
                    const stepthreeContent_g = stepthreeContent !== 'None' ? `<span style="color: blue;">直连</span>------------------------------------------<br><br>${stepthreeContent}` : `<span style="color: blue;">直连</span>----------------------------------------------<br><br>`
                    const stepfourContent_g = stepfourContent !== 'None' ? `<span style="color: blue;">转售后</span><br><br>${stepfourContent}` : `<span style="color: blue;">转售后</span><br><br>`
                    // {#const stepfiveContent_g = stepfiveContent !== 'None' ? `<span style="color: blue;">试用期间</span>----------------------<br><br>${stepfiveContent}` : `<span style="color: blue;">试用期间</span>----------------------<br><br>`#}
                    // {#const stepsixContent_g = stepsixContent !== 'None' ? `<span style="color: blue;">到期付费</span><br><br>${stepsixContent}` : `<span style="color: blue;">到期付费</span><br><br>`#}



                    // 设置 innerHTML

                    document.getElementById('step-one-content').innerHTML = stepOneContent_g !== 'None' ? stepOneContent_g : '';
                    // {#document.getElementById('step-two-content').innerHTML = steptwoContent_g !== 'None' ? steptwoContent_g : '';#}
                    document.getElementById('step-three-content').innerHTML = stepthreeContent_g !== 'None' ? stepthreeContent_g : '';
                    document.getElementById('step-four-content').innerHTML = stepfourContent_g !== 'None' ? stepfourContent_g : '';
                    // {#document.getElementById('step-five-content').innerHTML = stepfiveContent_g !== 'None' ? stepfiveContent_g : '';#}
                    // {#document.getElementById('step-six-content').innerHTML = stepsixContent_g !== 'None' ? stepsixContent_g : '';#}

                    timelineModal.show();
                });
            });

            document.getElementById('editForm').addEventListener('submit', function (event) {
                event.preventDefault();
                const form = this;
                const formData = new FormData(form);

                fetch('/do_presales_progress', {  // 替换为你的实际端点URL
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log("响应成功")
                            showCopySuccessToast();
                            location.reload();
                        } else {
                            alert('保存失败：' + data.message);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('保存失败：请检查网络连接');
                    });
            });

            // 获取所有的单选按钮
            var radioButtons = document.querySelectorAll('.btn-group.right-align.scale-search input[type="radio"]');
            const hiddenBtnradio = document.getElementById('hidden_btnradio');
            const persaler_list_value = "{{ persaler_list_value }}";  // 从模板获取值

            // 设置 hiddenBtnradio 的值
            hiddenBtnradio.value = persaler_list_value;
            const btnradio1 = document.getElementById('btnradio1');
            const btnradio2 = document.getElementById('btnradio2');
            const btnradio3 = document.getElementById('btnradio3');

            // 为每个单选按钮添加事件监听器
            radioButtons.forEach(function (button) {
                button.addEventListener('change', function () {
                    var selectedValue = this.id;  // 获取选中的单选按钮的ID
                    console.log("发送到服务器的请求:", selectedValue);
                    const formData = new FormData();
                    formData.append('selectedValue', selectedValue);
                    fetch('/update_presales_scale', {
                        method: 'POST',
                        body: formData
                    })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            if (data.success) {
                                // 成功后，重定向到客服协助跟进表页面
                                window.location.href = "{{ url_for('main.presales_progress') }}";
                            }
                        })
                        .catch((error) => {
                            console.error('Error:', error);
                        });
                });
            });


            btnradio1.addEventListener('change', function () {
                if (this.checked) {
                    hiddenBtnradio.value = '';
                }
            });

            btnradio2.addEventListener('change', function () {
                if (this.checked) {
                    hiddenBtnradio.value = 'w';
                }
            });

            btnradio3.addEventListener('change', function () {
                if (this.checked) {
                    hiddenBtnradio.value = 's';
                }
            });

        });


        function showCopySuccessToast() {
            console.log("showCopySuccessToast")
            var toastDiv = document.createElement('div');
            toastDiv.textContent = '已提交成功';
            toastDiv.style.position = 'fixed';
            toastDiv.style.top = '10%';
            toastDiv.style.left = '50%';
            toastDiv.style.transform = 'translateX(-50%)';
            toastDiv.style.backgroundColor = '#f8d7da';
            toastDiv.style.color = '#721c24';
            toastDiv.style.padding = '10px';
            toastDiv.style.borderRadius = '5px';
            toastDiv.style.zIndex = '1000';
            toastDiv.style.minWidth = '250px';
            toastDiv.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)';
            document.body.appendChild(toastDiv);
            // 移除提示信息
            setTimeout(function () {
                document.body.removeChild(toastDiv);
            }, 2000);
        }

        $(function () {
            var locale = {
                "format": 'YYYY-MM-DD',
                "separator": " - ",
                "applyLabel": "确定",
                "cancelLabel": "取消",
                "fromLabel": "起始时间",
                "toLabel": "结束时间'",
                "customRangeLabel": "自定义",
                "weekLabel": "W",
                "daysOfWeek": ["日", "一", "二", "三", "四", "五", "六"],
                "monthNames": ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],
                "firstDay": 1
            };

            $('#demo').daterangepicker({
                'locale': locale,
                ranges: {
                    '今日': [moment(), moment()],
                    '昨日': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                    '最近7日': [moment().subtract(6, 'days'), moment()],
                    '最近30日': [moment().subtract(29, 'days'), moment()],
                    '本月': [moment().startOf('month'), moment().endOf('month')],
                    '上月': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month')
                        .endOf('month')
                    ]
                },
                "alwaysShowCalendars": true,
                "startDate": new Date(),
                "endDate": new Date(),
                "opens": "right",
            }, function (start, end, label) {
                console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')');
            });
        })

        $(document).ready(function () {
            $('[data-bs-toggle="tooltip"]').tooltip();
        });

        document.addEventListener('DOMContentLoaded', function () {
            // 初始化所有的 Tooltip
            const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
            const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

            // 添加点击事件监听器
            const editableCells = document.querySelectorAll('.editable-cell');
            editableCells.forEach(cell => {
                let isEditing = false; // 标志变量，用于跟踪单元格是否处于编辑状态

                cell.addEventListener('click', function () {
                    if (!isEditing) {
                        const originalValue = this.textContent;
                        const input = document.createElement('input');
                        input.type = 'text';
                        input.value = originalValue;
                        input.classList.add('form-control');


                        this.innerHTML = '';
                        this.appendChild(input);

                        input.focus();

                        // 设置光标位置到内容后面
                        input.setSelectionRange(originalValue.length, originalValue.length);

                        // 添加双击事件监听器
                        input.addEventListener('dblclick', function (event) {
                            event.preventDefault(); // 阻止默认行为（选中全部内容）
                        });

                        isEditing = true; // 设置为编辑状态

                        input.addEventListener('blur', function () {
                            const newValue = this.value.trim();
                            this.parentNode.innerHTML = newValue;

                            // 发送 AJAX 请求保存到数据库
                            saveToDatabase(cell, newValue);

                            isEditing = false; // 重置编辑状态
                        });
                    }
                });
            });

            // 发送 AJAX 请求保存到数据库
            function saveToDatabase(cell, value) {
                const taskId = cell.getAttribute('data-task-id');
                const column = cell.getAttribute('data-column');

                fetch('/save_contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        task_id: taskId,
                        column: column,
                        value: value
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log('保存成功');
                        } else {
                            console.error('保存失败');
                        }
                    })
                    .catch(error => {
                        console.error('请求失败', error);
                    });
            }
        });


        $(document).ready(function () {
            // 获取输入框元素并设置其值为空字符串
            $('#demo').val('');
        });

        $(document).ready(function () {
            // 初始化模态对话框中的数据
            $('.baseedit-button').on('click', function () {
                var taskId = $(this).data('id');
                var companyId = $(this).data('company');
                var contact = $(this).data('contact');
                var yetai_remark = $(this).data('yetai_remark');
                var xin_remark = $(this).data('xin_remark');

                console.log('Task ID:', taskId); // 调试信息
                console.log('Company ID:', companyId); // 调试信息
                console.log('Contact:', contact); // 调试信息

                // 使用 Bootstrap 的 shown.bs.modal 事件来确保模态对话框显示时再填充数据
                $('#baseModal').on('shown.bs.modal', function () {
                    $('#id').val(taskId);
                    $('#company_id').val(companyId);
                    $('#contact').val(contact);
                    $('#yetai_remark').val(yetai_remark);
                    $('#xin_remark').val(xin_remark);
                });
            });

            // 表单提交处理
            $('#baseeditForm').on('submit', function (event) {
                event.preventDefault(); // 阻止表单默认提交行为

                // 获取表单数据
                var formData = $(this).serialize();

                // 获取 taskId 并添加到 formData 中
                var taskId = $('#id').val();
                formData += '&taskId=' + encodeURIComponent(taskId);

                console.log('Form Data:', formData); // 调试信息

                $.ajax({
                    url: '/save_contact', // 替换为你的后端API地址
                    type: 'POST',
                    data: formData,
                    success: function (response) {
                        // 处理成功响应
                        // {#alert('数据提交成功');#}
                        $('#baseModal').modal('hide'); // 关闭模态对话框
                        // 刷新页面或更新DOM
                        location.reload();
                    },
                    error: function (xhr, status, error) {
                        // 处理错误响应
                        console.error('数据提交失败:', xhr.responseText);
                        $('#company_id_feedback').text(xhr.responseText); // 显示错误信息
                    }
                });
            });
        });
