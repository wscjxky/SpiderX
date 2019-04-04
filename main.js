var kechengxingzhi = 4;
var keshi = 9;
var yingdaorenshu = 10;
var shidaorenshu = 11;
var class_tiyan = 0;
var class_1 = 0;
var class_5 = 0;
var class_8 = 0;
var class_9 = 0;
var sum = 0;
var price = 0;
var free_count = 0;
var free_course = 20;
var free_str = '';
$('#zhuban').change(function (e) {
    var file = this.files[0];
    var fileName = file.name;
    var fileType = fileName.substr(fileName.length - 4, fileName.length);
    $('#file-list').html(fileName);
    var files = e.target.files;
    var fileReader = new FileReader();
    fileReader.onload = function (ev) {
        try {
            var data = ev.target.result,
                workbook = XLSX.read(data, {
                    type: 'binary'
                }), // 以二进制流方式读取得到整份excel表格对象
                persons = []; // 存储获取到的数据
        } catch (e) {
            console.log(e);
            console.log('文件类型不正确');
            return;
        }
        var fromTo = '';
        // 遍历每张表读取

        for (var sheet in workbook.Sheets) {
            if (sheet != '素养教师电子课时单') {
                console.log(sheet);
                continue;
            }
            if (workbook.Sheets.hasOwnProperty(sheet)) {
                fromTo = workbook.Sheets[sheet]['!ref'];
                var rows = (XLSX.utils.sheet_to_json(workbook.Sheets[sheet]));
                for (var idx in rows) {
                    var count = -1;
                    var row = rows[idx];
                    var len = (Object.keys(row).length);
                    if (len < 12)
                        continue;
                    if (!row["应到\n人数"] || !row["对应\n课时"])
                        continue;
                    keshi = row["对应\n课时"];
                    if (free_count == free_course - 1 && keshi == 2) {
                        cal_pri(row, 1);
                        free_count += 1;
                    } else if (free_count < free_course) {
                        cal_pri(row, 0);

                        free_count += keshi;
                    } else {
                        cal_pri(row, 2);
                    }
                    var trtd = $('<tr> <td>' + (parseInt(idx) + 2) + '</td>' +
                        '<td>' + kechengxingzhi + '</td>' +
                        ' <td >' + yingdaorenshu + '</td>' +
                        ' <td> ' + shidaorenshu + '</td> ' +
                        '<td > ' + keshi + '</td> ' +
                        '<td > ' + price.toFixed(2) + '</td>' +
                        '<td > ' + sum.toFixed(2) + '</td>' +
                        ' </tr>');
                    trtd.appendTo($('#process'));

                }
                $('#1').html(class_1);
                $('#5').html(class_5);
                $('#8').html(class_8);
                $('#9').html(class_9);
                $('#tiyan').html(class_tiyan);
                $('#sum').html(sum.toFixed(2));
                break; // 如果只取第一张表，就取消注释这行
            }
        }
    };
    // 以二进制方式打开文件
    fileReader.readAsBinaryString(files[0]);
});

$('#peiban').change(function (e) {
    kechengxingzhi = 4;
    keshi = 9;
    yingdaorenshu = 10;
    shidaorenshu = 11;
    class_tiyan = 0;
    class_1 = 0;
    class_5 = 0;
    class_8 = 0;
    class_9 = 0;
    price = 0;
    free_count = 0;
    free_course = 20;
    free_str = '';
    var file = this.files[0];
    var fileName = file.name;
    var fileType = fileName.substr(fileName.length - 4, fileName.length);
    // if (fileType != '.xls' && fileType != '.xlsx') {
    //     alert("文件类型不对");
    //     return
    //
    // }
    $('#file1-list').html(fileName);
    var files = e.target.files;
    var fileReader = new FileReader();
    fileReader.onload = function (ev) {
        try {
            var data = ev.target.result,
                workbook = XLSX.read(data, {
                    type: 'binary'
                }), // 以二进制流方式读取得到整份excel表格对象
                persons = []; // 存储获取到的数据
        } catch (e) {
            console.log(e);
            console.log('文件类型不正确');
            return;
        }
        var fromTo = '';
        // 遍历每张表读取

        for (var sheet in workbook.Sheets) {
            if (sheet != '素养教师电子课时单') {
                console.log(sheet);
                continue;
            }
            if (workbook.Sheets.hasOwnProperty(sheet)) {

                fromTo = workbook.Sheets[sheet]['!ref'];
                var rows = (XLSX.utils.sheet_to_json(workbook.Sheets[sheet]));
                for (var idx in rows) {
                    var count = -1;
                    var row = rows[idx];
                    var len = (Object.keys(row).length);
                    if (len < 12)
                        continue;
                    if (!row["应到\n人数"] || !row["对应\n课时"])
                        continue;
                    keshi = row["对应\n课时"];

                    cal_priban_pri(row);
                    var trtd = $('<tr> <td>' + (parseInt(idx) + 2) + '</td>' +
                        '<td>' + kechengxingzhi + '</td>' +
                        ' <td >' + yingdaorenshu + '</td>' +
                        ' <td> ' + shidaorenshu + '</td> ' +
                        '<td > ' + keshi + '</td> ' +
                        '<td > ' + price.toFixed(2) + '</td>' +
                        '<td > ' + sum.toFixed(2) + '</td>' +
                        ' </tr>');
                    trtd.appendTo($('#process'));

                }
                $('#1').html(class_1);
                $('#5').html(class_5);
                $('#8').html(class_8);
                $('#9').html(class_9);
                $('#tiyan').html(class_tiyan);
                $('#sum').html(sum.toFixed(2));
                break; // 如果只取第一张表，就取消注释这行
            }
        }
    };
    fileReader.readAsBinaryString(files[0]);

});

