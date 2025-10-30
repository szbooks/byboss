/* global bootstrap: false */
(() => {
  'use strict'
  const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.forEach(tooltipTriggerEl => {
    new bootstrap.Tooltip(tooltipTriggerEl)
  })
})()


$(document).ready(function(){


    var sidebarVisible = localStorage.getItem("sidebar");

    // 如果 sidebarVisible 为 null 或未定义，则设置为 true 并更新 localStorage
    if (sidebarVisible === null || sidebarVisible === undefined) {
        sidebarVisible = true; // 默认设置为 true
        localStorage.setItem("sidebar", true); // 更新 localStorage
    } else {
        // 将 localStorage 中的字符串转换为布尔值
        sidebarVisible = sidebarVisible === "true";
    }

    console.log("sidebarVisible1 :"+sidebarVisible)
    if (!sidebarVisible) {
        $(".sidebar").hide(); // 如果状态为 false，隐藏侧边栏
    } else {
        $(".sidebar").show(); // 如果状态为 true，显示侧边栏
    }



    $("#sidebarToggleButton").click(function(){
        $(".sidebar").toggle(); // 使用自定义的类名来切换侧边栏的显示和隐藏
        sidebarVisible = !sidebarVisible;
        localStorage.setItem('sidebar', sidebarVisible);
        console.log("sidebarVisible1 :"+sidebarVisible)

    });
});

// document.addEventListener('DOMContentLoaded', function() {
//     var sidebarToggleButton = document.getElementById('sidebarToggleButton');
//     var navbarBrand = document.getElementById('navbarBrand');
//
//     sidebarToggleButton.addEventListener('click', function() {
//         // 切换navbarBrand的显示与隐藏
//         if (navbarBrand.style.display === 'none') {
//             navbarBrand.style.display = 'block';
//         } else {
//             navbarBrand.style.display = 'none';
//         }
//         var sidebar = document.getElementById('sidfold');
//     if (sidebar.style.marginLeft === '145px' || sidebar.style.marginLeft === '') {
//         // 如果margin-left已经是145px或者没有设置（默认为0），则重置为0
//         sidebar.style.marginLeft = '0px';
//     } else {
//         // 否则，设置为145px
//         sidebar.style.marginLeft = '145px'; }
//     });
// });


$('#sidebarToggleButton').click(function() {
    var sidebar = $('#sidebar');
    if (sidebar.css('margin-left') === '145px' || sidebar.css('margin-left') === '0px') {
        // 如果margin-left已经是145px或0px，则切换
        sidebar.css('margin-left', sidebar.css('margin-left') === '145px' ? '0px' : '145px');
    }
});