function cal_pri(row, flag) {
    keshi = parseFloat(row["对应\n课时"]);
    kechengxingzhi = stripscript(row["课程\n性质"]);
    shidaorenshu = parseFloat(row["实到\n人数"]);
    yingdaorenshu = parseFloat(row["应到\n人数"]);
    zhuanhuarenshu = row["转化学生\n人数"];
    zhuanhuarenshu = parseFloat(row[Object.keys(row)[Object.keys(row).length - 1]]);
    if (kechengxingzhi == "常规") {
        if (yingdaorenshu == 1) {
            price = 20;
            class_1 += keshi;
        } else if (yingdaorenshu >= 2 && yingdaorenshu <= 5) {
            price = shidaorenshu / 5.0 * 20;
            class_5 += keshi;
        } else {
            price = shidaorenshu / 4.0 * 20;
            class_5 += keshi;
        }

    } else if (kechengxingzhi == "综合素养") {
        if (shidaorenshu < 9.0) {
            price = 20;
            class_8 += keshi;
        } else {
            price = 24;
            class_9 += keshi;
        }
    } else if (kechengxingzhi == "体验") {
        console.log(zhuanhuarenshu);
        if (zhuanhuarenshu == 1.00) {
            price = 20;
            kechengxingzhi += "成功"
        } else {
            price = 10;
            kechengxingzhi += "失败"

        }
        class_tiyan += 1;
        keshi = 1;
    }
    if (flag == 1)
        sum += price;
    else if (flag == 0)
        sum = 0;
    else
        sum += price * keshi;

}

function cal_priban_pri(row) {
    keshi = parseFloat(row["对应\n课时"]);
    console.log(keshi);
    kechengxingzhi = stripscript(row["课程\n性质"]);
    shidaorenshu = parseFloat(row["实到\n人数"]);
    yingdaorenshu = parseFloat(row["应到\n人数"]);
    zhuanhuarenshu = row["转化学生\n人数"];
    zhuanhuarenshu = parseFloat(row[Object.keys(row)[Object.keys(row).length - 1]]);
    if (kechengxingzhi == "常规") {
        if (yingdaorenshu >= 4) {
            price = 15;
            class_5 += keshi;
        } else {
            price = 15 - (4 - shidaorenshu) * 5;
            // price = 0;
            class_1 += keshi;
        }

    } else if (kechengxingzhi == "综合素养") {
        price = 0;
        class_9 += keshi;

    } else if (kechengxingzhi == "体验") {
        console.log(zhuanhuarenshu);
        if (zhuanhuarenshu == 0.00) {
            price = 20;
            kechengxingzhi += "成功"
        } else {
            price = 10;
            kechengxingzhi += "失败"

        }
        class_tiyan += 1;
        keshi = 1;
    }

    sum += price * keshi;
}

function stripscript(s) {
    var pattern = new RegExp("[`~!@#$^&*()=|{}':;',\\[\\].<>/?~！@#￥……&*（）——|{}【】‘；：”“'。，、？]")
    var rs = "";
    for (var i = 0; i < s.length; i++) {
        rs = rs + s.substr(i, 1).replace(pattern, '');
    }
    return rs;
}
